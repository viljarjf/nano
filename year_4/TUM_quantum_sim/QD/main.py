import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from scipy import sparse as sp

from TUM_quantum_sim import constants as c
from TUM_quantum_sim import utils
from TUM_quantum_sim.QD import QD_LOGGER as logging

def main():
    matplotlib.use("QtAgg")

    logging.info("Starting simulation")

    logging.info("Simulation finished, exiting...")
