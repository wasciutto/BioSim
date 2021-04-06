"""BioSim is a basic environment simulator that tracks vegetation and precipitation values over time.  The
more "balanced" the environment's initial conditions are tuned, the longer the simulation will run before all of the vegetation dies out.

To experiment with getting the best initial conditions, the simulator can be run
repeatedly and viewed in aggregate through a weighted scatterplot."""

import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(asctime)s %(message)s')