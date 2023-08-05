// Copyright Nikolay Mladenov 2007.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#include <boost/python/object/function_doc_signature.hpp>
#include <boost/python/docstring_options.hpp>
#include <vector>

namespace boost { namespace python {

dict& docstring_options::format() {
    static dict fmt = []{
        auto fmt_ = dict{
            "doc"_kw = "\n{python_signature}{docstring}{cpp_signature}",
            "docstring_indent"_kw = "    ",
            "cpp"_kw = dict{
                "signature"_kw = "\nC++ signature:\n"
                                "    {cpptype_return} {function_name}({parameters})",
                "parameter"_kw = "{cpptype}{lvalue} {name}{default_value}",
                "unnamed"_kw = "arg{}",
                "default_value"_kw = "={!r}",
                "lvalue"_kw = " {lvalue}",
                "separator"_kw = ", ",
                "optional_open"_kw = "[",
                "optional_close"_kw = "]",
                "raw"_kw = "PyObject* args, PyObject* kwargs"
            },
            "python"_kw = dict{
                "signature"_kw = "{function_name}({parameters}) -> {pytype_return}:",
                "parameter"_kw = "{name}: {pytype}{default_value}",
                "unnamed"_kw = "arg{}",
                "default_value"_kw = "={!r}",
                "lvalue"_kw = "",
                "separator"_kw = ", ",
                "optional_open"_kw = "[",
                "optional_close"_kw = "]",
                "raw"_kw = "*args, **kwargs"
            }
        };

        // Small hack here -> look for better solution.
        // Because this dict has static storage duration, its destructor may be called
        // after the Python interpreter has been finalized. This causes a segmentation
        // fault when decref is called in the destructor. Incrementing the count here
        // will prevent this. This creates a reference leak, but we expect it to live
        // until exit anyway, so it's not a huge deal. (But a better solutions would be
        // really *really* nice.)
        incref(fmt_.ptr());

        return fmt_;
    }();

    return fmt;
}

void docstring_options::update_format(dict m) { format().update(m); }
void docstring_options::update_cpp_format(dict m) { format()["cpp"].attr("update")(m); }
void docstring_options::update_python_format(dict m) { format()["python"].attr("update")(m); }

}} // namespace boost::python

namespace boost { namespace python { namespace objects {

bool function_doc_signature_generator::are_seq_overloads(function const* f1, function const* f2) {
    if (f2->m_fn.max_arity() != f1->m_fn.max_arity() + 1)
        return false;
    if (f2->doc() != f1->doc())
        return false;
    if (f2->m_arg_names.slice(0, -1) != f1->m_arg_names)
        return false;

    // check if the argument types are the same
    auto s1 = f1->m_fn.signature();
    auto s2 = f2->m_fn.signature();
    for (unsigned i = 0; i <= f1->m_fn.max_arity(); ++i) {
        if (s1[i].cpptype != s2[i].cpptype)
            return false;
    }

    return true;
}

inline char const* get_pytype_string(python::detail::signature_element const& s,
                                     bool is_return = false)
{
    if (s.cpptype == typeid(void))
        return "None";

    auto const& r = python::converter::registry::lookup(s.cpptype);
    auto pytype = is_return ? r.to_python_target_type() : r.expected_from_python_type();
    return pytype ? pytype->tp_name : "object";
}

str function_doc_signature_generator::pretty_signature(function const* f, std::size_t num_optional, dict fmt) {
    auto arity = f->m_fn.max_arity();
    auto signature = f->m_fn.signature();
    auto arg_names = f->m_arg_names;

    auto cpptype_return = str{signature[0].cpptype.pretty_name()};
    auto params = list{};
    if (arity != objects::py_function::no_arity) {
        // regular function
        for (unsigned n = 1; n <= arity; ++n) {
            auto kwarg = (arg_names && arg_names[n-1]) ? object{arg_names[n-1]} : object{};

            auto pytype = get_pytype_string(signature[n]);
            auto name = [&]{
                if (kwarg)
                    return str{kwarg[0]};
                else if (n == 1 && f->m_namespace == pytype)
                    return "self"_s;
                else
                    return str{fmt["unnamed"]}.format(n);
            }();

            auto parameter_map = dict{
                "name"_kw = name,
                "pytype"_kw = pytype,
                "cpptype"_kw = str{signature[n].cpptype.pretty_name()},
                "lvalue"_kw = signature[n].lvalue ? str{fmt["lvalue"]} : ""_s,
                "default_value"_kw = (kwarg && len(kwarg) == 2)
                                    ? str{fmt["default_value"]}.format(kwarg[1])
                                    : ""_s
            };

            params.append(str{fmt["parameter"]}.format(**parameter_map));
        }
    }
    else {
        // raw function
        params.append(fmt["raw"]);
        cpptype_return = "PyObject*";
    }

    auto signature_map = dict{
        "cpptype_return"_kw = cpptype_return,
        "pytype_return"_kw = get_pytype_string(signature[0], true),
        "function_name"_kw = f->m_name,
        "parameters"_kw = [&]{
            auto separator = str{fmt["separator"]};
            auto optional_open = str{fmt["optional_open"]};
            auto optional_separator = str{optional_open + separator};

            return separator.join(params.slice(0, arity - num_optional))
                + (num_optional ? (num_optional != arity ? optional_separator : optional_open) : ""_s)
                + optional_separator.join(params.slice(arity - num_optional, arity))
                + str{fmt["optional_close"]} * num_optional;
        }()
    };

    return str{fmt["signature"]}.format(**signature_map);
}

list function_doc_signature_generator::function_doc_signatures(function const* f) {
    // flatten overloads and take out 'not_implemented_function'
    auto overloads = [f]{
        struct overload {
            function const* f;
            int num_optional;
        };
        auto result = std::vector<overload>{};

        auto name = f->name();
        auto num_optional = 0;
        for (auto current = f; current; current = current->m_overloads.get()) {
            if (current->name() != name)
                continue; // ignore 'not_implemented_function'

            auto next = current->m_overloads.get();
            if (!next) {
                result.push_back({current, num_optional});
                break;
            }

            // check if next starts a new chain of overloads
            if (!are_seq_overloads(current, next)) {
                result.push_back({current, num_optional});
                num_optional = 0;
            }
            else {
                ++num_optional;
            }
        }

        return result;
    }();

    auto const& format = docstring_options::format();
    auto doc = str{format["doc"]};
    auto indent = str{format["docstring_indent"]};

    auto docs = list{};
    for (auto const& func : overloads) {
        auto docstring = func.f->doc() ? str{func.f->doc()} : ""_s;
        auto mapping = dict{
            "python_signature"_kw = func.f->show_python_signature
                ? pretty_signature(func.f, func.num_optional, dict{format["python"]}) + "\n"_s
                : ""_s,
            "docstring"_kw = docstring
                ? indent + indent.join(docstring.splitlines(true)) + "\n"_s
                : ""_s,
            "cpp_signature"_kw = func.f->show_cpp_signature
                ? pretty_signature(func.f, func.num_optional, dict{format["cpp"]})
                : ""_s
        };

        docs.append(doc.format(**mapping).rstrip());
    }

    return docs;
}

}}} // namespace boost::python::objects
