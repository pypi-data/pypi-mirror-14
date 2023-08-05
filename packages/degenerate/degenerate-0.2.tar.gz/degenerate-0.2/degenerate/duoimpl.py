"""
This module implements a decorator to provide several implementation of the
same method for a class, and initialize objects using the implementation name.
"""


class DuoImpl(object):
    """
    A method replacement Descriptor whcih returns appropriate implementation
    depending on the class variable.
    """
    def __init__(self, name, default_impl):
        super(DuoImpl, self).__init__()

        self.impls = {}
        self._name = name
        self.default = default_impl

    def __get__(self, owner, klass=None):
        if not owner:  # This is for definition phase
            return self

        current_impl = getattr(owner, DuoImplMeta.IMPL_ATTR_NAME, None)

        if not current_impl:
            impl_name = self.impls.get(self.default)
        else:
            impl_name = self.impls.get(current_impl)

        impl = getattr(owner, impl_name, None) if impl_name else None

        if not impl:
            raise TypeError("'%s' is not implemented for '%s'"
                            % (self._name, current_impl))

        return impl.__get__(owner, klass)

    def duoimpl(self, impl_name):
        def wrapper(func):
            self.impls[impl_name] = func.__name__

            return func

        return wrapper


class DuoImplMeta(type):
    """
    A metaclass that inspects and collects all possible implementations, and
    makes it possible to select an implementation class instance using static
    fields.
    """
    _duoimpl_all_impls = set()
    IMPL_ATTR_NAME = '_duoimpl_impl'

    def __init__(cls, *more):
        for attr, value in [(attr, getattr(cls, attr)) for attr in dir(cls)]:
            if not isinstance(value, DuoImpl):
                continue

            default_impl_name = value.default
            default_impl = value.impls[default_impl_name]
            default_func_name = "%s_%s" % (attr, default_impl_name)
            setattr(cls, default_func_name, default_impl)
            value.impls[default_impl_name] = default_func_name

            cls._duoimpl_all_impls.update(value.impls.keys())

        super(DuoImplMeta, cls).__init__(*more)

    def __getattr__(cls, name):
        if name not in cls._duoimpl_all_impls:
            raise AttributeError("'%s' object has no attribute '%s'"
                                 % (cls.__name__, name))

        def init(*args, **kwargs):
            obj = cls(*args, **kwargs)
            setattr(obj, DuoImplMeta.IMPL_ATTR_NAME, name)

            return obj

        return init


class duoimpl(object):
    """
    A decorator that enables providing several implementations for a method
    """
    def __init__(self, impl_name):
        super(duoimpl, self).__init__()

        self._impl_name = impl_name

    def __call__(self, obj):
        impl = DuoImpl(obj.__name__, default_impl=self._impl_name)
        impl.impls[self._impl_name] = obj

        return impl
