import dataclasses
import functools
import types
from typing import *

import tofunc

__all__ = ["singledispatch"]


def identity(value, /):
    return value


def singledispatch(old, /):
    return Data(old).ans


@dataclasses.dataclass(frozen=True)
class Unpack:
    kind: Any
    func: Any

    @classmethod
    def byValue(cls, value: Any):
        try:
            func = value.__func__
        except AttributeError:
            func = value
            kind = identity
        else:
            kind = type(value)
        return cls(kind=kind, func=func)


class Data:
    def __init__(self, old: Any) -> None:
        self.ans = self.makeans(old)

    def ans_1(self, arg: Any, /, *args: Any, **kwargs: Any) -> Any:
        variant = self.getvariant(arg)
        return variant(arg, *args, **kwargs)

    def getvariant(self, arg: Any) -> Any:
        for key, value in self.ans.registry.items():
            if isinstance(arg, key):
                return value
        return self.ans.default

    def makeans(self, old: Any) -> Any:
        unpack = Unpack.byValue(old)
        ans = tofunc.tofunc(self.ans_1)
        functools.wraps(unpack.func)(ans)
        ans = unpack.kind(ans)
        ans._data = self
        ans.default = unpack.func
        ans.registry = dict()
        ans.register = self.makeregister()
        return ans

    def makeregister(self) -> types.FunctionType:
        def register(key: Any):
            return Register(ans=self.ans, key=key)

        return register


@dataclasses.dataclass
class Register:
    ans: Any
    key: Any

    def __call__(self, value: Any) -> Any:
        self.ans.registry[self.key] = Unpack.byValue(value).func
        return self.ans
