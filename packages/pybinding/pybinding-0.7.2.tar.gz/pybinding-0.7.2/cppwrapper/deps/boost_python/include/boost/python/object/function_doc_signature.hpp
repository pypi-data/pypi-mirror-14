// Copyright Nikolay Mladenov 2007.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef FUNCTION_SIGNATURE_20070531_HPP
# define FUNCTION_SIGNATURE_20070531_HPP

#include <boost/python/object/function.hpp>
#include <boost/python/str.hpp>
#include <boost/python/dict.hpp>

namespace boost { namespace python { namespace objects {

class function_doc_signature_generator {
    static bool are_seq_overloads(function const* f1, function const* f2);

public:
    static str pretty_signature(function const* f, std::size_t num_optional, dict fmt);
    static list function_doc_signatures(function const* f);
};

}}}//end of namespace boost::python::objects

#endif //FUNCTION_SIGNATURE_20070531_HPP
