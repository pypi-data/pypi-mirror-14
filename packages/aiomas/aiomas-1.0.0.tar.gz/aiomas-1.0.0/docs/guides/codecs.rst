Codecs for message serialization
================================

Codecs are used to convert the objects that you are going to send over the
network to bytes and the bytes that you received back to the original objects.
This is called *serialization* and *deserialization*.

A codec specifies, how the text representation of a certain object looks like.
It can also recreate the object based on its text representation.

For example, the JSON encoded representation of the list ``['spam', 3.14]``
would be ``b'["spam",3.14]'``.

Many different codecs exists.  Some of the most widely used ones are JSON__,
XML__ or MsgPack__.  They mainly differ in their:

- verbosity or compactness: How many bytes are needed to encode an
  object?

- performance: How fast can they encode and decode objects?

- readability: Can the result easily be read by humans?

- availability on different platforms: For which programming languages do
  libraries or bindings exist?

- security: Is it possible to decode bytes to arbitrary objects?

__ http://www.json.org/
__ http://www.w3.org/XML/
__ http://msgpack.org/

Which codec is the best very much depends on your specific requirements.
An evaluation of different codecs and serialization formats is beyond
the scope of this document, though.


Which codecs does aiomas support?
---------------------------------

Aiomas implements the following codecs:

- :class:`aiomas.codecs.JSON`

- :class:`aiomas.codecs.MsgPack`

- :class:`aiomas.codecs.MsgPackBlosc`

JSON
^^^^

We chose JSON as default, because it is available through the standard library
(no additional dependencies) and because it is relatively efficient (both, in
terms of performance and serialization results).  It is also widely used and
supported as well as human readable.


MsgPack
^^^^^^^

The MsgPack codec can be more efficient but requires you to compile
a C extension.  For this reason, it is not enabled by default but available as
an extra feature.  To install it run:

.. code-block:: bash

   $ pip install -U aiomas[mp]  # Install aiomas with MsgPack
   $ # or
   $ pip install -U aiomas msgpack-python


MsgPackBlosc
^^^^^^^^^^^^

If you want to send long messages, e.g., containing large NumPy arrays, further
compressing the results of MsgPack with Blosc__ can give you additional
performance.  To enable it, install:

__ http://blosc.org/

.. code-block:: bash

   $ pip install -U aiomas[mpb]  # Install aiomas with MsgPack-Blosc
   $ # or
   $ pip install -U aiomas msgpack-python blosc


Which codec should I use?
^^^^^^^^^^^^^^^^^^^^^^^^^

You should always start with the default JSON codec.  It should usually be
"good enough".

If your messages contain large chunks of binary data (e.g., serialized NumPy
arrays), you should evaluate MsgPack, because it natively serializes objects to
bytes.

MsgPackBlosc may yield better performance then MsgPack if your messages become
very large and/or you really send *a lot* of messages.  The codec can decrease
the memory consumption of your program and reduce the time it takes to send
a message.

.. note::

   All codecs live in the :mod:`aiomas.codecs` package but, for your
   convenience, you can also import them directly from :mod:`aiomas`.


How do I use codecs?
--------------------

As a normal user, you don't have to interact with codecs directly.  You only
need to pass the class object of the desired codec as a parameter to some
functions and classes if you don't want to use the default.

.. _which-object-types-can-be-de-serialized:

Which object types can be (de)serialized?
-----------------------------------------

All codecs bundled with aiomas support serializing the following types out of
the box:

- ``NoneType``

- ``bool``

- ``int``

- ``float``

- ``str``

- ``list`` / ``tuple``

- ``dict``

MsgPack and MsgPackBlosc also support ``bytes``.

.. note::

   JSON deserializes both, lists *and* tuples, to lists.  MsgPack on the other
   hand deserializes them to tuples.

RPC connections support serializing arbitrary objects with RPC routers which
get deserialized to Proxies for the corresponding remote object.  See
:ref:`rpc_router_serialization` for details.

In addition, connections made by a :class:`~aiomas.agent.Container` support
Arrow__ date objects.

__ http://crsmithdev.com/arrow/


How do I add serializers for additional object types?
-----------------------------------------------------

All functions and classes that accept a *codec* parameter also accept an
optional list of *extra_serializers*.  The list must contain callables with the
following signature: ``callable() -> tuple(type, serialization_func,
deserialisation_func)``.

The *type* is a class object.  The serializer will be applied to all *direct*
instances of that class but *not* to subclasses.  This may change in the
future, however.  The only exception is a serializer for ``object`` which, if
specified, serves as a fall-back for objects that couln't be serialized other
ways (this is used by RPC connections to serialize objects with an RPC router).

The *serializer_func* is a callable with one argument -- the object to be
serialized -- and needs to return an object that is serializable by the base
codec (e.g., a *str*, *bytes* or *dict*).

The *deserializer_func* has the same signature, but the argument is the
serialized object and the return value a deserialized equivalent of the
original object.  Usually, "equivalent" means "an object of the same type as
the original", but objects with an RPC router, for example, get deserialized to
proxies for the original objects in order to allow remote procedure calls on
them.

Here is an example that shows how a serializer for NumPy arrays might look
like.  It will only work for the *MsgPack* and *MsgPackBlosc* codecs, because
the dict returned by *_serialize_ndarray()* contains byte strings which JSON
cannot handle:

.. code-block:: python

   import aiomas
   import numpy as np

   def get_np_serializer():
      """Return a tuple *(type, serialize(), deserialize())* for NumPy arrays
      for usage with an :class:`aiomas.codecs.MsgPack` codec.

      """
      return np.ndarray, _serialize_ndarray, _deserialize_ndarray


   def _serialize_ndarray(obj):
      return {
         'type': obj.dtype.str,
         'shape': obj.shape,
         'data': obj.tostring(),
      }


   def _deserialize_ndarray(obj):
      array = np.fromstring(obj['data'], dtype=np.dtype(obj['type']))
      return array.reshape(obj['shape'])


   # Usage:
   c = aiomas.Container(('localhost', 5555), codec=aiomas.MsgPack,
                        extra_serializers=[get_np_serializer])


How to create custom codecs
---------------------------

The base class for all codecs is :class:`aiomas.codecs.Codec`.

Subclasses must at least implement the :meth:`~aiomas.codecs.Codec.encode()`
and :meth:`~aiomas.codecs.Codec.decode()` methods.

You can use the existing codecs (e.g., :class:`~aiomas.codecs.JSON` or
:class:`~aiomas.codecs.MsgPack`) as examples.
