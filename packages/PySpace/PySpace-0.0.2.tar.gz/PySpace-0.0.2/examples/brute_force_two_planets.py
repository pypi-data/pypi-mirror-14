#!usr/bin/env python
from pyspace.planet import PlanetArray
from pyspace.simulator import BruteForceSimulator
import numpy

x = numpy.array([0,100])
y = numpy.array([0,0])
z = numpy.array([0,0])

m = numpy.array([1000,1])

v_y = numpy.array([0,4])

pa = PlanetArray(x, y, z, v_y=v_y, m=m)

sim = BruteForceSimulator(pa, 1, 1, "two_planets")

sim.simulate(3000, dump_output = True)

