'''
    Python wrapper around fastpbkdf2
    See pydoc multikdf for LICENSE terms

    Note that only the following methods from the scrypt library are wrapped
        fastpbkdf2_hmac_sha1
        fastpbkdf2_hmac_sha256
        fastpbkdf2_hmac_sha512

    The following methods should be exactly equivalent to the corresponding
    methods in the existing python wrappers:
        ---------------------------------------------------------------
        Module.method                       Identical to
        ---------------------------------------------------------------
        multikdf.fastpbkdf2.pbkdf2_hmac     fastpbkdf2.pbkdf2_hmac
        ---------------------------------------------------------------
'''
from . import lib, ffi, getbuf
from cffi_utils.utils2to3 import toBytes


algorithm = dict.fromkeys(['sha1', 'sha256', 'sha512'])


def pbkdf2_hmac(h, i, s, r, kl=None):
    '''
    Should be identical to original fastpbkdf2.pbkdf2_hmac
    h-->str: hash function (name)
    i-->bytes: input data (password etc)
    s-->bytes: salt
    r-->int: rounds
    kl-->int: desired key length in bytes

    Returns-->bytes:
    '''
    buf = getbuf(kl)
    if h == 'sha1':
        lib.fastpbkdf2_hmac_sha1(i, len(i), s, len(s), r, buf, kl)
    elif h == 'sha256':
        lib.fastpbkdf2_hmac_sha256(i, len(i), s, len(s), r, buf, kl)
    elif h == 'sha512':
        lib.fastpbkdf2_hmac_sha512(i, len(i), s, len(s), r, buf, kl)
    return ffi.get_bytes(buf)


def pbkdf2(i, s, r=1000, kl=64, h='SHA512'):
    '''
    i-->bytes: input data (password etc)
    s-->bytes: salt
    r-->int: rounds
    kl-->int: desired key length in bytes
    h-->str: hash function (name)

    Returns-->bytes:
    '''
    h = h.lower()
    if h not in algorithm:
        raise ValueError('h must be one of: ' + str(algorithm.keys()))
    (i, s, h) = (toBytes(i), toBytes(s), toBytes(h))
    return pbkdf2_hmac(h, i, s, r, kl=kl)
