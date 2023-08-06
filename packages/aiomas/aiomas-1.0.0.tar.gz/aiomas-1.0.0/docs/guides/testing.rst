Testing and debugging
=====================

Here are some general rules and ideas for developing and debugging distributed
systems with aiomas:

- Distributed systems are complex.  Always start as simple as possible.
  Examine and understand the behavior of that system.  Start adding a bit more
  complexity.  Repeat.

- I find using a debugger does not work very well with async., distributed
  systems, so I tend to add a lot of logging and or :func:`print()`\ s to my
  code for debugging purposes.

- Read `Develop with asyncio`__.

  __ https://docs.python.org/3/library/asyncio-dev.html

- If you `enable asyncio's debug mode`__, aiomas also falls into debug mode.
  It gives you better / more detailed exceptions in some cases.  This impacts
  performance, so it isn't activated always.

  __ https://docs.python.org/3/library/asyncio-dev.html#asyncio-debug-mode

- Write unit and integration tests and run them as often as possible.  Also
  check that your tests will fail if they should.


Testing coroutines and agents with pytest
-----------------------------------------

My preferred testing tool is `pytest <http://pytest.org/>`_.  The plug-in
`pytest-asyncio <https://pypi.python.org/pypi/pytest-asyncio>`_ makes testing
asyncio based programs a lot easier.

As an introduction, I also suggest reading my `articles on testing with asyncio
<https://stefan.sofa-rockers.org/tag/asyncio/>`_.  They are especially helpful
if you are using the channel and RPC layers.  Testing agent systems is a bit
"easier" (in the sense that the tests are easier to setup).  You can, of
course, also look at `aiomas' test suite
<https://bitbucket.org/sscherfke/aiomas/src/tip/tests/>`_ itself.

Here is a small example that demonstrate how you could test an agent.  In this
case, the agent class itself and the tests for it are in the same module.  In
real life, you would have the agent and its test in separate packages (e.g.,
:file:`exampleagent.py` and :file:`test_exampleagent.py`).

.. literalinclude:: test_example.py
   :lines: 1-41,47-
