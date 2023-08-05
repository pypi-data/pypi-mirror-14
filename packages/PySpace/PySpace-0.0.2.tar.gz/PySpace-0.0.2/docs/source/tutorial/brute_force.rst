========
Tutorial
========

--------------------
Brute Force Tutorial
--------------------

Imports
~~~~~~~

.. code-block:: python

    import numpy    

    # PySpace PlanetArray imports
    from pyspace.planet import PlanetArray

    # PySpace Simulator imports
    from pyspace.simulator import BruteForceSimulator

.. note::
    
    These are common to all simulations with brute force.
    For dumping vtk output with custom data, use the ``dump_vtk`` function in
    ``pyspace.utils``.


Setting up PlanetArray
~~~~~~~~~~~~~~~~~~~~~~

``PlanetArray`` is the container for all objects in a simulation.
The following example sets up a PlanetArray with planets arranged in a cube

.. code-block:: python

    x, y, z = numpy.mgrid[0:500:5j, 0:500:5j, 0:500:5j]
    x = x.ravel(); y = y.ravel(); z = z.ravel()

    pa = PlanetArray(x=x, y=y, z=z)


Setting up the Simulation
~~~~~~~~~~~~~~~~~~~~~~~~~

``BruteForceSimulator`` is the base of all computations in PySpace.
The following snippet shows how to set up the simulation.

.. code-block:: python

    G = 1
    dt = 0.1

    sim = BruteForceSimulator(pa, G, dt, "square_grid")


Running the simulator
~~~~~~~~~~~~~~~~~~~~~

``BruteForceSimulator::simulate`` simulates the system for a given time.
Following is the syntax for ``simulate``.

.. code-block:: python

    # Simulate for 1000 secs, ie. 1000/0.1 = 10e4 time steps
    sim.simulate(total_time = 1000, dump_output = True)

.. note::
    
    ``dump_output = True`` essentially dumps a vtk output for every timestep.

Dumping custom vtk output
~~~~~~~~~~~~~~~~~~~~~~~~~

``pyspace.simulator.BruteForceSimulator`` by default only dumps 
:math:`v_x, v_y, v_z` ie. the velocity in the generated vtk output. To dump
additional data, you need to use ``pyspace.simulator.Simulator.set_data``
function. 

Using this method for the above problem, you can write,

.. code-block:: python

    # Do all imports and set up the PlanetArray as done above
    # Import dump_vtk from pyspace.utils
    from pyspace.utils import dump_vtk

    # Set up the simulator
    sim = BruteForceSimulator(pa, G, dt, "square_grid")

    # Use set_data() to tell the simulator what to dump
    # For this problem, lets say you only need a_x, a_y and a_z
    sim.set_data(a_x = 'a_x', a_y = 'a_y', a_z = 'a_z')

    sim.simulate(total_time = total_time, dump_output = True)

.. note::

    Arguments of ``set_data`` is a property name, attribute name pair.
    For the above example, we could have called ``set_data`` as
    ``set_data(acc_x = 'a_x', ...)`` and it would still work.


