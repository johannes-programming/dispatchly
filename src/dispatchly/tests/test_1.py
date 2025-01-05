import unittest
from typing import *

from dispatchly.core import singledispatch


@singledispatch
def fun(arg: Any):
    return arg


@fun.register(int)
def fun(arg: int):
    return -arg


@fun.register(float)
def fun(arg: float):
    return arg**2


class TestFunFunction(unittest.TestCase):

    def test_default_behavior(self):
        self.assertEqual(fun(8), -8)
        self.assertEqual(fun(2.0), 4.0)


if __name__ == "__main__":
    unittest.main()
