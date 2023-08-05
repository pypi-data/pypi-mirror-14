# distutils: language = c++
import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport sqrt

cdef class PlanetArray:
    """PlanetArray for storing planets"""
    def __init__(self, ndarray x, ndarray y, ndarray z,
            ndarray v_x = None, ndarray v_y = None,  ndarray v_z = None,
            ndarray m = None, ndarray r = None):
        """Constructor for PlanetArray

        Parameters:

        x: np.ndarray
            'x' coordinates of planets

        y: np.ndarray
            'y' coordinates of planets

        z: np.ndarray
            'z' coordinates of planets

        v_x: np.ndarray
            'x' components of initial velocity
            Default value: 0

        v_y: np.ndarray
            'y' components of initial velocity
            Default value: 0

        v_z: np.ndarray
            'z' components of initial velocity
            Default value: 0

        m: np.ndarray
            Mass of planets
            Default value: 1

        r: np.ndarray
            Radius of planets
            Default value: 1

        """
        self.x = x.astype(np.float64)
        self.y = y.astype(np.float64)
        self.z = z.astype(np.float64)

        cdef int num_planets = self.get_number_of_planets()

        if v_x is None:
            self.v_x = np.zeros(num_planets)
        else:
            self.v_x = v_x.astype(np.float64)

        if v_y is None:
            self.v_y = np.zeros(num_planets)
        else:
            self.v_y = v_y.astype(np.float64)

        if v_z is None:
            self.v_z = np.zeros(num_planets)
        else:
            self.v_y = v_y.astype(np.float64)

        if m is None:
            self.m = np.ones(num_planets)
        else:
            self.m = m.astype(np.float64)

        if r is None:
            self.r = np.ones(num_planets)
        else:
            self.r = r.astype(np.float64)

        self.a_x = np.zeros(num_planets)
        self.a_y = np.zeros(num_planets)
        self.a_z = np.zeros(num_planets)

        self.x_ptr = <double*> self.x.data
        self.y_ptr = <double*> self.y.data
        self.z_ptr = <double*> self.z.data

        self.v_x_ptr = <double*> self.v_x.data
        self.v_y_ptr = <double*> self.v_y.data
        self.v_z_ptr = <double*> self.v_z.data

        self.a_x_ptr = <double*> self.a_x.data
        self.a_y_ptr = <double*> self.a_y.data
        self.a_z_ptr = <double*> self.a_z.data

        self.m_ptr = <double*> self.m.data
        self.r_ptr = <double*> self.r.data

    cpdef int get_number_of_planets(self):
        """Returns number of planets in the PlanetArray

        Parameters:

        None

        Returns:

        int: Number of planets in PlanetArray

        """
        return self.x.size

    cpdef double dist(self, int i, int j):
        """Distance between planet 'i' and planet 'j'

        Parameters:

        i, j: int
            Indices of planets whose distance is sought.

        """
        return sqrt((self.x_ptr[i] - self.x_ptr[j])**2 + (self.y_ptr[i] - self.y_ptr[j])**2 + \
                (self.z_ptr[i] - self.z_ptr[j])**2)

    @cython.cdivision(True)
    cpdef double potential_energy_planet(self, double G, int i):
        """Returns potential energy of planet 'i'

        Parameters:

        G: double
            Universal Gravitational constant

        i: int
            Index of the particle whose potential energy is sought

        """
        cdef double pot_energy = 0
        cdef int num_planets = self.get_number_of_planets()
        cdef int j

        for j from 0<=j<num_planets:
            pot_energy += -G*self.m_ptr[i]*self.m_ptr[j]/self.dist(i,j)

        return pot_energy

    cpdef double kinetic_energy_planet(self, int i):
        """Returns kinetic energy of planet 'j'"""
        return 0.5*self.m_ptr[i]*(self.v_x_ptr[i]**2 + self.v_y_ptr[i]**2 + self.v_z_ptr[i]**2)

    @cython.cdivision(True)
    cpdef double potential_energy(self, double G):
        """Returns total potential energy of PlanetArray"""
        cdef double tot_pot_energy = 0
        cdef int num_planets = self.get_number_of_planets()
        cdef int i

        for i from 0<=i<num_planets:
            tot_pot_energy += self.potential_energy_planet(G,i)

        return tot_pot_energy/2

    cpdef double kinetic_energy(self):
        """Returns total kinetic energy of PlanetArray"""
        cdef double tot_kin_energy = 0
        cdef int num_planets = self.get_number_of_planets()
        cdef int i

        for i from 0<=i<num_planets:
            tot_kin_energy += self.kinetic_energy_planet(i)

        return tot_kin_energy

    cpdef double total_energy_planet(self, double G, int i):
        """Returns total energy of planet 'i'"""
        return self.potential_energy_planet(G,i) + self.kinetic_energy_planet(i)

    cpdef double total_energy(self, double G):
        """Returns total energy of PlanetArray"""
        return self.potential_energy(G) + self.kinetic_energy()

