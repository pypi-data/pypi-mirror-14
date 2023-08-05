// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef MAKE_INSTANCE_DWA200296_HPP
# define MAKE_INSTANCE_DWA200296_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/object/instance.hpp>
# include <boost/python/converter/registered.hpp>
# include <boost/python/detail/none.hpp>
# include <boost/python/handle.hpp>

namespace boost { namespace python { namespace objects { 

template <class T, class Holder, class Derived>
struct make_instance_impl {
    using instance_t = objects::instance<Holder>;

    template<class Arg>
    static PyObject* execute(Arg&& x) {
        static_assert(std::is_class<T>::value || std::is_union<T>::value, "");

        PyTypeObject* type = Derived::get_class_object(x);

        if (type == nullptr)
            return python::detail::none();

        PyObject* raw_instance = type->tp_alloc(
            type, objects::additional_instance_size<Holder>::value
        );

        if (raw_instance) {
            python::handle<> protect(raw_instance);
            auto instance = (instance_t*)raw_instance;
            
            // construct the new C++ object and install the pointer
            // in the Python object.
            Derived::construct(
                &instance->storage, raw_instance, std::forward<Arg>(x)
            )->install(raw_instance);

            // Note the position of the internally-stored Holder,
            // for the sake of destruction
            Py_SIZE(instance) = offsetof(instance_t, storage);

            // Release ownership of the python object
            protect.release();
        }

        return raw_instance;
    }
};
    

template <class T, class Holder>
struct make_instance : make_instance_impl<T, Holder, make_instance<T, Holder>> {
    template <class U>
    static PyTypeObject* get_class_object(U&) {
        return converter::registered<T>::converters.get_class_object();
    }

    template<class Arg>
    static Holder* construct(void* storage, PyObject* instance, Arg&& x) {
        return new (storage) Holder(instance, std::forward<Arg>(x));
    }
};
  

}}} // namespace boost::python::object

#endif // MAKE_INSTANCE_DWA200296_HPP
