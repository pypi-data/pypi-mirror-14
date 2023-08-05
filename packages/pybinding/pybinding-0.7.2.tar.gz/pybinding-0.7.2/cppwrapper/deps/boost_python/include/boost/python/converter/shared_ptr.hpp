// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef SHARED_PTR_FROM_PYTHON_DWA20021130_HPP
# define SHARED_PTR_FROM_PYTHON_DWA20021130_HPP

# include <boost/python/handle.hpp>
# include <boost/python/register_ptr_to_python.hpp>

# include <boost/python/converter/shared_ptr_fwd.hpp>
# include <boost/python/converter/to_python_fwd.hpp>
# include <boost/python/converter/from_python.hpp>
# include <boost/python/converter/rvalue_from_python_data.hpp>
# include <boost/python/converter/registered.hpp>

# include <boost/python/detail/none.hpp>

namespace boost { namespace python { namespace converter {

struct shared_ptr_deleter {
    shared_ptr_deleter(handle<> owner) : owner(owner) {}

    void operator()(void const*) {
        owner.reset();
    }

    handle<> owner;
};

template <class T>
struct shared_ptr_from_python {
    shared_ptr_from_python() {
        // register the converter for both const and non-const versions of the underlying type
        using ptr_to_const = shared_ptr<cpp14::add_const_t<T>>;
        using ptr_to_non_const = shared_ptr<cpp14::remove_const_t<T>>;

        for (auto& cpptype : {type_id<ptr_to_const>(), type_id<ptr_to_non_const>()}) {
            registry::insert_rvalue_converter(
                &convertible, &construct, cpptype, nullptr, &registry::lookup(type_id<T>())
            );
        }
    }

private:
    static void* convertible(PyObject* p) {
        if (p == Py_None)
            return p;
        else
            return converter::get_lvalue_from_python(p, registered<T>::converters);
    }
    
    static void construct(PyObject* source, rvalue_from_python_stage1_data* data) {
        void* const storage = ((converter::rvalue_from_python_storage<shared_ptr<T>>*)
            data)->storage.bytes;

        if (data->convertible == Py_None) {
            new (storage) shared_ptr<T>{};
        }
        else {
            // workaround for enable_shared_from_this
            shared_ptr<void> hold_convertible_ref_count{
                nullptr,
                shared_ptr_deleter{handle<>{borrowed(source)}}
            };
            // use aliasing constructor
            new (storage) shared_ptr<T>{
                hold_convertible_ref_count,
                static_cast<T*>(data->convertible)
            };
        }
        
        data->convertible = storage;
    }
};

} // namespace converter

template<class T>
struct to_python_value<converter::shared_ptr<T>> {
    PyObject* operator()(converter::shared_ptr<T> const& source) const {
        if (!source) {
            return python::detail::none();
        }
        else if (auto* d = converter::get_deleter<converter::shared_ptr_deleter>(source)) {
            return incref(d->owner.get());
        }
        else {
            auto const& converters = converter::registered<converter::shared_ptr<T>>::converters;
            if (!converters.has_to_python())
                register_ptr_to_python<converter::shared_ptr<cpp14::remove_const_t<T>>>();
            return converters.to_python(&source);
        }
    }
};

}} // namespace boost::python

#endif // SHARED_PTR_FROM_PYTHON_DWA20021130_HPP
