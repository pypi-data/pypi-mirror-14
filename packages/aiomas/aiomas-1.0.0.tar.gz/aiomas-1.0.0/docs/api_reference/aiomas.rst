.. module:: aiomas

``aiomas``
==========

This module provides easier access to the most used components of *aiomas*.
This purely for your convenience and you can, of cource, also import everything
from its actual submodule.

Decorators
----------

.. autosummary::
   ~aiomas.rpc.expose
   ~aiomas.codecs.serializable


Functions
---------

.. autosummary::
   ~aiomas.util.async
   ~aiomas.local_queue.get_queue
   ~aiomas.util.make_ssl_server_context
   ~aiomas.util.make_ssl_client_context
   ~aiomas.util.run


Exceptions
----------

.. autosummary::
   ~aiomas.exceptions.AiomasError
   ~aiomas.exceptions.RemoteException


Classes
-------

.. currentmodule:: aiomas.codecs
.. autosummary::
   ~aiomas.agent.Agent
   ~aiomas.clocks.AsyncioClock
   ~aiomas.agent.Container
   ~aiomas.clocks.ExternalClock
   ~aiomas.codecs.JSON
   ~aiomas.codecs.MsgPack
   ~aiomas.codecs.MsgPackBlosc
   ~aiomas.agent.SSLCerts
