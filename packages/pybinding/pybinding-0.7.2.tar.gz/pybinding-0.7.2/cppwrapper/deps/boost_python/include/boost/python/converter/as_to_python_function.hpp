// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef AS_TO_PYTHON_FUNCTION_DWA2002121_HPP
# define AS_TO_PYTHON_FUNCTION_DWA2002121_HPP
# include <boost/python/detail/prefix.hpp>
# include <type_traits>
# include <utility> // for std::move_if_noexcept

namespace boost { namespace python { namespace converter { 

// Given a typesafe to_python conversion function, produces a
// to_python_function which can be registered in the usual way.
template <class T, class ToPython>
struct as_to_python_function
{
    static PyObject* convert(void const* x)
    {
        static_assert(std::is_same<decltype(ToPython::convert), PyObject*(T)>::value ||
                      std::is_same<decltype(ToPython::convert), PyObject*(T const&)>::value,
                      "Convert function must take value or const reference");
        
        // Yes, the const_cast below opens a hole in const-correctness,
        // but it's needed to convert auto_ptr<U> to python.
        //
        // How big a hole is it?  It allows ToPython::convert() to be
        // a function which modifies its argument. The upshot is that
        // client converters applied to const objects may invoke
        // undefined behavior. The damage, however, is limited by the
        // use of the assertion function. Thus, the only way this can
        // modify its argument is if T is an auto_ptr-like type. There
        // is still a const-correctness hole w.r.t. auto_ptr<U> const,
        // but c'est la vie.
        return convert_impl(*const_cast<T*>(static_cast<T const*>(x)),
                            std::is_copy_constructible<T>{});
    }

private:
    static PyObject* convert_impl(T& x, std::true_type) {
        return ToPython::convert(x);
    }

    static PyObject* convert_impl(T& x, std::false_type) {
        return ToPython::convert(std::move_if_noexcept(x));
    }
};

}}} // namespace boost::python::converter

#endif // AS_TO_PYTHON_FUNCTION_DWA2002121_HPP
