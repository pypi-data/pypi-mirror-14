============================================================
cffi_utils: Utilities to write python wrappers around C code
============================================================

cffi_utils.sowrapper:
---------------------

.. code-block:: text
    get_lib_ffi_resource(module_name, libpath, c_hdr)
        module_name-->str: module name to retrieve resource
        libpath-->str: shared library filename with optional path
        c_hdr-->str: C-style header definitions for functions to wrap
        Returns-->(ffi, lib)
        
        The 'clobbered' paths are tried FIRST, falling back to trying the
            unchanged libpath
        For generating the 'clobbered' filenames,libpath has to end in '.so'
        
        Use this method when you are loading a package-specific shared library
        If you want to load a system-wide shared library, use get_lib_ffi_shared
        instead
    
    get_lib_ffi_shared(libpath, c_hdr)
        libpath-->str: shared library filename with optional path
        c_hdr-->str: C-style header definitions for functions to wrap
        Returns-->(ffi, lib)



cffi_utils.ffi:
---------------

.. code-block:: text
    class FFIExt(cffi.api.FFI)
        get_buffer(self, *args)
            all args-->_cffi_backend.CDataOwn
            Must be a pointer or an array
            Returns-->buffer (if a SINGLE argument was provided)
                  LIST of buffer (if a args was a tuple or list)

        get_bytes(self, *args)
            all args-->_cffi_backend.CDataOwn
            Must be a pointer or an array
            Returns-->bytes (if a SINGLE argument was provided)
                  LIST of bytes (if a args was a tuple or list)

        get_cdata(self, *args)
            all args-->_cffi_backend.buffer
            Returns-->cdata (if a SINGLE argument was provided)
                  LIST of cdata (if a args was a tuple or list)



cffi_utils.utils2to3:
---------------------

.. code-block:: text
    toBytes(s)
        s-->str / bytes
        Returns-->bytes (Py2/3 compatible)

    fromBytes(b)
        b-->bytes / str
        Returns-->str (Py2/3 compatible)

    chr(x)
        Returns-->str (Py2/3 compatible)
    ord(x)
        Returns-->int (Py2/3 compatible)

    decode(s, encoding='latin-1')
    encode(s, encoding='latin-1')
    
    
    Function decorators - converts all inputs / outputs
        inputFromBytes(func, *args, **kwargs)
        inputToBytes(func, *args, **kwargs)
        outputFromBytes(func, *args, **kwargs)
        outputToBytes(func, *args, **kwargs)
    

LICENSE:
--------
Licensed under the GPL version 3 or later. See LICENSE-GPL-v3.txt


**EXAMPLES:**

See the following projects for examples where I have used this:



**INSTALLATION:**

Using pip from pypi:
    pip install cffi_utils

Using pip from git:
    pip install 'git+https://github.com/sundarnagarajan/py_poly1305-donna.git'

Using setup.py:
    python setup.py install

**BUILD / INSTALL REQUIREMENTS:**

*GNU/Linux:*
- Python
  Tested on 2.7.6, 3.4.3, pypy 2.7.10 (pypy 4.0.1)
- cffi >= 1.0.0
- six
