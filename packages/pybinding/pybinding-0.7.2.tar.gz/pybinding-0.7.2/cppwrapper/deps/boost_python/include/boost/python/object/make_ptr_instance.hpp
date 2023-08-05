// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef MAKE_PTR_INSTANCE_DWA200296_HPP
# define MAKE_PTR_INSTANCE_DWA200296_HPP

# include <boost/python/object/make_instance.hpp>
# include <boost/python/converter/registry.hpp>
# include <boost/python/detail/get_pointer.hpp>

namespace boost { namespace python { namespace objects { 

template<class T, class Holder>
struct make_ptr_instance : make_instance_impl<T, Holder, make_ptr_instance<T, Holder>> {
    template<class Arg>
    static Holder* construct(void* storage, PyObject* /*instance*/, Arg&& x) {
        return new (storage) Holder(std::forward<Arg>(x));
    }
    
    template<class Ptr>
    static PyTypeObject* get_class_object(Ptr const& x) {
        auto p = get_pointer(x);
        if (p == nullptr)
            return nullptr; // means "return None".

        using pointee = cpp14::remove_pointer_t<decltype(p)>;
        if (std::is_polymorphic<pointee>::value) {
            if (auto r = converter::registry::query(typeid(*p)))
                return r->m_class_object;
        }

        return converter::registered<T>::converters.get_class_object();
    }
};

}}} // namespace boost::python::object

#endif // MAKE_PTR_INSTANCE_DWA200296_HPP
