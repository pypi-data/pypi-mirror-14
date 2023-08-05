// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef TUPLE_20020706_HPP
# define TUPLE_20020706_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/object.hpp>
# include <boost/python/converter/pytype_object_mgr_traits.hpp>

namespace boost { namespace python {

class tuple : public object {
public:
    tuple() : object{detail::new_reference(PyTuple_New(0))} {}

    template <class T>
    explicit tuple(T const& sequence) : object{call(object{sequence})} {}

private:
    static detail::new_reference call(object const& arg) {
        return (detail::new_reference)PyObject_CallFunctionObjArgs(
            upcast<PyObject>(&PyTuple_Type), arg.ptr(), nullptr
        );
    }

public: // implementation detail -- for internal use only
    BOOST_PYTHON_FORWARD_OBJECT_CONSTRUCTORS(tuple, object)
};

//
// Converter Specializations
//
namespace converter {
    template <>
    struct object_manager_traits<tuple>
        : pytype_object_manager_traits<&PyTuple_Type, tuple>
    {};
}

template <class... Args>
tuple make_tuple(Args const&... args) {
    return tuple{detail::new_reference(
        PyTuple_Pack(sizeof...(Args), object{args}.ptr()...)
    )};
};

}}  // namespace boost::python

#endif
