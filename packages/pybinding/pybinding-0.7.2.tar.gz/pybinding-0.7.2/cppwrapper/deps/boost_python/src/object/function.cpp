// Copyright David Abrahams 2001.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#include <boost/python/docstring_options.hpp>
#include <boost/python/object/function_object.hpp>
#include <boost/python/object/function_handle.hpp>
#include <boost/python/object/function_doc_signature.hpp>
#include <boost/python/args.hpp>
#include <boost/python/extract.hpp>
#include <boost/python/tuple.hpp>

#include <algorithm>
#include <cstring>

namespace boost { namespace python {
  volatile bool docstring_options::show_user_defined_ = true;
  volatile bool docstring_options::show_cpp_signatures_ = true;
#ifndef BOOST_PYTHON_NO_PY_SIGNATURES
  volatile bool docstring_options::show_py_signatures_ = true;
#else
  volatile bool docstring_options::show_py_signatures_ = false;
#endif
}}

namespace boost { namespace python { namespace objects {

extern PyTypeObject function_type;

function::function(py_function implementation,
                   python::detail::keyword const* const names_and_defaults,
                   unsigned num_keywords)
    : m_fn{std::move(implementation)}
{
    if (names_and_defaults) {
        auto max_arity = m_fn.max_arity();
        auto keyword_offset = (max_arity > num_keywords) ? max_arity - num_keywords : 0;

        auto tuple_size = static_cast<ssize_t>(num_keywords ? max_arity : 0);
        m_arg_names = object{handle<>{PyTuple_New(tuple_size)}};

        if (num_keywords != 0) {
            for (unsigned j = 0; j < keyword_offset; ++j)
                PyTuple_SET_ITEM(m_arg_names.ptr(), j, python::detail::none());
        }
        
        for (unsigned i = 0; i < num_keywords; ++i) {
            tuple kv;

            auto const* const p = names_and_defaults + i;
            if (p->default_value) {
                kv = make_tuple(p->name, p->default_value);
                ++m_nkeyword_values;
            }
            else {
                kv = make_tuple(p->name);
            }

            PyTuple_SET_ITEM(m_arg_names.ptr(), i + keyword_offset, incref(kv.ptr()));
        }
    }
    else {
        m_arg_names = object{handle<>{PyTuple_New(0)}};
    }
    
    PyObject* p = this;
    if (Py_TYPE(&function_type) == nullptr) {
        Py_TYPE(&function_type) = &PyType_Type;
        PyType_Ready(&function_type);
    }

    PyObject_Init(p, &function_type);
}

function::~function() {}

PyObject* function::call(PyObject* args, PyObject* keywords) const {
    auto const n_unnamed_actual = [&]{
        auto const size = PyTuple_GET_SIZE(args);
        return static_cast<std::size_t>(size >= 0 ? size : 0);
    }();
    auto const n_keyword_actual = [&]{
        auto const size = keywords ? PyDict_Size(keywords) : 0;
        return static_cast<std::size_t>(size >= 0 ? size : 0);
    }();
    auto const n_actual = n_unnamed_actual + n_keyword_actual;

    // Try overloads looking for a match
    for (function const* f = this; f; f = f->m_overloads.get()) {
        // Check for a plausible number of arguments
        auto const min_arity = f->m_fn.min_arity();
        auto const max_arity = f->m_fn.max_arity();
        if (n_actual + f->m_nkeyword_values < min_arity || n_actual > max_arity)
            continue;

        // This will be the args that actually get passed
        handle<> inner_args(allow_null(borrowed(args)));

        if (n_keyword_actual > 0     // Keyword arguments were supplied
            || n_actual < min_arity) // or default keyword values are needed
        {
            if (f->m_arg_names.is_none())
                continue; // this overload doesn't accept keywords

            // "all keywords are none" is a special case
            // indicating we will accept any number of keyword
            // arguments
            if (PyTuple_GET_SIZE(f->m_arg_names.ptr()) != 0) {
                // build a new arg tuple, will adjust its size later
                inner_args = handle<>{
                    PyTuple_New(static_cast<ssize_t>(max_arity))
                };

                // Fill in the positional arguments
                for (auto i = 0u; i < n_unnamed_actual; ++i)
                    PyTuple_SET_ITEM(inner_args.get(), i, incref(PyTuple_GET_ITEM(args, i)));

                // Grab remaining arguments by name from the keyword dictionary
                auto n_actual_processed = n_unnamed_actual;

                for (auto arg_pos = n_unnamed_actual; arg_pos < max_arity ; ++arg_pos) {
                    // Get the keyword[, value pair] corresponding
                    PyObject* kv = PyTuple_GET_ITEM(f->m_arg_names.ptr(), arg_pos);

                    // If there were any keyword arguments,
                    // look up the one we need for this
                    // argument position
                    PyObject* value = n_keyword_actual
                        ? PyDict_GetItem(keywords, PyTuple_GET_ITEM(kv, 0))
                        : nullptr;

                    if (!value) {
                        // Not found; check if there's a default value
                        if (PyTuple_GET_SIZE(kv) > 1)
                            value = PyTuple_GET_ITEM(kv, 1);

                        if (!value)
                            break; // still not found; matching fails
                    }
                    else {
                        ++n_actual_processed;
                    }

                    PyTuple_SET_ITEM(inner_args.get(), arg_pos, incref(value));
                }

                if (n_actual_processed < n_actual)
                    continue; // missing argument for this overload
            }
        }

        // Call the function.  Pass keywords in case it's a
        // function accepting any number of keywords
        PyObject* result = inner_args ? f->m_fn(inner_args.get(), keywords) : nullptr;

        // If the result is NULL but no error was set, m_fn failed
        // the argument-matching test.

        // This assumes that all other error-reporters are
        // well-behaved and never return NULL to python without
        // setting an error.
        if (result || PyErr_Occurred())
            return result;
    }

    // None of the overloads matched; time to generate the error message
    argument_error(args, keywords);
    return nullptr;
}

void function::argument_error(PyObject* args, PyObject* /*keywords*/) const {
    static handle<> exception{
        PyErr_NewException(const_cast<char*>("Boost.Python.ArgumentError"),
                           PyExc_TypeError, nullptr)
    };

    auto actual_args = list{};
    for (ssize_t i = 0; i < PyTuple_Size(args); ++i) {
        actual_args.append(PyTuple_GetItem(args, i)->ob_type->tp_name);
    }

    auto cpp_fmt = dict{docstring_options::format()["cpp"]};
    cpp_fmt.update(dict{"signature"_kw = "{function_name}({parameters})"});

    auto cpp_signatures = list{};
    for (auto f = this; f; f = f->m_overloads.get()) {
        cpp_signatures.append(function_doc_signature_generator::pretty_signature(f, 0, cpp_fmt));
    }

    auto fmt = "Python argument types in\n"
               "    {function_name}({actual_args})\n"
               "did not match C++ signature:\n"
               "    {signatures}"_s;

    auto message = fmt.format(**dict{
        "function_name"_kw = "{}.{}"_s.format(m_namespace, m_name),
        "actual_args"_kw = ", "_s.join(actual_args),
        "signatures"_kw = "\n    "_s.join(cpp_signatures)
    });

    PyErr_SetObject(exception.get(), message.ptr());
    throw_error_already_set();
}

void function::add_overload(handle<function> const& overload_) {
    function* parent = this;
    
    while (parent->m_overloads)
        parent = parent->m_overloads.get();

    parent->m_overloads = overload_;

    // If we have no documentation, get the docs from the overload
    if (!m_doc)
        m_doc = overload_->m_doc;
}

namespace
{
  char const* const binary_operator_names[] =
  {
      "add__",
      "and__",
      "div__",
      "divmod__",
      "eq__",
      "floordiv__",
      "ge__",
      "gt__",
      "le__",
      "lshift__",
      "lt__",
      "mod__",
      "mul__",
      "ne__",
      "or__",
      "pow__",
      "radd__",
      "rand__",
      "rdiv__",
      "rdivmod__", 
      "rfloordiv__",
      "rlshift__",
      "rmod__",
      "rmul__",
      "ror__",
      "rpow__", 
      "rrshift__",
      "rshift__",
      "rsub__",
      "rtruediv__",
      "rxor__",
      "sub__",
      "truediv__", 
      "xor__"
  };

  inline bool is_binary_operator(char const* name) {
      return name[0] == '_' && name[1] == '_' && std::binary_search(
          std::begin(binary_operator_names), std::end(binary_operator_names),
          name + 2, [](char const* x, char const* y) {
              return std::strcmp(x, y) < 0;
          }
      );
  }

  // Something for the end of the chain of binary operators
  PyObject* not_implemented(PyObject*, PyObject*)
  {
      Py_INCREF(Py_NotImplemented);
      return Py_NotImplemented;
  }
  
  handle<function> not_implemented_function()
  {
      static object keeper(
          function_object(
              py_function(&not_implemented, detail::type_list<void>(), 2)
            , python::detail::keyword_range())
          );
      return handle<function>(borrowed(downcast<function>(keeper.ptr())));
  }
}

void function::add_to_namespace(object const& name_space, char const* name_,
                                object const& attribute, char const* doc)
{
    str const name(name_);
    PyObject* const ns = name_space.ptr();
    
    if (attribute.ptr()->ob_type == &function_type) {
        function* new_func = downcast<function>(attribute.ptr());
        handle<> dict;
        
#if PY_MAJOR_VERSION < 3 // Old-style class is gone in Python 3
        if (PyClass_Check(ns))
            dict = handle<>(borrowed(((PyClassObject*)ns)->cl_dict));
        else
#endif
        if (PyType_Check(ns))
            dict = handle<>(borrowed(((PyTypeObject*)ns)->tp_dict));
        else    
            dict = handle<>(PyObject_GetAttrString(ns, "__dict__"));

        if (!dict)
            throw_error_already_set();

        handle<> existing(allow_null(::PyObject_GetItem(dict.get(), name.ptr())));
        
        if (existing) {
            if (existing->ob_type == &function_type) {
                new_func->add_overload(
                    handle<function>(
                        borrowed(downcast<function>(existing.get()))
                    )
                );
            }
            else if (existing->ob_type == &PyStaticMethod_Type) {
                PyErr_Format(
                    PyExc_RuntimeError,
                    "Boost.Python - All overloads must be exported "
                    "before calling \'class_<...>(\"%s\").staticmethod(\"%s\")\'",
                    extract<char const*>{name_space.attr("__name__")}(),
                    name_
                );
                throw_error_already_set();
            }
        }
        else if (is_binary_operator(name_)) {
            // Binary operators need an additional overload which
            // returns NotImplemented, so that Python will try the
            // __rxxx__ functions on the other operand. We add this
            // when no overloads for the operator already exist.
            new_func->add_overload(not_implemented_function());
        }

        // A function is named the first time it is added to a namespace.
        if (new_func->name().is_none())
            new_func->m_name = name;

        handle<> name_space_name{
            allow_null(PyObject_GetAttrString(name_space.ptr(), "__name__"))
        };
        
        if (name_space_name)
            new_func->m_namespace = object(name_space_name);

        // signature options are set per function
        new_func->show_python_signature = docstring_options::show_py_signatures_;
        new_func->show_cpp_signature = docstring_options::show_cpp_signatures_;
    }

    // The PyObject_GetAttrString() or PyObject_GetItem calls above may
    // have left an active error
    PyErr_Clear();
    if (PyObject_SetAttr(ns, name.ptr(), attribute.ptr()) < 0)
        throw_error_already_set();

    if (doc && docstring_options::show_user_defined_) {
        object mutable_attribute(attribute);
        mutable_attribute.attr("__doc__") = str{doc};
    }
}

BOOST_PYTHON_DECL void add_to_namespace(object const& name_space, char const* name,
                                        object const& attribute, char const* doc)
{
    function::add_to_namespace(name_space, name, attribute, doc);
}


extern "C"
{
    // Stolen from Python's funcobject.c
#if PY_MAJOR_VERSION >= 3
    static PyObject* function_descr_get(PyObject *func, PyObject *obj, PyObject * /*type_*/) {
        // The implement is different in Python 3 because of the removal of unbound method
        if (obj == Py_None || obj == NULL) {
            Py_INCREF(func);
            return func;
        }
        return PyMethod_New(func, obj);
    }
#else
    static PyObject* function_descr_get(PyObject *func, PyObject *obj, PyObject *type_) {
        if (obj == Py_None)
            obj = nullptr;
        return PyMethod_New(func, obj, type_);
    }
#endif

    static void function_dealloc(PyObject* p) {
        delete static_cast<function*>(p);
    }

    static PyObject* function_call(PyObject* func, PyObject* args, PyObject* kw) {
        PyObject* result = nullptr;
        handle_exception([&]() {
            result = static_cast<function*>(func)->call(args, kw);
        });
        return result;
    }

    //
    // Here we're using the function's tp_getset rather than its
    // tp_members to set up __doc__ and __name__, because tp_members
    // really depends on having a POD object type (it relies on
    // offsets). It might make sense to reformulate function as a POD
    // at some point, but this is much more expedient.
    //
    static PyObject* function_get_doc(PyObject* op, void*) {
        list signatures = function_doc_signature_generator::function_doc_signatures(
            downcast<function>(op)
        );
        if (!signatures)
            return python::detail::none();

        signatures.reverse();
        return "\n"_s.join(signatures).release();
    }
    
    static int function_set_doc(PyObject* op, PyObject* doc, void*) {
        function* f = downcast<function>(op);
        f->doc(doc ? object(python::detail::borrowed_reference(doc)) : object());
        return 0;
    }
    
    static PyObject* function_get_name(PyObject* op, void*) {
        function* f = downcast<function>(op);
        if (f->name().is_none())
            return BOOST_PyString_PyString_InternFromString("<unnamed Boost.Python function>");
        else
            return python::incref(f->name().ptr());
    }

    // We add a dummy __class__ attribute in order to fool PyDoc into
    // treating these as built-in functions and scanning their
    // documentation
    static PyObject* function_get_class(PyObject* /*op*/, void*) {
        return python::incref(upcast<PyObject>(&PyCFunction_Type));
    }

    static PyObject* function_get_module(PyObject* op, void*) {
        object const& ns = downcast<function>(op)->get_namespace();
        if (!ns.is_none()) {
            return python::incref(ns.ptr());
        }

        PyErr_SetString(PyExc_AttributeError, "Boost.Python function __module__ unknown.");
        return nullptr;
    }
}

static PyGetSetDef function_getsetlist[] = {
    {const_cast<char*>("__name__"), (getter)function_get_name, 0, 0, 0 },
    {const_cast<char*>("func_name"), (getter)function_get_name, 0, 0, 0 },
    {const_cast<char*>("__module__"), (getter)function_get_module, 0, 0, 0 },
    {const_cast<char*>("func_module"), (getter)function_get_module, 0, 0, 0 },
    {const_cast<char*>("__class__"), (getter)function_get_class, 0, 0, 0 },    // see note above
    {const_cast<char*>("__doc__"), (getter)function_get_doc, (setter)function_set_doc, 0, 0},
    {const_cast<char*>("func_doc"), (getter)function_get_doc, (setter)function_set_doc, 0, 0},
    {NULL, 0, 0, 0, 0} /* Sentinel */
};

PyTypeObject function_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "Boost.Python.function",
    sizeof(function),
    0,
    (destructor)function_dealloc,               /* tp_dealloc */
    0,                                  /* tp_print */
    0,                                  /* tp_getattr */
    0,                                  /* tp_setattr */
    0,                                  /* tp_compare */
    0, //(reprfunc)func_repr,                   /* tp_repr */
    0,                                  /* tp_as_number */
    0,                                  /* tp_as_sequence */
    0,                                  /* tp_as_mapping */
    0,                                  /* tp_hash */
    function_call,                              /* tp_call */
    0,                                  /* tp_str */
    0, // PyObject_GenericGetAttr,            /* tp_getattro */
    0, // PyObject_GenericSetAttr,            /* tp_setattro */
    0,                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT /* | Py_TPFLAGS_HAVE_GC */,/* tp_flags */
    0,                                  /* tp_doc */
    0, // (traverseproc)func_traverse,          /* tp_traverse */
    0,                                  /* tp_clear */
    0,                                  /* tp_richcompare */
    0, //offsetof(PyFunctionObject, func_weakreflist), /* tp_weaklistoffset */
    0,                                  /* tp_iter */
    0,                                  /* tp_iternext */
    0,                                  /* tp_methods */
    0, // func_memberlist,              /* tp_members */
    function_getsetlist,                /* tp_getset */
    0,                                  /* tp_base */
    0,                                  /* tp_dict */
    function_descr_get,                 /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0, //offsetof(PyFunctionObject, func_dict),      /* tp_dictoffset */
    0,                                      /* tp_init */
    0,                                      /* tp_alloc */
    0,                                      /* tp_new */
    0,                                      /* tp_free */
    0,                                      /* tp_is_gc */
    0,                                      /* tp_bases */
    0,                                      /* tp_mro */
    0,                                      /* tp_cache */
    0,                                      /* tp_subclasses */
    0,                                      /* tp_weaklist */
    0,                                      /* tp_del */
    0,                                      /* tp_version_tag */
#if PY_MAJOR_VERSION >= 3 && PY_MINOR_VERSION >= 4
    0                                       /* tp_finalize */
#endif
};

object function_object(
    py_function f
    , python::detail::keyword_range const& keywords)
{
    return python::object(
        python::detail::new_non_null_reference(
            new function(
                std::move(f), keywords.first, static_cast<unsigned>(keywords.second - keywords.first))));
}

handle<> function_handle_impl(py_function f)
{
    return python::handle<>(
        allow_null(
            new function(std::move(f), 0, 0)));
}

} // namespace objects

namespace detail
{
  object BOOST_PYTHON_DECL make_raw_function(objects::py_function f)
  {
      static keyword k;
    
      return objects::function_object(
          std::move(f)
          , keyword_range(&k,&k));
  }
  void BOOST_PYTHON_DECL pure_virtual_called()
  {
      PyErr_SetString(
          PyExc_RuntimeError, const_cast<char*>("Pure virtual function called"));
      throw_error_already_set();
  }
}

}} // namespace boost::python
