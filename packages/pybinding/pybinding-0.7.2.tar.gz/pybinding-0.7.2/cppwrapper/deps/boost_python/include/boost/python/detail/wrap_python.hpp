//  (C) Copyright David Abrahams 2000.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//
//  The author gratefully acknowleges the support of Dragon Systems, Inc., in
//  producing this work.

//  This file serves as a wrapper around <Python.h> which allows it to be
//  compiled with GCC 2.95.2 under Win32 and which disables the default MSVC
//  behavior so that a program may be compiled in debug mode without requiring a
//  special debugging build of the Python library.


//  To use the Python debugging library, #define BOOST_DEBUG_PYTHON on the
//  compiler command-line.

// Revision History:
// 05 Mar 01  Suppress warnings under Cygwin with Python 2.0 (Dave Abrahams)
// 04 Mar 01  Rolled in some changes from the Dragon fork (Dave Abrahams)
// 01 Mar 01  define PyObject_INIT() for Python 1.x (Dave Abrahams)

#ifdef _DEBUG
# ifndef BOOST_DEBUG_PYTHON
#  ifdef _MSC_VER  
    // VC8.0 will complain if system headers are #included both with
    // and without _DEBUG defined, so we have to #include all the
    // system headers used by pyconfig.h right here.
#   include <stddef.h>
#   include <stdarg.h>
#   include <stdio.h>
#   include <stdlib.h>
#   include <assert.h>
#   include <errno.h>
#   include <ctype.h>
#   include <wchar.h>
#   include <basetsd.h>
#   include <io.h>
#   include <limits.h>
#   include <float.h>
#   include <string.h>
#   include <math.h>
#   include <time.h>
#  endif
#  undef _DEBUG // Don't let Python force the debug library just because we're debugging.
#  define DEBUG_UNDEFINED_FROM_WRAP_PYTHON_H
# endif
#endif

# include <pyconfig.h>

//
// Python's LongObject.h helpfully #defines ULONGLONG_MAX for us,
// which confuses Boost's config
//
#include <limits.h>
#ifndef ULONG_MAX
# define BOOST_PYTHON_ULONG_MAX_UNDEFINED
#endif
#ifndef LONGLONG_MAX
# define BOOST_PYTHON_LONGLONG_MAX_UNDEFINED
#endif
#ifndef ULONGLONG_MAX
# define BOOST_PYTHON_ULONGLONG_MAX_UNDEFINED
#endif

//
// Get ahold of Python's version number
//
#include <patchlevel.h>

#if PY_MAJOR_VERSION<2 || PY_MAJOR_VERSION==2 && PY_MINOR_VERSION<7
#error Python 2.7 or higher is required for this version of Boost.Python.
#endif

//
// Some things we need in order to get Python.h to work with compilers other
// than MSVC on Win32
//
#if defined(_WIN32) || defined(__CYGWIN__)
# if defined(__GNUC__) && defined(__CYGWIN__)
#  define SIZEOF_LONG 4
# endif

#endif // _WIN32

# include <Python.h>

#ifdef BOOST_PYTHON_ULONG_MAX_UNDEFINED
# undef ULONG_MAX
# undef BOOST_PYTHON_ULONG_MAX_UNDEFINED
#endif

#ifdef BOOST_PYTHON_LONGLONG_MAX_UNDEFINED
# undef LONGLONG_MAX
# undef BOOST_PYTHON_LONGLONG_MAX_UNDEFINED
#endif

#ifdef BOOST_PYTHON_ULONGLONG_MAX_UNDEFINED
# undef ULONGLONG_MAX
# undef BOOST_PYTHON_ULONGLONG_MAX_UNDEFINED
#endif

#ifdef DEBUG_UNDEFINED_FROM_WRAP_PYTHON_H
# undef DEBUG_UNDEFINED_FROM_WRAP_PYTHON_H
# define _DEBUG
# ifdef _CRT_NOFORCE_MANIFEST_DEFINED_FROM_WRAP_PYTHON_H
#  undef _CRT_NOFORCE_MANIFEST_DEFINED_FROM_WRAP_PYTHON_H
#  undef _CRT_NOFORCE_MANIFEST
# endif
#endif

#ifdef _MSC_VER
# pragma warning(disable:4786)
#endif

#if defined(HAVE_LONG_LONG)
# if defined(PY_LONG_LONG)
#  define BOOST_PYTHON_LONG_LONG PY_LONG_LONG
# elif defined(LONG_LONG)
#  define BOOST_PYTHON_LONG_LONG LONG_LONG
# else
#  error "HAVE_LONG_LONG defined but not PY_LONG_LONG or LONG_LONG"
# endif
#endif

//
// Python 2 and 3 compatibility
//
#if PY_MAJOR_VERSION >= 3
# define BOOST_PyInt_Type PyLong_Type
# define BOOST_PyInt_AsLong PyLong_AsLong
# define BOOST_PyInt_AS_LONG PyLong_AS_LONG
# define BOOST_PyInt_AsSsize_t PyLong_AsSsize_t
# define BOOST_PyString_Type PyUnicode_Type
# define BOOST_PyString_FromString PyUnicode_FromString
# define BOOST_PyString_FromStringAndSize PyUnicode_FromStringAndSize
# define BOOST_PyString_PyString_InternFromString PyUnicode_InternFromString
#else
# define BOOST_PyInt_Type PyInt_Type
# define BOOST_PyInt_AsLong PyInt_AsLong
# define BOOST_PyInt_AS_LONG PyInt_AS_LONG
# define BOOST_PyInt_AsSsize_t PyInt_AsSsize_t
# define BOOST_PyString_Type PyString_Type
# define BOOST_PyString_FromString PyString_FromString
# define BOOST_PyString_FromStringAndSize PyString_FromStringAndSize
# define BOOST_PyString_PyString_InternFromString PyString_InternFromString
#endif
