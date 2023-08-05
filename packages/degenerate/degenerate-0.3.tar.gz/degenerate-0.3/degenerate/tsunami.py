"""
The Tornado utilities for DuoImpl.
"""
from functools import wraps
try:
    from tornado.gen import coroutine, Return
except ImportError:  # pragma: no cover
    raise ImportError("Imported '%s' without Tornado installed"
                      % __name__)

from degenerate import degenerate_base
from degenerate.duosync import DuoSync


def degenerate(func):
    """
    Generator unwinder decorator for Twisted `inlineCallbacks` methods
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return degenerate_base(func(*args, **kwargs),
                               return_exc=Return)

    return wrapper


def duosync(func):
    """
    Decorator for making methods DuoSync.
    """
    def decorator(impl_name):
        return DuoSync(impl_name, func, degenerate, coroutine)

    return decorator
