import nose2
from qgis.testing import unittest

class TestExport(unittest.TestCase):

    def test_dummy(self):
        self.assertTrue(True)

if __name__ == '__main__':
    nose2.main()
