// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef REFERENT_STORAGE_DWA200278_HPP
# define REFERENT_STORAGE_DWA200278_HPP
# include <boost/python/cpp14/type_traits.hpp>

namespace boost { namespace python { namespace detail {

// This is a little ugly, but the "bytes" data member
// is needed for backward compatibility.
template <class T>
struct aligned_storage {
    cpp14::aligned_storage_t<sizeof(T), alignof(T)> bytes[1];
};

template <bool is_array = false>
struct value_destroyer {
    template <class T>
    static void execute(T const volatile* p) {
        p->~T();
    }
};

template <>
struct value_destroyer<true> {
    template <class A, class T>
    static void execute(A*, T const volatile* const first) {
        for (T const volatile* p = first; p != first + sizeof(A)/sizeof(T); ++p) {
            value_destroyer<std::is_array<T>::value>::execute(p);
        }
    }

    template <class T>
    static void execute(T const volatile* p) {
        execute(p, *p);
    }
};

template <class T>
inline void destroy_stored(void* p)
{
    using value_t = cpp14::remove_reference_t<T>;
    value_destroyer<std::is_array<value_t>::value>::execute((value_t*)p);
}

template<class T, class U = cpp14::remove_reference_t<T>>
inline U& void_ptr_to_reference(void const volatile* p) {
    return *(U*)p;
}

}}} // namespace boost::python::detail

#endif // REFERENT_STORAGE_DWA200278_HPP
