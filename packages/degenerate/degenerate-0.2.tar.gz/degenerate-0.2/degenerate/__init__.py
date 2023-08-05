"""
This is the foundation of degenerate, where the generator unwinder is defined
and implemented.
"""

import types
from functools import wraps


class ReturnException(BaseException):
    """
    This is a return value carrier custom exception.
    """
    def __init__(self, value):
        super(ReturnException, self).__init__()

        self.value = value


def degenerate_base(gen, return_exc=ReturnException, return_exc_attr='value'):
    """
    This method unwinds the provided generator until `StopIteration`
    or `return_exc` is caught. In the first case the `None` is returned.
    In the second case the value of attribute named `return_exc_attr`
    is returned.
    """
    if not isinstance(return_exc, type) or \
       not issubclass(return_exc, BaseException):
        raise TypeError("return_exc must be a subclass of BaseException")

    if not isinstance(gen, types.GeneratorType):
        raise TypeError("gen must be a generator")

    result = gen.next()
    try:
        while True:
            if isinstance(result, types.GeneratorType):
                result = degenerate_base(result, return_exc, return_exc_attr)

            result = gen.send(result)
    except StopIteration:
        return None
    except return_exc as exc:
        return getattr(exc, return_exc_attr)


def degenerate(func):
    """
    Just a conveniece decorator to transform a generator into a regular
    function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return degenerate_base(func(*args, **kwargs))

    return wrapper
