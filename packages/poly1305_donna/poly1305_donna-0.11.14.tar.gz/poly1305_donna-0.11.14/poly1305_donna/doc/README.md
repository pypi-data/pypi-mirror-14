# py_poly1305_donna
Fork of poly1305-donna by floodberry (<https://github.com/floodyberry/poly1305-donna>) adding a Python wrapper as an extension module

## What is a HMAC (Hash-based Message Authentication Code)?
From wikipedia (<https://en.wikipedia.org/wiki/Hash-based_message_authentication_code>):

In cryptography, a keyed-hash message authentication code (HMAC) is a specific construction for calculating a message authentication code (MAC) involving a cryptographic hash function in combination with a secret cryptographic key. As with any MAC, it may be used to simultaneously verify both the data integrity and the authentication of a message. Any cryptographic hash function, such as MD5 or SHA-1, may be used in the calculation of an HMAC; the resulting MAC algorithm is termed HMAC-MD5 or HMAC-SHA1 accordingly. The cryptographic strength of the HMAC depends upon the cryptographic strength of the underlying hash function, the size of its hash output, and on the size and quality of the key.

## What is poly1305?
From <http://cr.yp.to/mac.html>:

Poly1305-AES is a state-of-the-art secret-key message-authentication code suitable for a wide variety of applications. Poly1305-AES computes a 16-byte authenticator of a message of any length, using a 16-byte nonce (unique message number) and a 32-byte secret key. Attackers can't modify or forge messages if the message sender transmits an authenticator along with each message and the message receiver checks each authenticator.

# LICENSE:
Following floodberry's code license, this code is also released into the public domain. See LICENSE file.

The 'floodberry.poly1305_donna' directory contains the unmodified source code forked from poly1305-donna from <https://github.com/floodyberry/poly1305-donna>

# EXAMPLES
~~~~ {.sourceCode .python}
from poly1305_donna import (
    self_test, get_key, authenticate, verify,
)
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
~~~~

Alternately, run the test script that is shipped:

~~~~ {.sourceCode .python}
python -m poly1305_donna.test
~~~~

To run a simple benchmark:

~~~~ {.sourceCode .python}
python -m poly1305_donna.benchmark
~~~~

# INSTALLATION
Using pip:

    pip install 'git+https://github.com/sundarnagarajan/py_poly1305-donna.git'

Using setup.py: 

    python setup.py install

# BUILD / INSTALL REQUIREMENTS
*GNU/Linux:* 
- Python Tested on 2.7.6, 3.4.3, pypy 2.7.10 (pypy 4.0.1) 
- cffi >= 1.0.0 
- six 
- Python.h (libpython-dev on Debian-like systems) 
- gcc (build-essential on Debian-like systems)

# NOTES
py_poly1305_donna does not offer an API for incremental update and HMAC calculation.
