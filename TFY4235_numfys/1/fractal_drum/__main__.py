from fractal_drum import float_version
from fractal_drum import int_version
import logging

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.DEBUG,
        datefmt='%H:%M:%S'
    )
    loggers = ["numba", "matplotlib", "PIL"]
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.WARNING)
    l = 5
    sub = 2
    logging.info(f"Starting fractal drum calculations at fractal level {l} and subdivision {sub}")
    int_version.main(l, sub)
