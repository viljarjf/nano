"""
GaAs qubit, 
exited in resonance by an external wave
"""

import logging

QB_LOGGER = logging.getLogger("QB")

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)
