=====================
The PySpace Framework
=====================

This document is an introduction to the design of PySpace. This provides high level details
on the functionality of PySpace. This should allow the user to use the module and extend it
effectively.

To understand the framework, we will work through a general N-body problem.

Here we will be using the ``BruteForceSimulator``, however the framework
is essentially the same for any ``Simulator``.

--------------
N-body problem
--------------

Consider a problem of :math:`n` bodies with mass :math:`m_i` for the :math:`i^{th}` planet. 

Equations
~~~~~~~~~

.. math::
    :label: force    

    \vec{a_i} = \sum_{\substack{j=1 \\ j\neq i}}^{n} G \frac{m_j}{r_{ij}^3} (\vec{r_j} - \vec{r_i})

Numerical Integration
~~~~~~~~~~~~~~~~~~~~~

``BruteForceSimulator`` uses leap frog integrator for updating velocity and positions of planets.

.. math::
    :label: position

    x_{i+1} = x_i + v_i\Delta t + \frac{1}{2}a_i\Delta t^2

.. math::
    :label: velocity

    v_{i+1} = v_i + \frac{1}{2}(a_i + a_{i+1})\Delta t


Understanding the framework
~~~~~~~~~~~~~~~~~~~~~~~~~~~

PySpace uses ``pyspace.planet.PlanetArray`` for storing planets.

``pyspace.planet.PlanetArray`` stores numpy arrays for :math:`x, y, z, v_x, v_y, v_z, a_x, a_y, a_z, m, r` and also stores a raw pointer to each numpy array.

.. code-block:: cython

    cdef public ndarray x
    cdef public ndarray y
    cdef public ndarray z
    cdef public ndarray v_x
    cdef public ndarray v_y
    cdef public ndarray v_z
    cdef public ndarray a_x
    cdef public ndarray a_y
    cdef public ndarray a_z
    cdef public ndarray m
    cdef public ndarray r

    cdef double* x_ptr
    cdef double* y_ptr
    cdef double* z_ptr

    cdef double* v_x_ptr
    cdef double* v_y_ptr
    cdef double* v_z_ptr

    cdef double* a_x_ptr
    cdef double* a_y_ptr
    cdef double* a_z_ptr

    cdef double* m_ptr
    cdef double* r_ptr

.. note::

    Currently ``r`` doesn't have any use per se. However, we plan to use it
    for better collision handling in the future.

Here we will be using ``pyspace.simulator.BruteForceSimulator`` which uses
the :math:`O(n^2)` brute force algorithm for calculating forces in a planet.

``pyspace.simulator.BruteForceSimulator`` then passes these raw pointers to the C++ function, ``brute_force_update`` which then updates the pointers using the above numerical integration 
scheme.

-------------
Visualization
-------------

PySpace dumps a vtk output of the simulations. These can then be visualized using tools such as 
Paraview, MayaVi, etc.

The vtk dump is controlled by the ``dump_output`` flag in ``Simulator::simulate``.
The vtk dump by default only dumps :math:`v_x, v_y, v_z` ie. velocities
of the planets.
For dumping custom data, use ``set_data`` in ``pyspace.simulator.Simulator``.

