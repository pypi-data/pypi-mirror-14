// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef COPY_NON_CONST_REFERENCE_DWA2002131_HPP
# define COPY_NON_CONST_REFERENCE_DWA2002131_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/to_python_value.hpp>

namespace boost { namespace python { 

struct copy_non_const_reference {
    template <class T>
    struct apply {
        static_assert(
            std::is_reference<T>::value &&
            !std::is_const<cpp14::remove_reference_t<T>>::value,
            "copy_non_const_reference expects a non const reference return type"
        );
        using type = make_to_python_value<T>;
    };
};


}} // namespace boost::python

#endif // COPY_NON_CONST_REFERENCE_DWA2002131_HPP
