// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef MANAGE_NEW_OBJECT_DWA200222_HPP
# define MANAGE_NEW_OBJECT_DWA200222_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/to_python_indirect.hpp>

namespace boost { namespace python { 

struct manage_new_object
{
    template <class T>
    struct apply
    {        
        using type = to_python_indirect<T, detail::make_owning_holder>;
        static_assert(std::is_pointer<T>::value,
            "manage_new_object requires a pointer return type");
    };
};

}} // namespace boost::python

#endif // MANAGE_NEW_OBJECT_DWA200222_HPP
