// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef ITERATOR_DWA2002512_HPP
# define ITERATOR_DWA2002512_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/detail/target.hpp>
# include <boost/python/object/iterator.hpp>
# include <boost/python/object_core.hpp>

# include <functional>

namespace boost { namespace python { 

namespace detail
{
  // Adds an additional layer of binding to
  // objects::make_iterator(...), which allows us to pass member
  // function and member data pointers.
  template <class NextPolicies, class Target, class Accessor1, class Accessor2>
  inline object make_iterator(Accessor1 get_start, Accessor2 get_finish)
  {
      using namespace std::placeholders;
      return objects::make_iterator_function<NextPolicies, Target>(
          std::bind(get_start, _1),
          std::bind(get_finish, _1)
      );
  }

  // Guts of template class iterators<>, below.
  template <bool const_ = false>
  struct iterators_impl
  {
      template <class T>
      struct apply
      {
          typedef typename T::iterator iterator;
          static iterator begin(T& x) { return x.begin(); }
          static iterator end(T& x) { return x.end(); }
      };
  };

  template <>
  struct iterators_impl<true>
  {
      template <class T>
      struct apply
      {
          typedef typename T::const_iterator iterator;
          static iterator begin(T& x) { return x.begin(); }
          static iterator end(T& x) { return x.end(); }
      };
  };
}

// An "ordinary function generator" which contains static begin(x) and
// end(x) functions that invoke T::begin() and T::end(), respectively.
template <class T>
struct iterators
    : detail::iterators_impl<
        std::is_const<T>::value
      >::template apply<T>
{
};

// Create an iterator-building function which uses the given
// accessors. Deduce the Target type from the accessors. The iterator
// returns copies of the inderlying elements.
template <class Accessor1, class Accessor2>
object range(Accessor1 start, Accessor2 finish)
{
    return detail::make_iterator<
        objects::default_iterator_call_policies, detail::target_t<Accessor1>
    >(start, finish);
}

// Create an iterator-building function which uses the given accessors
// and next() policies. Deduce the Target type.
template <class NextPolicies, class Accessor1, class Accessor2>
object range(Accessor1 start, Accessor2 finish)
{
    return detail::make_iterator<
        NextPolicies, detail::target_t<Accessor1>
    >(start, finish);
}

// Create an iterator-building function which uses the given accessors
// and next() policies, operating on the given Target type
template <class NextPolicies, class Target, class Accessor1, class Accessor2>
object range(Accessor1 start, Accessor2 finish)
{
    return detail::make_iterator<NextPolicies, Target&>(start, finish);
}

// A Python callable object which produces an iterator traversing
// [x.begin(), x.end()), where x is an instance of the Container
// type. NextPolicies are used as the CallPolicies for the iterator's
// next() function.
template <class Container
          , class NextPolicies = objects::default_iterator_call_policies>
struct iterator : object
{
    iterator()
        : object(
            python::range<NextPolicies>(
                &iterators<Container>::begin, &iterators<Container>::end
                ))
    {
    }
};

}} // namespace boost::python

#endif // ITERATOR_DWA2002512_HPP
