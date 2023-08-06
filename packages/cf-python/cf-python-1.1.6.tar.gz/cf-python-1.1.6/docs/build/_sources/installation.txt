.. currentmodule:: cf
.. default-role:: obj

.. highlight:: bash

Installation
============


To install by conda
-------------------

These two commands will install cf-python, all of its required
dependencies and the two optional packages cf-plot and ESMF::

   conda install -c ncas -c scitools cf-python cf-plot  
   conda install -c nesii esmpy

To install cf-python and all of its required dependencies alone::

   conda install -c ncas -c scitools cf-python

To install with pip
-------------------

::

   pip install cf-python

To install from source
----------------------

Download the cf package from `<https://bitbucket.org/cfpython/cf-python/downloads>`_

Unpack the library::

   tar zxvf cf-python-1.1.5.tar.gz
   cd cf-python-1.1.5

To install the cf package to a central location::

   python setup.py install

To install the cf package locally to the user in a default location::

   python setup.py install --user

To install the cf package in the <directory> of your choice::

   python setup.py install --home=<directory>


Issues
------

Please raise any questions or problems at
`<https://bitbucket.org/cfpython/cf-python/issues>`_
