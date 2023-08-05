// Copyright David Abrahams 2003.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef NULLARY_FUNCTION_ADAPTOR_DWA2003824_HPP
# define NULLARY_FUNCTION_ADAPTOR_DWA2003824_HPP

# include <boost/python/detail/prefix.hpp>

namespace boost { namespace python { namespace detail { 

// nullary_function_adaptor -- a class template which ignores its
// arguments and calls a nullary function instead.  Used for building
// error-reporting functions, c.f. pure_virtual
template <class NullaryFunction>
struct nullary_function_adaptor
{
    nullary_function_adaptor(NullaryFunction fn)
      : m_fn(fn) {}

    template<class... Args>
    void operator()(Args const&...) const {
        m_fn();
    }
    
 private:
    NullaryFunction m_fn;
};

}}} // namespace boost::python::detail

#endif // NULLARY_FUNCTION_ADAPTOR_DWA2003824_HPP
