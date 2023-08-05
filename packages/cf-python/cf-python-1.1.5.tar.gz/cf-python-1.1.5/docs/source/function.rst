.. currentmodule:: cf
.. default-role:: obj

.. _function:

Functions of the :mod:`cf` module
=================================

Input and output
----------------

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: function.rst

   cf.close_files
   cf.close_one_file
   cf.dump
   cf.open_files
   cf.open_files_threshold_exceeded
   cf.pickle
   cf.read 
   cf.write
   cf.unpickle

Aggregation
-----------

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: function.rst

   cf.aggregate

.. _functions-mathematical-operations:

Mathematical operations
-----------------------

Comparison
----------

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: function.rst

   cf.equals
   cf.equivalent

The following functions generate `cf.Query` instances for evaluating
objects against given criteria. For example, ``cf.wi(3, 5)`` generates
a query for testing whether, or where, an object is in the range [3,
5].

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: function.rst

   cf.contain
   cf.eq
   cf.ge
   cf.gt
   cf.le
   cf.lt
   cf.ne
   cf.set
   cf.wi
   cf.wo

**Climatological seasons**

The following functions generate `cf.Query` instances for evaluating
objects against given criteria. For example, ``cf.djf()`` generates a
query for testing whether, or where, a date-time object is in a
December--February season.

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: function.rst

   cf.djf
   cf.mam
   cf.jja
   cf.son
   cf.seasons

**Date-time**

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: function.rst

   cf.dteq
   cf.dtge
   cf.dtgt
   cf.dtle
   cf.dtlt
   cf.dtne
   cf.year
   cf.month
   cf.day
   cf.hour
   cf.minute
   cf.second

**Coordinate cell bounds**

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: function.rst

   cf.cellgt
   cf.cellge
   cf.cellle
   cf.celllt
   cf.cellwi
   cf.cellwo
   cf.cellsize

Date-time
---------

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: function.rst

   cf.dt
   cf.Y
   cf.M
   cf.D
   cf.h
   cf.m
   cf.s

Retrieval and setting of constants
----------------------------------

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: function.rst

   cf.ATOL
   cf.CHUNKSIZE
   cf.FM_THRESHOLD
   cf.MINNCFM
   cf.OF_FRACTION
   cf.REGRID_LOGGING
   cf.RTOL
   cf.TEMPDIR

Miscellaneous
-------------

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: function.rst

   cf.abspath
   cf.dirname
   cf.flat
   cf.pathjoin
   cf.relpath
