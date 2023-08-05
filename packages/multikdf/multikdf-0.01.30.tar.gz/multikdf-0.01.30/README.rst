pymultikdf
==========

| This python module provides wrappers for C functions implementing the
| following Key Derivation Functions (KDF)s:

-  PBKDF2
-  bcrypt
-  scrypt

What is a Key Derivation Function?
----------------------------------

From wikipedia (https://en.wikipedia.org/wiki/Key_derivation_function):

In cryptography, a key derivation function (or KDF) derives one or more
secret keys from a secret value such as a master key, a password, or a
passphrase using a pseudo-random function.[1][2] KDFs can be used to
stretch keys into longer keys or to obtain keys of a required format,
such as converting a group element that is the result of a
Diffie–Hellman key exchange into a symmetric key for use with AES. Keyed
cryptographic hash functions are popular examples of pseudo-random
functions used for key derivation.

What is PBKDF2?
~~~~~~~~~~~~~~~

PBKDF2 (Password-Based Key Derivation Function 2) is a key derivation
function that is part of RSA Laboratories' Public-Key Cryptography
Standards (PKCS) series, specifically PKCS #5 v2.0, also published as
Internet Engineering Task Force's RFC 2898. It replaces an earlier
standard, PBKDF1, which could only produce derived keys up to 160 bits
long.

See: https://en.wikipedia.org/wiki/PBKDF2

What is bcrypt?
~~~~~~~~~~~~~~~

bcrypt is a key derivation function for passwords designed by Niels
Provos and David Mazières, based on the Blowfish cipher, and presented
at USENIX in 1999.[1] Besides incorporating a salt to protect against
rainbow table attacks, bcrypt is an adaptive function: over time, the
iteration count can be increased to make it slower, so it remains
resistant to brute-force search attacks even with increasing computation
power.

The bcrypt function is the default password hash algorithm for BSD and
other systems including some Linux distributions such as SUSE Linux.[2]
The prefix "$2a$" or "$2b$" (or "$2y$") in a hash string in a shadow
password file indicates that hash string is a bcrypt hash in modular
crypt format.[3] The rest of the hash string includes the cost
parameter, a 128-bit salt (base-64 encoded as 22 characters), and 184
bits of the resulting hash value (base-64 encoded as 31 characters).[4]
The cost parameter specifies a key expansion iteration count as a power
of two, which is an input to the crypt algorithm.

See: https://en.wikipedia.org/wiki/Bcrypt

What is scrypt?
~~~~~~~~~~~~~~~

In cryptography, scrypt is a password-based key derivation function
created by Colin Percival, originally for the Tarsnap online backup
service.[1] The algorithm was specifically designed to make it costly to
perform large-scale custom hardware attacks by requiring large amounts
of memory. In 2012, the scrypt algorithm was published by IETF as an
Internet Draft, intended to become an informational RFC.[2]

See: https://en.wikipedia.org/wiki/Scrypt

Relationship to existing packages
=================================

Existing python packages for PBKDF2, bcrypt, scrypt

-  pip install fastpbkdf2
-  pip install bcrypt
-  pip install scrypt

Why a new module?
-----------------

Sometimes one wants to try or use MULTIPLE different Key Derivation
Functions. In such cases, instead of installing MULTIPLE SEPARATE
python, packages, just this single module can be installed and used.

This may also be a convenience when porting your code to run under
'Python For Android (https://github.com/kivy/python-for-android)

Are there any differences?
--------------------------

Exactly and ONLY the following C functions have been wrapped

From fastpbkdf2:

::

    fastpbkdf2_hmac_sha1
    fastpbkdf2_hmac_sha256
    fastpbkdf2_hmac_sha512

From bcrypt:

::

    bcrypt_kdf

From scrypt:

::

    crypto_scrypt

The following methods should be exactly equivalent to the corresponding
methods in the existing python wrappers:

::

        ---------------------------------------------------------------
        Module.method                       Identical to
        ---------------------------------------------------------------
        multikdf.fastpbkdf2.pbkdf2_hmac     fastpbkdf2.pbkdf2_hmac
        multikdf.bcrypt.kdf                 bcrypt.kdf
        multikdf.scrypt.hash                scrypt.hash
        ---------------------------------------------------------------

Test code
=========

See multikdf.test (test.py under the multikdf module directory)

.. code:: python

        import os
        from .fastpbkdf2 import pbkdf2, algorithm as hash_algorithms
        from .bcrypt import bcrypt_kdf
        from .scrypt import scrypt_kdf

        min_passwd_len = 8
        max_passwd_len = 10

        min_pbkdf_rounds = 1000
        max_pbkdf_rounds = 5000
        step_pbkdf_rounds = 200

        min_bcrypt_rounds = 2
        max_bcrypt_rounds = 8

        min_scrypt_r = 7
        max_scrypt_r = 8
        min_scrypt_p = 1
        max_scrypt_p = 2
        min_scrypt_n = 13
        max_scrypt_n = 14

        def test_pbkdf2(s):
            for l in range(min_passwd_len, max_passwd_len + 1):
                i = os.urandom(l)
                for r in range(min_pbkdf_rounds,
                               max_pbkdf_rounds + 1,
                               step_pbkdf_rounds):
                    for h in hash_algorithms.keys():
                        print('Testing pbkdf2: l=%d, r=%d, h=%s' % (l, r, h))
                        pbkdf2(i, s, r=r, kl=kl, h=h)

        def test_bcrypt(s):
            for l in range(min_passwd_len, max_passwd_len + 1):
                i = os.urandom(l)
                for r in range(min_bcrypt_rounds, max_bcrypt_rounds + 1):
                    print('Testing bcrypt: l=%d, r=%d' % (l, r))
                    bcrypt_kdf(i, s, r=r, kl=kl)

        def test_scrypt(s):
            for l in range(min_passwd_len, max_passwd_len + 1):
                i = os.urandom(l)
                for r in range(min_scrypt_r, max_scrypt_r + 1):
                    for p in range(min_scrypt_p, max_scrypt_p + 1):
                        for n in range(min_scrypt_n, max_scrypt_n + 1):
                            print('Testing scrypt: l=%d, r=%d, p=%d, n=%d' % (
                                l, r, p, n))
                            scrypt_kdf(i, s, r=r, p=p, n=n, kl=kl)

        s = os.urandom(64)
        kl = 64

        test_pbkdf2(s)
        test_bcrypt(s)
        test_scrypt(s)

INSTALLING:
===========

From github directly using pip:

::

    pip install 'git+https://github.com/sundarnagarajan/pymultikdf.git'

From github after downloading / cloning:

::

    python setup.py install

From pypi:

::

    pip install multikdf

LICENSE
=======

The files under multikdf/c/fastpbkdf2 are from ctz and are copied
unchanged from https://github.com/ctz/fastpbkdf2.git These files under
the terms of the CC0 1.0 Universal License - see the file named LICENSE
under multikdf/c/fastpbkdf2

The files under multikdf/c/py-bcrypt are from py-bcrypt (automatically
exported from code.google.com/p/py-bcrypt) and imported unchanged. These
files under the terms of the ISC/BSD licence. See the file named LICENSE
under multikdf/c/py-bcrypt

The files under multikdf/c/scrypt are from Tarsnap and are copied
unchanged from https://github.com/Tarsnap/scrypt.git The files under
multikdf/c/scrypt/lib are licensed under the terms of the 2-clause BSD
license. See the file named README.md under the directory
multikdf/c/scrypt/lib.

The files under multikdf/c/scrypt/libcperciva are licensed under the
terms of the license specified in the file
multikdf/c/scrypt/libcperciva/COPYRIGHT.

All remaining files in this package are licensed under the GNU General
Public License version 3 or (at your option) any later version. See the
file LICENSE-GPLv3.txt for details of the GNU General Public License
version 3.

Documentation (pydoc)
=====================

Package multikdf
----------------

PACKAGE CONTENTS
~~~~~~~~~~~~~~~~

::

    bcrypt
    fastpbkdf2
    libmultikdf
    scrypt
    test

FUNCTIONS
~~~~~~~~~

::

    getbuf(l)

multikdf.fastpbkdf2
-------------------

FUNCTIONS
~~~~~~~~~

::

    pbkdf2(i, s, r=1000, kl=64, h='SHA512')
        i-->bytes: input data (password etc)
        s-->bytes: salt
        r-->int: rounds
        kl-->int: desired key length in bytes
        h-->str: hash function (name)
        
        Returns-->bytes:

    pbkdf2_hmac(h, i, s, r, kl=None)
        Should be identical to original fastpbkdf2.pbkdf2_hmac
        h-->str: hash function (name)
        i-->bytes: input data (password etc)
        s-->bytes: salt
        r-->int: rounds
        kl-->int: desired key length in bytes
        
        Returns-->bytes:

DATA
~~~~

::

    algorithm = {'sha1': None, 'sha256': None, 'sha512': None}

multikdf.bcrypt
---------------

FUNCTIONS
~~~~~~~~~

::

    bcrypt_kdf(i, s, r=10, kl=64)
        i-->bytes: input data (password etc)
        s-->bytes: salt (os.urandom)
        r-->int: rounds
        kl-->int: desired key length in bytes
        Returns-->bytes:
        
        (rounds * PerSec) = Machine-specific constant

    kdf(password, salt, desired_key_bytes, rounds)
        Should be identical to original bcrypt.kdf
        password-->bytes: input data (password etc)
        salt-->bytes: salt
        desired_key_bytes-->int: desired key length in bytes
        rounds-->int: rounds
        
        Returns-->bytes:

multikdf.scrypt
---------------

FUNCTIONS
~~~~~~~~~

::

    hash(i, s, N=16384, r=8, p=1, buflen=64)
        Should be identical to scrypt.hash
        i-->bytes: input data (password etc)
        s-->bytes: salt
        N-->int: General work factor. Should be a power of 2
                 if N < 2, it is set to 2. Defaults to 16384
        r-->int: Memory cost - defaults to 8
        p-->int: Compuation (parallelization) cost - defaults to 1
        buflen-->int: Desired key length in bytes
        Returns-->bytes:

    scrypt_kdf(i, s, r=8, p=1, n=14, kl=64)
        i-->bytes: input data (password etc)
        s-->bytes: salt (os.urandom)
        r-->int: Memory cost - defaults to 8
        p-->int: Compuation (parallelization) cost - defaults to 1
        n-->int: General work factor. passed to scrypt as 2^n
                 if n < 1, it is set to 1. Defaults to 14 (scrypt n=16384)
        Returns-->bytes:
        
        (r * p) should be < 2^30
        see pydoc scrypt.hash
        
        (2^n) * r * p * PerSec = Machine-specific constant

