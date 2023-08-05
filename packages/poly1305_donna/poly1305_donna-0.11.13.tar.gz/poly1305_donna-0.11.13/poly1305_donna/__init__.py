import os
from cffi_utils.utils2to3 import toBytes
from cffi_utils.sowrapper import get_lib_ffi_resource


c_hdr = '''
void poly1305_auth(unsigned char mac[16],
                   const unsigned char *m,
                   size_t bytes,
                   const unsigned char key[32]);

int poly1305_verify(const unsigned char mac1[16],
                    const unsigned char mac2[16]);

int poly1305_power_on_self_test(void);
'''
module_name = 'poly1305_donna'
libpath = 'libpoly1305donna.so'


(ffi, lib) = get_lib_ffi_resource(
    module_name=module_name, libpath=libpath, c_hdr=c_hdr)


def self_test():
    '''
    Returns-->boolean
    '''
    return (lib.poly1305_power_on_self_test() == 1)


def get_key(random_fn=None):
    '''
    random_fn-->callable: takes one int param: number of random bytes
                Preferably leave unset; os.urandom() will be used
    Returns-->bytes: Secure key
    '''
    if random_fn is None:
        random_fn = os.urandom
    kr = ffi.new('unsigned char[32]', random_fn(32))
    return ffi.get_bytes(kr)


def authenticate(kr, msg, random_fn=None):
    '''
    kr-->bytes: Secure key - returned by get_key()
    msg-->str or bytes: Message to be authenticated
    random_fn-->callable: takes one int param: number of random bytes
                Preferably leave unset; os.urandom() will be used
    Returns-->bytes: auth
    '''
    if random_fn is None:
        random_fn = os.urandom
    auth = ffi.new('unsigned char[16]')
    msg = toBytes(msg)

    lib.poly1305_auth(auth, msg, len(msg), kr)
    return ffi.get_bytes(auth)


def verify(auth, kr, msg, random_fn=None):
    '''
    auth-->bytes
    kr-->bytes: Secure key - returned by get_key()
    msg-->str or bytes: Message to be authenticated
    Returns-->boolean
    '''
    (auth, kr, msg) = (toBytes(auth), toBytes(kr), toBytes(msg))
    auth2 = authenticate(kr, msg, random_fn=random_fn)
    return (lib.poly1305_verify(auth, auth2) == 1)
