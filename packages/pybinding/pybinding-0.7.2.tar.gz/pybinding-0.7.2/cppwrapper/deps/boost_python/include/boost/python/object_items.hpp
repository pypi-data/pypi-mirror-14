// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef OBJECT_ITEMS_DWA2002615_HPP
# define OBJECT_ITEMS_DWA2002615_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/proxy.hpp>
# include <boost/python/object_core.hpp>
# include <boost/python/object_protocol.hpp>

namespace boost { namespace python { namespace api {

struct const_item_policies {
    using key_type = object;

    static object get(object const& target, object const& key) { return getitem(target, key); }
};

struct item_policies : const_item_policies {
    static object const& set(object const& target, object const& key, object const& value) {
        setitem(target, key, value);
        return value;
    }

    static void del(object const& target, object const& key) { delitem(target, key); }
};

//
// implementation
//
template <class U>
inline object_item object_operators<U>::operator[](object_cref key) {
    return {this->derived(), key};
}

template <class U>
inline const_object_item object_operators<U>::operator[](object_cref key) const {
    return {this->derived(), key};
}

template <class U>
template <class T>
inline const_object_item object_operators<U>::operator[](T const& key) const {
    return (*this)[object(key)];
}

template <class U>
template <class T>
inline object_item object_operators<U>::operator[](T const& key) {
    return (*this)[object(key)];
}

}}} // namespace boost::python::api

#endif // OBJECT_ITEMS_DWA2002615_HPP
