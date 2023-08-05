// Copyright David Abrahams 2003.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef PURE_VIRTUAL_DWA2003810_HPP
# define PURE_VIRTUAL_DWA2003810_HPP

# include <boost/python/def_visitor.hpp>
# include <boost/python/default_call_policies.hpp>

# include <boost/python/detail/nullary_function_adaptor.hpp>

namespace boost { namespace python { 

namespace detail
{
  //
  // @group Helpers for pure_virtual_visitor. {
  //
  
  // Raises a Python RuntimeError reporting that a pure virtual
  // function was called.
  void BOOST_PYTHON_DECL pure_virtual_called();

  // Replace the two front elements of Sig with T1 and T2
  template <class Sig, class T1, class T2> struct replace_front2;

  template <class T1, class T2, class A1, class A2, class... Args>
  struct replace_front2<type_list<A1, A2, Args...>, T1, T2> {
      using type = type_list<T1, T2, Args...>;
  };
    
  template <class Sig, class T1, class T2>
  using replace_front2_t = typename replace_front2<Sig, T1, T2>::type;

  // Given F representing a member function [object], returns a type_list
  // whose return type is replaced by void, and whose first argument is
  // replaced by C&.
  template<class F, class C>
  using error_signature = replace_front2_t<get_signature_t<F>, void, C&>;

  //
  // } 
  //

  //
  // A def_visitor which defines a method as usual, then adds a
  // corresponding function which raises a "pure virtual called"
  // exception unless it's been overridden.
  //
  template <class PointerToMemberFunction>
  struct pure_virtual_visitor
    : def_visitor<pure_virtual_visitor<PointerToMemberFunction> >
  {
      pure_virtual_visitor(PointerToMemberFunction pmf)
        : m_pmf(pmf)
      {}
      
   private:
      friend class python::def_visitor_access;
      
      template <class C_, class Options>
      void visit(C_& c, char const* name, Options& options) const
      {
          // This should probably be a nicer error message
          static_assert(!Options::has_default_implementation, "");

          // Add the virtual function dispatcher
          c.def(
              name
            , m_pmf
            , options.doc()
            , options.keywords()
            , options.policies()
          );

          typedef typename C_::metadata::held_type held_type;
          
          // Add the default implementation which raises the exception
          c.def(
              name
            , make_function(
                  detail::nullary_function_adaptor<void(*)()>(pure_virtual_called)
                , default_call_policies()
                , detail::error_signature<PointerToMemberFunction, held_type>{}
              )
          );
      }
      
   private: // data members
      PointerToMemberFunction m_pmf;
  };
}

//
// Passed a pointer to member function, generates a def_visitor which
// creates a method that only dispatches to Python if the function has
// been overridden, either in C++ or in Python, raising a "pure
// virtual called" exception otherwise.
//
template <class PointerToMemberFunction>
detail::pure_virtual_visitor<PointerToMemberFunction>
pure_virtual(PointerToMemberFunction pmf)
{
    return detail::pure_virtual_visitor<PointerToMemberFunction>(pmf);
}

}} // namespace boost::python

#endif // PURE_VIRTUAL_DWA2003810_HPP
