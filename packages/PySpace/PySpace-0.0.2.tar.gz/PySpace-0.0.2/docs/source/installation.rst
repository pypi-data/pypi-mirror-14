============
Installation
============

------------
Dependencies
------------

- Numpy
- PyEVTK (``pip install pyevtk``)
- gcc compiler
- OpenMP (optional)
- ParaView / MayaVi or any other vtk rendering tool (optional)

-------------
Linux and OSX
-------------

| Clone this repository by
  ``git clone https://github.com/adityapb/pyspace.git``
| Run ``python setup.py install`` to install.

To install without OpenMP, set ``USE_OPENMP`` environment variable
to 0 by ``export USE_OPENMP=0`` and then run ``python setup.py install``

| **PySpace doesn't support Windows currently**


