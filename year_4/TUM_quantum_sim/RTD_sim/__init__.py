"""
Biased resonant-tunnelling diode simulation software.

GaAs/AlGaAs heterostructure, simulated for electrons using pragmatic approximations.

Simulated using transfer matrices
"""

import logging

RTD_SIM_LOGGER = logging.getLogger("RTD_sim")

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%H:%M:%S'
    )
