'''
    utils2to3: Utility functions for Py2/Py3 compatibility

    Copyright (C) 2016 Sundar Nagarajan

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

    For details of the GNU General Pulic License version 3, see the
    LICENSE.txt file that accompanied this program
'''

# Import as: from utils2to3 import long, bytes, chr, ord

import six

if six.PY3:
    long = int
    xrange = range
elif six.PY2:
    long = long
    xrange = xrange


def toBytes(s):
    '''
    s-->str (or bytes)
    Returns-->bytes (works in PY2, PY3)
    '''
    if six.PY3:
        if isinstance(s, bytes):
            return s
        elif isinstance(s, str):
            return encode(s, 'latin-1')
    elif six.PY2:
        if isinstance(s, bytearray):
            return str(s)
        elif isinstance(s, list):
            return str(bytearray(s))
        elif isinstance(s, str):
            return s


def fromBytes(b):
    '''
    s-->bytes (or str)
    Returns-->str (works in PY2, PY3)
    '''
    if six.PY3:
        if isinstance(b, bytes):
            return decode(b, 'latin-1')
        elif isinstance(b, list):
            return decode(bytes(b), 'latin-1')
        elif isinstance(b, str):
            return b
    elif six.PY2:
        if isinstance(b, bytearray):
            return str(b)
        elif isinstance(b, list):
            return str(bytearray(b))
        elif isinstance(b, str):
            return b


def encode(s, encoding='latin-1'):
    '''
    s-->str
    encoding-->str: encoding to use. Recommended to use default
    Returns-->bytes: s encoded to bytes using encoding
        Works in PY2, PY3
    '''
    if six.PY3:
        import codecs
        if isinstance(s, str):
            return bytes(s, encoding)
        elif isinstance(s, bytes):
            return codecs.encode(s, encoding)
    elif six.PY2:
        if isinstance(s, str):
            return s.encode(encoding=encoding)
        elif isinstance(s, bytearray):
            return toBytes(fromBytes(s).encode(encoding=encoding))


def decode(b, encoding='latin-1'):
    '''
    b-->bytes
    encoding-->str: encoding to use. Recommended to use default
    Returns-->str: b decoded to str using encoding
        Works in PY2, PY3
    '''
    if six.PY3:
        import codecs
        return codecs.decode(b, encoding)
    elif six.PY2:
        if isinstance(b, str):
            return b.decode(encoding=encoding)
        elif isinstance(b, bytearray):
            return toBytes(fromBytes(b).decode(encoding=encoding))

_chr = chr
_ord = ord


def chr(x):
    '''
    x-->int / byte
    Returns-->byte / str of length 1
        Behaves like PY2 chr() in PY2 or PY3
    '''
    global _chr
    if isinstance(x, int):
        return toBytes(_chr(x))
    else:
        return toBytes(x)


def ord(x):
    '''
    x-->int / byte
    Returns-->int
        Behaves like PY2 ord() in PY2 or PY3
    '''
    global _ord
    if isinstance(x, int):
        return x
    else:
        return _ord(x)


def _convToBytes(s):
    if isinstance(s, str):
        return toBytes(s)
    else:
        return s


def _convFromBytes(b):
    if isinstance(b, bytes) or isinstance(b, bytearray):
        return fromBytes(b)
    else:
        return b


def _convInputs(func, f, *args, **kwargs):
    def wrapper(*args, **kwargs):
        def wrapped(*args, **kwargs):
            newargs = []
            for a in args:
                newargs += [f(a)]
            for (k, v) in kwargs.items():
                kwargs[k] = f(v)
            result = func(*newargs, **kwargs)
            return result
        return wrapped
    return wrapper()


def _convResults(func, f, *args, **kwargs):
    def wrapper(*args, **kwargs):
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, tuple) or isinstance(result, list):
                newres = []
                for r in result:
                    newres += [f(r)]
            else:
                newres = f(result)
            return newres
        return wrapped
    return wrapper()


def inputFromBytes(func, *args, **kwargs):
    '''
    Descriptor that converts all arguments to str
    '''
    return _convInputs(func, _convFromBytes, *args, **kwargs)


def inputToBytes(func, *args, **kwargs):
    '''
    Descriptor that converts all arguments to bytes
    '''
    return _convInputs(func, _convToBytes, *args, **kwargs)


def outputToBytes(func, *args, **kwargs):
    '''
    Descriptor that converts all return values to bytes
    '''
    return _convResults(func, _convToBytes, *args, **kwargs)


def outputFromBytes(func, *args, **kwargs):
    '''
    Descriptor that converts all return values to str
    '''
    return _convResults(func, _convFromBytes, *args, **kwargs)
