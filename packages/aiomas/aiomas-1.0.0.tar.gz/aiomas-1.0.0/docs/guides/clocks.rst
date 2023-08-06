Container clocks
================

.. currentmodule:: aiomas.clocks

Clocks and time are a very important instrument and required, if your agents
want to delay the execution of a task for some time, schedule a task at
a certain time or just need to define a timeout.

Usually, the real (or wall-clock) time is used for this.  In some contexts,
however, you need a different notion of time – for example if you want to
couple a multi-agent system with external simulators that usually run faster
than real-time.

For this reason, every agent container provides a clock via its
:attr:`~aiomas.agent.Container.clock` attribute.  The default clock is the
real-time clock that asyncio uses (:class:`AsyncioClock`).

An alternative clock is the :class:`ExternalClock`.  The time of this clock can
be set by external processes so that the time within your agent system passes
as fast (or slow) as in that external process.

The benefit of using aiomas' clocks compared to just using what asyncio offers
is, that you can easily switch clocks (e.g., from the :class:`AsyncioClock` to
the :class:`ExternalClock`) without touching the agents:

.. code-block:: python3

   >>> import aiomas
   >>>
   >>>
   >>> CLOCK = aiomas.AsyncioClock()
   >>> # CLOCK = aiomas.ExternalClock('2016-01-01T00:00:00')
   >>>
   >>> class Sleeper(aiomas.Agent):
   ...     async def run(self):
   ...          # await asyncio.sleep(.5)  # <-- Don't use this!
   ...          # Depending on the clock used, this sleeps for a "real" half
   ...          # second or whatever the ExternalClock tells you:
   ...          await self.container.clock.sleep(.5)
   >>>
   >>> container = aiomas.Container.create(('127.0.0.1', 5555), clock=CLOCK)
   >>> agent = Sleeper(container)
   >>> aiomas.run(agent.run())
   >>> container.shutdown()

*(If you uncomment the ExternalClock in the example above, your program won't
terminate because there's no process that sets its time.)*


Date/time representations
-------------------------

All clocks represent time as a monotonically increasing number (not necessarily
with a defined initial value) and as date/time object (for which the `arrow
<https://arrow.readthedocs.org/en/latest/>`_ package is used).

You can get the numeric time via the clock's :meth:`~BaseClock.time()` method.
Its usage is comparable to that of Python's :func:`time.monotonic()` function.

The method :meth:`~BaseClock.utcnow()` returns an :class:`~arrow.arrow.Arrow`
object with the current date and time in `UTC
<https://en.wikipedia.org/wiki/Coordinated_Universal_Time>`_.

.. note::

   You should work with UTC dates as much as possible.  Input dates with
   a local timezone should be converted to UTC as early as possible.  If you
   output dates, convert them as late as possible back to local time.

   Doing date and time calclulations in UTC saves you from a lot of bugs, i.e.,
   when dealing with daylight-saving times.

   `This blog post`__ by Armin Ronacher and `this talk`__ by Taavi Burns
   provide more background to the issue.

   __ http://lucumr.pocoo.org/2011/7/15/eppur-si-muove/
   __ https://www.youtube.com/watch?v=LnVkLXRIbIg


Sleeping
--------

The container clock provides tasks that let your agent sleep *for* a given
amount of time or *until* a given time is reached.

In order to sleep for a given time, you have to use the method
:meth:`~BaseClock.sleep()` with the number of seconds (as float) that you want
to sleep.

The method :meth:`~BaseClock.sleep_until()` also accepts a number in seconds
(which must be greater than the current value of :meth:`~BaseClock.time()`) or
an :class:`~arrow.arrow.Arrow` date object (which must be greater than the
current value of :meth:`~BaseClock.utcnow()`).

Both methods return a future which you have to ``await`` / ``yield from`` in
order to actually sleep.


Scheduling tasks
----------------

Comparably to sleeping, you can schedule the future execution of a task *in*
a given period of time or *at* a given time.

The method :meth:`~BaseClock.call_in()` will run the specified task after
a delay *dt* in seconds; :meth:`BaseClock.call_at()` will run the task at the
specified date (either in seconds or as :class:`~arrow.arrow.Arrow` date).  You
can only pass positional arguments to these methods, because that's what the
underlying *asyncio* functions allow.

Both methods are normal functions that return a handle to the scheduled call.
You can use this handle to :meth:`~TimerHandle.cancel()` the scheduled
execution of the task.


How to use the ExternalClock
----------------------------

Remember the first example which did not actually work if you used the
:class:`ExternalClock`?  Here is a fully working version of it:

.. code-block:: python3

   >>> import asyncio
   >>> import time
   >>>
   >>> import aiomas
   >>>
   >>>
   >>> CLOCK = aiomas.ExternalClock('2016-01-01T00:00:00')
   >>>
   >>> class Sleeper(aiomas.Agent):
   ...     async def run(self):
   ...          print('Gonna sleep for 1s ...')
   ...          await self.container.clock.sleep(1)
   >>>
   >>>
   >>> async def clock_setter(factor=0.5):
   ...     """Let the time pass *factor* as fast as real-time."""
   ...     while True:
   ...         await asyncio.sleep(factor)
   ...         CLOCK.set_time(CLOCK.time() + 1)
   >>>
   >>> container = aiomas.Container.create(('127.0.0.1', 5555), clock=CLOCK)
   >>>
   >>> # Start the process that sets the clock:
   >>> t_clock_setter = asyncio.async(clock_setter())
   >>>
   >>> # Start the agent an measure how long he runs in real-time:
   >>> agent = Sleeper(container)
   >>> start = time.monotonic()
   >>> aiomas.run(agent.run())
   Gonna sleep for 1s ...
   >>> print('Agent process finished after %.1fs' % (time.monotonic() - start))
   Agent process finished after 0.5s
   >>>
   >>> _ = t_clock_setter.cancel()
   >>> container.shutdown()

Now that we have a background process that steps the time forward, the example
actually terminates.

In scenarios where you want to couple you agent system with the clock of
another system, the ``clock_setter()`` process would not sleep but receive
clock updates from that other process and use these updates to set the agent's
clock to a new time.

If you distribute your agent system over multiple processes, make sure that you
spread the clock updates to all agent containers.  Therefore, the
:class:`~aiomas.subproc.Manager` agent in the :mod:`aiomas.subproc` exposes
a :meth:`~aiomas.subproc.Manager.set_time()` method that an agent in your
master process can call.
