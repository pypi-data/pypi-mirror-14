"""
Pyjo.Reactor.Asyncio - Low-level event reactor with asyncio support
===================================================================
::

    import Pyjo.Reactor.Asyncio

    # Watch if handle becomes readable or writable
    reactor = Pyjo.Reactor.Asyncio.new()

    def io_cb(reactor, writable):
        if writable:
            print('Handle is writable')
        else:
            print('Handle is readable')

    reactor.io(io_cb, handle)

    # Change to watching only if handle becomes writable
    reactor.watch(handle, read=False, write=True)

    # Add a timer
    def timer_cb(reactor):
        reactor.remove(handle)
        print('Timeout!')

    reactor.timer(timer_cb, 15)

    # Start reactor if necessary
    if not reactor.is_running:
        reactor.start()

:mod:`Pyjo.Reactor.Asyncio` is a low-level event reactor based on :mod:`asyncio`.

:mod:`Pyjo.Reactor.Asyncio` will be used as the default backend for
:mod:`Pyjo.IOLoop` if it is loaded before any module using the loop or if
the ``PYJO_REACTOR`` environment variable is set to ``Pyjo.Reactor.Asyncio`` value.

Debugging
---------

You can set the ``PYJO_REACTOR_DEBUG`` environment variable to get some
advanced diagnostics information printed to ``stderr``. ::

    PYJO_REACTOR_DEBUG=1

You can set the ``PYJO_REACTOR_DIE`` environment variable to make reactor die if task
dies with exception. ::

    PYJO_REACTOR_DIE=1

Events
------

:mod:`Pyjo.Reactor.Asyncio` inherits all events from :mod:`Pyjo.Reactor.Base`.

Classes
-------
"""

import Pyjo.Reactor.Base

try:
    import asyncio
except ImportError:
    try:
        import trollius as asyncio
    except ImportError:
        import asyncio  # again for better error message

import weakref

from Pyjo.Util import getenv, md5_sum, rand, setenv, steady_time, warn


DEBUG = getenv('PYJO_REACTOR_DEBUG', False)
DIE = getenv('PYJO_REACTOR_DIE', False)

loop = asyncio.get_event_loop()
"""::

    Pyjo.Reactor.Asyncio.loop = asyncio.new_event_loop()

The :mod:`asyncio` event loop used by first :mod:`Pyjo.Reactor.Asyncio`
object. The default value is ``asyncio.get_event_loop()``.
"""

_instance_counter = 0

setenv('PYJO_REACTOR', getenv('PYJO_REACTOR', 'Pyjo.Reactor.Asyncio'))


class Pyjo_Reactor_Asyncio(Pyjo.Reactor.Base.object):
    """
    :mod:`Pyjo.Reactor.Asyncio` inherits all attributes and methods from
    :mod:`Pyjo.Reactor.Base` and implements the following new ones.
    """

    def __init__(self, **kwargs):
        """

            reactor = Pyjo.Reactor.Asyncio.new()
            reactor2 = Pyjo.Reactor.Asyncio.new(loop=asyncio.get_event_loop())

        Creates new reactor based on asyncio main loop. It uses existing
        :mod:`asyncio` loop for first object and create new async io loop for
        another.
        """
        super(Pyjo_Reactor_Asyncio, self).__init__(**kwargs)

        global loop, _instance_counter

        self.loop = kwargs.get('loop')
        """::

            asyncio_loop = reactor.loop

        asyncio main event loop.
        """

        self.auto_stop = kwargs.get('auto_stop', lambda: not self.loop)
        """::
            auto_stop = reactor.auto_stop
            reactor.auto_stop = False
        :mod:`asyncio` loop will be stopped if there is no active I/O or timer
        events in :mod:`Pyjo.Reactor.Asyncio`.
        This is disabled by default if ``loop`` is provided and enabled
        otherwise.
        """

        self._ios = {}
        self._timers = {}

        if not self.loop:
            if _instance_counter:
                self.loop = asyncio.new_event_loop()
            else:
                self.loop = loop

        _instance_counter += 1

    def again(self, tid):
        """::

            reactor.again(tid)

        Restart active timer.
        """
        timer = self._timers[tid]

        # Warning: this is private property of TimeHandler
        timer['handler']._when = self.loop.time() + timer['after']

    def io(self, cb, handle):
        """::

            reactor = reactor.io(cb, handle)

        Watch handle for I/O events, invoking the callback whenever handle becomes
        readable or writable.
        """
        fd = handle.fileno()

        if fd in self._ios:
            self._ios[fd]['cb'] = cb
            if DEBUG:
                warn("-- Reactor found io[{0}] = {1}".format(fd, self._ios[fd]))
        else:
            self._ios[fd] = {'cb': cb, 'reader': False, 'writer': False}
            if DEBUG:
                warn("-- Reactor adding io[{0}] = {1}".format(fd, self._ios[fd]))

        return self.watch(handle, True, True)

    @property
    def is_running(self):
        """::

            boolean = reactor.is_running

        Check if reactor is running.
        """
        return self.loop.is_running()

    def one_tick(self):
        """::

            reactor.one_tick()

        Run reactor until an event occurs. Note that this method can recurse back into
        the reactor, so you need to be careful.
        """
        loop = self.loop

        if loop.is_running():
            return

        loop.call_soon(loop.stop)

        loop.run_forever()

    def recurring(self, cb, after):
        """::

            tid = reactor.recurring(cb, 0.25)

        Create a new recurring timer, invoking the callback repeatedly after a given
        amount of time in seconds.
        """
        return self._timer(cb, True, after)

    def remove(self, remove):
        """::

            boolean = reactor.remove(handle)
            boolean = reactor.remove(tid)

        Remove handle or timer.
        """
        if remove is None:
            if DEBUG:
                warn("-- Reactor remove None")
            return

        if isinstance(remove, str):
            if DEBUG:
                if remove in self._timers:
                    warn("-- Reactor remove timer[{0}] = {1}".format(remove, self._timers[remove]))
                else:
                    warn("-- Reactor remove timer[{0}] = None".format(remove))

            if remove in self._timers:
                self._timers[remove]['handler'].cancel()
                del self._timers[remove]

        else:
            if hasattr(remove, 'fileno'):
                fd = remove.fileno()
            else:
                fd = remove

            if DEBUG:
                if fd in self._ios:
                    warn("-- Reactor remove fd {0} = {1}".format(fd, self._ios[fd]))
                else:
                    warn("-- Reactor remove fd {0} = None".format(fd))

            if fd in self._ios:
                if 'reader' in self._ios[fd]:
                    self.loop.remove_reader(fd)
                if 'writer' in self._ios[fd]:
                    self.loop.remove_writer(fd)
                del self._ios[fd]

    def reset(self):
        """::

            reactor.reset()

        Remove all handles and timers.
        """
        loop = self.loop

        for fd in self._ios:
            io = self._ios[fd]

            if io['reader']:
                if DEBUG:
                    warn("-- Reactor reset fd {0} reader".format(fd))
                loop.remove_reader(fd)

            if io['writer']:
                if DEBUG:
                    warn("-- Reactor reset fd {0} writer".format(fd))
                loop.remove_writer(fd)

        self._ios = {}

        for tid in self._timers:
            timer = self._timers[tid]

            if timer['handler']:
                if DEBUG:
                    warn("-- Reactor timer[{0}]".format(tid))
                timer['handler'].cancel()

        self._timers = {}

    def start(self):
        """::

            reactor.start()

        Start watching for I/O and timer events, this will block until :meth:`stop` is
        called or there is no any active I/O or timer event.
        """
        loop = self.loop

        if loop.is_running():
            return

        if self.auto_stop:
            def stop_if_no_events(self):
                if not self._timers and not self._ios:
                    self.stop()

            loop.call_soon(stop_if_no_events, self)

        loop.run_forever()

    def stop(self):
        """::

            reactor.stop()

        Stop watching for I/O and timer events.
        """
        loop = self.loop
        if loop.is_running():
            self.loop.stop()

    def timer(self, cb, after):
        """::

            tid = reactor.timer(cb, 0.5)

        Create a new timer, invoking the callback after a given amount of time in
        seconds.
        """
        return self._timer(cb, False, after)

    def watch(self, handle, read, write):
        """::

            reactor = reactor.watch(handle, read, write)

        Change I/O events to watch handle for with true and false values. Note
        that this method requires an active I/O watcher.
        """
        fd = handle.fileno()

        def io_cb(reactor, cb, message, write, fd):
            if DEBUG:
                warn("-- Reactor {0} = {1}".format(message, reactor._ios[fd] if fd in reactor._ios else None))

            if DIE:
                cb(reactor, write)
            else:
                try:
                    cb(reactor, write)
                except Exception as e:
                    reactor.emit('error', e, message)

            if self.auto_stop and not reactor._ios and not reactor._timers:
                reactor.stop()

        if fd not in self._ios:
            self._ios[fd] = {'reader': False, 'writer': False}

        io = self._ios[fd]
        cb = io['cb']

        loop = self.loop

        if read:
            if io['reader']:
                loop.remove_reader(fd)
            else:
                io['reader'] = True
            if DEBUG:
                warn("-- Reactor add fd {0} reader".format(fd))
            loop.add_reader(fd, io_cb, weakref.proxy(self), cb, "Read fd {0}".format(fd), False, fd)
        elif io['reader']:
            if DEBUG:
                warn("-- Reactor remove fd {0} reader".format(fd))
            loop.remove_reader(fd)
            io['reader'] = False

        if write:
            if io['writer']:
                loop.remove_writer(fd)
            else:
                io['writer'] = True
            if DEBUG:
                warn("-- Reactor add fd {0} writer".format(fd))
            loop.add_writer(fd, io_cb, weakref.proxy(self), cb, "Write fd {0}".format(fd), True, fd)
        elif io['writer']:
            if DEBUG:
                warn("-- Reactor remove fd {0} writer".format(fd))
            loop.remove_writer(fd)
            io['writer'] = False

        return self

    def _timer(self, cb, recurring, after):
        tid = None
        while True:
            tid = md5_sum('t{0}{1}'.format(steady_time(), rand()).encode('ascii'))
            if tid not in self._timers:
                break

        timer = {'cb': cb, 'after': after, 'recurring': recurring}

        if DEBUG:
            warn("-- Reactor adding timer[{0}] = {1}".format(tid, timer))

        def timer_cb(reactor, cb, recurring, after, tid):
            if DEBUG:
                warn("-- Reactor alarm timer[{0}] = {1}".format(tid, reactor._timers[tid]))

            if recurring:
                reactor._timers[tid]['handler'] = reactor.loop.call_later(after, timer_cb, reactor, cb, recurring, after, tid)
            else:
                reactor.remove(tid)

            if DIE:
                cb(reactor)
            else:
                try:
                    cb(reactor)
                except Exception as e:
                    reactor.emit('error', e, 'Timer {0}'.format(tid))

            if self.auto_stop and not reactor._ios and not reactor._timers:
                reactor.stop()

        timer['handler'] = self.loop.call_later(after, timer_cb, weakref.proxy(self), cb, recurring, after, tid)
        self._timers[tid] = timer

        return tid


new = Pyjo_Reactor_Asyncio.new
object = Pyjo_Reactor_Asyncio
