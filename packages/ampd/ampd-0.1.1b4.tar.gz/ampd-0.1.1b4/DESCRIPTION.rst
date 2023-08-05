Asynchronous MPD client library
===============================

Uses the GLib main event loop and python generators for asynchronous communication with a Music Player Daemon server.

A ``Client`` connects to an MPD server.
MPD commands are executed by a ``Worker`` (or several), which is created by calling a worker function and is executed by the main loop.
A ``Worker`` can be started either directly within the ``Client``, or, for more complex applications, within a ``WorkerGroup``.

A worker function is a python generator decorated by ``@worker``::

  @worker
  def worker_example(arg1, ...):
      ...
      reply = yield request1(a, b)
      ...
      reply = yield request2()
      ...

The first argument for the worker function (``self``, if a method) must be one of:

a. A ``Client``.
b. A ``WorkerGroup``.
c. An object with a ``WorkerGroup`` attribute named ``ampd_worker_group``.

The function returns a new ``Worker`` immediately.
Its code is later executed by the main loop.
A statement of the form::

  reply = yield request

suspends execution until something happens and a reply is available.
The request can be:

a. An MPD command [1]_ (other than ``idle`` and ``noidle``).
   Returns when the server's reply arrives::

     yield play(5)
     reply = yield status()

b. A passive request, emulating MPD's ``idle`` command, with some improvements.
   Returns as soon as one of the conditions is satisfied, with a list of the satisfied conditions::

     reply = yield condition, ... | iterable

   Conditions can be:

   - A SUBSYSTEM name (in uppercase) or ``ANY`` to match any subsystem.
   - ``TIMEOUT(ms)`` - satisfied after 'ms' milliseconds.
   - ``CONNECT`` - client is connected to server.
   - ``IDLE`` - client is idle.
   - ``WORKER(worker, ... | iterable)`` - all workers are done.

c. Special request::

     yield _self()

   Returns the executing ``Worker``.

d. A request list.
   Emulates MPD's command list, returns a list of replies::

     yield request, ... | iterable


.. [1] For MPD commands and subsystems see http://www.musicpd.org/doc/protocol/command_reference.html

.. Local Variables:
.. ispell-local-dictionary: "british"
.. End:
