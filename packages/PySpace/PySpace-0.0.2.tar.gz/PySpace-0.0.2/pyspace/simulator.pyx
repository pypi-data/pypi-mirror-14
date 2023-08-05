# distutils: language = c++
cimport cython
import os
from pyspace.utils import dump_vtk

cdef class Simulator:
    def __init__(self, PlanetArray pa, double G, double dt, str sim_name = "pyspace"):
        self.planets = pa
        self.G = G
        self.dt = dt
        self.sim_name = sim_name
        self._custom_data = False

        self.num_planets = pa.get_number_of_planets()

    cpdef simulate(self, double total_time, bint dump_output = False):
        """Implement this in derived classes to get final state"""
        raise NotImplementedError("Simulator::simulate called")

    def set_data(self, **kwargs):
        """Sets what data has to be dumped to the vtk output

        Parameters:

        **kwargs: {property name = attribute name}

        """
        self._custom_data = True
        self._data = kwargs

    cdef dict get_data(self):
        """Gets data for vtk dumps"""
        cdef dict data = {}
        if not self._custom_data:
            return data
        cdef str property_name, attribute_name
        for property_name, attribute_name in self._data.iteritems():
            data[property_name] = getattr(self.planets, attribute_name)
        return data

cdef class BruteForceSimulator(Simulator):
    """Simulator using Brute Force algorithm"""
    def __init__(self, PlanetArray pa, double G, double dt, str sim_name = "pyspace"):
        """Constructor for BruteForceSimulator

        Parameters:

        pa: PlanetArray
            Planet array for simulation

        G: double
            Universal Gravitational constant

        dt: double
            Time step for simulation

        Notes:

        Uses brute force for simulation

        """
        Simulator.__init__(self, pa, G, dt, sim_name)

    @cython.cdivision(True)
    cdef void _simulate(self, double total_time, bint dump_output = False):

        cdef double G = self.G
        cdef double dt = self.dt

        cdef int n_steps = <int> floor(total_time/dt)
        cdef int i

        for i from 0<=i<n_steps:
            brute_force_update(self.planets.x_ptr, self.planets.y_ptr, self.planets.z_ptr,
                    self.planets.v_x_ptr, self.planets.v_y_ptr, self.planets.v_z_ptr,
                    self.planets.a_x_ptr, self.planets.a_y_ptr, self.planets.a_z_ptr,
                    self.planets.m_ptr, G, dt, self.num_planets)
            if dump_output:
                dump_vtk(self.planets, self.sim_name + str(i),
                        base = self.sim_name, **self.get_data())

    cpdef simulate(self, double total_time, bint dump_output = False):
        """Calculates position and velocity of all particles
        after time 'total_time'

        Parameters:

        total_time: double
            Total time for simulation

        """
        if dump_output and (not os.path.isdir(self.sim_name)):
            os.mkdir(self.sim_name)

        self._simulate(total_time, dump_output)


