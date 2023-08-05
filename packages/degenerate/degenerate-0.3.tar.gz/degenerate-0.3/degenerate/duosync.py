"""
DuoSync Base
"""
from degenerate.duoimpl import DuoImplMeta


class DuoSync(object):
    """
    Method replacement descriptor for Async Framework, that returns either a
    generator or a plain method depending on the owner class specified
    DuoImpl implementation.
    """
    def __init__(self, impl_name, func,
                 degenerate, cowrapper):
        super(DuoSync, self).__init__()

        self._impl_name = impl_name
        self._func = func
        self._degenerate = degenerate
        self._cowrapper = cowrapper

    def __get__(self, owner, klass=None):
        if not owner:
            return self

        current_impl = getattr(owner,
                               DuoImplMeta.IMPL_ATTR_NAME,
                               None)
        if current_impl == self._impl_name:
            return self._cowrapper(self._func).__get__(owner, klass)
        else:
            return self._degenerate(self._func).__get__(owner, klass)
