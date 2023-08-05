// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef NUMARRAY_DWA2002922_HPP
# define NUMARRAY_DWA2002922_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/tuple.hpp>
# include <boost/python/str.hpp>

namespace boost { namespace python { namespace numeric {

class array;
BOOST_PYTHON_DECL object demand_array_function();

namespace aux
{
  struct BOOST_PYTHON_DECL array_base : object
  {
      template<class... Objects>
      array_base(Objects const&... xs)
          : object(demand_array_function()(xs...))
      {}

      object argmax(long axis=-1);
      object argmin(long axis=-1);
      object argsort(long axis=-1);
      object astype(object const& type = object());
      void byteswap();
      object copy() const;
      object diagonal(long offset = 0, long axis1 = 0, long axis2 = 1) const;
      void info() const;
      bool is_c_array() const;
      bool isbyteswapped() const;
      array new_(object type) const;
      void sort();
      object trace(long offset = 0, long axis1 = 0, long axis2 = 1) const;
      object type() const;
      char typecode() const;

      object factory(
          object const& sequence = object()
        , object const& typecode = object()
        , bool copy = true
        , bool savespace = false
        , object type = object()
        , object shape = object());

      object getflat() const;
      long getrank() const;
      object getshape() const;
      bool isaligned() const;
      bool iscontiguous() const;
      long itemsize() const;
      long nelements() const;
      object nonzero() const;
   
      void put(object const& indices, object const& values);
   
      void ravel();
   
      object repeat(object const& repeats, long axis=0);
   
      void resize(object const& shape);
      
      void setflat(object const& flat);
      void setshape(object const& shape);
   
      void swapaxes(long axis1, long axis2);
   
      object take(object const& sequence, long axis = 0) const;
   
      void tofile(object const& file) const;
   
      str tostring() const;
   
      void transpose(object const& axes = object());
   
      object view() const;

   public: // implementation detail - do not touch.
      BOOST_PYTHON_FORWARD_OBJECT_CONSTRUCTORS(array_base, object);
  };

  struct BOOST_PYTHON_DECL array_object_manager_traits
  {
      static bool check(PyObject* obj);
      static detail::new_non_null_reference adopt(PyObject* obj);
  };
} // namespace aux

class array : public aux::array_base
{
    typedef aux::array_base base;
 public:

    object astype() { return base::astype(); }
    
    template <class Type>
    object astype(Type const& type_)
    {
        return base::astype(object(type_));
    }

    template <class Type>
    array new_(Type const& type_) const
    {
        return base::new_(object(type_));
    }

    template <class Sequence>
    void resize(Sequence const& x)
    {
        base::resize(object(x));
    }
    
    template<typename... Ls>
    void resize(Ls... xs)
    {
        resize(make_tuple(long(xs)...));
    }

    template <class Sequence>
    void setshape(Sequence const& x)
    {
        base::setshape(object(x));
    }
    
    template<typename... Ls>
    void setshape(Ls... xs)
    {
        setshape(make_tuple(long(xs)...));
    }

    template <class Indices, class Values>
    void put(Indices const& indices, Values const& values)
    {
        base::put(object(indices), object(values));
    }
    
    template <class Sequence>
    object take(Sequence const& sequence, long axis = 0)
    {
        return base::take(object(sequence), axis);
    }

    template <class File>
    void tofile(File const& f) const
    {
        base::tofile(object(f));
    }

    object factory()
    {
        return base::factory();
    }
    
    template <class Sequence>
    object factory(Sequence const& sequence)
    {
        return base::factory(object(sequence));
    }
    
    template <class Sequence, class Typecode>
    object factory(
        Sequence const& sequence
      , Typecode const& typecode_
      , bool copy = true
      , bool savespace = false
    )
    {
        return base::factory(object(sequence), object(typecode_), copy, savespace);
    }

    template <class Sequence, class Typecode, class Type>
    object factory(
        Sequence const& sequence
      , Typecode const& typecode_
      , bool copy
      , bool savespace
      , Type const& type
    )
    {
        return base::factory(object(sequence), object(typecode_), copy, savespace, object(type));
    }
    
    template <class Sequence, class Typecode, class Type, class Shape>
    object factory(
        Sequence const& sequence
      , Typecode const& typecode_
      , bool copy
      , bool savespace
      , Type const& type
      , Shape const& shape
    )
    {
        return base::factory(object(sequence), object(typecode_), copy, savespace, object(type), object(shape));
    }
    
    template<class... Ts>
    explicit array(Ts const&... xs)
        : base(object(xs)...)
    {}

    static BOOST_PYTHON_DECL void set_module_and_type(char const* package_name = 0, char const* type_attribute_name = 0);
    static BOOST_PYTHON_DECL std::string get_module_name();

 public: // implementation detail -- for internal use only
    BOOST_PYTHON_FORWARD_OBJECT_CONSTRUCTORS(array, base);
};

} // namespace boost::python::numeric

namespace converter
{
  template <>
  struct object_manager_traits< numeric::array >
      : numeric::aux::array_object_manager_traits
  {
      static constexpr bool is_specialized = true;
  };
}

}} // namespace boost::python

#endif // NUMARRAY_DWA2002922_HPP
