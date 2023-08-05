#!/usr/bin/env python
'''
    Python wrapper around fastpbkdf2, scrypt and bcrypt
    Note that only the following specific C functions are wrapped:
        From fastpbkdf2:
            fastpbkdf2_hmac_sha1
            fastpbkdf2_hmac_sha256
            fastpbkdf2_hmac_sha512
        From bcrypt:
            bcrypt_kdf
        From scrypt:
            crypto_scrypt

    The following methods should be exactly equivalent to the corresponding
    methods in the existing python wrappers:

        ---------------------------------------------------------------
        Module.method                       Identical to
        ---------------------------------------------------------------
        multikdf.fastpbkdf2.pbkdf2_hmac     fastpbkdf2.pbkdf2_hmac
        multikdf.bcrypt.kdf                 bcrypt.kdf
        multikdf.scrypt.hash                scrypt.hash
        ---------------------------------------------------------------

    The files under multikdf/c/fastpbkdf2 are from ctz and are copied
    unchanged from https://github.com/ctz/fastpbkdf2.git
    These files under the terms of the CC0 1.0 Universal License - see
    the file named LICENSE under multikdf/c/fastpbkdf2

    The files under multikdf/c/py-bcrypt are from py-bcrypt (automatically
    exported from code.google.com/p/py-bcrypt) and imported unchanged.
    These files under the terms of the ISC/BSD licence. See the file named
    LICENSE under multikdf/c/py-bcrypt

    The files under multikdf/c/scrypt are from Tarsnap and are copied
    unchanged from https://github.com/Tarsnap/scrypt.git
    The files under multikdf/c/scrypt/lib are licensed under the terms of
    the 2-clause BSD license. See the file named README.md under the directory
    multikdf/c/scrypt/lib.
    The files under multikdf/c/scrypt/libcperciva are licensed under the
    terms of the license specified in the file
    multikdf/c/scrypt/libcperciva/COPYRIGHT.

    All remaining files in this package are licensed under the GNU
    General Public License version 3 or (at your option) any later version.

    See the file LICENSE-GPLv3.txt for details of the GNU General Public
    License version 3.

    Copyright (C) 2016  Sundar Nagarajan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from cffi_utils.sowrapper import get_lib_ffi_resource


c_hdr = '''
// fastpbkdf2
void fastpbkdf2_hmac_sha1(const uint8_t *passwd, size_t passwdlen,
                          const uint8_t *salt, size_t saltlen,
                          uint32_t rounds,
                          uint8_t *key, size_t keylen);
void fastpbkdf2_hmac_sha256(const uint8_t *passwd, size_t passwdlen,
                            const uint8_t *salt, size_t saltlen,
                            uint32_t rounds,
                            uint8_t *key, size_t keylen);
void fastpbkdf2_hmac_sha512(const uint8_t *passwd, size_t passwdlen,
                            const uint8_t *salt, size_t saltlen,
                            uint32_t rounds,
                            uint8_t *key, size_t keylen);

// bcrypt
int bcrypt_pbkdf(const uint8_t *pass, size_t passlen,
                 const uint8_t *salt, size_t saltlen,
                 uint8_t *key, size_t keylen,
                 unsigned int rounds
                 );

// scrypt
int crypto_scrypt(const uint8_t *passwd, size_t passwdlen,
                  const uint8_t *salt, size_t saltlen,
                  uint64_t n,
                  uint32_t r,
                  uint32_t p,
                  uint8_t *key, size_t keylen
                  );
'''

module_name = 'multikdf'
libpath = 'libmultikdf.so'
(ffi, lib) = get_lib_ffi_resource(
    module_name=module_name, libpath=libpath, c_hdr=c_hdr)


def getbuf(l):
    cdecl = 'uint8_t [%d]' % (l,)
    return ffi.new(cdecl)
