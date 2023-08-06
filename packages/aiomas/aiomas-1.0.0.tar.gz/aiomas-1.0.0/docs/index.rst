=================================
Welcome to aiomas' documentation!
=================================

`PyPI <https://pypi.python.org/pypi/aiomas>`_ |
`Bitbucket <https://bitbucket.org/sscherfke/aiomas>`_ |
`Mailing list <https://groups.google.com/forum/#!forum/python-tulip>`_ |
IRC: #asyncio

*aiomas* is an easy-to-use library for *request-reply channels*, *remote
procedure calls (RPC)* and *multi-agent systems (MAS)*.  It’s written in pure
Python on top of `asyncio <https://docs.python.org/3/library/asyncio.html>`_.

The package is released under the MIT license. It requires Python 3.4 and above
and runs on Linux, OS X, and Windows.

Below you’ll find a list of features.  You can also take a look at the
:doc:`overview section <overview>` to learn what aiomas is and see some simple
examples.  If you like this package, go and :doc:`install <installation>` it!


Features
========

- Three layers of abstraction around raw TCP / unix domain sockets:

  #. Request-reply channels

  #. Remore-procedure calls (RPC)

  #. Agents and containers

- TLS support for authorization and encrypted communication.

- Interchangeable and extensible codecs: JSON__ and MsgPack__ (the latter
  optionally compressed with Blosc) are built-in.  You can add custom codecs or
  write (de)serializers for your own objects to extend a codec.

- Deterministic, emulated sockets: A *LocalQueue* transport lets you send and
  receive message in a deterministic and reproducible order within a single
  process.  This helps testing and debugging distributed algorithms.

__ http://www.json.org/
__ http://msgpack.org/


Contents:
=========

.. toctree::
   :maxdepth: 2

   overview
   installation
   guides/index
   api_reference/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
