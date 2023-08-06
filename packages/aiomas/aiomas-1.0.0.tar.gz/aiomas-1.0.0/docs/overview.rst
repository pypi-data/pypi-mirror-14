Overview
========

Aiomas' main goal is making it easier to create distributed systems (like
*multi-agent systems (MAS))* with pure Python and `asyncio`__.

Therefore, it adds three layers of abstraction around the transports (TCP or
Unix domain sockets) that asyncio provides:

__ https://docs.python.org/3/library/asyncio.html

.. image:: /_static/overview.*
   :width: 430
   :align: center
   :alt: The three architectual layers of aiomas


1. The :doc:`channel layer <guides/channel>` allows you to send and receive
   actual data like strings, lists of numbers instead of single bytes.

   The :class:`~aiomas.channel.Channel` class lets you make *requests* and
   asynchronously wait for the corresponding *replies*.

   Every *channel* has a :class:`~aiomas.codecs.Codec` instance that is
   responsible for (de)serializing the data that is being sent via the channel.
   By default, JSON__ is used for that.  Alternatively, you can use MsgPack__
   and optionally compress it using Blosc__.  You can also extend codecs with
   custom serializers for more object types.

   __ http://www.json.org/
   __ http://msgpack.org/
   __ http://blosc.org/

   .. code-block:: python3

      >>> import aiomas
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
      >>> async def client():
      ...     """Client coroutine: Send a greeting to the server and wait for a
      ...     reply."""
      ...     channel = await aiomas.channel.open_connection(('localhost', 5555))
      ...     rep = await channel.send('ohai')
      ...     print(rep)
      ...     await channel.close()
      >>>
      >>>
      >>> server = aiomas.run(aiomas.channel.start_server(('localhost', 5555), handle_client))
      >>> aiomas.run(client())
      ohai
      cya
      >>> server.close()
      >>> aiomas.run(server.wait_closed())

2. The :doc:`remote procedure call (RPC) layer <guides/rpc>` lets you call
   function on remote objects.

   You can expose the methods of an object as well as normal functions within
   a dict.  On the peer side of the connection, proxy objects represent these
   exposed functions.

   .. code-block:: python3

      >>> import aiomas
      >>>
      >>>
      >>> class MathServer:
      ...     router = aiomas.rpc.Service()
      ...
      ...     @router.expose
      ...     def add(self, a, b):
      ...         return a + b
      ...
      >>>
      >>> async def client():
      ...     """Client coroutine: Call the server's "add()" method."""
      ...     rpc_con = await aiomas.rpc.open_connection(('localhost', 5555))
      ...     rep = await rpc_con.remote.add(3, 4)
      ...     print('What’s 3 + 4?', rep)
      ...     await rpc_con.close()
      >>>
      >>> server = aiomas.run(aiomas.rpc.start_server(('localhost', 5555), MathServer()))
      >>> aiomas.run(client())
      What’s 3 + 4? 7
      >>> server.close()
      >>> aiomas.run(server.wait_closed())

3. The :doc:`agent layer <guides/agent>` hides some of the *RPC* layer's
   complexity and allows you to create thousands of interconnected objects
   *(agents)* without opening thousands of unique connections between them.

   Therefore, all agents live within a *container*.  Containers take care of
   handling agent instances and performing the communication between them.

   The container provides a *clock* for the agents. This clock can either be
   synchronized with the real (wall-clock) time or be set by an external
   process (e.g., external simulators).

   .. code-block:: python3

      >>> import aiomas
      >>>
      >>> class TestAgent(aiomas.Agent):
      ...     def __init__(self, container):
      ...         super().__init__(container)
      ...         print('Ohai, I am %s' % self)
      ...
      ...     async def run(self, addr):
      ...         remote_agent = await self.container.connect(addr)
      ...         ret = await remote_agent.service(42)
      ...         print('%s got %s from %s' % (self, ret, remote_agent))
      ...
      ...     @aiomas.expose
      ...     def service(self, value):
      ...         return value
      >>>
      >>> c = aiomas.Container.create(('localhost', 5555))
      >>> agents = [TestAgent(c) for i in range(2)]
      Ohai, I am TestAgent('tcp://localhost:5555/0')
      Ohai, I am TestAgent('tcp://localhost:5555/1')
      >>> aiomas.run(until=agents[0].run(agents[1].addr))
      TestAgent('tcp://localhost:5555/0') got 42 from TestAgentProxy('tcp://localhost:5555/1')
      >>> c.shutdown()

The following sections explain theses layers in more detail.
