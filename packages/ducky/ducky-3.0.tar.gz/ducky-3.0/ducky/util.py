import collections
import functools
import string

from six import iteritems, integer_types, PY2

from ctypes import sizeof

def align(boundary, n):
  return (n + boundary - 1) & ~(boundary - 1)

def str2int(s):
  if isinstance(s, integer_types):
    return s

  if s.startswith('0x'):
    return int(s, base = 16)

  if s.startswith('0'):
    return int(s, base = 8)

  return int(s)

def sizeof_fmt(n, suffix = 'B', max_unit = 'Zi'):
  for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
    if abs(n) < 1024.0 or max_unit == unit:
      return "%3.1f%s%s" % (n, unit, suffix)

    n /= 1024.0

  return "%.1f%s%s" % (n, 'Yi', suffix)

class Formatter(string.Formatter):
  def format_field(self, value, format_spec):
    if format_spec and format_spec[-1] in 'BSWL':
      return self.format_int(format_spec, value)

    return super(Formatter, self).format_field(value, format_spec)

  def format_int(self, format_spec, value):
    i = value if isinstance(value, integer_types) else value.value

    if format_spec.endswith('B'):
      return '0x{:02X}'.format(i & 0xFF)

    if format_spec.endswith('S'):
      return '0x{:04X}'.format(i & 0xFFFF)

    if format_spec.endswith('W'):
      return '0x{:08X}'.format(i & 0xFFFFFFFF)

    if format_spec.endswith('L'):
      return '0x{:016X}'.format(i & 0xFFFFFFFFFFFFFFFF)

    return '{:d}'.format(i)

_F = Formatter()
F = _F.format

UINT8_FMT  = functools.partial(_F.format_int, 'B')
UINT16_FMT = functools.partial(_F.format_int, 'S')
UINT32_FMT = functools.partial(_F.format_int, 'W')
UINT64_FMT = functools.partial(_F.format_int, 'L')


if PY2:
  _BaseFile = file  # noqa

  bytes2str = str
  str2bytes = str
  int2bytes = chr

else:
  from io import IOBase as _BaseFile
  import functools

  bytes2str = functools.partial(str, encoding = 'latin-1')
  str2bytes = functools.partial(bytes, encoding = 'latin-1')

  def int2bytes(b):
    return bytes([b])

def isfile(o):
  return isinstance(o, (_BaseFile, BinaryFile))


class BinaryFile(object):
  """
  Base class of all classes that represent "binary" files - binaries, core dumps.
  It provides basic methods for reading and writing structures.
  """

  @staticmethod
  def do_open(logger, path, mode = 'rb', klass = None):
    if 'b' not in mode:
      mode += 'b'

    stream = open(path, mode)

    if not PY2:
      import io

      if 'r' in mode:
        if 'w' in mode:
          stream = io.BufferedRandom(stream)

        else:
          stream = io.BufferedReader(stream)

      else:
        stream = io.BufferedWriter(stream)

    klass = klass or BinaryFile

    return klass(logger, stream)

  @staticmethod
  def open(*args, **kwargs):
    return BinaryFile.do_open(*args, **kwargs)

  def __init__(self, logger, stream):
    self.stream = stream

    self.DEBUG = logger.debug
    self.INFO = logger.info
    self.WARN = logger.warning
    self.ERROR = logger.error
    self.EXCEPTION = logger.exception

    self.close = stream.close
    self.flush = stream.flush
    self.name = stream.name
    self.read = stream.read
    self.readinto = stream.readinto
    self.readline = stream.readline
    self.seek = stream.seek
    self.tell = stream.tell
    self.write = stream.write

    self.setup()

  def __enter__(self):
    return self

  def __exit__(self, *args, **kwargs):
    self.close()

  def setup(self):
    pass

  def read_struct(self, st_class):
    """
    Read structure from current position in file.

    :returns: instance of class ``st_class`` with content read from file
    :rtype: ``st_class``
    """

    pos = self.tell()

    st = st_class()
    self.readinto(st)

    self.DEBUG('read_struct: %s: %s bytes: %s', pos, sizeof(st_class), st)

    return st

  def write_struct(self, st):
    """
    Write structure into file at the current position.

    :param class st: ``ctype``-based structure
    """

    pos = self.tell()

    self.DEBUG('write_struct: %s: %s bytes: %s', pos, sizeof(st), st)

    self.write(st)

class LRUCache(collections.OrderedDict):
  """
  Simple LRU cache, based on ``OrderedDict``, with limited size. When limit
  is reached, the least recently inserted item is removed.

  :param logging.Logger logger: logger object instance should use for logging.
  :param int size: maximal number of entries allowed.
  """

  def __init__(self, logger, size, *args, **kwargs):
    super(LRUCache, self).__init__(*args, **kwargs)

    self.size = size

    self.reads   = 0
    self.inserts = 0
    self.hits    = 0
    self.misses  = 0
    self.prunes  = 0

    self.DEBUG = logger.debug
    self.INFO = logger.info
    self.WARN = logger.warn
    self.ERROR = logger.error
    self.EXCEPTION = logger.exception

  def make_space(self):
    """
    This method is called when there is no free space in cache. It's responsible
    for freeing at least one slot, upper limit of removed entries is not enforced.
    """

    self.DEBUG('%s.make_space', self.__class__.__name__)

    self.popitem(last = False)
    self.prunes += 1

  def __getitem__(self, key):
    """
    Return entry with specified key.
    """

    self.DEBUG('%s.__getitem__: key=%s', self.__class__.__name__, key)

    self.reads += 1

    if key in self:
      self.hits += 1
    else:
      self.misses += 1

    return super(LRUCache, self).__getitem__(key)

  def __setitem__(self, key, value):
    """
    Called when item is inserted into cache. Size limit is checked and if there's no free
    space in cache, ``make_space`` method is called.
    """

    self.DEBUG('%s.__setitem__: key=%s, value=%s', self.__class__.__name__, key, value)

    if len(self) == self.size:
      self.make_space()

    super(LRUCache, self).__setitem__(key, value)
    self.inserts += 1

  def get_object(self, key):
    """
    The real workhorse - responsible for getting requested item from outside when it's
    not present in cache. Called by ``__missing__`` method. This method itself makes no
    changes to cache at all.
    """

    raise NotImplementedError('Cache %s does not implement get() method' % self.__class__.__name__)

  def __missing__(self, key):
    """
    Called when requested entry is not in cache. It's responsible for getting missing item
    and inserting it into cache. Returns new item.
    """

    self.DEBUG('%s.__missing__: key=%s', self.__class__.__name__, key)

    self[key] = value = self.get_object(key)
    return value

class StringTable(object):
  """
  Simple string table, used by many classes operating with files (core, binaries, ...).
  String can be inserted into table and read, each has its starting offset and its end is
  marked with null byte (\0).

  Thsi is a helper class - it makes working with string, e.g. section and symbol names,
  much easier.
  """

  def __init__(self):
    super(StringTable, self).__init__()

    self.buff = ''

  def put_string(self, s):
    """
    Insert new string into table. String is appended at the end of internal buffer,
    and terminating zero byte (\0) is appended to mark end of string.

    :returns: offset of inserted string
    :rtype: ``int``
    """

    offset = len(self.buff)

    self.buff += chr(len(s))
    self.buff += s

    return offset

  def get_string(self, offset):
    """
    Read string from table.

    :param int offset: offset of the first character from the beginning of the table
    :returns: string
    :rtype: ``string``
    """

    l = ord(self.buff[offset])
    return ''.join(self.buff[offset + 1:offset + 1 + l])

class SymbolTable(dict):
  def __init__(self, binary):
    self.binary = binary

  def __getitem__(self, address):
    last_symbol = None
    last_symbol_offset = 0xFFFE

    for symbol_name, symbol in iteritems(self.binary.symbols):
      if symbol.address > address:
        continue

      if symbol.address == address:
        return (symbol_name, 0)

      offset = abs(address - symbol.address)
      if offset < last_symbol_offset:
        last_symbol = symbol_name
        last_symbol_offset = offset

    return (last_symbol, last_symbol_offset)

  def get_symbol(self, name):
    return self.binary.symbols[name]


class Flags(object):
  _flags = []
  _labels = ''
  _encoding = []  # silence Codacy warning - _encoding will have a real value

  @classmethod
  def create(cls, **kwargs):
    flags = cls()

    for name in cls._flags:
      setattr(flags, name, True if kwargs.get(name, False) is True else False)

    return flags

  @classmethod
  def encoding(cls):
    return cls._encoding

  @classmethod
  def from_encoding(cls, encoding):
    flags = cls()
    flags.load_encoding(encoding)
    return flags

  def to_encoding(self):
    encoding = self._encoding()
    self.save_encoding(encoding)
    return encoding

  def load_encoding(self, encoding):
    for name in [field[0] for field in encoding._fields_]:
      setattr(self, name, True if getattr(encoding, name) == 1 else False)

  def save_encoding(self, encoding):
    for name in [field[0] for field in encoding._fields_]:
      setattr(encoding, name, 1 if getattr(self, name) is True else 0)

  def to_int(self):
    u = 0

    for i, name in enumerate(self._flags):
      if getattr(self, name) is True:
        u |= (1 << i)

    return u

  def load_int(self, u):
    for i, name in enumerate(self._flags):
      setattr(self, name, True if u & (1 << i) else False)

  @classmethod
  def from_int(cls, u):
    flags = cls()
    flags.load_int(u)
    return flags

  def to_string(self):
    return ''.join([
      self._labels[i] if getattr(self, name) is True else '-' for i, name in enumerate(self._flags)
    ])

  def load_string(self, s):
    s = s.upper()

    for i, name in enumerate(self._flags):
      setattr(self, name, True if self._labels[i] in s else False)

  @classmethod
  def from_string(cls, s):
    flags = cls()
    flags.load_string(s)
    return flags

  def __repr__(self):
    return '<{}: {}>'.format(self.__class__.__name__, self.to_string())
