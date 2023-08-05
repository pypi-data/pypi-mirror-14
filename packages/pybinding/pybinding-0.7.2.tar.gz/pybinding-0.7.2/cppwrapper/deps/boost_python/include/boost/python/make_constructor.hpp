// Copyright David Abrahams 2001.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef MAKE_CONSTRUCTOR_DWA20011221_HPP
# define MAKE_CONSTRUCTOR_DWA20011221_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/default_call_policies.hpp>
# include <boost/python/args.hpp>
# include <boost/python/object_fwd.hpp>

# include <boost/python/object/function_object.hpp>
# include <boost/python/object/pointer_holder.hpp>
# include <boost/python/converter/context_result_converter.hpp>

# include <boost/python/detail/caller.hpp>
# include <boost/python/detail/none.hpp>

namespace boost { namespace python {

namespace detail
{
  template <class T>
  struct install_holder : converter::context_result_converter
  {
      install_holder(PyObject* args_)
        : m_self(PyTuple_GetItem(args_, 0)) {}

      PyObject* operator()(T x) const
      {
          dispatch(x, std::is_pointer<T>());
          return none();
      }

   private:
      template <class U>
      void dispatch(U* x, std::true_type) const
      {
          std::auto_ptr<U> owner(x);
          dispatch(owner, std::false_type());
      }
      
      template <class Ptr>
      void dispatch(Ptr x, std::false_type) const
      {
          typedef typename pointee<Ptr>::type value_type;
          typedef objects::pointer_holder<Ptr,value_type> holder;
          typedef objects::instance<holder> instance_t;

          void* memory = holder::allocate(this->m_self, offsetof(instance_t, storage), sizeof(holder));
          try {
              (new (memory) holder(x))->install(this->m_self);
          }
          catch(...) {
              holder::deallocate(this->m_self, memory);
              throw;
          }
      }
      
      PyObject* m_self;
  };
  
  struct constructor_result_converter {
      template<class T>
      struct apply {
          using type = install_holder<T>;
      };
  };

  template<class BasePolicy = default_call_policies>
  struct constructor_policy : BasePolicy {
      constructor_policy(BasePolicy base) : BasePolicy(base) {}
      
      // If the BasePolicy supplied a result converter it would be
      // ignored; issue an error if it's not the default.
      static_assert(std::is_same<typename BasePolicy::result_converter,
                                 default_result_converter>::value, 
                    "make_constructor supplies its own result converter that would override yours");
      
      using result_converter = constructor_result_converter;
      using argument_package = offset_args<1>;
  };

  template <class InnerSignature> struct outer_constructor_signature;

  template <class A0, class... Args>
  struct outer_constructor_signature<type_list<A0, Args...>> {
      using type = type_list<void, object, Args...>;
  };

  template <class Sig>
  using outer_constructor_signature_t = typename outer_constructor_signature<Sig>::type;
  
  // These helper functions for make_constructor (below) do the raw work
  // of constructing a Python object from some invokable entity. See
  // <boost/python/detail/caller.hpp> for more information about how
  // the Signature arguments is used.
  template<class Signature, class Function, class CallPolicies>
  object make_constructor_aux(Function f, CallPolicies const& cp) {
      return objects::function_object(
          objects::py_function{
              detail::caller<Function, constructor_policy<CallPolicies>, Signature>{f, cp},
              outer_constructor_signature_t<Signature>{}
          }
      );
  }
  
  // As above, except that it accepts argument keywords. NumKeywords
  // is used only for a compile-time assertion to make sure the user
  // doesn't pass more keywords than the function can accept. To
  // disable all checking, pass 0 for NumKeywords.
  template<class Signature, int NumKeywords, class Function, class CallPolicies>
  object make_constructor_aux(Function f, CallPolicies const& cp, detail::keyword_range const& kw) {
      static_assert(NumKeywords <= Signature::size, "More keywords than function arguments");
      
      return objects::function_object(
          objects::py_function{
              detail::caller<Function, constructor_policy<CallPolicies>, Signature>{f, cp},
              outer_constructor_signature_t<Signature>{}
          },
          kw
      );
  }

  //   These dispatch functions are used to discriminate between the
  //   cases when the 3rd argument is keywords or when it is a
  //   signature.
  template<class Function, class CallPolicies, class Keywords>
  object make_constructor_dispatch(Function f, CallPolicies const& cp, Keywords const& kw,
                                   std::true_type)
  {
      return detail::make_constructor_aux<
          detail::get_signature_t<Function>, Keywords::size
      >(
          f, cp, kw.range()
      );
  }

  template<class Function, class CallPolicies, class Signature>
  object make_constructor_dispatch(Function f, CallPolicies const& cp, Signature const&,
                                   std::false_type)
  {
      return detail::make_constructor_aux<Signature>(f, cp);
  }
}

//   These overloaded functions wrap a function or member function
//   pointer as a Python object, using optional CallPolicies,
//   Keywords, and/or Signature.
template<class Function>
object make_constructor(Function f) {
    return detail::make_constructor_aux<detail::get_signature_t<Function>>(
        f, default_call_policies{}
    );
}

template<class Function, class CallPolicies>
object make_constructor(Function f, CallPolicies const& cp) {
    return detail::make_constructor_aux<detail::get_signature_t<Function>>(f, cp);
}

template<class Function, class CallPolicies, class KeywordsOrSignature>
object make_constructor(Function f, CallPolicies const& cp, KeywordsOrSignature const& kw_or_sig) {
    return detail::make_constructor_dispatch(
        f, cp, kw_or_sig, detail::is_keywords<KeywordsOrSignature>{}
    );
}

template<class Function, class CallPolicies, class Keywords, class Signature>
object make_constructor(Function f, CallPolicies const& cp, Keywords const& kw, Signature const&) {
    return detail::make_constructor_aux<Signature, Keywords::size>(f, cp, kw.range());
}

}}

#endif // MAKE_CONSTRUCTOR_DWA20011221_HPP
