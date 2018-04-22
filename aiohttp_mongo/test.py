from coverage import Coverage
cov = Coverage(source=['cnfmanager'])
cov.start()


import unittest
from tests import *


if __name__ == '__main__':
    unittest.main(exit=False)

    cov.stop()
    cov.report()