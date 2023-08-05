///////////////////////////////////////////////////////////////////////////////
//
// Copyright David Abrahams 2002, Joel de Guzman, 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//
///////////////////////////////////////////////////////////////////////////////
#ifndef SIGNATURE_JDG20020813_HPP
# define SIGNATURE_JDG20020813_HPP

# include <boost/python/cpp14/type_traits.hpp>
# include <boost/python/detail/type_list.hpp>

namespace boost { namespace python { namespace detail {

// A metafunction returning C1 if C1 is derived from C2, and C2 otherwise
template <class C1, class C2>
using most_derived_t = cpp14::conditional_t<std::is_convertible<C1*, C2*>::value, C1, C2>;


//  The following includes generate metafunctions which return signatures
//  for non-member functions:
//
//      Return (BOOST_PYTHON_FN_CC *)(Args...)
//      -> type_list<Return, Args...>
//
//  where BOOST_PYTHON_FN_CC is a calling convention keyword, can be:
//      empty, for default calling convention
//      __cdecl (if BOOST_PYTHON_ENABLE_CDECL is defined)
//      __stdcall (if BOOST_PYTHON_ENABLE_STDCALL is defined)
//      __fastcall (if BOOST_PYTHON_ENABLE_FASTCALL is defined)
//
//
//  For member functions an appropriate assortment of cv-qualifications
//  is defined:
//      Return (BOOST_PYTHON_FN_CC Class::*)(Args...) [const] [volatile]
//      -> type_list<Return, Class-or-Target, Args...>
//
//
//  For functions objects 'operator()' is inspected and the Class type
//  is remove from the signature:
//      Return (BOOST_PYTHON_FN_CC Class::*)(Args...) [const]
//      -> type_list<Return, Args...>
//
//
//  There are two forms for invoking get_signature:
//      get_signature_t<Function>
//      get_signature_t<Function, Target>
//
//  These metafunctions extract the return type, class (for member
//  functions) and arguments of the input signature and stuff them in
//  a type_list (the calling convention is dropped).
//
//  Note that cv-qualification is dropped from the "hidden this" param
//  of member functions; that is a necessary sacrifice to ensure that
//  an lvalue from_python converter is used. A pointer is not used so
//  that None will be rejected for overload resolution.
//
//  The second form of get_signature essentially downcasts the "hidden
//  this" argument of member functions to Target, because the function
//  may actually be a member of a base class which is not wrapped, and
//  in that case conversion from python would fail.


// This is selected if all the function pointer specializations fail to match.
// Assume it's a function object and pass the type of its operator() to another
// specialization which is going to discard the Class type from the signature.
template<class FuncObject, class /*Target*/>
struct get_signature {
    using type = typename get_signature<decltype(&FuncObject::operator()), int>::type;
};

// 'default' calling convention
# define BOOST_PYTHON_FN_CC
# include <boost/python/detail/get_signature.hpp>
# undef BOOST_PYTHON_FN_CC

// Alternate calling conventions are obsolete on Windows for x64 and ARM
# if !defined(_M_X64) && !defined(_M_ARM)
// __cdecl calling convention
#  if defined(BOOST_PYTHON_ENABLE_CDECL)
#   define BOOST_PYTHON_FN_CC __cdecl
#   define BOOST_PYTHON_FN_CC_IS_CDECL
#   include <boost/python/detail/get_signature.hpp>
#   undef BOOST_PYTHON_FN_CC
#   undef BOOST_PYTHON_FN_CC_IS_CDECL
#  endif

// __stdcall calling convention
#  if defined(BOOST_PYTHON_ENABLE_STDCALL)
#   define BOOST_PYTHON_FN_CC __stdcall
#   include <boost/python/detail/get_signature.hpp>
#   undef BOOST_PYTHON_FN_CC
#  endif

// __fastcall calling convention
#  if defined(BOOST_PYTHON_ENABLE_FASTCALL)
#   define BOOST_PYTHON_FN_CC __fastcall
#   include <boost/python/detail/get_signature.hpp>
#   undef BOOST_PYTHON_FN_CC
#  endif
# endif

template<class Function, class Target = void>
using get_signature_t = typename get_signature<Function, Target>::type;

}}} // namespace boost::python::detail

# endif // SIGNATURE_JDG20020813_HPP
