// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef REFERENCE_EXISTING_OBJECT_DWA200222_HPP
# define REFERENCE_EXISTING_OBJECT_DWA200222_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/to_python_indirect.hpp>

namespace boost { namespace python { 

struct reference_existing_object
{
    template <class T>
    struct apply
    {
        using type = to_python_indirect<T, detail::make_reference_holder>;
        static_assert(std::is_pointer<T>::value || std::is_reference<T>::value,
                      "reference_existing_object requires a pointer or reference return type");
    };
};

}} // namespace boost::python

#endif // REFERENCE_EXISTING_OBJECT_DWA200222_HPP
