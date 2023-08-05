#!/usr/bin/env python
'''
    Python wrapper around bcrypt from Tarsnap
    See pydoc multikdf for LICENSE terms

    Note that only the 'bcrypt_pbkdf' method from the bcrypt library
    is wrapped
    The following methods should be exactly equivalent to the corresponding
    methods in the existing python wrappers:
        ---------------------------------------------------------------
        Module.method                       Identical to
        ---------------------------------------------------------------
        multikdf.bcrypt.kdf                 bcrypt.kdf
        ---------------------------------------------------------------
'''
from . import lib, ffi, getbuf
from cffi_utils.utils2to3 import toBytes


def kdf(password, salt, desired_key_bytes, rounds):
    '''
    Should be identical to original bcrypt.kdf
    password-->bytes: input data (password etc)
    salt-->bytes: salt
    desired_key_bytes-->int: desired key length in bytes
    rounds-->int: rounds

    Returns-->bytes:
    '''
    buf = getbuf(desired_key_bytes)
    lib.bcrypt_pbkdf(password, len(password),
                     salt, len(salt),
                     buf, desired_key_bytes, rounds)
    return ffi.get_bytes(buf)


def bcrypt_kdf(i, s, r=10, kl=64):
    '''
    i-->bytes: input data (password etc)
    s-->bytes: salt (os.urandom)
    r-->int: rounds
    kl-->int: desired key length in bytes
    Returns-->bytes:

    (rounds * PerSec) = Machine-specific constant
    '''
    (i, s) = (toBytes(i), toBytes(s))
    return kdf(i, s, kl, r)
