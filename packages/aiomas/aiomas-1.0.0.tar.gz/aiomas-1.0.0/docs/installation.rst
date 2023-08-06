Installation
============

*aiomas* requires Python >= 3.4 and runs on Linux, OS X and Windows.  The
default installation uses the *JSON* codec and only has pure Python
dependencies.

If you have an active virtualenv__, you can just run pip__ to install it:

.. code-block:: console

   $ pip install aiomas

If you don't use a virtualenv (you should) and are not sure, which Python
interpreter pip will use, you can manually select one:

.. code-block:: console

   $ python3.5 -m pip install aiomas

__ https://virtualenv.pypa.io/en/latest/
__ https://pip.pypa.io/


Updating aiomas
---------------

To upgrade your installation, use the ``-U`` flag for the ``install`` command:

.. code-block:: console

   $ pip install -U aiomas


.. _install_msgpack_blosc:

Using MsgPack and Blosc
-----------------------

The MsgPack__ codec and its Blosc__ compressed version are optional features,
that you need to explicitly install if you need them.  Both packages require
a C compiler for the installation:

.. code-block:: console

   $ pip install aiomas[mp]   # Enables the MsgPack codec
   $ pip install aiomas[mpb]  # Enables the MsgPack and MsgPackBlosc codecs

__ https://pypi.python.org/pypi/msgpack-python/
__ https://pypi.python.org/pypi/blosc/

Windows users can download pre-compiled binary packages from `Christoph
Gohlke’s website`__ (msgpack__ | blosc__) and install them with *pip*:

.. code-block:: doscon

   C:\> pip install aiomas
   C:\> pip install Downloads\msgpack_python-0.4.7-cp35-none-win_amd64.whl
   C:\> pip install Downloads\blosc-1.2.8-cp35-none-win_amd64.whl

__ http://www.lfd.uci.edu/~gohlke/pythonlibs/
__ http://www.lfd.uci.edu/~gohlke/pythonlibs/#msgpack
__ http://www.lfd.uci.edu/~gohlke/pythonlibs/#blosc
