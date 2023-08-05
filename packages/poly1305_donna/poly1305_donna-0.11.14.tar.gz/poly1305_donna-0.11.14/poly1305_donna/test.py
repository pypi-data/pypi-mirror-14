from . import get_key, authenticate, verify, self_test


if __name__ == '__main__':
    print('Power-On Self Test result: ' + str(self_test()))
    msg = 'Hello world'
    print('\nTest class methods - authenticate, verify')
    kr = get_key()
    auth = authenticate(kr, msg)

    bad_kr = get_key()
    bad_msg = msg + '1'
    bad_auth = authenticate(kr, bad_msg)

    print('Good: %s\nBad auth: %s\nBad kr: %s\nBad msg: %s' % (
        str(verify(auth, kr, msg)),
        str(verify(bad_auth, kr, msg)),
        str(verify(auth, bad_kr, msg)),
        str(verify(auth, kr, bad_msg))
    ))
