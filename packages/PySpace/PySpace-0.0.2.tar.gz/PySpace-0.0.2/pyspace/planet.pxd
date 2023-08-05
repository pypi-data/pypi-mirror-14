# distutils: language = c++
import numpy as np
cimport numpy as np

cdef extern from "numpy/arrayobject.h":
    ctypedef int intp
    ctypedef extern class numpy.ndarray [object PyArrayObject]:
        cdef char *data
        cdef int nd
        cdef intp *dimensions
        cdef intp *strides
        cdef int flags

cdef class PlanetArray:
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

    cpdef int get_number_of_planets(self)
    cpdef double dist(self, int i, int j)

    cpdef double potential_energy_planet(self, double G, int i)
    cpdef double kinetic_energy_planet(self, int i)

    cpdef double potential_energy(self, double G)
    cpdef double kinetic_energy(self)

    cpdef double total_energy_planet(self, double G, int i)
    cpdef double total_energy(self, double G)


