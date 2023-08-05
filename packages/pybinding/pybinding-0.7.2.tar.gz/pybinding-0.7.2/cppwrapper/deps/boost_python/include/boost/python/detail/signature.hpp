// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef SIGNATURE_DWA20021121_HPP
# define SIGNATURE_DWA20021121_HPP

# include <boost/python/type_id.hpp>
# include <boost/python/detail/type_list.hpp>
# include <boost/python/converter/registry.hpp>

# include <vector>

namespace boost { namespace python { namespace detail { 

struct signature_element {
    type_info cpptype;
    bool lvalue;
};

using py_func_sig_info = std::vector<signature_element>;

template<class T>
using is_reference_to_non_const = std::integral_constant<bool,
	std::is_reference<T>::value && !std::is_const<cpp14::remove_reference_t<T>>::value
>;

template<class Sig> struct signature;

template<class... Args>
struct signature<type_list<Args...>> {
    static py_func_sig_info elements() {
        return {
            { type_id<cpp14::remove_pointer_t<Args>>(),
              is_reference_to_non_const<Args>::value }...
        };
    }
};

}}} // namespace boost::python::detail

#endif // SIGNATURE_DWA20021121_HPP
