The RPC layer
=============

*Remote procedure calls* let you, as the name suggest, call functions or
methods of remote objects via a network connection (nearly) like you would call
local functions.  This often leads to more readable code compared to using the
lower level :doc:`channels <channel>`.


Basics
------

The basic idea behind RPC is as follows: You have a remote object with some
methods.  On the local side of the connection you have a proxy object which has
the same signature, but when you call one of the proxy's methods, it actually
sends a message *(method_name, args, kwargs)* to the peer.  The peer has
a router that maps *method_name* to an actual method.  It calls the method and
sends its return value back to the proxy.  The proxy method returns this value
as if it was calculated locally.  This works very similarly to how
web-frameworks like Django resolve URLs and map them to views.

The following list briefly explains the most important components of aiomas
RPC:

Service side:

- An *RPC server:* It starts a server socket and as a *root* object whose methods
  can be called by clients.

- An *RPC service* (or a hierarchy of services): RPC services are classes with
  methods that clients can call.  Instead of classes with methods you can also
  use dicts with normal functions.  Services can be nested to created
  hierarchies.

- *RPC routers:* Routers map function names (or paths) to actual methods.  An
  class with an RPC service automatically creates a new router for each of its
  instances.

- *Exposed* methods:  Methods/functions need to be explicitly exposed via
  a simple decorator.  This is a security and safety measure which makes sure
  that clients can only call functions they are intended to.

Client side:

- An *RPC client:* It represents a network connection to an RPC server and
  provides a proxy object to its service.

- *RPC proxies:* Proxy objects represent the remote services.  They resemble
  the signature of the services they represent and delegate method calls to
  them.

Here is a simple example that demonstrate how these components work together:

.. code-block:: python3

   >>> import aiomas
   >>>
   >>>
   >>> class MathServer:
   ...     # The "Service" creates a router for each instance of "MathServer":
   ...     router = aiomas.rpc.Service()
   ...
   ...     # Exposed methods can be called by clients:
   ...     @aiomas.expose
   ...     def add(self, a, b):
   ...         return a + b
   ...
   >>>
   >>> async def client():
   ...     """Client coroutine: Call the server's "add()" method."""
   ...     # Connect to the RPC server and get an "RpcClient":
   ...     rpc_con = await aiomas.rpc.open_connection(('localhost', 5555))
   ...     # "remote" is a Proxy to the remote service.
   ...     # We cann call its "add()" method:
   ...     rep = await rpc_con.remote.add(3, 4)
   ...     print('What’s 3 + 4?', rep)
   ...     await rpc_con.close()
   >>>
   >>> # Start the RPC server with an instance of the "MathServer" service:
   >>> server = aiomas.run(aiomas.rpc.start_server(('localhost', 5555), MathServer()))
   >>>
   >>> aiomas.run(client())
   What’s 3 + 4? 7
   >>> server.close()
   >>> aiomas.run(server.wait_closed())

Let's discuss the details of what we just did:

The class ``MathServer`` is going to be the root node of our RPC server.
Therefore, it needs to be marked as RPC service by giving it a *router*
attribute with an :class:`aiomas.rpc.Service` instance.  ``Service`` is
a descriptor; when you access the *router* attribute through the ``MathServer``
class, you get the ``Service`` instance, but when you access it via a
``MathServer`` instance, you get an :class:`aiomas.rpc.Router` instance
instead.  The ``Service`` descriptor makes sure that every instance of
``MathServer`` automatically gets its own ``Router`` instance.

The ``add()`` method is decorated with :func:`~aiomas.rpc.expose()` which makes
it available for RPC calls.  The arguments and return values of exposed
functions must be serializable by the :class:`~aiomas.codecs.Codec` used.
Numbers, booleans, strings, lists and dicts should always work.

When we start our RPC server (via :func:`aiomas.rpc.start_server()`) we need to
pass an instance of our ``MathServer`` class to it.

In the client, we create an RPC connection via
:func:`aiomas.rpc.open_connection()`.  It returns an
:class:`aiomas.rpc.RpcClient` instance.  We can get the proxy to the RPC root
node via its :attr:`~aiomas.rpc.RpcClient.remote` attribute.  In contrast to
normal method calls, we need to use the :keyword:`await` (or ``yield
from``) statement for remote method calls.


Using dictionaries with functions as RPC services
-------------------------------------------------

Sometimes, you don't want or don't need classes but plain Python functions.
With aiomas you can put them in a dict and expose them as an RPC service, too.
Here's a rewrite of out math server example that we discussed in the last
section:

.. code-block:: python3

   >>> @aiomas.expose
   ... def add(a, b):
   ...     return a + b
   ...
   >>> math_service = aiomas.rpc.ServiceDict({
   ...     'add': add,
   ... })
   >>>
   >>> # Start the RPC server with the math service:
   >>> server = aiomas.run(aiomas.rpc.start_server(('localhost', 5555), math_service))
   >>>
   >>> # The client stays the same as in our last example:
   >>> aiomas.run(client())
   What’s 3 + 4? 7
   >>> server.close()
   >>> aiomas.run(server.wait_closed())


You just need a dict mapping names to the respective functions and wrap it with
:class:`aiomas.rpc.ServiceDict`.  You can then uses this to start an RPC
server.


How to build hierarchies of RPC services
----------------------------------------

When you want to expose a lot of functions, you may wish to group and
categorize them.  You can do this by building hierarchies of RPC services (just
think of the RPC services as folders and the exposed methods as files, for
example).  On the client side, you use the ``.`` operator to access
a sub-service (e.g., ``root_service.sub_service.method()``).

When you build service hierarchies, you can freely mix class-based and
dictionary-based services.

If the parent service is a dictionary, you can add sub services as a new
``name: service_instance`` pair:

.. code-block:: python3

   >>> @aiomas.expose
   ... def add(a, b):
   ...     return a + b
   ...
   >>> # A Sub-service for addition
   >>> adding_service = aiomas.rpc.ServiceDict({
   ...     'add': add,
   ... })
   >>>
   >>> # A Sub-service for subtraction
   >>> class SubService:
   ...     router = aiomas.rpc.Service()
   ...
   ...     @aiomas.expose
   ...     def sub(self, a, b):
   ...         return a - b
   ...
   >>> # Service dict with two sub-services:
   >>> root_service = aiomas.rpc.ServiceDict({
   ...     'addition': adding_service,   # Service dict
   ...     'subtraction': SubService(),  # Instance(!) of service class
   ... })
   >>>
   >>> async def client():
   ...     rpc_con = await aiomas.rpc.open_connection(('localhost', 5555))
   ...     # Call the addition service:
   ...     rep = await rpc_con.remote.addition.add(3, 4)
   ...     print('What’s 3 + 4?', rep)
   ...     # Call the subtraction service:
   ...     rep = await rpc_con.remote.subtraction.sub(4, 3)
   ...     print('What’s 4 - 3?', rep)
   ...     await rpc_con.close()
   >>>
   >>> server = aiomas.run(aiomas.rpc.start_server(('localhost', 5555), root_service))
   >>>
   >>> aiomas.run(client())
   What’s 3 + 4? 7
   What’s 4 - 3? 1
   >>> server.close()
   >>> aiomas.run(server.wait_closed())

As you can see, this is very straight forward.  Like a folder that can contain
sub-folders and files, a :class:`~aiomas.rpc.ServiceDict` can contain
sub-services and exposed functions.

Adding sub-services to a service class looks a little bit more complicated, but
basically works the same:

.. code-block:: python3

   >>> @aiomas.expose
   ... def add(a, b):
   ...     return a + b
   ...
   >>> # A Sub-service for addition
   >>> adding_service = aiomas.rpc.ServiceDict({
   ...     'add': add,
   ... })
   >>>
   >>> # A Sub-service for subtraction
   >>> class SubService:
   ...     router = aiomas.rpc.Service()
   ...
   ...     @aiomas.expose
   ...     def sub(self, a, b):
   ...         return a - b
   ...
   >>> class RootService:
   ...     # You first have to declare that instances of this class will have
   ...     # the following sub-services:
   ...     router = aiomas.rpc.Service(['addition', 'subtraction'])
   ...
   ...     def __init__(self):
   ...         # For each(!) instance, you have to add instances of the
   ...         # declared sub-services:
   ...         self.addition = adding_service
   ...         self.subtraction = SubService()
   >>>
   >>>
   >>> server = aiomas.run(aiomas.rpc.start_server(('localhost', 5555), RootService()))
   >>>
   >>> # The client remains the same
   >>> aiomas.run(client())
   What’s 3 + 4? 7
   What’s 4 - 3? 1
   >>> server.close()
   >>> aiomas.run(server.wait_closed())

What makes adding sub-services to classes a bit more complicated is the fact
that classes define the service hierarchy but you use instances for the actual
RPC servers.   That's why you first need to declare at class level which
attributes will hold sub-services and then actually add these sub-services in
the class' ``__init__()``.

You can also manually compose hierarchies with the router's
:meth:`~aiomas.rpc.Router.add()` and
:meth:`~aiomas.rpc.Router.set_sub_router()` methods.  These methods give you
a bit more flexibility to create service hierarchies on-the-fly:

.. code-block:: python3

   >>> @aiomas.expose
   ... def add(a, b):
   ...     return a + b
   ...
   >>> # A Sub-service for addition
   >>> adding_service = aiomas.rpc.ServiceDict({
   ...     'add': add,
   ... })
   >>>
   >>> # A Sub-service for subtraction
   >>> class SubService:
   ...     router = aiomas.rpc.Service()
   ...
   ...     @aiomas.expose
   ...     def sub(self, a, b):
   ...         return a - b
   ...
   >>> class RootService:
   ...     # In contrast to the last example, we don't declare any sub-services:
   ...     router = aiomas.rpc.Service()
   ...
   ...     def __init__(self):
   ...         # Add a sub-services via the router's "add()" method:
   ...         self.addition = adding_service
   ...         self.router.add('addition')
   ...
   ...         # Add a sub-service via the router's "set_sub_router()" method:
   ...         self.subtraction = SubService()
   ...         self.router.set_sub_router(self.subtraction.router, 'subtraction')
   >>>
   >>>
   >>> server = aiomas.run(aiomas.rpc.start_server(('localhost', 5555), RootService()))
   >>>
   >>> # The client remains the same
   >>> aiomas.run(client())
   What’s 3 + 4? 7
   What’s 4 - 3? 1
   >>> server.close()
   >>> aiomas.run(server.wait_closed())

The method :meth:`~aiomas.rpc.Router.add()` looks the associated object has an
attribute with the specified name that holds the sub services.  That service is
then exposed via the same name.

Using the method :meth:`~aiomas.rpc.Router.set_sub_router()`, you can set any
router as a sub-router and expose it via the specified name.  This provides the
most flexibility for building service hierarchies.


.. _rpc_router_serialization:

Bi-directional RPC: How to allow callbacks from server to client
----------------------------------------------------------------

Aiomas supports bi-directional RPC.  That means that not only can a client call
server methods, but a server can also call client methods.

For uni-directional RPC, the server specifies an RPC services and a client gets
a proxy to it when it makes a connection to the server.  For bi-directional
RPC, you also need to define a service for your client.  The client can pass
its service instance as argument of an RPC to the server.  The server will
then receive a proxy to that service, that it can use to make calls back to the
client.

That works because objects with a ``router`` attribute that is an RPC router
can be serialized and be sent to the peer where they get deserialized to an RPC
proxy object.

Let's look at an example to see how it works.  The first example uses
class-based services:

.. code-block:: python3

   >>> import aiomas
   >>>
   >>>
   >>> class Client:
   ...     # The client needs to be marked as RPC service:
   ...     router = aiomas.rpc.Service()
   ...
   ...     def __init__(self, name):
   ...         self.name = name
   ...
   ...     async def run(self):
   ...         # When we open a connection, we need to pass the service instance
   ...         # ("self" in this case) so that a background task for it can be
   ...         # started:
   ...         rpc_con = await aiomas.rpc.open_connection(('localhost', 5555),
   ...                                                    rpc_service=self)
   ...
   ...         # We can now pass the service to the server when we call one of its
   ...         # methods:
   ...         rep = await rpc_con.remote.server_method(self)
   ...         print('Server reply:', rep)
   ...
   ...         await rpc_con.close()
   ...
   ...     # This method is exposed to the server:
   ...     @aiomas.expose
   ...     def get_client_name(self):
   ...         return self.name
   >>>
   >>>
   >>> class Server:
   ...     router = aiomas.rpc.Service()
   ...
   ...     @aiomas.expose
   ...     async def server_method(self, client_proxy):
   ...         # When a client passes a reference to its service, we'll receive it as
   ...         # a proxy object which we can use to call a client method:
   ...         client_name = await client_proxy.get_client_name()
   ...         return 'Client name is "%s"' % client_name
   >>>
   >>>
   >>> server = aiomas.run(aiomas.rpc.start_server(('localhost', 5555), Server()))
   >>>
   >>> aiomas.run(Client('Monty').run())
   Server reply: Client name is "Monty"
   >>>
   >>> server.close()
   >>> aiomas.run(server.wait_closed())

Bi-directional RPC works with class-based as well as dict-based services.
Furthermore, if your server or client provide a hierarchy of services, you can
not only pass the root service but also any of its sub-services as function
arguments.


How to handle remote exceptions
-------------------------------

If an RPC raises an error, aiomas wraps it with
a :exc:`~aiomas.exceptions.RemoteException` and forwards it to the caller.  It
also provides you the source (peer name) of the exception and its original
traceback:

.. code-block:: python3

   >>> @aiomas.expose
   ... def fail_badly():
   ...     raise ValueError('"spam" is not a number')
   >>>
   >>> service = aiomas.rpc.ServiceDict({'fail_badly': fail_badly})
   >>>
   >>> async def client():
   ...     rpc_con = await aiomas.rpc.open_connection(('127.0.0.1', 5555))
   ...     try:
   ...         await rpc_con.remote.fail_badly()
   ...     except aiomas.RemoteException as exc:
   ...         print('Origin:', exc.origin)
   ...         print('Traceback:', exc.remote_traceback)
   >>>
   >>> server = aiomas.run(aiomas.rpc.start_server(('127.0.0.1', 5555), service))
   >>>
   >>> aiomas.run(client())
   Origin: ('127.0.0.1', 5555)
   Traceback: Traceback (most recent call last):
     ...
   ValueError: "spam" is not a number
   <BLANKLINE>
   >>> server.close()
   >>> aiomas.run(server.wait_closed())

It is currently not possible to forward the original exception instance,
because the caller might not have the required code available (However, I won't
rule out the possibility that I might eventually implement this).


How to get a list of connected clients
--------------------------------------

An RPC service on the server side does not know if or when a new client
connects.  However, you can pass a *client connected callback* to
:func:`aiomas.rpc.start_server()` that cats called once for each new
connection.  Its only argument is the :class:`~aiomas.rpc.RpcClient` for that
connection.  You can uses this, for example, to close the connection with the
client or call the client's exposed methods (if there are some).

.. code-block:: python3

   >>> service = aiomas.rpc.ServiceDict({})
   >>>
   >>> async def client():
   ...     rpc_con = await aiomas.rpc.open_connection(('127.0.0.1', 5555))
   ...     await rpc_con.close()
   >>>
   >>> def client_connected_cb(rpc_client):
   ...     print('Client connected:', rpc_client)
   >>>
   >>> server = aiomas.run(aiomas.rpc.start_server(('127.0.0.1', 5555), service,
   ...                                             client_connected_cb))
   >>>
   >>> aiomas.run(client())
   Client connected: <aiomas.rpc.RpcClient object at 0x...>
   >>> server.close()
   >>> aiomas.run(server.wait_closed())


How to handle connection losses
-------------------------------

For many reasons, the connection between two endpoints can be lost at any time.

If you are in a coroutine and actively doing RPC, you will get
a :exc:`ConnectionResetError` thrown into your coroutine if the connection
drops:

.. code-block:: python3

   >>> import aiomas
   >>>
   >>>
   >>> async def client():
   ...     rpc_con = await aiomas.rpc.open_connection(('localhost', 5555))
   ...     # The server will close the connection when we make the following call:
   ...     try:
   ...         await rpc_con.remote.close_connection()
   ...     except ConnectionResetError:
   ...         print('Connection lost :(')
   >>>
   >>>
   >>> class Server:
   ...     router = aiomas.rpc.Service()
   ...
   ...     def __init__(self):
   ...         self.clients = []
   ...
   ...     def client_connected(self, client):
   ...         """*Client connected cb.* that adds new clients to ``self.clients``"""
   ...         self.clients.append(client)
   ...
   ...     @aiomas.expose
   ...     async def close_connection(self):
   ...         """Close all open connections and remove them from ``self.clients``."""
   ...         while self.clients:
   ...             client = self.clients.pop()
   ...             await client.close()
   >>>
   >>> server_service = Server()
   >>> server = aiomas.run(aiomas.rpc.start_server(('localhost', 5555),
   ...                                             server_service,
   ...                                             server_service.client_connected))
   >>>
   >>> aiomas.run(client())
   Connection lost :(
   >>>
   >>> server.close()
   >>> aiomas.run(server.wait_closed())

If you only serve an RPC service, it gets a little bit more complicated,
because RPC services are not connection-aware.  However,
:meth:`aiomas.rpc.RpcClient.on_connection_reset()` lets you register a callback
that gets called when the connection is lost.  (You get an instance of
:class:`~aiomas.rpc.RpcClient` as return value from
:func:`~aiomas.rpc.open_connection()` or via
:func:`~aiomas.rpc.start_server()`'s *client connected callback*.)

In the following example, the server again has a list of connected clients.
But this time, the client disconnects and the server removes the closed
connection from its list of clients:

.. code-block:: python3

   >>> import aiomas
   >>>
   >>>
   >>> async def client():
   ...     rpc_con = await aiomas.rpc.open_connection(('localhost', 5555))
   ...     await rpc_con.close()
   >>>
   >>>
   >>> class Server:
   ...     router = aiomas.rpc.Service()
   ...
   ...     def __init__(self):
   ...         self.clients = []
   ...
   ...     def client_connected(self, client):
   ...         # Register a callback that removes the client from our list
   ...         # when it disconnects:
   ...         def remove_client(exc):
   ...             print('Client disconnected :(')
   ...             self.clients.remove(client)
   ...
   ...         client.on_connection_reset(remove_client)
   ...         print('Client connected :)')
   ...         self.clients.append(client)
   >>>
   >>> server_service = Server()
   >>> server = aiomas.run(aiomas.rpc.start_server(('localhost', 5555),
   ...                                             server_service,
   ...                                             server_service.client_connected))
   >>>
   >>> aiomas.run(client())
   Client connected :)
   Client disconnected :(
   >>>
   >>> server.close()
   >>> aiomas.run(server.wait_closed())
