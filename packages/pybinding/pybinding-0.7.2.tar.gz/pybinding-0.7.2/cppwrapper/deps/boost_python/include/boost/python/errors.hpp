//  (C) Copyright David Abrahams 2000.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//
//  The author gratefully acknowleges the support of Dragon Systems, Inc., in
//  producing this work.

#ifndef ERRORS_DWA052500_H_
# define ERRORS_DWA052500_H_

# include <boost/python/detail/prefix.hpp>
# include <functional>

namespace boost { namespace python {

struct BOOST_PYTHON_DECL_EXCEPTION error_already_set
{
  virtual ~error_already_set();
};

// Handles exceptions caught just before returning to Python code.
// Returns true iff an exception was caught.
// All exceptions will be caugth inside, hence the 'noexcept' specifier.
namespace detail {
    BOOST_PYTHON_DECL bool handle_exception_impl(std::function<void()>) noexcept;
}

template <class T>
inline bool handle_exception(T&& f) noexcept {
    return detail::handle_exception_impl(std::forward<T>(f));
}

inline void handle_exception() noexcept {
    handle_exception([]{ throw; }); // rethrow existing
}

BOOST_PYTHON_DECL void throw_error_already_set();

template <class T>
inline T* expect_non_null(T* x)
{
    if (x == nullptr)
        throw_error_already_set();
    return x;
}

// Return source if it is an instance of pytype; throw an appropriate
// exception otherwise.
BOOST_PYTHON_DECL PyObject* pytype_check(PyTypeObject* pytype, PyObject* source);

}} // namespace boost::python

#endif // ERRORS_DWA052500_H_
