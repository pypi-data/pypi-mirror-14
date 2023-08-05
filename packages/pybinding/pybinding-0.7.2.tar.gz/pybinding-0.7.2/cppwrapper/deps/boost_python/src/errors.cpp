// Copyright David Abrahams 2001.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef BOOST_PYTHON_SOURCE
# define BOOST_PYTHON_SOURCE
#endif

#include <boost/python/errors.hpp>
#include <boost/python/detail/exception_handler.hpp>

#include <stdexcept>

namespace boost { namespace python {

error_already_set::~error_already_set() {}

// IMPORTANT: this function may only be called from within a catch block!
BOOST_PYTHON_DECL bool detail::handle_exception_impl(std::function<void()> f) noexcept
{
    try
    {
        if (detail::exception_handler::chain)
            return detail::exception_handler::chain->handle(f);
        f();
        return false;
    }
    catch(const boost::python::error_already_set&)
    {
        // The python error reporting has already been handled.
    }
    catch(const std::bad_alloc&)
    {
        PyErr_NoMemory();
    }
    catch(const std::overflow_error& x)
    {
        PyErr_SetString(PyExc_OverflowError, x.what());
    }
    catch(const std::out_of_range& x)
    {
        PyErr_SetString(PyExc_IndexError, x.what());
    }
    catch(const std::invalid_argument& x)
    {
        PyErr_SetString(PyExc_ValueError, x.what());
    }
    catch(const std::exception& x)
    {
        PyErr_SetString(PyExc_RuntimeError, x.what());
    }
    catch(...)
    {
        PyErr_SetString(PyExc_RuntimeError, "unidentifiable C++ exception");
    }
    return true;
}

void BOOST_PYTHON_DECL throw_error_already_set()
{
    throw error_already_set();
}

namespace detail {

std::unique_ptr<exception_handler> exception_handler::chain;
exception_handler* exception_handler::tail;

} // namespace boost::python::detail

}} // namespace boost::python


