"""
GaAs quantum dot, 
modelled as a two-level system.
Exited in resonance by an external wave
"""

import logging

QD_LOGGER = logging.getLogger("QD")

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%H:%M:%S'
    )
