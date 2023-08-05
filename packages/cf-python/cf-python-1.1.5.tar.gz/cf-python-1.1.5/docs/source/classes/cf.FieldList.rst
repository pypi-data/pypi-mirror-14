.. currentmodule:: cf
.. default-role:: obj

.. _fieldlist:

cf.FieldList
============

.. autoclass:: cf.FieldList
   :no-members:
   :no-inherited-members:

.. _fieldlist_methods:

Domain operations
-----------------

**Domain axes**

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.FieldList.autocyclic

Subspacing
----------

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.FieldList.subspace

Mathematical functions
----------------------

**Trigonometry**

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.FieldList.cos
   ~cf.FieldList.sin
   ~cf.FieldList.tan

**Exponents and logarithms**

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.FieldList.exp
   ~cf.FieldList.log


**Rounding**

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.FieldList.ceil  
   ~cf.FieldList.floor
   ~cf.FieldList.rint
   ~cf.FieldList.trunc

**Statistics**

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.FieldList.collapse

**Miscellaneous mathematical functions**

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.FieldList.clip

Data array operations
---------------------

.. rubric:: Data array mask

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: attribute.rst

   ~cf.FieldList.binary_mask
   ~cf.FieldList.mask

**Order and number of dimensions**

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.FieldList.expand_dims
   ~cf.FieldList.squeeze
   ~cf.FieldList.transpose
   ~cf.FieldList.unsqueeze

**Rearranging elements**

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.FieldList.anchor
   ~cf.FieldList.flip
   ~cf.FieldList.roll

Regridding operations
---------------------

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.FieldList.regrids

Date-time operations
--------------------
 
.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.FieldList.asdatetime
   ~cf.FieldList.asreftime


Logic functions
---------------
 
**Comparison**

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.FieldList.equals
   ~cf.FieldList.equivalent
   ~cf.FieldList.equivalent_data
   ~cf.FieldList.equivalent_domain


Miscellaneous
-------------

.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.FieldList.binary_mask
   ~cf.FieldList.chunk
   ~cf.FieldList.close
   cf.FieldList.concatenate
   ~cf.FieldList.copy 
   ~cf.FieldList.datum
   ~cf.FieldList.dump
   ~cf.FieldList.fill_value
   ~cf.FieldList.identity
   ~cf.FieldList.insert_data
   ~cf.FieldList.mask_invalid
   ~cf.FieldList.match
   ~cf.FieldList.name
   ~cf.FieldList.override_units
   ~cf.FieldList.override_calendar
   ~cf.FieldList.promote
   ~cf.FieldList.remove_data
   ~cf.FieldList.select
   ~cf.FieldList.weights
   ~cf.FieldList.where

List-like operations
--------------------

These methods provide functionality similar to that of a
:ref:`built-in list <python:tut-morelists>`.


.. autosummary::
   :nosignatures:
   :toctree: ../generated/
   :template: method.rst

   ~cf.FieldList.append
   ~cf.FieldList.count
   ~cf.FieldList.extend
   ~cf.FieldList.index
   ~cf.FieldList.insert
   ~cf.FieldList.pop
   ~cf.FieldList.reverse
   ~cf.FieldList.sort
   ~cf.FieldList.__contains__
   ~cf.FieldList.__getitem__ 
   ~cf.FieldList.__len__
   ~cf.FieldList.__setitem__ 

Arithmetic and comparison operations
------------------------------------

Any arithmetic, bitwise or comparison operation is applied
independently to each field element of the field list

In particular, the built-in :py:obj:`list` arithmetic and comparison
operator behaviours do not apply. For example, adding ``2`` to a field
list will add ``2`` to the data array of each of its fields, but the
``+`` operator will concatenate two built-in lists.

**Comparison operators**

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.FieldList.__lt__
   ~cf.FieldList.__le__
   ~cf.FieldList.__eq__
   ~cf.FieldList.__ne__
   ~cf.FieldList.__gt__
   ~cf.FieldList.__ge__

**Binary arithmetic operators**

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.FieldList.__add__     
   ~cf.FieldList.__sub__     
   ~cf.FieldList.__mul__     
   ~cf.FieldList.__div__     
   ~cf.FieldList.__truediv__ 
   ~cf.FieldList.__floordiv__
   ~cf.FieldList.__pow__     
   ~cf.FieldList.__mod__     

**Binary arithmetic operators with reflected (swapped) operands**

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.FieldList.__radd__     
   ~cf.FieldList.__rsub__     
   ~cf.FieldList.__rmul__     
   ~cf.FieldList.__rdiv__     
   ~cf.FieldList.__rtruediv__ 
   ~cf.FieldList.__rfloordiv__
   ~cf.FieldList.__rpow__   
   ~cf.FieldList.__rmod__   

**Augmented arithmetic assignments**

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.FieldList.__iadd__ 
   ~cf.FieldList.__isub__ 
   ~cf.FieldList.__imul__ 
   ~cf.FieldList.__idiv__ 
   ~cf.FieldList.__itruediv__
   ~cf.FieldList.__ifloordiv__
   ~cf.FieldList.__ipow__ 
   ~cf.FieldList.__imod__ 

**Unary arithmetic operators**

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.FieldList.__neg__    
   ~cf.FieldList.__pos__    
   ~cf.FieldList.__abs__    

**Binary bitwise operators**

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.FieldList.__and__     
   ~cf.FieldList.__or__
   ~cf.FieldList.__xor__     
   ~cf.FieldList.__lshift__
   ~cf.FieldList.__rshift__     

**Binary bitwise operators with reflected (swapped) operands**

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.FieldList.__rand__     
   ~cf.FieldList.__ror__
   ~cf.FieldList.__rxor__     
   ~cf.FieldList.__rlshift__
   ~cf.FieldList.__rrshift__     

**Augmented bitwise assignments**

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.FieldList.__iand__     
   ~cf.FieldList.__ior__
   ~cf.FieldList.__ixor__     
   ~cf.FieldList.__ilshift__
   ~cf.FieldList.__irshift__     

**Unary bitwise operators**

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.FieldList.__invert__ 

Special methods
---------------

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: method.rst

   ~cf.FieldList.__deepcopy__
   ~cf.FieldList.__repr__
   ~cf.FieldList.__str__
