///////////////////////////////////////////////////////////////////////////////
//
// Copyright David Abrahams 2002, Joel de Guzman, 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//
///////////////////////////////////////////////////////////////////////////////
#ifndef INIT_JDG20020820_HPP
# define INIT_JDG20020820_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/args_fwd.hpp>
# include <boost/python/def_visitor.hpp>

# include <boost/python/detail/type_list.hpp>
# include <boost/python/detail/type_list_utils.hpp>
# include <boost/python/detail/make_keyword_range_fn.hpp>

namespace boost { namespace python {

template<class... Ts>
class init; // forward declaration

template<class... Ts>
using optional = detail::type_list<Ts...>;

namespace detail {
  template <int NDefaults>
  struct define_class_init_helper;
}

template<class Derived>
struct init_base : def_visitor<Derived> {
    init_base(char const* docstring, detail::keyword_range const& keywords)
        : m_doc(docstring), m_keywords(keywords)
    {}

    init_base(char const* docstring)
        : m_doc(docstring)
    {}

    Derived const& derived() const {
        return *static_cast<Derived const*>(this);
    }
    
    char const* doc_string() const { return m_doc; }

    detail::keyword_range const& keywords() const { return m_keywords; }

    static default_call_policies call_policies() { return {}; }

private:
    //  visit
    //
    //      Defines a set of n_defaults + 1 constructors for its
    //      class_<...> argument. Each constructor after the first has
    //      one less argument to its right.
    //      Example:
    //          init<int, optional<char, long, double> >
    //      Defines:
    //          __init__(int, char, long, double)
    //          __init__(int, char, long)
    //          __init__(int, char)
    //          __init__(int)
    template<class Class>
    void visit(Class& cl) const {
        using signature = typename Derived::signature;
        using n_defaults = typename Derived::n_defaults;

        detail::define_class_init_helper<n_defaults::value>::template apply<signature>(
            cl
          , derived().call_policies()
          , derived().doc_string()
          , derived().keywords());
    }
    
    friend class python::def_visitor_access;
    
private:
    char const* m_doc;
    detail::keyword_range m_keywords;
};

template<class CallPolicies, class Init>
class init_with_call_policies : public init_base<init_with_call_policies<CallPolicies, Init>> {
    using base = init_base<init_with_call_policies<CallPolicies, Init>>;

public:
    using n_arguments = typename Init::n_arguments;
    using n_defaults = typename Init::n_defaults;
    using signature = typename Init::signature;

    init_with_call_policies(CallPolicies const& cp, char const* docstring,
                            detail::keyword_range const& keywords)
        : base(docstring, keywords), m_policies(cp)
    {}

    CallPolicies const& call_policies() const { return m_policies; }
    
private:
    CallPolicies m_policies;
};


template<class... Ts>
class init : public init_base<init<Ts...>> {
    using base = init_base<init<Ts...>>;
public:
    using self_t = init<Ts...>;

    init(char const* docstring = nullptr) : base{docstring} {}

    template <std::size_t N>
    init(detail::keywords<N> const& kw, char const* docstring = nullptr)
        : base{docstring, kw.range()}
    {
        static_assert(N <= n_arguments::value + 1, "More keywords than init arguments.");
    }

    template<std::size_t N>
    init(char const* docstring, detail::keywords<N> const& kw) : init{kw, docstring} {}

    template<class CallPolicies>
    init_with_call_policies<CallPolicies, self_t>
    operator[](CallPolicies const& policies) const {
        return {policies, this->doc_string(), this->keywords()};
    }

    using signature_ = detail::type_list<Ts...>;
    using back = detail::tl::back_t<signature_>;
    using back_is_optional = detail::is_<detail::type_list, back>;
    
    using optional_args = cpp14::conditional_t<
        back_is_optional::value,
        back,
        detail::type_list<>
    >;

    using signature = cpp14::conditional_t<
        !back_is_optional::value,
        signature_,
        detail::tl::concat_t<
            detail::tl::drop_t<signature_, 1>,
            optional_args
        >
    >;

    // TODO: static assert to make sure there are no other optional elements

    // Count the number of default args
    using n_defaults = std::integral_constant<std::size_t, optional_args::size>;
    using n_arguments = std::integral_constant<std::size_t, signature::size>;
};

namespace detail
{
  template<class Signature, class Class, class CallPolicies>
  inline void def_init_aux(Class& cl, CallPolicies const& cp, char const* docstring,
                           detail::keyword_range const& kw)
  {
      cl.def(
          "__init__",
          make_keyword_range_constructor<Signature, typename Class::metadata::holder>(cp, kw),
          docstring
      );
  }

  ///////////////////////////////////////////////////////////////////////////////
  //
  //  define_class_init_helper<N>::apply
  //
  //      General case
  //
  //      Accepts a class_ and an arguments list. Defines a constructor
  //      for the class given the arguments and recursively calls
  //      define_class_init_helper<N-1>::apply with one fewer argument (the
  //      rightmost argument is shaved off)
  //
  ///////////////////////////////////////////////////////////////////////////////
  template <int NDefaults>
  struct define_class_init_helper {
      template<class Signature, class Class, class CallPolicies>
      static void apply(Class& cl, CallPolicies const& cp, char const* docstring,
                        detail::keyword_range kw)
      {
          def_init_aux<Signature>(cl, cp, docstring, kw);

          if (kw.second > kw.first)
              --kw.second;

          using sig = tl::drop_t<Signature, 1>;
          define_class_init_helper<NDefaults-1>::template apply<sig>(cl, cp, docstring, kw);
      }
  };

  ///////////////////////////////////////////////////////////////////////////////
  //
  //  define_class_init_helper<0>::apply
  //
  //      Terminal case
  //
  //      Accepts a class_ and an arguments list. Defines a constructor
  //      for the class given the arguments.
  //
  ///////////////////////////////////////////////////////////////////////////////
  template <>
  struct define_class_init_helper<0> {
      template<class Signature, class Class, class CallPolicies>
      static void apply(Class& cl, CallPolicies const& cp, char const* docstring,
                        detail::keyword_range const& kw)
      {
          detail::def_init_aux<Signature>(cl, cp, docstring, kw);
      }
  };
}

}} // namespace boost::python

#endif // INIT_JDG20020820_HPP
