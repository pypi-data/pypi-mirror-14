#!/usr/bin/env python
'''
    Python wrapper around fastpbkdf2, scrypt and bcrypt

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

if __name__ == '__main__':
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
