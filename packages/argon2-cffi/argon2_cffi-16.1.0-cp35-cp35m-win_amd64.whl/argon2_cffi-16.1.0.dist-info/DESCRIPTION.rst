=====================================
CFFI-based Argon2 Bindings for Python
=====================================

.. image:: https://readthedocs.org/projects/argon2-cffi/badge/?version=stable
  :target: http://argon2-cffi.readthedocs.org/en/latest/?badge=stable
  :alt: Documentation Status

.. image:: https://travis-ci.org/hynek/argon2_cffi.svg?branch=master
  :target: https://travis-ci.org/hynek/argon2_cffi

.. image:: https://codecov.io/github/hynek/argon2_cffi/coverage.svg?branch=master
  :target: https://codecov.io/github/hynek/argon2_cffi

.. image:: https://ci.appveyor.com/api/projects/status/3faufu7qgwc8nv2v/branch/master?svg=true
  :target: https://ci.appveyor.com/project/hynek/argon2-cffi

.. image:: https://www.irccloud.com/invite-svg?channel=%23cryptography-dev&amp;hostname=irc.freenode.net&amp;port=6697&amp;ssl=1
  :target: https://www.irccloud.com/invite?channel=%23cryptography-dev&amp;hostname=irc.freenode.net&amp;port=6697&amp;ssl=1

.. teaser-begin

`Argon2 <https://github.com/p-h-c/phc-winner-argon2>`_ won the `Password Hashing Competition <https://password-hashing.net/>`_ and ``argon2_cffi`` is the simplest way to use it in Python and PyPy:

.. code-block:: pycon

  >>> from argon2 import PasswordHasher
  >>> ph = PasswordHasher()
  >>> hash = ph.hash("s3kr3tp4ssw0rd")
  >>> hash  # doctest: +SKIP
  '$argon2i$v=19$m=512,t=2,p=2$5VtWOO3cGWYQHEMaYGbsfQ$AcmqasQgW/wI6wAHAMk4aQ'
  >>> ph.verify(hash, "s3kr3tp4ssw0rd")
  True
  >>> ph.verify(hash, "t0t411ywr0ng")
  Traceback (most recent call last):
    ...
  argon2.exceptions.VerifyMismatchError: The password does not match the supplied hash


``argon2_cffi``\ ’s documentation lives at `Read the Docs <https://argon2-cffi.readthedocs.org/>`_, the code on `GitHub <https://github.com/hynek/argon2_cffi>`_.
It’s rigorously tested on Python 2.7, 3.4+, and PyPy.


Release Information
===================

16.1.0 (2016-04-19)
-------------------

Vendoring Argon2 @ UNRELEASED

Backward-incompatible changes:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Python 3.3 and 2.6 aren't supported anymore.
  They may work by chance but any support to them has been ceased.

  The last Python 2.6 release was on October 29, 2013 and isn't supported by the CPython core team anymore.
  Major Python packages like Django and Twisted dropped Python 2.6 a while ago already.

  Python 3.3 never had a significant user base and wasn't part of any distribution's LTS release.

Changes:
^^^^^^^^

- Add ``VerifyMismatchError`` that is raised if verification fails only because of a password/hash mismatch.
  It's a subclass of ``VerificationError`` therefore this change is completely backward compatible.
- Add support for `Argon2 1.3 <https://www.ietf.org/mail-archive/web/cfrg/current/msg07948.html>`_.
  Old hashes remain functional but opportunistic rehashing is strongly recommended.

`Full changelog <https://argon2-cffi.readthedocs.org/en/stable/changelog.html>`_.

Credits & License
=================

``argon2_cffi`` is maintained by Hynek Schlawack and released under the `MIT license <https://github.com/hynek/argon2_cffi/blob/master/LICENSE>`_.

The development is kindly supported by `Variomedia AG <https://www.variomedia.de/>`_.

A full list of contributors can be found in GitHub's `overview <https://github.com/hynek/argon2_cffi/graphs/contributors>`_.


Vendored Code
-------------

Argon2
^^^^^^

The original Argon2 repo can be found at https://github.com/P-H-C/phc-winner-argon2/.

Except for the components listed below, the Argon2 code in this repository is copyright (c) 2015 Daniel Dinu, Dmitry Khovratovich (main authors), Jean-Philippe Aumasson and Samuel Neves, and under CC0_ license.

The string encoding routines in src/encoding.c are copyright (c) 2015 Thomas Pornin, and under CC0_ license.

The `BLAKE2 <https://blake2.net>`_ code in ``src/blake2/`` is copyright (c) Samuel Neves, 2013-2015, and under CC0_ license.

The authors of Argon2 also were very helpful to get the library to compile on ancient versions of Visual Studio for ancient versions of Python.

The documentation also quotes frequently from the Argon2 paper_ to avoid mistakes by rephrasing.

.. _CC0: https://creativecommons.org/publicdomain/zero/1.0/
.. _paper: https://password-hashing.net/argon2-specs.pdf

msinttypes
^^^^^^^^^^

In order to be able to compile on Visual Studio 2008 and Visual Studio 2010 which are required for Python 2.7 and 3.4 respectively, we also ship two C headers with integer types.
They are from the `msinttypes project <https://code.google.com/p/msinttypes/>`_ (`auto-import on GitHub <https://github.com/chemeris/msinttypes>`_) and licensed under New BSD:

Copyright (c) 2006-2013 Alexander Chemeris

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  1. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
  3. Neither the name of the product nor the names of its contributors may
     be used to endorse or promote products derived from this software
     without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ''AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


