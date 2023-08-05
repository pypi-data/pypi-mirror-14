#!usr/bin/env python
from pyspace.planet import PlanetArray
from pyspace.simulator import BruteForceSimulator
import numpy

x, y, z = numpy.mgrid[0:500:5j, 0:500:5j, 0:500:5j]
x = x.ravel(); y = y.ravel(); z = z.ravel()

pa = PlanetArray(x, y, z)

sim = BruteForceSimulator(pa, 1, 1, "square_grid")

sim.simulate(1000, dump_output = True)

