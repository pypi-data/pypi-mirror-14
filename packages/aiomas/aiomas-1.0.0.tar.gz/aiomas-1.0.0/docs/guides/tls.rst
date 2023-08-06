Enabling transport security (TLS)
=================================

.. We need to change the cwd to the directory containing the test certs:
   >>> import os
   >>> os.chdir('tests/certs/')

This guide explains how you can encrypt all messages sent with aiomas.
Transport layer security (`TLS`__, formerly known as SSL) can be applied in
a similar fashion to all three layers (channel, RPC, agent) of aiomas and the
following sections will show you how.

__ https://en.wikipedia.org/wiki/Transport_Layer_Security

.. note::

   Even if you don't have much experience with cryptography, you should be able
   to follow this guide and use TLS encryption for your program.

   Nonetheless, I strongly recommend you to learn the basics of it.  A good
   read is `Crypto 101, by Laurens Van Houtven`__.  Sean Cassidy also provides
   a `nice overview about starting with crypto`__.  There are also various
   tutorials for setting up your own PKI (1__, 2__, 3__, 4__).

   __ https://www.crypto101.io/
   __ https://www.seancassidy.me/so-you-want-to-crypto.html
   __ http://datacenteroverlords.com/2012/03/01/creating-your-own-ssl-certificate-authority/
   __ http://blog.gosquadron.com/use-tls
   __ https://blog.cloudflare.com/how-to-build-your-own-public-key-infrastructure/
   __ http://www.area536.com/projects/be-your-own-certificate-authority-with-openssl/


Security architecture
---------------------

This guide assumes that your system is self-contained and you control all parts
of it.  This allows you to use TLS 1.2 with a modern cipher and to setup
a public key infrastructure (PKI) with a self-signed root CA.  All machines
that you deploy your system on only thrust that CA (and ignore the CAs bundled
with your OS or web browser).

Ideally, the root CA should be created on separate, non-production machine.
Depending on your security requirements, that machine should not even be
connected to the network.

You create a certificate signing request (CSR) on each production machine.  You
copy the CSR to your root CA which signs it.  You then copy the signed
certificate back to the production machine.  Ideally, you should use an SD card
for this (they are more secure than USB flash drives), but again, this depends
on your security requirements and using SSH might also work for you.


The root CA
-----------

First, you create the root CA's private key.  It should at least be 2048, or
better, 4096 bits long.  It should also be encrypted with a strong passphrase:

.. code-block:: bash

   $ openssl genrsa -aes256 -out ca.key 4096

The key should never leave the machine, except if you store it somewhere save
(e.g., on an SD card).

Now you sign the key and create the root certificate.  You use it together with
the private key for signing CSRs for other machines:

.. code-block:: bash

   $ openssl req -new -x509 -nodes -key ca.key -out ca.pem -days 1000

The command above requires some input from you.  The *Common Name* (e.g., the
FQDN) that you associate with the certificate must be different from the ones
that you use for your production machine's CSRs.  The certificate should be
valid for a longer period of time than the CSRs that it signs.


Certificates for production machines
------------------------------------

You need to create one private key and CSR on each of your production machines:

.. code-block:: bash

   $ openssl genrsa -out device.key 4096
   $ openssl req -new -key device.key -out device.csr

This time, the private key is not encrypted.  Otherwise, you'd have to
hard-code the password into your source code (which would make the encryption
futile) or enter it each time you start your program (which is unfeasible for
a distributed multi-agent system).  The private key should still not leave the
machine; so don't even think of putting it into version control or reusing it
on another machine.

The CSR creation requires similar input as the CA certificate that you created
above.  As *Common Name* or *FQDN* you should enter the address on which the
machines server socket will be listening.

Copy :file:`device.csr` to the root CA machine and sign it there:

.. code-block:: bash

   $ openssl x509 -CA ca.pem -CAkey ca.key -CAcreateserial -req -in device.csr -out device.pem -days 365

The certificate will be valid for one year.  You can change this if you want.

Transfer the certificate :file:`device.pem` as well as copy of the CA
certificate :file:`ca.pem` back to the originating machine.

The :file:`device.pem` will be used to authenticate that machine against other
machines.  :file:`ca.pem` will be used to verify other machine's certificates
when they try to authenticate themselves.


Enabling TLS for channels and RPC connections
---------------------------------------------

In pure *asyncio* programs, you enable SSL/TLS by passing an
:class:`ssl.SSLContext` instance to
:meth:`~asyncio.BaseEventLoop.create_connection()` and
:meth:`~asyncio.BaseEventLoop.create_server()`.

:meth:`aiomas.channel.open_connection()` and
:meth:`aiomas.channel.start_server()` (and similarly in the :mod:`aiomas.rpc`
module) are just wrappers for the corresponding asyncio methods and will
forward an :class:`~ssl.SSLContext` to them if one is provided.

Here is a minimal, commented example that demonstrate how to create proper
SSL contexts:

.. code-block:: python

   >>> import asyncio
   >>> import ssl
   >>>
   >>> import aiomas
   >>>
   >>>
   >>> async def client(addr, ssl):
   ...     """Connect to *addr* and use the *ssl* context to enable TLS.
   ...     Send "ohai" to the server, print its reply and terminate."""
   ...     channel = await aiomas.channel.open_connection(addr, ssl=ssl)
   ...     reply = await channel.send('ohai')
   ...     print(reply)
   ...     await channel.close()
   >>>
   >>>
   >>> async def handle_client(channel):
   ...     """Handle client requests by printing them.  Send a reply and
   ...     terminate."""
   ...     request = await channel.recv()
   ...     print(request.content)
   ...     await request.reply('cya')
   ...     await channel.close()
   >>>
   >>>
   >>> addr = ('127.0.0.1', 5555)
   >>>
   >>> # Create an SSLContext for the server supporting (only) TLS 1.2 with
   >>> # Eliptic Curve Diffie-Hellman and AES in Galois/Counter Mode
   >>> server_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
   >>> server_ctx.set_ciphers('ECDH+AESGCM')
   >>> # Load the cert and key for authentication against clients
   >>> server_ctx.load_cert_chain(certfile='device.pem', keyfile='device.key')
   >>> # The client also needs to authenticate itself with a cert signed by ca.pem
   >>> server_ctx.verify_mode = ssl.CERT_REQUIRED
   >>> server_ctx.load_verify_locations(cafile='ca.pem')
   >>> # Only use ECDH keys once per SSL session
   >>> server_ctx.options |= ssl.OP_SINGLE_ECDH_USE
   >>> # Disable TLS compression
   >>> server_ctx.options |= ssl.OP_NO_COMPRESSION
   >>>
   >>> # Start the server.
   >>> # It will use "server_ctx" to enable TLS for each connection.
   >>> server = aiomas.run(aiomas.channel.start_server(addr, handle_client,
   ...                                                 ssl=server_ctx))
   >>>
   >>> # Create an SSLContext for the client supporting (only) TLS 1.2 with
   >>> # Eliptic Curve Diffie-Hellman and AES in Galois/Counter Mode
   >>> client_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
   >>> client_ctx.set_ciphers('ECDH+AESGCM')
   >>> # The server needs to authenticate itself with a cert signed by ca.pem.
   >>> # And we also want ot verify its hostname.
   >>> client_ctx.verify_mode = ssl.CERT_REQUIRED
   >>> client_ctx.load_verify_locations(cafile='ca.pem')
   >>> client_ctx.check_hostname = True
   >>> # Load the cert and key for authentication against the server
   >>> client_ctx.load_cert_chain(certfile='device.pem', keyfile='device.key')
   >>>
   >>> # Run the client.  It will use "client_ctx" to enable TLS.
   >>> aiomas.run(client(addr, client_ctx))
   ohai
   cya
   >>>
   >>> # Shutdown the server
   >>> server.close()
   >>> aiomas.run(server.wait_closed())

As you can see, the SSL contexts used by servers and clients are slightly
different.  Clients should verify that the hostname they connected to is the
same as in the server's certificate.  Servers on the other hand can set a few
more options for a TLS connection.

:mod:`aiomas` offers two functions that create secure SSL contexts with the
same settings as in the example above
– :func:`~aiomas.util.make_ssl_server_context()` and
:func:`~aiomas.util.make_ssl_client_context()`:

.. code-block:: python

   >>> server_ctx = aiomas.make_ssl_server_context('ca.pem', 'device.pem', 'device.key')
   >>> server = aiomas.run(aiomas.channel.start_server(
   ...     addr, handle_client, ssl=server_ctx))
   >>>
   >>> client_ctx = aiomas.make_ssl_client_context('ca.pem', 'device.pem', 'device.key')
   >>> aiomas.run(client(addr, client_ctx))
   ohai
   cya
   >>> server.close()
   >>> aiomas.run(server.wait_closed())


TLS configuration for agent containers
--------------------------------------

An agent :class:`~aiomas.agent.Container` has its own server socket and creates
a number of client sockets when it connects to other containers.

You can easily enable TLS for both socket types by passing an
:class:`~aiomas.agent.SSLCerts` instance to the container.  This is a named
tuple with the filenames of the root CA certificate, the certificate for
authenticating the container as well as the corresponding private key:

.. code-block:: python

   >>> import aiomas
   >>>
   >>> sslcerts = aiomas.SSLCerts('ca.pem', 'device.pem', 'device.key')
   >>> c = aiomas.Container.create(('127.0.0.1', 5555), ssl=sslcerts)
   >>>
   >>> # Start agents and run your system
   >>> # ...
   >>>
   >>> c.shutdown()

The container will use the :func:`~aiomas.util.make_ssl_server_context()` and
:func:`~aiomas.util.make_ssl_client_context()` functions to create the
necessary SSL contexts.

If you need more flexibility, you can alternatively pass a tuple with two SSL
contexts (one for the server and one for client sockets) to the container:

.. code-block:: python

   >>> import aiomas
   >>>
   >>> server_ctx = aiomas.make_ssl_server_context('ca.pem', 'device.pem', 'device.key')
   >>> client_ctx = aiomas.make_ssl_client_context('ca.pem', 'device.pem', 'device.key')
   >>> c = aiomas.Container.create(('127.0.0.1', 5555), ssl=(server_ctx, client_ctx))
   >>>
   >>> # Start agents and run your system
   >>> # ...
   >>>
   >>> c.shutdown()
