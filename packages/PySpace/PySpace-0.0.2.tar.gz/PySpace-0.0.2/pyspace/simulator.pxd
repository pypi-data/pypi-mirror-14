# distutils: language = c++
from libcpp.vector cimport vector
from libc.math cimport floor
from pyspace.planet cimport PlanetArray

cdef extern from "numpy/arrayobject.h":
    ctypedef int intp
    ctypedef extern class numpy.ndarray [object PyArrayObject]:
        cdef char *data
        cdef int nd
        cdef intp *dimensions
        cdef intp *strides
        cdef int flags

cdef extern from "pyspace.h":
    cdef void brute_force_update(double*, double*, double*,
            double*, double*, double*,
            double*, double*, double*,
            double*, double, double, int) nogil

cdef class Simulator:
    cdef PlanetArray planets

    cdef double G
    cdef double dt
    cdef str sim_name
    cdef int num_planets

    cdef bint _custom_data
    cdef dict _data

    cpdef simulate(self, double total_time, bint dump_output = *)
    cdef dict get_data(self)

cdef class BruteForceSimulator(Simulator):

    cdef void _simulate(self, double total_time, bint dump_output = *)
    cpdef simulate(self, double total_time, bint dump_output = *)

