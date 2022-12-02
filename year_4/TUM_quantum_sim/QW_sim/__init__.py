"""
Quantum wire simulation software.

GaAs/AlGaAs heterostructure, simulated for electrons using pragmatic approximations.

Simulated using finite differences
"""

import logging

QW_SIM_LOGGER = logging.getLogger("QW_sim")

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%H:%M:%S'
    )
