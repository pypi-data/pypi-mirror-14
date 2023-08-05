#!/usr/bin/env python
from inspect import *
from collections import *
from decorator import *
from public import *

results = defaultdict(dict)


class TypeError(TypeError):
    pass


@public
def cached(function):
    if not isfunction(function):
        err = "@cached requires function"
        raise TypeError(err)

    def wrapper(f, *args, **kwargs):
        id = str(args) + str(kwargs)
        funcresults = results[f]
        if id in funcresults:
            return funcresults[id]
        result = f(*args, **kwargs)
        results[f][id] = result
        return result
    return decorator(wrapper, function)

if __name__ == "__main__":
    def func():
        print("log")
    cached(func)()
    cached(func)()  # CACHED!
    # @decorator

    @cached
    def func2():
        print("log2")
    cached(func2)()
    cached(func2)()  # CACHED!
    # func(*args,**kwargs)

    def func3(*args, **kwargs):
        print("args = %s, kwargs= %s" % (args, kwargs))
    cached(func3)("arg1", "arg2", kwarg1="value1")
    cached(func3)("arg1", "arg2", kwarg1="value1")  # CACHED!
    cached(func3)("arg1", "arg2", "arg3")
    try:
        cached(None)()
    except TypeError:
        pass
    try:
        import os
        cached(os)()
    except TypeError:
        pass
