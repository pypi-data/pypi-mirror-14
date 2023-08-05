from ctypes import *
import ctypes.util
import os

#_LZMATPATH = ctypes.util.find_library('lzmat')
_LZMATPATH = os.path.join(os.path.dirname(__file__), 'lzmat.so')
lib = cdll.LoadLibrary(_LZMATPATH)


def encode(data):
    size = len(data)
    outlen = (size)+((size+7) >> 3)+0x21
    out = create_string_buffer(outlen+sizeof(c_int()))
    outlen = c_int(outlen)
    ret = lib.lzmat_encode(byref(out), byref(outlen), data, len(data))
    if ret == 0:
        return out[:outlen.value]
    else:
        raise Exception('Return error: %d' % ret)


def decode(data, size):
    if size:
        outlen = size
    else:
        outlen = len(data)*10000
    out = create_string_buffer(outlen)
    outlen = c_int(outlen)
    ret = lib.lzmat_decode(byref(out), byref(outlen), str(data), len(data))
    if ret == 0:
        return out[:outlen.value]
    else:
        raise Exception('Return error: %d' % ret)


if __name__ == '__main__':
    print "testing with string Lorem Ipsum"
    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"
    print "Plain:", lorem
    print "Plain length:", len(lorem)
    enc = encode(lorem)
    print "Encoded:", str(enc).encode('hex')
    print "Encoded len", len(enc)
    dec = decode(bytearray(enc))
    print "Decoded:", dec
    print "Ddecoded len", len(dec)
    print "Success:", (lorem == dec)
