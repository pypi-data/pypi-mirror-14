// Copyright David Abrahams 2003.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef DEF_VISITOR_DWA2003810_HPP
# define DEF_VISITOR_DWA2003810_HPP

# include <boost/python/detail/prefix.hpp>

namespace boost { namespace python {

template <class DerivedVisitor> class def_visitor;
template<class W, class... Args> class class_;

class def_visitor_access
{
    template <class Derived> friend class def_visitor;
    
    // unnamed visit, c.f. init<...>, container suites
    template <class V, class classT>
    static void visit(V const& v, classT& c)
    {
        v.derived_visitor().visit(c);
    }

    // named visit, c.f. object, pure_virtual
    template <class V, class classT, class OptionalArgs>
    static void visit(
        V const& v
      , classT& c
      , char const* name
      , OptionalArgs const& options
    ) 
    {
        v.derived_visitor().visit(c, name, options);
    }
    
};


template <class DerivedVisitor>
class def_visitor
{
    friend class def_visitor_access;
    template<class W, class... Args> friend class class_;

    // unnamed visit, c.f. init<...>, container suites
    template <class classT>
    void visit(classT& c) const
    {
        def_visitor_access::visit(*this, c);
    }

    // named visit, c.f. object, pure_virtual
    template <class classT, class OptionalArgs>
    void visit(classT& c, char const* name, OptionalArgs const& options) const
    {
        def_visitor_access::visit(*this, c, name, options);
    }
    
 protected:
    DerivedVisitor const& derived_visitor() const
    {
        return static_cast<DerivedVisitor const&>(*this);
    }
};

}} // namespace boost::python

#endif // DEF_VISITOR_DWA2003810_HPP
