// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef EXCEPTION_TRANSLATOR_DWA2002810_HPP
# define EXCEPTION_TRANSLATOR_DWA2002810_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/detail/exception_handler.hpp>

namespace boost { namespace python { 

// Used to translate C++ exceptions of type ExceptionType 
// into Python exceptions by invoking an object of type Translate.
template <class ExceptionType, class Translate>
void register_exception_translator(Translate translate)
{
    detail::exception_handler::add([translate](
        detail::exception_handler const& handler,
        std::function<void()> const& f
    ) -> bool
    {
        try
        {
            return handler(f);
        }
        catch(ExceptionType const& e)
        {
            translate(e);
            return true;
        }
    });
}

}} // namespace boost::python

#endif // EXCEPTION_TRANSLATOR_DWA2002810_HPP
