"""
This module provides simple reactor core that runs each of registered tasks at
least once during one iteration of its internal loop.

There are two different kinds of objects that reactor manages:

- task - it's called periodicaly, at least once in each reactor loop iteration
- event - asynchronous events are queued and executed before running any tasks.
  If there are no runnable tasks, reactor loop waits for incomming events.
"""

import collections
import errno
import select

from .interfaces import IReactorTask

FDCallbacks = collections.namedtuple('FDCallbacks', ['on_read', 'on_write', 'on_error'])

class CallInReactorTask(IReactorTask):
  """
  This task request running particular function during the reactor loop. Useful
  for planning future work, and for running tasks in reactor's thread.

  :param fn: callback to fire.
  :param args: arguments for callback.
  :param kwargs: keyword arguments for callback.
  """

  def __init__(self, fn, *args, **kwargs):
    self.fn = fn
    self.args = args
    self.kwargs = kwargs

  def run(self):
    self.fn(*self.args, **self.kwargs)

class RunInIntervalTask(IReactorTask):
  """
  This task will run its callback every ``ticks`` iterations of reactor's main loop.

  :param int ticks: number of main loop iterations between two callback calls.
  :param args: arguments for callback.
  :param kwargs: keyword arguments for callback.
  """

  def __init__(self, ticks, fn, *args, **kwargs):
    self.ticks = ticks
    self.counter = 0

    self.fn = fn
    self.args = args
    self.kwargs = kwargs

  def run(self):
    self.counter += 1

    if self.counter < self.ticks:
      return

    self.counter = 0

    self.fn(self, *self.args, **self.kwargs)

class SelectTask(IReactorTask):
  """
  Private task, serving as a single point where ``select`` syscall is being
  executed. When a subsystem is interested in IO on a file descriptor, such
  file descriptor should be set as non-blocking, and then registered with
  reactor - it's not viable to place ``select`` calls everywhere in different
  drivers. This task takes list of registered file descriptors, checks for
  possible IO oportunities, and fires callbacks accordingly.

  :param ducky.machine.Machine machine: VM this task (and reactor) belongs to.
  :param dict fds: dictionary, where keys are descriptors, and values are lists
    of their callbacks.
  """

  def __init__(self, machine, fds, *args, **kwargs):
    super(SelectTask, self).__init__(*args, **kwargs)

    self.machine = machine

    self.fds = fds
    self.real_fds = {}

    self.poll = select.poll()

  def add_fd(self, fd, on_read = None, on_write = None, on_error = None):
    """
    Register file descriptor with reactor. File descriptor will be checked for
    read/write/error posibilities, and appropriate callbacks will be fired.

    No arguments are passed to callbacks.

    :param int fd: file descriptor.
    :param on_read: function that will be called when file descriptor is available for
      reading.
    :param on_write: function that will be called when file descriptor is available for
      write.
    :param on_error: function that will be called when error state raised on file
      descriptor.
    """

    self.machine.DEBUG('%s.add_fd: fd=%s, on_read=%s, on_write=%s, on_error=%s', self.__class__.__name__, fd, on_read, on_write, on_error)

    if not isinstance(fd, int):
      fd = fd.fileno()

    self.fds[fd] = FDCallbacks(on_read, on_write, on_error)
    self.poll.register(fd, select.POLLERR | (select.POLLIN if on_read is not None else 0) | (select.POLLOUT if on_write is not None else 0))

  def remove_fd(self, fd):
    """
    Unregister file descriptor. It will no longer be checked by its main loop.

    :param int fd: previously registered file descriptor.
    """

    self.machine.DEBUG('%s.remove_fd: fd=%s', self.__class__.__name__, fd)

    if not isinstance(fd, int):
      fd = fd.fileno()

    self.poll.unregister(fd)
    del self.fds[fd]

  def run(self):
    self.machine.DEBUG('%s.run: fds=%s', self.__class__.__name__, self.fds.keys())

    try:
      events = self.poll.poll(0.1)

    except select.error as e:
      if e.args[0] == errno.EINTR:
        self.machine.DEBUG('%s.run: interrupted syscall', self.__class__.__name__)
        return

      raise e

    if not events:
      return

    self.machine.DEBUG('%s.run: events=%s', self.__class__.__name__, events)

    for fd, events in events:
      callbacks = self.fds[fd]

      if events & select.POLLERR:
        if callbacks.on_error is None:
          self.machine.WARN('  unhandled error: fd=%s', fd)
          continue

        self.machine.DEBUG('  trigger err: fd=%s, handler=%s', fd, callbacks.on_error)
        callbacks.on_error()
        continue

      if events & select.POLLIN and callbacks.on_read is not None:
        self.machine.DEBUG('  trigger read: fd=%s, handler=%s', fd, callbacks.on_read)
        callbacks.on_read()

      if events & select.POLLOUT and callbacks.on_write is not None:
        self.machine.DEBUG('  trigger err: fd=%s, handler=%s', fd, callbacks.on_write)
        callbacks.on_write()

class Reactor(object):
  """
  Main reactor class.
  """

  def __init__(self, machine):
    self.machine = machine

    self.tasks = []
    self.runnable_tasks = []
    self.events = []

    self.fds = {}
    self.fds_task = SelectTask(self.machine, self.fds)

  def add_task(self, task):
    """
    Register task with reactor's main loop.
    """

    self.tasks.append(task)

  def remove_task(self, task):
    """
    Unregister task, it will never be ran again.
    """

    self.task_suspended(task)
    self.tasks.remove(task)

  def task_runnable(self, task):
    """
    If not yet marked as such, task is marked as runnable, and its ``run()``
    method will be called every iteration of reactor's main loop.
    """

    if task not in self.runnable_tasks:
      self.runnable_tasks.append(task)

  def task_suspended(self, task):
    """
    If runnable, task is marked as suspended, not runnable, and it will no
    longer be ran by reactor. It's still registered, so reactor's main loop
    will not quit, and task can be later easily re-enabled by calling
    :py:meth:`ducky.reactor.Reactor.task_runnable`.
    """

    if task in self.runnable_tasks:
      self.runnable_tasks.remove(task)

  def add_event(self, event):
    """
    Enqueue asynchronous event.
    """

    self.events.append(event)

  def add_call(self, fn, *args, **kwargs):
    """
    Enqueue function call. Function will be called in reactor loop.
    """

    self.add_event(CallInReactorTask(fn, *args, **kwargs))

  def add_fd(self, fd, on_read = None, on_write = None, on_error = None):
    """
    Register file descriptor with reactor. File descriptor will be checked for
    read/write/error posibilities, and appropriate callbacks will be fired.

    No arguments are passed to callbacks.

    :param int fd: file descriptor.
    :param on_read: function that will be called when file descriptor is available for
      reading.
    :param on_write: function that will be called when file descriptor is available for
      write.
    :param on_error: function that will be called when error state raised on file
      descriptor.
    """

    self.machine.DEBUG('%s.add_fd: fd=%s, on_read=%s, on_write=%s, on_error=%s', self.__class__.__name__, fd, on_read, on_write, on_error)
    self.fds_task.add_fd(fd, on_read = on_read, on_write = on_write, on_error = on_error)

    if len(self.fds) == 1:
      self.add_task(self.fds_task)
      self.task_runnable(self.fds_task)

  def remove_fd(self, fd):
    """
    Unregister file descriptor. It will no longer be checked by its main loop.

    :param int fd: previously registered file descriptor.
    """

    self.machine.DEBUG('Reactor.remove_fd: fd=%s', fd)
    self.fds_task.remove_fd(fd)

    if not self.fds:
      self.remove_task(self.fds_task)

  def run(self):
    """
    Starts reactor loop. Enters endless loop, calling runnable tasks and events,
    and - in case there are no runnable tasks - waits for new events.

    When there are no tasks managed by reactor, loop quits.
    """

    while True:
      if not self.tasks:
        break

      if self.runnable_tasks:
        for task in self.runnable_tasks:
          task.run()

        while self.events:
          e = self.events.pop(0)
          e.run()

      else:
        # This would be better with some sort of interruptible sleep...
        # Maybe use an Event for that, and avoid using Queue when it's
        # not necessary. But that needs more testing, and since I don't
        # have much use for machine that's totally idle, that will come
        # one day in the future
        import time
        time.sleep(0.01)
