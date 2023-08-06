import sys
import ctypes
import optparse
import re
import tabulate

from six import viewkeys

from . import add_common_options, parse_options
from ..cpu.instructions import DuckyInstructionSet, get_instruction_set
from ..mm import u16_t, u32_t, UINT16_FMT, SIZE_FMT, UINT32_FMT, UINT8_FMT
from ..mm.binary import File, SectionTypes, SECTION_TYPES, SYMBOL_DATA_TYPES, SymbolDataTypes, RelocFlags, SymbolFlags, SectionFlags

from ..cpu.coprocessor.math_copro import MathCoprocessorInstructionSet  # noqa

def show_file_header(logger, f):
  f_header = f.get_header()

  logger.info('=== File header ===')
  logger.info('  Magic:    0x%X', f_header.magic)
  logger.info('  Version:  %i', f_header.version)
  logger.info('  Sections: %i', f_header.sections)
  logger.info('  Flags:    %s (0x%02X)', ''.join(['M' if f_header.flags.mmapable == 1 else '-']), ctypes.cast(ctypes.byref(f_header.flags), ctypes.POINTER(ctypes.c_ubyte)).contents.value)
  logger.info('')

def show_sections(logger, f):
  logger.info('=== Sections ===')
  logger.info('')

  f_header = f.get_header()

  table = [
    ['Index', 'Name', 'Type', 'Flags', 'Base', 'Items', 'Data size', 'File size', 'Offset']
  ]

  for i in range(0, f_header.sections):
    header, content = f.get_section(i)

    header_flags = SectionFlags.from_encoding(header.flags)

    table.append([
      header.index,
      f.string_table.get_string(header.name),
      SECTION_TYPES[header.type],
      '%s (%s)' % (header_flags.to_string(), UINT16_FMT(header_flags.to_int())),
      UINT32_FMT(header.base),
      header.items,
      SIZE_FMT(header.data_size),
      SIZE_FMT(header.file_size),
      SIZE_FMT(header.offset)
    ])

  logger.table(table)

  logger.info('')

def show_disassemble(logger, f):
  logger.info('=== Disassemble ==')
  logger.info('')

  instruction_set = DuckyInstructionSet
  f_header = f.get_header()

  for i in range(0, f_header.sections):
    header, content = f.get_section(i)

    if header.type != SectionTypes.TEXT:
      continue

    logger.info('  Section %s', f.string_table.get_string(header.name))

    csp = header.base
    for raw_inst in content:
      csp_str = UINT32_FMT(csp)
      csp += 4

      inst, desc, opcode = instruction_set.decode_instruction(logger, raw_inst.value)
      logger.info('  %s (%s) %s', csp_str, UINT32_FMT(raw_inst), instruction_set.disassemble_instruction(logger, raw_inst.value))

      if opcode == DuckyInstructionSet.opcodes.SIS:
        instruction_set = get_instruction_set(inst.immediate)

  logger.info('')

def show_reloc(logger, f):
  logger.info('=== Reloc entries ===')
  logger.info('')

  f_header = f.get_header()

  table = [
    ['Name', 'Flags', 'Patch section', 'Patch address', 'Patch offset', 'Patch size']
  ]

  for i in range(0, f_header.sections):
    header, content = f.get_section(i)

    if header.type != SectionTypes.RELOC:
      continue

    for index, entry in enumerate(content):
      _header, _content = f.get_section(entry.patch_section)

      table.append([
        f.string_table.get_string(entry.name),
        RelocFlags.from_encoding(entry.flags).to_string(),
        f.string_table.get_string(_header.name),
        UINT32_FMT(entry.patch_address),
        entry.patch_offset,
        entry.patch_size
      ])

  logger.table(table)
  logger.info('')

def show_symbols(logger, f):
  ascii_replacements = {
    '\n':   '\\n',
    '\r':   '\\r',
    '\x00': '\\0'
  }

  def ascii_replacer(m):
    return ascii_replacements[m.group(0)]

  ascii_replace = re.compile(r'|'.join(viewkeys(ascii_replacements)))

  logger.info('=== Symbols ===')
  logger.info('')

  f_header = f.get_header()

  table = [
    ['Name', 'Section', 'Flags', 'Address', 'Type', 'Size', 'File', 'Line', 'Content']
  ]

  for i in range(0, f_header.sections):
    header, content = f.get_section(i)

    if header.type != SectionTypes.SYMBOLS:
      continue

    for index, entry in enumerate(content):
      _header, _content = f.get_section(entry.section)

      table_row = [
        f.string_table.get_string(entry.name),
        f.string_table.get_string(_header.name),
        SymbolFlags.from_encoding(entry.flags).to_string(),
        UINT32_FMT(entry.address),
        '%s (%i)' % (SYMBOL_DATA_TYPES[entry.type], entry.type),
        SIZE_FMT(entry.size),
        f.string_table.get_string(entry.filename),
        entry.lineno
      ]

      symbol_content = ''

      if _header.flags.bss == 1:
        pass

      else:
        if entry.type == SymbolDataTypes.INT:
          def __get(i):
            return _content[entry.address - _header.base + i].value << (8 * i)

          symbol_content = u32_t(__get(0) | __get(1) | __get(2) | __get(3))
          symbol_content = UINT32_FMT(symbol_content.value)

        elif entry.type == SymbolDataTypes.SHORT:
          def __get(i):
            return _content[entry.address - _header.base + i].value << (8 * i)

          symbol_content = u16_t(__get(0) | __get(1))
          symbol_content = UINT16_FMT(symbol_content.value)

        elif entry.type in (SymbolDataTypes.BYTE, SymbolDataTypes.CHAR):
          symbol_content = UINT8_FMT(_content[entry.address - _header.base].value)

        elif entry.type == SymbolDataTypes.ASCII:
          symbol_content = ''.join(['%s' % chr(c.value) for c in _content[entry.address - _header.base:entry.address - _header.base + entry.size]])

        elif entry.type == SymbolDataTypes.STRING:
          symbol_content = ''.join(['%s' % chr(c.value) for c in _content[entry.address - _header.base:entry.address - _header.base + entry.size]])

        if entry.type == SymbolDataTypes.ASCII or entry.type == SymbolDataTypes.STRING:
          if len(symbol_content) > 32:
            symbol_content = symbol_content[0:29] + '...'

          symbol_content = '"' + ascii_replace.sub(ascii_replacer, symbol_content) + '"'

      table_row.append(symbol_content)
      table.append(table_row)

  for line in tabulate.tabulate(table, headers = 'firstrow', tablefmt = 'simple', numalign = 'right').split('\n'):
    logger.info(line)

  logger.info('')

def main():
  parser = optparse.OptionParser()
  add_common_options(parser)

  parser.add_option('-i', dest = 'file_in', action = 'append', default = [], help = 'File to inspect')

  parser.add_option('-H', dest = 'header',      default = False, action = 'store_true', help = 'Show file header')
  parser.add_option('-D', dest = 'disassemble', default = False, action = 'store_true', help = 'Disassemble TEXT sections')
  parser.add_option('-s', dest = 'symbols',     default = False, action = 'store_true', help = 'List symbols')
  parser.add_option('-r', dest = 'reloc',       default = False, action  ='store_true', help = 'List reloc entries')
  parser.add_option('-S', dest = 'sections',    default = False, action = 'store_true', help = 'List sections')
  parser.add_option('-a', dest = 'all',         default = False, action = 'store_true', help = 'All of above')

  options, logger = parse_options(parser)

  if not options.file_in:
    parser.print_help()
    sys.exit(1)

  if options.all:
    options.header = options.disassemble = options.symbols = options.sections = options.reloc = True

  for file_in in options.file_in:
    logger.info('Input file: %s', file_in)

    with File.open(logger, file_in, 'r') as f_in:
      f_in.load()

      logger.info('')

      if options.header:
        show_file_header(logger, f_in)

      if options.sections:
        show_sections(logger, f_in)

      if options.symbols:
        show_symbols(logger, f_in)

      if options.reloc:
        show_reloc(logger, f_in)

      if options.disassemble:
        show_disassemble(logger, f_in)
