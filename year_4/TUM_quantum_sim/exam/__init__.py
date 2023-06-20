"""
Superconducting quantum interference device simulation software.

Simulated using finite difference and leapfrog time propagation
"""

import logging

EXAM_LOGGER = logging.getLogger("EXAM")

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)
