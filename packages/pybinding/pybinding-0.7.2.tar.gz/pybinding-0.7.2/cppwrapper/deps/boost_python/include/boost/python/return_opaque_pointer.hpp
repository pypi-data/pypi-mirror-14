// Copyright Gottfried Gan�auge 2003.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
/*
 * Generic Return value converter generator for opaque C++-pointers
 */
# ifndef RETURN_OPAQUE_POINTER_HPP_
# define RETURN_OPAQUE_POINTER_HPP_

# include <boost/python/detail/prefix.hpp>
# include <boost/python/opaque_pointer_converter.hpp>
# include <boost/python/to_python_value.hpp>
# include <boost/python/detail/value_arg.hpp>

namespace boost { namespace python {

struct return_opaque_pointer {
    template <class R>
    struct apply {
        static_assert(std::is_pointer<R>::value, 
                      "return_opaque_pointer expects a pointer type");

        struct type : boost::python::make_to_python_value<R> {
            type() {
                using pointee = cpp14::remove_cv_t<cpp14::remove_pointer_t<R>>;
                [](...){}(opaque<pointee>::instance); // lambda to ignore unused variable warning
            }
        };
    };
};

}} // namespace boost::python
# endif // RETURN_OPAQUE_POINTER_HPP_
