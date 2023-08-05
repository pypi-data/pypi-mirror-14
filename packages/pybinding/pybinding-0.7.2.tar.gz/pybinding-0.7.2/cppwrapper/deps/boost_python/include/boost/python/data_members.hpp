// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef DATA_MEMBERS_DWA2002328_HPP
# define DATA_MEMBERS_DWA2002328_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/return_value_policy.hpp>
# include <boost/python/return_by_value.hpp>
# include <boost/python/return_internal_reference.hpp>
# include <boost/python/make_function.hpp>

# include <boost/python/converter/builtin_converters.hpp>

namespace boost { namespace python {

//
// This file defines the make_getter and make_setter function
// families, which are responsible for turning pointers, references,
// and pointers-to-data-members into callable Python objects which
// can be used for attribute access on wrapped classes.
//

namespace detail {
  //
  // Helper metafunction for determining the default CallPolicy to use
  // for attribute access.  If T is a [reference to a] class type X
  // whose conversion to python would normally produce a new copy of X
  // in a wrapped X class instance (as opposed to types such as
  // std::string, which are converted to native Python types, and
  // smart pointer types which produce a wrapped class instance of the
  // pointee type), to-python conversions will attempt to produce an
  // object which refers to the original C++ object, rather than a
  // copy. See default_getter_policy for rationale.
  template<class T, class = void>
  struct uses_registry : std::false_type {};

  // SFINAE workaround for VS2015 RC
  template<bool> struct bool_void { using type = void; };

  template<class T>
  struct uses_registry<T, typename bool_void<make_to_python_value<T>::uses_registry>::type>
      : std::integral_constant<bool, make_to_python_value<T>::uses_registry>
  {};

  template <class T>
  using default_getter_by_ref = std::integral_constant<bool,
      uses_registry<T>::value && std::is_class<T>::value
  >;

  // Metafunction computing the default CallPolicy to use for reading
  // non-member data.
  template<class Data>
  struct default_getter_policy : cpp14::conditional_t<
      default_getter_by_ref<cpp14::remove_pointer_t<Data>>::value,
      return_value_policy<reference_existing_object>,
      return_value_policy<return_by_value>
  > {};

  // Metafunction computing the default CallPolicy to use for reading
  // data members
  //
  // If it's a regular class type (not an object manager or other
  // type for which we have to_python specializations, use
  // return_internal_reference so that we can do things like
  //    x.y.z =  1
  // and get the right result.
  template<class Data, class Class>
  struct default_getter_policy<Data Class::*> : cpp14::conditional_t<
      default_getter_by_ref<Data>::value,
      return_internal_reference<>,
      return_value_policy<return_by_value>
  > {};

  //
  // make_getter helper function family -- These helpers to
  // boost::python::make_getter are used to dispatch behavior.

  // Handle non-member pointers
  template<class Data, class CallPolicies>
  inline object make_getter(Data* d, CallPolicies const& call_policies) {
      return python::make_function(
          [d]() -> Data& { return *d; },
          call_policies
      );
  }

  // Handle pointers-to-members
  template<class Class, class Data, class CallPolicies>
  inline object make_getter(Data Class::*pm, CallPolicies const& call_policies) {
      return python::make_function(
          [pm](Class& c) -> Data& { return c.*pm; },
          call_policies
      );
  }

  // Handle references
  template<class Data, class CallPolicies>
  inline object make_getter(Data& d, CallPolicies const& cp) {
      return detail::make_getter(&d, cp);
  }

  //
  // make_setter helper function family -- These helpers to
  // boost::python::make_setter are used to dispatch behavior.
  
  // Handle non-member pointers
  template<class Data, class CallPolicies>
  inline object make_setter(Data* d, CallPolicies const& call_policies) {
      return python::make_function(
          [d](Data const& rhs) { *d = rhs; },
          call_policies
      );
  }

  // Handle pointers-to-members
  template<class Class, class Data, class CallPolicies>
  inline object make_setter(Data Class::*pm, CallPolicies const& call_policies) {
      return python::make_function(
          [pm](Class& c, Data const& rhs) { c.*pm = rhs; },
          call_policies
      );
  }

  // Handle references
  template<class Data, class CallPolicies>
  inline object make_setter(Data& x, CallPolicies const& cp) {
      return detail::make_setter(&x, cp);
  }
}

//
// make_getter function family -- build a callable object which
// retrieves data through the first argument and is appropriate for
// use as the `get' function in Python properties .  The second,
// policies argument, is optional.
template<class Data, class CallPolicies = detail::default_getter_policy<Data>>
inline object make_getter(Data const& d, CallPolicies const& cp = {}) {
    return detail::make_getter(d, cp);
}

//
// make_setter function family -- build a callable object which
// writes data through the first argument and is appropriate for
// use as the `set' function in Python properties .  The second,
// policies argument, is optional.
template<class Data, class CallPolicies = default_call_policies>
inline object make_setter(Data&& d, CallPolicies const& cp = {}) {
    return detail::make_setter(d, cp);
}

}} // namespace boost::python

#endif // DATA_MEMBERS_DWA2002328_HPP
