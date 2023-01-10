"""
Superconducting quantum interference device simulation software.

Simulated using finite difference and Crank-Nicholson time propagation
"""

import logging

SQUID_LOGGER = logging.getLogger("SQUID")

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%H:%M:%S'
    )
