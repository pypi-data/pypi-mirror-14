import unittest
import numpy
from . import findifftool
from findifftool.attributes import *


class NewTest(unittest.TestCase):

    def setUp(self):
        class simple(object):
            x = numpy.ones(1)

            def get_x(self):
                return self.x

        self.simple = simple()

        class coupled(object):
            other = simple()

        self.coupled = coupled()


    def tearDown(self):
        pass


    def test_simple_new_identical(self):
        f, x = get_method_and_copy_of_attribute(self.simple, 'get_x', 'x')
        self.assertEqual(x, self.simple.x)
        self.assertIs(x, self.simple.x)

    def test_simple_old_equal(self):
        simple_x_orig = self.simple.x
        f, x = get_method_and_copy_of_attribute(self.simple, 'get_x', 'x')
        self.assertEqual(x, simple_x_orig)
        self.assertIsNot(x, simple_x_orig)

    def test_coupled_new_identical(self):
        f, x = get_method_and_copy_of_attribute(self.coupled, 'other.get_x', 'other.x')
        self.assertEqual(x, self.coupled.other.x)
        self.assertIs(x, self.coupled.other.x)

    def test_coupled_old_equal(self):
        coupled_x_orig = self.coupled.other.x
        f, x = get_method_and_copy_of_attribute(self.coupled, 'other.get_x', 'other.x')
        self.assertEqual(x, coupled_x_orig)
        self.assertIsNot(x, coupled_x_orig)

if __name__ == "__main__":
    unittest.main()
