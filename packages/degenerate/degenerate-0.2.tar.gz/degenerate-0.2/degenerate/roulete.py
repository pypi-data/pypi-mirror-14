"""
The Twisted utilities for DuoImpl.
"""
from functools import wraps
try:
    from twisted.internet.defer import _DefGen_Return, inlineCallbacks
except ImportError:  # pragma: no cover
    raise ImportError("Imported '%s' without Twisted installed"
                      % __name__)

from degenerate import degenerate_base
from degenerate.duoimpl import DuoImplMeta


def degenerate(func):
    """
    Generator unwinder decorator for Twisted `inlineCallbacks` methods
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return degenerate_base(func(*args, **kwargs),
                               return_exc=_DefGen_Return)

    return wrapper


class DuoSync(object):
    """
    Method replacement descriptor for Twisted, that returns either a Twisted
    generator or a plain method depending on the owner class specified
    DuoImpl implementation.
    """
    def __init__(self, impl_name, func):
        super(DuoSync, self).__init__()

        self._impl_name = impl_name
        self._func = func

    def __get__(self, owner, klass=None):
        if not owner:
            return self

        current_impl = getattr(owner,
                               DuoImplMeta.IMPL_ATTR_NAME,
                               None)
        if current_impl == self._impl_name:
            return inlineCallbacks(self._func).__get__(owner, klass)
        else:
            return degenerate(self._func).__get__(owner, klass)


def duosync(func):
    """
    Decorator for making methods DuoSync.
    """
    def decorator(impl_name):
        return DuoSync(impl_name, func)

    return decorator
