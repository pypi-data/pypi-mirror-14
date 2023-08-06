.. currentmodule:: cf
.. default-role:: obj

.. _fs_field_list:

Introduction to the `cf.FieldList` object
=========================================

A `cf.FieldList` object is an ordered sequence of `cf.Field` objects.

It supports nearly all of the :ref:`python list-like operations
<python:typesseq-mutable>`, the exceptions being the arithmetic and
comparison operators for which it has :ref:`its own definitions
<fs-fl-a-and-c>`. For example:

>>> fl
[<CF Field: x_wind(grid_latitude(110), grid_longitude(106)) m s-1>,
 <CF Field: air_temperature(time(12), latitude(73), longitude(96)) K>]
>>> fl[0]
<CF Field: air_temperature(time(12), latitude(73), longitude(96)) K>
>>> fl[::-1] 
[<CF Field: air_temperature(time(12), latitude(73), longitude(96)) K>,
 <CF Field: x_wind(grid_latitude(110), grid_longitude(106)) m s-1>]
>>> fl[slice(1, -1, 2)]
[<CF Field: x_wind(grid_latitude(110), grid_longitude(106)) m s-1>]

Note that an integer index returns an individual field, but other
types of index always return a field list.

>>> len(fl)
2
>>> f = fl.pop()
>>> f
<CF Field: air_temperature(time(12), latitude(73), longitude(96)) K>
>>> len(fl)
1
>>> fl.append(f)
>>> len(fl)
2
>>> f in fl
True
>>> from operator import attrgetter
>>> fl
[<CF Field: x_wind(grid_latitude(110), grid_longitude(106)) m s-1>,
 <CF Field: air_temperature(time(12), latitude(73), longitude(96)) K>]
>>> fl.sort(key=attrgetter('standard_name'))
[<CF Field: air_temperature(time(12), latitude(73), longitude(96)) K>,
 <CF Field: x_wind(grid_latitude(110), grid_longitude(106)) m s-1>]


Field list methods
^^^^^^^^^^^^^^^^^^

A subset of a field's callable methods are also available to a field
list object (see the list of :ref:`field list methods
<fieldlist_methods>`). In general, these are methods which, on a
field, return a field or `None`. On a field list the same methods
return a field list or `None` respectively:


>>> gl = fl.max()
>>> fl.max(i=True)

is exactly equivalent to

>>> gl = cf.FieldList([f.max() for f in fl])
>>> for f in fl:
...     f.max(i=True)

The `~cf.FieldList.subspace` attribute .....

>>> fl
[<CF Field: air_temperature(time(12), latitude(73), longitude(96)) K>,
 <CF Field: air_pressure(time(12), latitude(73), longitude(96)) hPa>]
>>> fl.subspace[0]
[<CF Field: air_temperature(time(1), latitude(73), longitude(96)) K>,
 <CF Field: air_pressure(time(1), latitude(73), longitude(96)) hPa>]
>>> fl.subspace(latitude=0)
[<CF Field: air_temperature(time(12), latitude(1), longitude(96)) K>,
 <CF Field: air_pressure(time(12), latitude(1), longitude(96)) hPa>]

For cases for which there is no field list method to apply changes to
each field element, fields must be updated individually; For example:
list are easily carried out in a loop:

>>> fl[-1].standard_name = 'y_wind'
>>> for f in fl:
...     f.long_name = 'An even longer ' + f.long_name

.. _fs-fl-a-and-c:

Arithmetic and comparison
^^^^^^^^^^^^^^^^^^^^^^^^^

Any arithmetic and comparison operation is applied independently to
each field element, so all of the :ref:`operators defined for a field
<Arithmetic-and-comparison>` are allowed.

In particular, the usual :ref:`python list-like arithmetic and
comparison operator behaviours <python:numeric-types>` do **not**
apply. For example, the ``+`` operator will concatenate two built-in
lists, but adding ``2`` to a field list will add ``2`` to the data
array of each of its fields.

For example these commands:

>>> gl = fl + 2
>>> gl = 2 // fl
>>> gl = fl == 0
>>> fl += 2

are exactly equivalent to:

>>> gl = cf.FieldList(f + 2 for f in fl)
>>> gl = cf.FieldList(2 // f for f in fl)
>>> gl = cf.FieldList(f == 0 for f in fl)
>>> for f in fl:
...     f += 2

Field versus field list
^^^^^^^^^^^^^^^^^^^^^^^

In some contexts, whether an object is a field or a field list is not
known. So to avoid awkward type testing, some aspects of the
`cf.FieldList` interface are shared by a `cf.Field` object and vice
versa.

A field may be used in the same iterative contexts as a field list:

>>> f
<CF Field: air_temperature(time(12), latitude(73), longitude(96)) K>
>>> f is f[0] is f[slice(-1, None, -1)] is f[::-1]
True
>>> for g in f:
...     print repr(g)
...
<CF Field: air_temperature(time(12), latitude(73), longitude(96)) K>

Field methods which 
