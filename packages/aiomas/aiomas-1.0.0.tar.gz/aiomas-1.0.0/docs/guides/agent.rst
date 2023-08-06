The agent layer
===============

.. currentmodule:: aiomas.agent

This section describes the agent layer and gives you enough information to
implement your own distributed system without going too much into detail.  For
that, you should also read the section about the :doc:`RPC layer <rpc>`.


Overview
--------

You can think of agents as small, independent programs running in parallel.
Each agent waits for input (e.g., incoming network messages), processes the
input and creates, based on its internal state and the input, some output (like
outgoing network messages).

You can also imagine them as being like normal objects that call other object's
methods.  But instead of calling these methods directly, they do remote
procedure calls (RPC) via a network connection.

In theory, that means that every agent has a little server with an event loop
that waits for incoming messages and dispatches them to the corresponding
method calls.

Using this model, you would quickly run out of resources with hundreds or
thousands of interconnected agents.  For this reason, agents are clustered in
containers.  A container provides the network server and event loop which all
agents within the container share.

Agents are uniquely identified by the container's address and an ID (which is
unique within a container), for example: *tcp://localhost:5555/42*.

The following image illustrates this:  If *Agent C* wants to send a message to
*Agent A*, its container connects to *A's* container.  *Agent C* can now send
a message to *Agent A*.  If *Agent C* now wanted to send a message to *Agent
B*, it would simply reuse the same connection:

.. image:: /_static/agent-container.*
   :width: 650
   :align: center
   :alt: Agents live in containers.  All agents within a container share the
         same network connection.

As you can see in the figure above, containers also have a *clock*, but you can
ignore that for the moment.  We'll come back to it later.


Components of a distributed system in aiomas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Agent:** You implement your business logic in subclasses of
   ``aiomas.Agent``.  Agents can be *reactive* or *proactive*.

   *Reactive* agents only react to incoming messages. That means, they simply
   expose some methods that other agents can call.

   *Proactive* agents actively perform one ore more tasks, i.e., calling
   other agent's methods.

   An agent can be both, *proactive* and *reactive* (that just means that your
   agent class exposes some methods and has one or more tasks running).

2. **Container:** All agents live in a container.  The agent container
   implements everything networking related (e.g., a shared RPC server) so that
   the agent base class can be as light-weight as possible.  It also defines
   the *codec* used for message (de)serialization and provides a *clock* for
   agents.

3. **Codec:** Codecs define how messages to other agents get serialized to
   byte strings that can be sent over the network.  The base codecs can only
   serialize the most common object types (like numbers, strings, lists or
   dicts) but you can extend them with serializers for custom object types.

   The :doc:`Codecs section <codecs>` explain all this in detail.

4. **Clock:** Every container provides a clock for agents.  Clocks are
   important for operations with a timeout (like ``sleep()``).  The default
   clock is a real-time clock synchronized to your system's time.

   However, if you want to integrate your MAS with a simulation, you may want
   to let the time pass faster then real-time (in order to decrease the
   duration of your simulation).  For that use case, aiomas provides a clock
   that can be synchronized with external sources.

   All clocks provide functions to get the current time, sleep for some time
   or execute a task after a given timeout.  If you use these function instead
   of the once asyncio provides, you can easily switch between different kinds
   of clocks.  The :doc:`Clocks section <clocks>` provides more details and
   examples.

Don't worry if you feel a bit confused now.  I'll explore all of this with
small, intuitive examples.


Hello World: A single, proactive agent
--------------------------------------

In our first example, we'll create a very simple agent which repeatedly prints
"Hello, World!":

.. code-block:: python3

   >>> import aiomas
   >>>
   >>> class HelloWorld(aiomas.Agent):
   ...     def __init__(self, container, name):
   ...         # We must pass a ref. to the container to "aiomas.Agent":
   ...         super().__init__(container)
   ...         self.name = name  # Our agent's name
   ...
   ...     async def run(self):
   ...         # This method defines the task that our agent will perform.
   ...         # It's usually called "run()" but you can name it as wou want.
   ...         print(self.name, 'says:')
   ...         clock = self.container.clock
   ...         for i in range(3):
   ...             await clock.sleep(0.1)
   ...             print('Hello, World!')

Agents should be a subclass of :class:`Agent`.  This base class needs
a reference to the container the agents live in, so you must forward
a *container* argument to it if you override ``__init__()``.

Our agent also defines a task ``run()`` which prints "Hello, World!" three
times.  The task also uses the container's clock to sleep for a small amout of
time between each print.

The task ``run()`` can either be started automatically in the agent's
``__init__()`` or manually after the agent has been instantiated.  In our
example, we will do the latter.

The clock (see :mod:`~aiomas.clocks`) exposes various time related functions
similar to those that asyncio offers, but you can easily exchange the default
real-time clock of a container with another one (e.g., one where time passes
faster than real-time, which is very useful in simulations).

Now lets see how we can instantiate and run our agent:

.. code-block:: python3

   >>> # Containers need to be started via a factory function:
   >>> container = aiomas.Container.create(('localhost', 5555))
   >>>
   >>> # Now we can instantiate an agent an start its task:
   >>> agent = HelloWorld(container, 'Monty')
   >>> aiomas.run(until=agent.run())
   Monty says:
   Hello, World!
   Hello, World!
   Hello, World!
   >>> container.shutdown()  # Close all connections and shutdown the server

In order to run the agent, you need to start a :class:`Container` first.  The
container will create an RPC server and bind it to the specified address.

The function :func:`~aiomas.util.run()` is just a wrapper for ``loop
= asyncio.get_event_loop(); loop.run_until_complete(task)``.

These are the very basics auf aiomas' agent module.  In the next example you'll
learn how an agent can call another agent's methods.


Calling other agent's methods
-----------------------------

The purpose of multi-agent systems is having multiple agents calling each
other's methods.  Let's see how we do this.  For the sake of clearness, we'll
create two different agent types in this example where ``Caller`` calls
a method of ``Callee``:

.. code-block:: python3

   >>> import asyncio
   >>> import aiomas
   >>>
   >>> class Callee(aiomas.Agent):
   ...     # This agent does not need to override "__init__()".
   ...
   ...     # "expose"d methods can be called by other agents:
   ...     @aiomas.expose
   ...     def spam(self, times):
   ...         """Return a lot of spam."""
   ...         return 'spam' * times
   >>>
   >>>
   >>> class Caller(aiomas.Agent):
   ...
   ...     async def run(self, callee_addr):
   ...         print(self, 'connecting to', callee_addr)
   ...         # Ask the container to make a connection to the other agent:
   ...         callee = await self.container.connect(callee_addr)
   ...         print(self, 'connected to', callee)
   ...         # "callee" is a proxy to the other agent.  It allows us to call
   ...         # the exposed methods:
   ...         result = await callee.spam(3)
   ...         print(self, 'got', result)
   >>>
   >>>
   >>> container = aiomas.Container.create(('localhost', 5555))
   >>> callee = Callee(container)
   >>> caller = Caller(container)
   >>> aiomas.run(until=caller.run(callee.addr))
   Caller('tcp://localhost:5555/1') connecting to tcp://localhost:5555/0
   Caller('tcp://localhost:5555/1') connected to CalleeProxy('tcp://localhost:5555/0')
   Caller('tcp://localhost:5555/1') got spamspamspam
   >>> container.shutdown()

The agent ``Callee`` exposes its method ``spam()`` via the ``@aiomas.expose``
decorator and thus allows other agents to call this method.  The arguments and
return values of exposed methods need to be :doc:`serializable <codecs>`.
Exposed methods can be normal functions or coroutines.

The ``Caller`` agent does not expose any methods, but defines a task ``run()``
which receives the address of the remote agent.  It can connect to that agent
via the container's :meth:`~Container.connect()` method.  This is a coroutine,
so you need to ``await`` its result.  It's return value is a proxy object to
the remote agent.

Proxies represent a remote object and provide access to exposed attributes
(like functions) of that object.  In the example above, we use the proxy to
call the ``spam()`` function.  Since this involves sending messages to the
remote agent, you always need to use ``await`` with remote method calls.


Distributing agents over multiple containers
--------------------------------------------

One container can house a (theoretically) unlimited number of agents.  As long
as your agents spent most of the time waiting for network IO, there’s no need
to use more than one container.

If you notice, that the Python process with your program fully utilizes its CPU
core (remember, pure Python only uses one core), its time to spawn
sub-processes with its own container to actually parallelize your application.
The :mod:`aiomas.subproc` module provides some helpers for this use case.

Running multiple agent containers in a single process might only be helpful for
demonstration or debugging purposes.  In the latter case, you should also take
a look at the :mod:`aiomas.local_queue` transport.  You can replace normal TCP
sockets with it and gain a deterministic order of outgoing and incoming
messages between multiple containers within a single process.
