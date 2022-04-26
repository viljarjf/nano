
from fractal_drum import float_version
from fractal_drum import int_version
import logging

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%H:%M:%S'
    )
    int_version.main()
