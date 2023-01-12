"""
Quantum cascade laser simulation

Simulated using finite difference, 
the fermi-dirac distribution function for occupation,
and the poisson equation for charge distribution
"""

import logging

QCL_LOGGER = logging.getLogger("QCL")

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%H:%M:%S'
    )
