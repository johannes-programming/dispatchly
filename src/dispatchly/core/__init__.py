import dataclasses
import functools
from typing import *

import tofunc

__all__ = ["singledispatch"]


def identity(value, /):
    return value


def singledispatch(old, /):
    return Data(old).ans


class Data:
    def __init__(self, old):
        self.ans = self.makeans(old)

    def ans_1(self, arg, /, *args, **kwargs):
        variant = self.getvariant(arg)
        return variant(arg, *args, **kwargs)

    def getvariant(self, arg):
        for key, value in self.ans.registry.items():
            if isinstance(arg, key):
                return value
        return self.ans.default

    def makeans(self, old):
        try:
            default = old.__func__
        except AttributeError:
            default = old
            bind = identity
        else:
            bind = type(old)
        ans = tofunc.tofunc(self.ans_1)
        functools.wraps(default)(ans)
        ans = bind(ans)
        ans._data = self
        ans.default = default
        ans.registry = dict()
        ans.register = self.makeregister()
        return ans

    def makeregister(self):
        def register(key: Any):
            return Register(ans=self.ans, key=key)

        return register


@dataclasses.dataclass
class Register:
    ans: Any
    key: Any

    def __call__(self, value):
        self.ans.registry[self.key] = value
        return self.ans
