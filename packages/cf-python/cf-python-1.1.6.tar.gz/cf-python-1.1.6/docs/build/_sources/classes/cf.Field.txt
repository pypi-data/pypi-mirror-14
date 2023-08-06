.. currentmodule:: cf
.. default-role:: obj

cf.Field
========

.. autoclass:: cf.Field
   :no-members:
   :no-inherited-members:

.. _field_cf_properties:

CF Properties
-------------
 
.. autosummary::
   :toctree: ../generated/
   :template: attribute.rst

   ~cf.Field.add_offset
   ~cf.Field.calendar
   ~cf.Field.cell_methods
   ~cf.Field.comment
   ~cf.Field.Conventions
   ~cf.Field._FillValue
   ~cf.Field.flag_masks
   ~cf.Field.flag_meanings
   ~cf.Field.flag_values
   ~cf.Field.history
   ~cf.Field.institution
   ~cf.Field.leap_month
   ~cf.Field.leap_year
   ~cf.Field.long_name
   ~cf.Field.missing_value
   ~cf.Field.month_lengths
   ~cf.Field.references
   ~cf.Field.scale_factor
   ~cf.Field.source
   ~cf.Field.standard_error_multiplier
   ~cf.Field.standard_name
   ~cf.Field.title
   ~cf.Field.units
   ~cf.Field.valid_max
   ~cf.Field.valid_min
   ~cf.Field.valid_range

Setting, retrieving and deleting non-standard (and reserved) CF
properties.

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.delprop
   ~cf.Field.getprop
   ~cf.Field.hasprop
   ~cf.Field.properties
   ~cf.Field.setprop

.. _field_methods:

Domain operations
-----------------

.. rubric:: Domain object

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: attribute.rst

   ~cf.Field.domain

.. rubric:: Domain axes

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.autocyclic
   ~cf.Field.axes
   ~cf.Field.axes_sizes
   ~cf.Field.axis
   ~cf.Field.axis_name
   ~cf.Field.axis_size
   ~cf.Field.cyclic
   ~cf.Field.data_axes
   ~cf.Field.insert_axis
   ~cf.Field.iscyclic 
   ~cf.Field.item_axes
   ~cf.Field.items_axes
   ~cf.Field.period
   ~cf.Field.remove_axes
   ~cf.Field.remove_axis

.. rubric:: Domain items

A domain item is a dimension coordinate, auxiliary coordinate, cell
measure or coordinate reference object.
   
.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.aux
   ~cf.Field.auxs
   ~cf.Field.coord
   ~cf.Field.coords
   ~cf.Field.dim
   ~cf.Field.dims 
   ~cf.Field.insert_aux
   ~cf.Field.insert_dim
   ~cf.Field.insert_measure
   ~cf.Field.insert_ref
   ~cf.Field.item
   ~cf.Field.items
   ~cf.Field.measure
   ~cf.Field.measures
   ~cf.Field.ref
   ~cf.Field.refs
   ~cf.Field.remove_item
   ~cf.Field.remove_items

Subspacing
----------

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.indices
   ~cf.Field.subspace

Mathematical functions
----------------------

.. http://docs.scipy.org/doc/numpy/reference/routines.math.html

.. rubric:: Trigonometry

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.cos
   ~cf.Field.sin
   ~cf.Field.tan

.. rubric:: Exponents and logarithms

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.exp
   ~cf.Field.log


.. rubric:: Rounding

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.ceil  
   ~cf.Field.floor
   ~cf.Field.rint
   ~cf.Field.trunc

.. rubric:: Statistics

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.collapse
   ~cf.Field.max
   ~cf.Field.mean
   ~cf.Field.mid_range
   ~cf.Field.min
   ~cf.Field.range
   ~cf.Field.sample_size
   ~cf.Field.sum  
   ~cf.Field.sd
   ~cf.Field.var
   ~cf.Field.weights

.. http://docs.scipy.org/doc/numpy/reference/routines.statistics.html

.. rubric:: Miscellaneous mathematical functions

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.clip

Data array operations
---------------------

.. http://docs.scipy.org/doc/numpy/reference/routines.array-manipulation.html

.. _field_data_array_access:


.. rubric:: Data array access

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: attribute.rst

   ~cf.Field.array
   ~cf.Field.data
   ~cf.Field.datum
   ~cf.Field.dtype
   ~cf.Field.hasdata
   ~cf.Field.ndim
   ~cf.Field.shape
   ~cf.Field.size
   ~cf.Field.varray


.. rubric:: Data array units

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: attribute.rst

   ~cf.Field.calendar
   ~cf.Field.units
   ~cf.Field.Units

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.override_units
   ~cf.Field.override_calendar

.. rubric:: Data array mask

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: attribute.rst

   ~cf.Field.binary_mask
   ~cf.Field.hardmask
   ~cf.Field.mask

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.fill_value
 
.. rubric:: Order and number of dimensions

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.expand_dims
   ~cf.Field.squeeze
   ~cf.Field.transpose
   ~cf.Field.unsqueeze

.. rubric:: Changing data array values

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.indices
   ~cf.Field.mask_invalid
   ~cf.Field.subspace
   ~cf.Field.where

.. rubric:: Adding and removing elements

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.unique

.. rubric:: Rearranging elements

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.anchor
   ~cf.Field.flip
   ~cf.Field.roll

.. rubric:: Miscellaneous data array operations

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: attribute.rst

   ~cf.Field.chunk
   ~cf.Field.insert_data
   ~cf.Field.isscalar
   ~cf.Field.remove_data

Regridding operations
---------------------

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.regrids

Date-time operations
--------------------
 
.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.asdatetime
   ~cf.Field.asreftime

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: attribute.rst

   ~cf.Field.day
   ~cf.Field.dtarray
   ~cf.Field.dtvarray
   ~cf.Field.hour
   ~cf.Field.minute
   ~cf.Field.month
   ~cf.Field.second
   ~cf.Field.year

Logic functions
---------------

.. http://docs.scipy.org/doc/numpy/reference/routines.logic.html#truth-value-testing

.. rubric:: Truth value testing

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.all
   ~cf.Field.any
 
.. rubric:: Comparison

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.allclose
   ~cf.Field.equals
   ~cf.Field.equivalent
   ~cf.Field.equivalent_data
   ~cf.Field.equivalent_domain

.. rubric:: Set operations

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.unique


Miscellaneous
-------------

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.close
   cf.Field.concatenate
   ~cf.Field.copy 
   ~cf.Field.dump
   ~cf.Field.field
   ~cf.Field.identity
   ~cf.Field.match
   ~cf.Field.name
   ~cf.Field.select

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: attribute.rst

   ~cf.Field.attributes
   ~cf.Field.Flags
   ~cf.Field.hasbounds
   ~cf.Field.isauxiliary
   ~cf.Field.isdimension
   ~cf.Field.ismeasure
   ~cf.Field.rank
   ~cf.Field.T
   ~cf.Field.X
   ~cf.Field.Y
   ~cf.Field.Z

List-like operations
--------------------

These methods view the field as a single element :ref:`field list
<fieldlist>`, e.g. ``f.count(g)`` is equivalent to
``cf.FieldList(f).count(g)``.

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.Field.count
   ~cf.Field.index
   ~cf.Field.reverse
   ~cf.Field.sort
   ~cf.Field.__contains__
   ~cf.Field.__getitem__ 
   ~cf.Field.__len__

Arithmetic and comparison operations
------------------------------------

Arithmetic, bitwise and comparison operations are defined on a field
as element-wise operations on its data array which yield a new
`cf.Field` object or, for augmented assignments, modify the field's
data array in-place.


.. rubric:: Comparison operators

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.Field.__lt__
   ~cf.Field.__le__
   ~cf.Field.__eq__
   ~cf.Field.__ne__
   ~cf.Field.__gt__
   ~cf.Field.__ge__

.. rubric:: Binary arithmetic operators

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.Field.__add__     
   ~cf.Field.__sub__     
   ~cf.Field.__mul__     
   ~cf.Field.__div__     
   ~cf.Field.__truediv__ 
   ~cf.Field.__floordiv__
   ~cf.Field.__pow__     
   ~cf.Field.__mod__     

.. rubric:: Binary arithmetic operators with reflected (swapped) operands

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.Field.__radd__     
   ~cf.Field.__rsub__     
   ~cf.Field.__rmul__     
   ~cf.Field.__rdiv__     
   ~cf.Field.__rtruediv__ 
   ~cf.Field.__rfloordiv__
   ~cf.Field.__rpow__   
   ~cf.Field.__rmod__   

.. rubric:: Augmented arithmetic assignments

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.Field.__iadd__ 
   ~cf.Field.__isub__ 
   ~cf.Field.__imul__ 
   ~cf.Field.__idiv__ 
   ~cf.Field.__itruediv__
   ~cf.Field.__ifloordiv__
   ~cf.Field.__ipow__ 
   ~cf.Field.__imod__ 

.. rubric:: Unary arithmetic operators

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.Field.__neg__    
   ~cf.Field.__pos__    
   ~cf.Field.__abs__    

.. rubric:: Binary bitwise operators

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.Field.__and__     
   ~cf.Field.__or__
   ~cf.Field.__xor__     
   ~cf.Field.__lshift__
   ~cf.Field.__rshift__     

.. rubric:: Binary bitwise operators with reflected (swapped) operands

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.Field.__rand__     
   ~cf.Field.__ror__
   ~cf.Field.__rxor__     
   ~cf.Field.__rlshift__
   ~cf.Field.__rrshift__     

.. rubric:: Augmented bitwise assignments

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.Field.__iand__     
   ~cf.Field.__ior__
   ~cf.Field.__ixor__     
   ~cf.Field.__ilshift__
   ~cf.Field.__irshift__     

.. rubric:: Unary bitwise operators

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.Field.__invert__ 
 
Special methods
---------------

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.Field.__deepcopy__
   ~cf.Field.__repr__
   ~cf.Field.__str__
