// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef OBJECT_SLICES_DWA2002615_HPP
# define OBJECT_SLICES_DWA2002615_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/proxy.hpp>
# include <boost/python/object_core.hpp>
# include <boost/python/slice_nil.hpp>
# include <boost/python/object_protocol.hpp>
# include <boost/python/handle.hpp>
# include <utility>

namespace boost { namespace python { namespace api {

struct const_slice_policies {
    using key_type = std::pair<handle<>, handle<>>;

    static object get(object const& target, key_type const& key) {
        return getslice(target, key.first, key.second);
    }
};

struct slice_policies : const_slice_policies {
    static object const& set(object const& target, key_type const& key, object const& value) {
        setslice(target, key.first, key.second, value);
        return value;
    }

    static void del(object const& target, key_type const& key) {
        delslice(target, key.first, key.second);
    }
};

template <class T, class U>
inline slice_policies::key_type slice_key(T x, U y) {
    return {handle<>(x), handle<>(y)};
}

//
// implementation
//
template <class U>
object_slice object_operators<U>::slice(object_cref start, object_cref finish) {
    return {this->derived(), api::slice_key(borrowed(start.ptr()), borrowed(finish.ptr()))};
}

template <class U>
const_object_slice object_operators<U>::slice(object_cref start, object_cref finish) const {
    return {this->derived(), api::slice_key(borrowed(start.ptr()), borrowed(finish.ptr()))};
}

template <class U>
object_slice object_operators<U>::slice(slice_nil, object_cref finish) {
    return {this->derived(), api::slice_key(allow_null<>(), borrowed(finish.ptr()))};
}

template <class U>
const_object_slice object_operators<U>::slice(slice_nil, object_cref finish) const {
    return {this->derived(), api::slice_key(allow_null<>(), borrowed(finish.ptr()))};
}

template <class U>
object_slice object_operators<U>::slice(slice_nil, slice_nil) {
    return {this->derived(), api::slice_key(allow_null<>(), allow_null<>())};
}

template <class U>
const_object_slice object_operators<U>::slice(slice_nil, slice_nil) const {
    return {this->derived(), api::slice_key(allow_null<>(), allow_null<>())};
}

template <class U>
object_slice object_operators<U>::slice(object_cref start, slice_nil) {
    return {this->derived(), api::slice_key(borrowed(start.ptr()), allow_null<>())};
}

template <class U>
const_object_slice object_operators<U>::slice(object_cref start, slice_nil) const {
    return {this->derived(), api::slice_key(borrowed(start.ptr()), allow_null<>())};
}

template <class U>
template <class T, class V>
inline const_object_slice object_operators<U>::slice(T const& start, V const& end) const {
    return this->slice(typename slice_bound<T>::type(start),
                       typename slice_bound<V>::type(end));
}

template <class U>
template <class T, class V>
inline object_slice object_operators<U>::slice(T const& start, V const& end) {
    return this->slice(typename slice_bound<T>::type(start),
                       typename slice_bound<V>::type(end));
}

}}} // namespace boost::python::api

#endif // OBJECT_SLICES_DWA2002615_HPP
