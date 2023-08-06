import time
import datetime

from six.moves import range

from . import Device, IRQProvider, IOProvider, IRQList
from ..errors import InvalidResourceError
from ..mm import u8_t, UINT16_FMT
from ..reactor import RunInIntervalTask
from ..util import F

DEFAULT_IRQ  = 0x00
DEFAULT_FREQ = 100
DEFAULT_PORT_RANGE = 0x300
PORT_RANGE = 0x0007

class RTCTask(RunInIntervalTask):
  def __init__(self, machine, rtc):
    super(RTCTask, self).__init__(10, self.on_tick)

    self.machine = machine
    self.rtc = rtc

    self.stamp = 0
    self.tick = 0

    self.update_tick()

  def update_tick(self):
    self.tick = 1.0 / float(self.rtc.frequency)
    self.machine.DEBUG('rtc: new frequency: %i => %f' % (self.rtc.frequency, self.tick))

  def on_tick(self, task):
    stamp = time.time()
    diff = stamp - self.stamp
    self.machine.DEBUG('rtc: tick: stamp=%s, last=%s, diff=%s, tick=%s, ?=%s' % (stamp, self.stamp, diff, self.tick, diff < self.tick))
    if diff < self.tick:
      return

    self.machine.DEBUG('rtc: trigger irq')

    self.stamp = stamp

    self.machine.trigger_irq(self.rtc)

class RTC(IRQProvider, IOProvider, Device):
  def __init__(self, machine, name, frequency = None, port = None, irq = None, *args, **kwargs):
    super(RTC, self).__init__(machine, 'rtc', name, *args, **kwargs)

    self.frequency = frequency or DEFAULT_FREQ
    self.port = port or DEFAULT_PORT_RANGE
    self.ports = list(range(port, port + PORT_RANGE))
    self.irq = irq or DEFAULT_IRQ
    self.timer_task = RTCTask(machine, self)

    if self.frequency >= 256:
      raise InvalidResourceError('Maximum RTC ticks per second is 255')

  @staticmethod
  def create_from_config(machine, config, section):
    return RTC(machine,
               section,
               frequency = config.getint(section, 'frequency', DEFAULT_FREQ),
               port = config.getint(section, 'port', DEFAULT_PORT_RANGE),
               irq = config.getint(section, 'irq', IRQList.TIMER))

  def boot(self):
    self.machine.DEBUG('RTC.boot')

    for port in self.ports:
      self.machine.register_port(port, self)

    self.machine.reactor.add_task(self.timer_task)
    self.machine.reactor.task_runnable(self.timer_task)

    now = datetime.datetime.now()

    self.machine.tenh('RTC: time %02i:%02i:%02i, date: %02i/%02i/%02i', now.hour, now.minute, now.second, now.day, now.month, now.year - 2000)

  def halt(self):
    for port in self.ports:
      self.machine.unregister_port(port)

    self.machine.reactor.remove_task(self.timer_task)

  def read_u8(self, port):
    if port not in self.ports:
      raise InvalidResourceError('Unhandled port: %s' % UINT16_FMT(port))

    port -= self.port

    if port == 0x0000:
      return u8_t(self.frequency).value

    now = datetime.datetime.now()

    if port == 0x0001:
      return u8_t(now.second).value

    if port == 0x0002:
      return u8_t(now.minute).value

    if port == 0x0003:
      return u8_t(now.hour).value

    if port == 0x0004:
      return u8_t(now.day).value

    if port == 0x0005:
      return u8_t(now.month).value

    if port == 0x0006:
      return u8_t(now.year - 2000).value

  def write_u8(self, port, value):
    if port not in self.ports:
      raise InvalidResourceError(F('Unhandled port: {port:S}', port = port))

    if port != self.ports[0]:
      raise InvalidResourceError(F('Unable to write to read-only port: port={port:S}, value={value:B}', port = port, value = value))

    self.frequency = value
    self.timer_task.update_tick()
