The channel layer
=================

.. currentmodule:: aiomas.channel

The channel layer is aiomas' lowest layer of abstraction.  It lets you send and
receive complete *messages*.  In contrast to `asyncio’s built-in stream
protocol <https://docs.python.org/3/library/asyncio-stream.html>`_ which just
sends byte strings, messages are JSON-encoded [*]_ data (which is a lot more
convenient).

.. [*] Actually, whether JSON is used for encoding, depends on the :doc:`codec
       <codecs>` that the channel uses.  JSON is the default, but you can also
       use MsgPack or something else.  At the bottom of this document, there's
       a section :ref:`explaining aiomas' message format in detail
       <aiomas_msg_format>`.

Here is a minimal example that shows how the :class:`~aiomas.channel.Channel`
can be used:

.. code-block:: python3

   >>> import aiomas
   >>>
   >>>
   >>> async def client():
   ...     """Client coroutine: Send a greeting to the server and wait for a
   ...     reply."""
   ...     channel = await aiomas.channel.open_connection(('localhost', 5555))
   ...     rep = await channel.send('ohai')
   ...     print(rep)
   ...     await channel.close()
   >>>
   >>>
   >>> async def handle_client(channel):
   ...     """Handle a client connection."""
   ...     req = await channel.recv()
   ...     print(req.content)
   ...     await req.reply('cya')
   ...     await channel.close()
   >>>
   >>>
   >>> server = aiomas.run(aiomas.channel.start_server(('localhost', 5555), handle_client))
   >>> aiomas.run(client())
   ohai
   cya
   >>> server.close()
   >>> aiomas.run(server.wait_closed())

A communication channel has two sides: The client side is created and returned
by :func:`open_connection()`.  For each client connection, the server creates
a :class:`Channel` instance and starts a new background task of the *client
connected callback (client_connected_cb)* to which it passes that channel
instance.

Both, the client and server side, can send and receive messages.  In the
example above, the client starts to send a request and the server side waits
for incoming requests.  A request has a :attr:`~Request.content` attribute
which holds the actual message.  To send a reply, you can either use
:meth:`Request.reply()` or :meth:`Request.fail()`.  :meth:`Channel.send()` and
:meth:`Request.reply()` take any data that the channel's codec can serialize
(e.g., strings, numbers, lists, dicts, ...).  :meth:`Request.fail()` takes an
exception instance which is raised at the requesting side as
:class:`~aiomas.exceptions.RemoteException`, as the following example
demonstrates:

.. code-block:: python3

   >>> import aiomas
   >>>
   >>>
   >>> async def client():
   ...     """Client coroutine: Send a greeting to the server and wait for a
   ...     reply."""
   ...     channel = await aiomas.channel.open_connection(('localhost', 5555))
   ...     try:
   ...         rep = await channel.send('ohai')
   ...         print(rep)
   ...     except aiomas.RemoteException as e:
   ...         print('Got an error:', str(e))
   ...     finally:
   ...         await channel.close()
   >>>
   >>>
   >>> async def handle_client(channel):
   ...     """Handle a client connection."""
   ...     req = await channel.recv()
   ...     print(req.content)
   ...     await req.fail(ValueError(42))
   ...     await channel.close()
   >>>
   >>>
   >>> server = aiomas.run(aiomas.channel.start_server(('127.0.0.1', 5555), handle_client))
   >>> aiomas.run(client())
   ohai
   Got an error: Origin: ('127.0.0.1', 5555)
   ValueError: 42
   <BLANKLINE>
   >>> server.close()
   >>> aiomas.run(server.wait_closed())

These are the basics of the channel layer.  The following sections answer some
detail questions.


How can I use and another codec?
--------------------------------

In order to use another codec as the default :class:`~aiomas.codecs.JSON` one,
just pass the corresponding codec class (e.g., :class:`~aiomas.codecs.MsgPack`
to :func:`open_connection()` and :func:`start_server()`:

.. code-block:: python3

   >>> import aiomas
   >>>
   >>> CODEC = aiomas.codecs.MsgPack
   >>>
   >>> async def client():
   ...     """Client coroutine: Send a greeting to the server and wait for a
   ...     reply."""
   ...     channel = await aiomas.channel.open_connection(('localhost', 5555),
   ...                                                    codec=CODEC)
   ...     rep = await channel.send('ohai')
   ...     print(rep)
   ...     await channel.close()
   >>>
   >>>
   >>> async def handle_client(channel):
   ...     """Handle a client connection."""
   ...     req = await channel.recv()
   ...     print(req.content)
   ...     await req.reply('cya')
   ...     await channel.close()
   >>>
   >>>
   >>> server = aiomas.run(aiomas.channel.start_server(('localhost', 5555), handle_client,
   ...                                                 codec=CODEC))
   >>> aiomas.run(client())
   ohai
   cya
   >>> server.close()
   >>> aiomas.run(server.wait_closed())

Note, that the codecs :class:`aiomas.codecs.MsgPack` and
:class:`aiomas.codecs.MsgPackBlosc` are not available by default but have to
:ref:`be explicitly enabled <install_msgpack_blosc>`.


How can I serialize custom data types?
--------------------------------------

Both, :func:`open_connection()` and :func:`start_server()` take a list of
*extra_serializers*.  Such a serializer is basically a function returning
a three-tuple *(type, serialize, deserialize)*.  You can find more details in
the :doc:`codecs guide <codecs>`.  Here is just a simple example:

.. code-block:: python3

   >>> import aiomas
   >>>
   >>>
   >>> class MyType:
   ...     """Our serializable type."""
   ...     def __init__(self, value):
   ...         self.value = value
   ...
   ...     def __repr__(self):
   ...         return '%s(%r)' % (self.__class__.__name__, self.value)
   >>>
   >>>
   >>> def serialize_mytype(obj):
   ...     """Return a JSON serializable version "MyType" instances."""
   ...     return obj.value
   >>>
   >>>
   >>> def deserialize_mytype(value):
   ...     """Make a "MyType" instance from *value*."""
   ...     return MyType(value)
   >>>
   >>>
   >>> def mytype_serializer():
   ...     return (MyType, serialize_mytype, deserialize_mytype)
   >>>
   >>>
   >>> EXTRA_SERIALIZERS = [mytype_serializer]
   >>>
   >>>
   >>> async def client():
   ...     """Client coroutine: Send a greeting to the server and wait for a
   ...     reply."""
   ...     channel = await aiomas.channel.open_connection(
   ...         ('localhost', 5555), extra_serializers=EXTRA_SERIALIZERS)
   ...     rep = await channel.send(['ohai', MyType(42)])
   ...     print(rep)
   ...     await channel.close()
   >>>
   >>>
   >>> async def handle_client(channel):
   ...     """Handle a client connection."""
   ...     req = await channel.recv()
   ...     print(req.content)
   ...     await req.reply(MyType('cya'))
   ...     await channel.close()
   >>>
   >>>
   >>> server = aiomas.run(aiomas.channel.start_server(('localhost', 5555), handle_client,
   ...                                                 extra_serializers=EXTRA_SERIALIZERS))
   >>> aiomas.run(client())
   ['ohai', MyType(42)]
   MyType('cya')
   >>> server.close()
   >>> aiomas.run(server.wait_closed())

A shorter version for common cases is using the
:func:`aiomas.codecs.serializable` decorator:

.. code-block:: python3

   >>> import aiomas
   >>>
   >>>
   >>> @aiomas.codecs.serializable
   ... class MyType:
   ...     """Our serializable type."""
   ...     def __init__(self, value):
   ...         self.value = value
   >>>
   >>>
   >>> EXTRA_SERIALIZERS = [MyType.__serializer__]
   >>>
   >>>
   >>> async def client():
   ...     """Client coroutine: Send a greeting to the server and wait for a
   ...     reply."""
   ...     channel = await aiomas.channel.open_connection(
   ...         ('localhost', 5555), extra_serializers=EXTRA_SERIALIZERS)
   ...     rep = await channel.send(['ohai', MyType(42)])
   ...     print(rep)
   ...     await channel.close()
   >>>
   >>>
   >>> async def handle_client(channel):
   ...     """Handle a client connection."""
   ...     req = await channel.recv()
   ...     print(req.content)
   ...     await req.reply(MyType('cya'))
   ...     await channel.close()
   >>>
   >>>
   >>> server = aiomas.run(aiomas.channel.start_server(('localhost', 5555), handle_client,
   ...                                                 extra_serializers=EXTRA_SERIALIZERS))
   >>> aiomas.run(client())
   ['ohai', MyType(value=42)]
   MyType(value='cya')
   >>> server.close()
   >>> aiomas.run(server.wait_closed())


How can I bind a server socket to a random port?
------------------------------------------------

You cannot ask your OS for an available port but have to try a randomly chosen
port until you succeed:

.. code-block:: python3

   >>> import errno
   >>> import random
   >>>
   >>> max_tries = 100
   >>> port_range = (49152, 65536)
   >>>
   >>> async def random_server(host, port_range, max_tries):
   ...     for i in range(max_tries):
   ...         try:
   ...             port = random.randrange(*port_range)
   ...             server = await aiomas.channel.start_server(
   ...                (host, port), handle_client)
   ...         except OSError as oe:
   ...             if oe.errno != errno.EADDRINUSE:
   ...                 # Re-raise if not errno 48 ("address already in use")
   ...                 raise
   ...         else:
   ...             return server, port
   ...     raise RuntimeError('Could not bind server to a random port.')
   >>>
   >>> server, port = aiomas.run(random_server('localhost', port_range, max_tries))
   >>> server.close()
   >>> aiomas.run(server.wait_closed())


Connection timeouts / Starting clients before the server
--------------------------------------------------------

Sometimes, you need to start a client before the server is started.  Therefore,
the function :func:`open_connection()` lets you specify a timeout.  It
repeatedly retries to connect until *timeout* seconds have passed.  By default,
*timeout* is 0 which means there is only one try.

.. code-block:: python3

   >>> import asyncio
   >>> import aiomas
   >>>
   >>>
   >>> async def client():
   ...     """Client coroutine: Send a greeting to the server and wait for a
   ...     reply."""
   ...     # Try to connect for 1s:
   ...     channel = await aiomas.channel.open_connection(('localhost', 5555),
   ...                                                    timeout=1)
   ...     rep = await channel.send('ohai')
   ...     print(rep)
   ...     await channel.close()
   >>>
   >>>
   >>> async def handle_client(channel):
   ...     """Handle a client connection."""
   ...     req = await channel.recv()
   ...     print(req.content)
   ...     await req.reply('cya')
   ...     await channel.close()
   >>>
   >>>
   >>> # Start the client in background, ...
   >>> t_client = asyncio.async(client())
   >>> # wait 0.5 seconds, ...
   >>> aiomas.run(asyncio.sleep(0.5))
   >>> # and finally start the server:
   >>> server = aiomas.run(aiomas.channel.start_server(('localhost', 5555), handle_client))
   >>> aiomas.run(t_client)
   ohai
   cya
   >>> server.close()
   >>> aiomas.run(server.wait_closed())



.. _aiomas_msg_format:

How exactly do messages look like?
----------------------------------

This section explains how aiomas messages look and how they are constructed.
You can easily implement this protocol in other languages, too, and write
programs that can communicate with aiomas.

Network messages consists of a four bytes long *header* and a *payload* of
arbitrary length.  The header is an unsigned integer (`uint32
<http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/stdint.h.html#tag_13_47_03_01>`_)
in network byte order (big-endian) and stores the number of bytes in the
payload.  The payload itself is an encoded [*]_ list containing the message
type, a message ID and the actual content:

.. image:: /_static/network-messages.*
   :width: 500
   :align: center
   :alt: Messages consist of a header and a payload.  The payload is a JSON
         list containing a message type, ID and the actual content.

.. [*] Depending on the :doc:`codec <codecs>` you use, the payload may be
       a UTF-8 encoded `JSON <http://www.json.org/>`_ string
       (``json.dumps().encode('utf-8')``) (this is the default), a `MsgPack
       <http://msgpack.org/>`_ list (``msgpack.packb()``), or whatever else
       the codec produces.

Messages send between two peers must follow the `request-reply pattern
<http://en.wikipedia.org/wiki/Request-response>`_.  That means, every request
that one peer makes must be responded to by the other peer.  Request use the
message type ``0``, replies use ``1`` for success or ``2`` to indicate
a failure.  The message ID is an integer that is unique for every request that
a network socket makes.  Replies (no matter if successful or failed) need to
use the message ID of the corresponding request.

On the channel layer, the *content* of a request can be anything.  On the RPC
level, it a three-tuple *(function_path, args, kwargs)*, e.g.:

.. code-block:: json

   [function, [arg0, arg1, ...], {kwarg0: val0, kwarg1: val1}]

Thereby, *function* is always a string containing the name of an exposed
functions; if you use nested services, sub-services and the function names are
separated by slashes (``/``) as in URLs. The type of the `arguments and keyword
arguments <https://docs.python.org/3/glossary.html#term-argument>`_ may vary
depending on the function.

The content types of replies are the same for both, the channel layer and the
RPC layer.  Normal (successful) replies can be anything.  The content of
failure replies are strings with the error message and/or a stack trace.

.. note::

   If the :class:`~aiomas.codecs.JSON` codec is used, aiomas messages are
   compatible with `simpy.io <https://bitbucket.org/simpy/simpy.io>`_ (and
   therewith with the co-simulation framework `mosaik
   <https://mosaik.offis.de>`_, too).
