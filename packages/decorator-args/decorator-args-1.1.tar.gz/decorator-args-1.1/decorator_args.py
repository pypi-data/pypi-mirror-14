import inspect
import sys


__all__ = [
    'decorator_args', 'optional_decorator_args', 'keyword_only_decorator_args',
    'optional_keyword_only_decorator_args', 'default_is_decoratable_object',
]


if sys.version_info[0] == 2:
    # Our own functools.update_wrapper() implementation instead of the
    # original python2 version that doesn't handle AttributeErrors.
    WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__doc__')
    WRAPPER_UPDATES = ('__dict__',)

    def update_wrapper(wrapper, wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
        for attr in assigned:
            try:
                value = getattr(wrapped, attr)
            except AttributeError:
                pass
            else:
                setattr(wrapper, attr, value)
        for attr in updated:
            getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
        wrapper.__wrapped__ = wrapped
        return wrapper
else:
    from functools import update_wrapper, WRAPPER_UPDATES


def default_is_decoratable_object(obj):
    return inspect.isroutine(obj) or inspect.ismethoddescriptor(obj) or inspect.isclass(obj)


# As a decorator function this could be a bit simpler but this way our decorator easily works
# also with instance/class/static methods that behave as decorators in their bound form.
class _DecoratorArgs(object):
    def __init__(self, decorator, keyword_only=False, optional=False, is_decoratable_object=None):
        super(_DecoratorArgs, self).__init__()
        if is_decoratable_object is not None:
            if keyword_only:
                raise ValueError('is_decoratable_object must be None when keyword_only==True')
            if not optional:
                raise ValueError('is_decoratable_object must be None when optional==False')

        # In case of receiving a class as a decorator we don't want to update
        # our instance __dict__ with the __dict__ of the wrapped class.
        updated = () if inspect.isclass(decorator) else WRAPPER_UPDATES
        # Since update_wrapper() updates our __dict__ we call it as
        # a first step to prevent it from screwing up our attributes.
        update_wrapper(self, decorator, updated=updated)
        self.decorator = decorator
        self.keyword_only = keyword_only
        self.optional = optional
        self.is_decoratable_object = is_decoratable_object or default_is_decoratable_object

    def __get__(self, instance, owner):
        bound_decorator_method = self.decorator.__get__(instance, owner)

        def wrapper(*args, **kwargs):
            return self._receive_decorator_args_or_perform_decoration(bound_decorator_method, args, kwargs)
        return update_wrapper(wrapper, bound_decorator_method)

    def __call__(self, *args, **kwargs):
        return self._receive_decorator_args_or_perform_decoration(self.decorator, args, kwargs)

    def _receive_decorator_args_or_perform_decoration(self, decorator, args, kwargs):
        if self.optional:
            if self.keyword_only:
                if len(args) >= 2 or (len(args) == 1 and kwargs):
                    raise TypeError('This decorator receives only keyword arguments')
                if len(args) == 1:
                    return decorator(args[0])
            elif not kwargs and len(args) == 1 and self.is_decoratable_object(args[0]):
                return decorator(args[0])
        elif self.keyword_only and args:
            raise TypeError('This decorator receives only keyword arguments')

        def decorate_with_args(decoratable):
            return decorator(decoratable, *args, **kwargs)
        return update_wrapper(decorate_with_args, decorator)


def decorator_args(decorator, keyword_only=False, optional=False, is_decoratable_object=None):
    return _DecoratorArgs(decorator=decorator,
                          keyword_only=keyword_only,
                          optional=optional,
                          is_decoratable_object=is_decoratable_object)
decorator_args = _DecoratorArgs(decorator_args, keyword_only=True, optional=True)


@decorator_args(keyword_only=True, optional=True)
def optional_decorator_args(decorator, keyword_only=False, is_decoratable_object=None):
    return _DecoratorArgs(decorator=decorator,
                          keyword_only=keyword_only,
                          optional=True,
                          is_decoratable_object=is_decoratable_object)


@decorator_args(keyword_only=True, optional=True)
def keyword_only_decorator_args(decorator, optional=False):
    return _DecoratorArgs(decorator=decorator,
                          keyword_only=True,
                          optional=optional)


@decorator_args(keyword_only=True, optional=True)
def optional_keyword_only_decorator_args(decorator):
    return _DecoratorArgs(decorator=decorator,
                          keyword_only=True,
                          optional=True)
