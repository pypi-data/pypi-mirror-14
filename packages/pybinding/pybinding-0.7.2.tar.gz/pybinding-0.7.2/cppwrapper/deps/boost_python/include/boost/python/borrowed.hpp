// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef BORROWED_DWA2002614_HPP
# define BORROWED_DWA2002614_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/cpp14/type_traits.hpp>
# include <boost/python/detail/is_xxx.hpp>

namespace boost { namespace python {

namespace detail {
    template<class T>
    class borrowed {
        using type = T;
    };

    template<class T>
    using is_borrowed_ptr = std::integral_constant<bool,
        std::is_pointer<T>::value &&
            detail::is_<borrowed, cpp14::remove_cv_t<cpp14::remove_pointer_t<T>>>::value
    >;
}

template <class T>
inline python::detail::borrowed<T>* borrowed(T* p)
{
    return (detail::borrowed<T>*)p;
}

template <class T>
inline T* get_managed_object(detail::borrowed<T> const volatile* p)
{
    return (T*)p;
}

}} // namespace boost::python

#endif // BORROWED_DWA2002614_HPP
