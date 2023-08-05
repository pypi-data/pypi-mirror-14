==========================================================
PySpace: a python-based framework for galactic simulations
==========================================================

PySpace is an open-source framework for galactic simulations.
It is implemented in Cython and the computational part is implemented in pure C++.

PySpace provides parallel support through OpenMP and we plan on providing GPU support
in future releases.

Here's a video of planets arranged in cube simulation using PySpace.

.. raw:: html

    <div align="center">
        <iframe width="420" height="315" src="https://www.youtube.com/embed/aJneOtU__LY" frameborder="0" allowfullscreen>
        </iframe>
    </div>


--------
Features
--------

-  A python interface for high performance C++ implementation of N-body
   simulation algorithms.
-  PySpace has a numpy friendly API which makes it easier to use.
-  Parallel support using OpenMP.
-  Dumps vtk output which allows users to take advantage of tools like
   ParaView, MayaVi, etc. for visualization.

-------
Credits
-------

PySpace has been developed as a part of ME766 (High Performance Scientific Computing)
project at IIT Bombay.

Lead developers:

- Aditya Bhosale
- Rahul Govind
- Raj Krishnan


