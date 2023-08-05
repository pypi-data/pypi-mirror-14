// Copyright David Abrahams 2004. Distributed under the Boost
// Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

#include <boost/python/wrapper.hpp>

namespace boost { namespace python { namespace detail {

override wrapper_base::get_override(char const* name, PyTypeObject* class_object) const {
    if (m_self) {
        if (auto m = handle<>{allow_null(PyObject_GetAttrString(m_self, name))}) {
            auto method = (PyMethodObject*)m.get();

            if (PyMethod_Check(m.get()) &&
                method->im_self == m_self &&
                class_object->tp_dict != nullptr)
            {
                PyObject* borrowed_f = PyDict_GetItemString(class_object->tp_dict, name);
                if (borrowed_f != method->im_func)
                    return override{m};
            }
        }
    }

    return override{handle<>{none()}};
};

}}} // namespace boost::python::detail
