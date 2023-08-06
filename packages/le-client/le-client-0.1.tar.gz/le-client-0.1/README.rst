=========
le_client
=========

This is yet another ACME/Let's Encrypt client.
It's inspired by acme-tiny, but does things differently.

.. image:: https://travis-ci.org/drdaeman/le_client.svg?branch=master
    :target: https://travis-ci.org/drdaeman/le_client


Requirements
------------

- The client is written in Python 3.
  It's incompatible with Python 2.x at the moment.

- There are no dependencies on any third-party
  Python modules. The code should run fine on
  a bare Python setup, without anything from PyPI.

- You need ``openssl`` command-line executable available
  for use in ``PATH``. It's used for keys and certificate
  request parsing.


Features and limitations
------------------------

- Does not know anything about servers or software.
  Its only purpose is to obtain a signed certificate.

- Currently, the only supported challenge type is
  ``http-01`` (webroot).

- Does not require any fancy privileges.

  It needs to access the certificate request, have write
  access to ``/.well-known/acme-challenge/`` and can output
  the obtained certificate to a file or on stdout.

- It works with either local account key file,
  or can use a special remote service that can sign
  requests.

  That was the primary reason why I wrote my own client:
  I didn't want to keep an account's private key
  on the untrusted machine.

- Currently, it only supports EC-256 account keys.
  It's easy to add other curve sizes and RSA support,
  but I'm lazy.

- It's meant to be either usable as a standalone
  command-line utility, or as a simple Python library.


Remote account key protocol
---------------------------

This client supports a special mode of operation where
it doesn't have a local account private key, but asks
a remote service to sign whatever payload it needs.

A remote service is located at a single URL, served
over HTTPS. To authenticate the client, CLI currently
supports only HTTP Basic Authentication.

To sign, we send POST request to a given URL,
appending ``nonce`` query parameter, and sending
the payload as the POST body. We expect the server
to answer with 200 OK an return a JWS as a response.

That's the whole protocol description.


License
-------

Copyright (c) 2016, Aleksey Zhukov

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

See ``LICENSE`` file for more information.
