"""
Double quantum well simulation, and electron distribution at thermal equilibrium

Simulated using finite difference, and the fermi-dirac distribution function
"""

import logging

DQW_LOGGER = logging.getLogger("DQW")

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)
