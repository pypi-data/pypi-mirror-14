======
engine
======

*Core event loop implementation.*

This package contains a configurable event loop and a set of hooks that allow
for async networking, time based scheduling, and coroutine management. Below
are samples of using each of the major components. Use caution. This project
is still very much in its infancy.

Example Usage
=============

Async Networking
----------------

.. code-block:: python

    # Create a non-blocking socket server that logs data and closes connections.

    import functools
    import socket

    from asyncdef.engine.core import Engine
    from asyncdef.engine.processors.selector import Selector

    # Generate a non-blocking socket listener.
    sock = socket.socket()
    sock.setblocking(0)
    sock.bind(('localhost', 9898))
    sock.listen()


    def handle_data(selector, conn):
        """Triggered on data waiting for read."""
        data = conn.recv(4096)
        print('Got data {}.'.format(data))
        selector.remove_reader(conn)
        conn.close()


    def handle_connection(selector, listening_socket):
        """Triggered on new incoming connection."""
        conn, addr = listening_socket.accept()
        conn.setblocking(0)
        selector.add_reader(
            conn,
            functools.partial(handle_data, selector),
        )

    # Create an instance of the selector and event loop.
    selector = Selector()
    loop = Engine(selector)

    # Set up the socket polling.
    selector.add_reader(sock, functools.partial(handle_connection, selector))

    # Start the event loop.
    loop.start()

Time Scheduling
---------------

.. code-block:: python

    # Schedule a function to run in five seconds.
    import functools

    from asyncdef.engine.core import Engine
    from asyncdef.engine.processors.time import Time


    def print_and_stop(loop):
        print("Stopping the loop.")
        loop.stop()

    time = Time()
    loop = Engine(time)
    handle = loop.defer_for(5, functools.partial(print_and_stop, loop))

    loop.start()

Coroutine Management
--------------------

.. code-block:: python

    import functools
    from concurrent.futures import Future

    from asyncdef.engine.core import Engine
    from asyncdef.engine.processors.coroutine import Coroutine
    from asyncdef.engine.processors.time import Time


    class AwaitableFuture(Future):

        """An awaitable version of the standard lib Future."""

        def __await__(self):
            """Return self until resolved."""
            while self._state != 'FINISHED':

                yield self

            return self.result()


    async def wait_for_future(loop, future):
        value = await future
        print('Got value {}. Stopping the loop.'.format(value))
        loop.stop()


    def resolve_future(future):
        print('Resolving future.')
        future.set_result(True)

    time = Time()
    coromgr = Coroutine()
    loop = Engine(coromgr, time)

    future = AwaitableFuture()
    time.defer_for(5, functools.partial(resolve_future, future))
    handle = coromgr.add(wait_for_future(loop, future))

    loop.start()

Testing
=======

All tests suites are paired one-to-one with the module they test and live
directly adjacent to that same module. All tests are expected to pass for
Python 3.5 and above. To run tests use tox with the included tox.ini file or
create a virtualenv and install the '[testing]' extras.

License
=======

    Copyright 2016 Kevin Conway

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

Contributing
============

Firstly, if you're putting in a patch then thank you! Here are some tips for
getting your patch merged:

Style
-----

As long as the code passes the PEP8 and PyFlakes gates then the style is
acceptable.

Docs
----

The PEP257 gate will check that all public methods have docstrings. If you're
adding something new, like a helper function, try out the
`napoleon style of docstrings <https://pypi.python.org/pypi/sphinxcontrib-napoleon>`_.

Tests
-----

Make sure the patch passes all the tests. If you're adding a new feature don't
forget to throw in a test or two. If you're fixing a bug then definitely add
at least one test to prevent regressions.
