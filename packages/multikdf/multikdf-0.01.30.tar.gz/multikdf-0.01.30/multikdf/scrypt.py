#!/usr/bin/env python
'''
    Python wrapper around scrypt
    See pydoc multikdf for LICENSE terms

    Note that only the 'crypto_scrypt' method from the scrypt library
    is wrapped
    The following methods should be exactly equivalent to the corresponding
    methods in the existing python wrappers:
        ---------------------------------------------------------------
        Module.method                       Identical to
        ---------------------------------------------------------------
        multikdf.scrypt.hash                 scrypt.hash
        ---------------------------------------------------------------
'''
from . import lib, ffi, getbuf
from cffi_utils.utils2to3 import toBytes


def hash(i, s, N=16384, r=8, p=1, buflen=64):
    '''
    Should be identical to scrypt.hash
    i-->bytes: input data (password etc)
    s-->bytes: salt
    N-->int: General work factor. Should be a power of 2
             if N < 2, it is set to 2. Defaults to 16384
    r-->int: Memory cost - defaults to 8
    p-->int: Compuation (parallelization) cost - defaults to 1
    buflen-->int: Desired key length in bytes
    Returns-->bytes:
    '''
    buf = getbuf(buflen)
    lib.crypto_scrypt(i, len(i), s, len(s), N, r, p, buf, buflen)
    return ffi.get_bytes(buf)


def scrypt_kdf(i, s, r=8, p=1, n=14, kl=64):
    '''
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
    '''
    (i, s) = (toBytes(i), toBytes(s))
    return hash(i=i, s=s, N=(2**n), r=r, p=p, buflen=kl)
