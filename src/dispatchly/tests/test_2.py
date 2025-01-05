import unittest
from typing import *

from dispatchly.core import singledispatch


@singledispatch
def fun(arg: Any, verbose: bool = False):
    return arg, "whatever" if verbose else ""


@fun.register(int)
def fun(arg: int, verbose: bool = False):
    return -arg, "integer" if verbose else ""


@fun.register(float)
def fun(arg: float, verbose: bool = True):
    return arg**2, "float" if verbose else ""


class TestSingleDispatchFunction(unittest.TestCase):

    def test_default_behavior(self):
        # Test with an unsupported type (e.g., string)
        result = fun("test", verbose=False)
        self.assertEqual(result, ("test", ""))
        result_verbose = fun("test", verbose=True)
        self.assertEqual(result_verbose, ("test", "whatever"))

    def test_int_behavior(self):
        # Test with an integer
        result = fun(10, verbose=False)
        self.assertEqual(result, (-10, ""))
        result_verbose = fun(10, verbose=True)
        self.assertEqual(result_verbose, (-10, "integer"))

    def test_float_behavior(self):
        # Test with a float
        result = fun(2.5, verbose=False)
        self.assertEqual(result, (6.25, ""))
        result_verbose = fun(2.5, verbose=True)
        self.assertEqual(result_verbose, (6.25, "float"))

    def test_edge_cases(self):
        # Test with edge cases like 0 and negative numbers
        self.assertEqual(fun(0, verbose=False), (0, ""))
        self.assertEqual(fun(0, verbose=True), (0, "integer"))
        self.assertEqual(fun(-3, verbose=False), (3, ""))
        self.assertEqual(fun(-3, verbose=True), (3, "integer"))
        self.assertEqual(fun(-1.5, verbose=False), (2.25, ""))
        self.assertEqual(fun(-1.5, verbose=True), (2.25, "float"))


if __name__ == "__main__":
    unittest.main()
