//  (C) Copyright David Abrahams 2000.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//
//  The author gratefully acknowleges the support of Dragon Systems, Inc., in
//  producing this work.

#ifndef CONFIG_DWA052200_H_
# define CONFIG_DWA052200_H_

/*****************************************************************************
 *
 *  Set up dll import/export options:
 *
 ****************************************************************************/

// backwards compatibility:
#ifdef BOOST_PYTHON_STATIC_LIB
#  define BOOST_PYTHON_STATIC_LINK
# elif !defined(BOOST_PYTHON_DYNAMIC_LIB)
#  define BOOST_PYTHON_DYNAMIC_LIB
#endif

#if defined(BOOST_PYTHON_DYNAMIC_LIB)

#  ifdef __GNUC__
#    define BOOST_PYTHON_USE_GCC_SYMBOL_VISIBILITY 1
#  endif 

#  if BOOST_PYTHON_USE_GCC_SYMBOL_VISIBILITY
#     if defined(BOOST_PYTHON_SOURCE)
#        define BOOST_PYTHON_DECL __attribute__ ((__visibility__("default")))
#        define BOOST_PYTHON_BUILD_DLL
#     else
#        define BOOST_PYTHON_DECL
#     endif
#     define BOOST_PYTHON_DECL_FORWARD
#     define BOOST_PYTHON_DECL_EXCEPTION __attribute__ ((__visibility__("default")))
#  elif (defined(_WIN32) || defined(__CYGWIN__))
#     if defined(BOOST_PYTHON_SOURCE)
#        define BOOST_PYTHON_DECL __declspec(dllexport)
#        define BOOST_PYTHON_BUILD_DLL
#     else
#        define BOOST_PYTHON_DECL __declspec(dllimport)
#     endif
#  endif

#endif

#ifndef BOOST_PYTHON_DECL
#  define BOOST_PYTHON_DECL
#endif

#ifndef BOOST_PYTHON_DECL_FORWARD
#  define BOOST_PYTHON_DECL_FORWARD BOOST_PYTHON_DECL
#endif

#ifndef BOOST_PYTHON_DECL_EXCEPTION
#  define BOOST_PYTHON_DECL_EXCEPTION BOOST_PYTHON_DECL
#endif

#ifndef BOOST_PYTHON_NO_PY_SIGNATURES
#define BOOST_PYTHON_SUPPORTS_PY_SIGNATURES // enables smooth transition
#endif

# ifndef BOOST_PYTHON_USE_STD_SHARED_PTR
#  define BOOST_PYTHON_USE_STD_SHARED_PTR
# endif
# ifndef BOOST_PYTHON_USE_STD_REF
#  define BOOST_PYTHON_USE_STD_REF
# endif

# define BP_DEPRECATED

#endif // CONFIG_DWA052200_H_
