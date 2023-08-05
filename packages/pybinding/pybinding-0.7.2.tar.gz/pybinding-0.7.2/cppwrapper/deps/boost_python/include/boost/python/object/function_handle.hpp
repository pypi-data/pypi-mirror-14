// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef FUNCTION_HANDLE_DWA2002725_HPP
# define FUNCTION_HANDLE_DWA2002725_HPP
# include <boost/python/handle.hpp>
# include <boost/python/detail/caller.hpp>
# include <boost/python/default_call_policies.hpp>
# include <boost/python/object/py_function.hpp>
# include <boost/python/signature.hpp>

namespace boost { namespace python { namespace objects { 

BOOST_PYTHON_DECL handle<> function_handle_impl(py_function f);

// Just like function_object, but returns a handle<> instead. Using
// this for arg_to_python<> allows us to break a circular dependency
// between object and arg_to_python.
template<class Signature, class Function>
inline handle<> function_handle(Function const& f) {
    return objects::function_handle_impl(
        python::detail::caller<Function, default_call_policies, Signature>{f, {}}
    );
}

// Just like make_function, but returns a handle<> intead. Same
// reasoning as above.
template<class Function>
handle<> make_function_handle(Function f) {
    return objects::function_handle<python::detail::get_signature_t<Function>>(f);
}

}}} // namespace boost::python::objects

#endif // FUNCTION_HANDLE_DWA2002725_HPP
