import dataclasses
import functools
import types
from typing import *

import tofunc
from argshold import FrozenArgumentHolder
from datarepr import datarepr

__all__ = ["dispatch"]


def dispatch(old: Any, /) -> Any:
    return Data(old).ans


def identity(value: Any, /) -> Any:
    return value


def ismatch(pre: FrozenArgumentHolder, post: FrozenArgumentHolder) -> bool:
    if len(pre.args) > len(post.args):
        return False
    for x, y in zip(pre.args, post.args):
        if not isinstance(y, x):
            return False
    for k, v in pre.kwargs.items():
        if k not in post.kwargs:
            return False
        if not isinstance(post.kwargs[k], v):
            return False
    return True


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

    def ans_1(self, *args: Any, **kwargs: Any) -> Any:
        post = FrozenArgumentHolder(*args, **kwargs)
        variant = self.getvariant(post)
        return holder.call(variant)

    def getvariant(self, post: FrozenArgumentHolder) -> Any:
        for pre, variant in self.ans.registry.items():
            if ismatch(pre=pre, post=post):
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


class Register:
    def __call__(self, value: Any) -> Any:
        self.ans.registry[self.key] = Unpack.byValue(value).func
        return self.ans

    def __init__(self, ans: Any, /, *args: Any, **kwargs: Any) -> None:
        self.ans = ans
        self.key = FrozenArgumentHolder(*args, **kwargs)

    def __repr__(self) -> str:
        return datarepr(type(self).__name__, ans=self.ans, key=self.key)
