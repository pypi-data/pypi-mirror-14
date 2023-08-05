# -*- coding: utf-8 -*-
import collections
import inspect
import functools


class cached_property(object):

    """Allows expensive property calls to be cached.

    Once the property is called, it's result is stored in the corresponding
    property name prefixed with an underscore.

    Example:

    .. code-block:: python

        class MyClass(object):
            @cached_property
            def expensive_call(self):
                # do something expensive

        klass = MyClass()
        klass.expensive_call  # initial call is made
        klass.expensive_call  # return value is retrieved from an internal cache
        del klass._expensive_call
    """

    def __init__(self, func):
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__
        self.key = '_{name}'.format(name=self.__name__)
        self.func = func

    def __get__(self, obj, type=None):
        if self.key not in obj.__dict__:
            obj.__dict__[self.key] = self.func(obj)
        return obj.__dict__[self.key]


def instance_set(ignore=None):

    """Allows initial binding of arguments to an __init__ method.

    Example:

    .. code-block:: python

        class MyClass(object):
            value = None

            @instance_set
            def __init__(self, value="Instance variable declaration"):
                pass

        klass = MyClass()
        klass.value  # Bound Value
    """
    def decorator(func):
        signature = inspect.signature(func)
        inspect._empty
        instance_args = collections.OrderedDict()
        for arg, param in signature.parameters.items():
            if arg == 'self':
                continue
            if isinstance(ignore, (list, tuple)) and arg in ignore:
                continue
            value = None if param.default is param.empty else param.default
            instance_args[arg] = value

        @functools.wraps(func)
        def init(self, *args, **kwargs):
            arg_iter = iter(args)
            for key in instance_args:
                try:
                    value = next(arg_iter)
                except StopIteration:
                    value = kwargs.get(key, instance_args[key])
                setattr(self, key, value)
            func(self, *args, **kwargs)
        return init

    if type(ignore) == type(decorator):
        return decorator(ignore)
    return decorator
