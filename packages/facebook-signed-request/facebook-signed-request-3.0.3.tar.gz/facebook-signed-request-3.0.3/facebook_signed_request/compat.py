import hashlib as _hashlib
import sys

IS_PYTHON2 = sys.version_info.major == 2

if IS_PYTHON2:
    str_class = basestring
else:
    str_class = str


if IS_PYTHON2:
    class HashLibWrapper(object):
        algorithms_available = _hashlib.algorithms

        def __getattr__(self, attr):
            return getattr(_hashlib, attr)

    hashlib = HashLibWrapper()
else:
    hashlib = _hashlib
