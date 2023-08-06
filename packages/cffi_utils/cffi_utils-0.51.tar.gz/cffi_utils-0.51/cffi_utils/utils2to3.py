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
import sys
import codecs


DEF_ENCODING = 'latin-1'
PY_VER = sys.version_info[0]
(PY2, PY3) = (PY_VER == 2, PY_VER == 3)
PYPY = (PY2 and sys.subversion[0].lower() == 'pypy')

del PY_VER
if PY3:
    xrange = range
    unicode = str
    unichr = chr
    long = int
_chr = chr
_ord = ord


def fromBytes(x, encoding=DEF_ENCODING):
    '''
    x-->unicode string | bytearray | bytes
    encoding-->str
    Returns-->unicode string, with encoding=encoding
    '''
    if isinstance(x, unicode):
        return x
    if isinstance(x, bytearray):
        x = bytes(x)
    elif isinstance(x, bytes):
        pass
    # Could raise an exception
    return codecs.decode(x, encoding)


def toBytes(x, encoding=DEF_ENCODING):
    '''
    x-->unicode string | bytearray | bytes
    encoding-->str
    Returns-->bytes

    If x is unicode, it is encoded using encoding
    '''
    if isinstance(x, bytes):
        return x
    elif isinstance(x, bytearray):
        return bytes(x)
    elif isinstance(x, unicode):
        pass
    # Could raise an exception
    return codecs.encode(x, encoding)


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
