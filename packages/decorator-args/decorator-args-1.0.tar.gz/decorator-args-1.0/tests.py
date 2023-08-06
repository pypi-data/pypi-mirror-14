import functools
import re

import mock
from unittest import TestCase

from decorator_args import (
    decorator_args, optional_decorator_args, keyword_only_decorator_args, optional_keyword_only_decorator_args,
    default_is_decoratable_object,
)


def test_log(*args, **kwargs):
    pass


def decoratable_function(*args, **kwargs):
    test_log('decoratable_function', *args, **kwargs)
    return 'result'


class DecoratableClass(object):
    def decoratable_instancemethod(self, decoratable):
        pass

    @classmethod
    def decoratable_classmethod(cls, decoratable):
        pass

    @staticmethod
    def decoratable_staticmethod(decoratable):
        pass


def non_wrapped_decorator(decoratable, *args, **kwargs):
    test_log('non_wrapped_decorator', decoratable, *args, **kwargs)
    return decoratable


@mock.patch(__name__ + '.test_log')
class TestOptionalDecoratorArgDetection(TestCase):
    def test_single_positional_function_arg_without_empty_brackets(self, mock_test_log):
        decorated_decorator = optional_decorator_args(non_wrapped_decorator)
        decorated = decorated_decorator(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertEqual(decorated, decoratable_function)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', decoratable_function),
            mock.call('decoratable_function', 43, kw1=1)
        ])

    def test_single_positional_function_arg_with_empty_brackets(self, mock_test_log):
        decorated_decorator = optional_decorator_args(non_wrapped_decorator)
        decorated = decorated_decorator()(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertEqual(decorated, decoratable_function)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', decoratable_function),
            mock.call('decoratable_function', 43, kw1=1)
        ])

    def test_single_positional_function_arg(self, mock_test_log):
        decorated_decorator = optional_decorator_args(non_wrapped_decorator)
        decorated = decorated_decorator(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertEqual(decorated, decoratable_function)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', decoratable_function),
            mock.call('decoratable_function', 43, kw1=1)
        ])

    def test_decorator_kwargs(self, mock_test_log):
        decorated_decorator = optional_decorator_args(non_wrapped_decorator)
        decorated = decorated_decorator(kwarg='kwarg')(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertEqual(decorated, decoratable_function)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', decoratable_function, kwarg='kwarg'),
            mock.call('decoratable_function', 43, kw1=1)
        ])

    def test_single_positional_class_arg(self, mock_test_log):
        decorated_decorator = optional_decorator_args(non_wrapped_decorator)
        decorated = decorated_decorator(DecoratableClass)
        self.assertEqual(decorated, DecoratableClass)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', DecoratableClass),
        ])

    def test_single_positional_instancemethod_arg(self, mock_test_log):
        decorated_decorator = optional_decorator_args(non_wrapped_decorator)
        method = DecoratableClass.__dict__['decoratable_instancemethod']
        decorated = decorated_decorator(method)
        self.assertEqual(decorated, method)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', method),
        ])

    def test_single_positional_classmethod_arg(self, mock_test_log):
        decorated_decorator = optional_decorator_args(non_wrapped_decorator)
        method = DecoratableClass.__dict__['decoratable_classmethod']
        decorated = decorated_decorator(method)
        self.assertEqual(decorated, method)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', method),
        ])

    def test_single_positional_staticmethod_arg(self, mock_test_log):
        decorated_decorator = optional_decorator_args(non_wrapped_decorator)
        method = DecoratableClass.__dict__['decoratable_staticmethod']
        decorated = decorated_decorator(method)
        self.assertEqual(decorated, method)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', method),
        ])

    def test_single_positional_non_routine_non_class_arg(self, mock_test_log):
        decorated_decorator = optional_decorator_args(non_wrapped_decorator)
        decorated = decorated_decorator('non_routine_non_class')(decoratable_function)
        self.assertEqual(decorated, decoratable_function)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', decoratable_function, 'non_routine_non_class'),
        ])


@optional_decorator_args
class _ClassInitDecorator(object):
    def __init__(self, wrapped, *args, **kwargs):
        object.__init__(self)
        self.wrapped = wrapped
        test_log('__init__', self, wrapped, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)


@mock.patch(__name__ + '.test_log')
class TestClassInitDecoratorWithOptionalArgs(TestCase):
    def test_without_empty_brackets(self, mock_test_log):
        decorated = _ClassInitDecorator(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertIsInstance(decorated, _ClassInitDecorator.__wrapped__)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('__init__', decorated, decoratable_function),
            mock.call('decoratable_function', 43, kw1=1)
        ])

    def test_with_empty_brackets(self, mock_test_log):
        decorated = _ClassInitDecorator()(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertIsInstance(decorated, _ClassInitDecorator.__wrapped__)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('__init__', decorated, decoratable_function),
            mock.call('decoratable_function', 43, kw1=1)
        ])

    def test_with_args(self, mock_test_log):
        decorated = _ClassInitDecorator(42, kw0=0)(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertIsInstance(decorated, _ClassInitDecorator.__wrapped__)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('__init__', decorated, decoratable_function, 42, kw0=0),
            mock.call('decoratable_function', 43, kw1=1)
        ])


class _ClassMagicMethodDecorator(object):
    @optional_decorator_args
    def __call__(self, wrapped, *args, **kwargs):
        test_log('__call__', self, wrapped, *args, **kwargs)

        def wrapper(*wrapper_args, **wrapper_kwargs):
            test_log('wrapper', *wrapper_args, **wrapper_kwargs)
            return wrapped(*wrapper_args, **wrapper_kwargs)
        return functools.update_wrapper(wrapper, wrapped)


@mock.patch(__name__ + '.test_log')
class TestCallMagicMethodDecoratorWithOptionalArgs(TestCase):
    def setUp(self):
        self.decorator = _ClassMagicMethodDecorator()

    def test_without_empty_brackets(self, mock_test_log):
        decorated = self.decorator(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('__call__', self.decorator, decoratable_function),
            mock.call('wrapper', 43, kw1=1),
            mock.call('decoratable_function', 43, kw1=1),
        ])

    def test_with_empty_brackets(self, mock_test_log):
        decorated = self.decorator()(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('__call__', self.decorator, decoratable_function),
            mock.call('wrapper', 43, kw1=1),
            mock.call('decoratable_function', 43, kw1=1),
        ])

    def test_with_args(self, mock_test_log):
        decorated = self.decorator(42, kw0=0)(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('__call__', self.decorator, decoratable_function, 42, kw0=0),
            mock.call('wrapper', 43, kw1=1),
            mock.call('decoratable_function', 43, kw1=1),
        ])


class _InstanceMethodDecoratorOwner(object):
    # The instancemethod below behaves as a decorator in bound form.
    @optional_decorator_args
    def decorator_when_bound(self, wrapped, *args, **kwargs):
        test_log('decorator_when_bound', self, wrapped, *args, **kwargs)

        def wrapper(*wrapper_args, **wrapper_kwargs):
            test_log('wrapper', *wrapper_args, **wrapper_kwargs)
            return wrapped(*wrapper_args, **wrapper_kwargs)
        return functools.update_wrapper(wrapper, wrapped)


@mock.patch(__name__ + '.test_log')
class TestInstanceMethodDecoratorWithOptionalArgs(TestCase):
    def setUp(self):
        self.instance = _InstanceMethodDecoratorOwner()
        self.decorator = self.instance.decorator_when_bound

    def test_without_empty_brackets(self, mock_test_log):
        decorated = self.decorator(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('decorator_when_bound', self.instance, decoratable_function),
            mock.call('wrapper', 43, kw1=1),
            mock.call('decoratable_function', 43, kw1=1),
        ])

    def test_with_empty_brackets(self, mock_test_log):
        decorated = self.decorator()(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('decorator_when_bound', self.instance, decoratable_function),
            mock.call('wrapper', 43, kw1=1),
            mock.call('decoratable_function', 43, kw1=1),
        ])

    def test_with_args(self, mock_test_log):
        decorated = self.decorator(42, kw0=0)(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('decorator_when_bound', self.instance, decoratable_function, 42, kw0=0),
            mock.call('wrapper', 43, kw1=1),
            mock.call('decoratable_function', 43, kw1=1),
        ])


class _ClassMethodDecoratorOwner(object):
    # The instancemethod below behaves as a decorator in bound form.
    @optional_decorator_args
    @classmethod
    def decorator_when_bound(cls, wrapped, *args, **kwargs):
        test_log('decorator_when_bound', cls, wrapped, *args, **kwargs)

        def wrapper(*wrapper_args, **wrapper_kwargs):
            test_log('wrapper', *wrapper_args, **wrapper_kwargs)
            return wrapped(*wrapper_args, **wrapper_kwargs)
        return functools.update_wrapper(wrapper, wrapped)


@mock.patch(__name__ + '.test_log')
class TestClassMethodDecoratorWithOptionalArgs(TestCase):
    def setUp(self):
        self.cls = _ClassMethodDecoratorOwner
        self.decorator = self.cls.decorator_when_bound

    def test_without_empty_brackets(self, mock_test_log):
        decorated = self.decorator(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('decorator_when_bound', self.cls, decoratable_function),
            mock.call('wrapper', 43, kw1=1),
            mock.call('decoratable_function', 43, kw1=1),
        ])

    def test_with_empty_brackets(self, mock_test_log):
        decorated = self.decorator()(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('decorator_when_bound', self.cls, decoratable_function),
            mock.call('wrapper', 43, kw1=1),
            mock.call('decoratable_function', 43, kw1=1),
        ])

    def test_with_args(self, mock_test_log):
        decorated = self.decorator(42, kw0=0)(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('decorator_when_bound', self.cls, decoratable_function, 42, kw0=0),
            mock.call('wrapper', 43, kw1=1),
            mock.call('decoratable_function', 43, kw1=1),
        ])


class _StaticMethodDecoratorOwner(object):
    # The instancemethod below behaves as a decorator in bound form.
    @optional_decorator_args
    @staticmethod
    def decorator_when_bound(wrapped, *args, **kwargs):
        test_log('decorator_when_bound', wrapped, *args, **kwargs)

        def wrapper(*wrapper_args, **wrapper_kwargs):
            test_log('wrapper', *wrapper_args, **wrapper_kwargs)
            return wrapped(*wrapper_args, **wrapper_kwargs)
        return functools.update_wrapper(wrapper, wrapped)


@mock.patch(__name__ + '.test_log')
class TestStaticMethodDecoratorWithOptionalArgs(TestCase):
    def setUp(self):
        self.cls = _StaticMethodDecoratorOwner
        self.instance = self.cls()

    def test_class_without_empty_brackets(self, mock_test_log):
        decorated = self.cls.decorator_when_bound(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('decorator_when_bound', decoratable_function),
            mock.call('wrapper', 43, kw1=1),
            mock.call('decoratable_function', 43, kw1=1),
        ])

    def test_instance_without_empty_brackets(self, mock_test_log):
        decorated = self.instance.decorator_when_bound(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('decorator_when_bound', decoratable_function),
            mock.call('wrapper', 43, kw1=1),
            mock.call('decoratable_function', 43, kw1=1),
        ])

    def test_class_with_empty_brackets(self, mock_test_log):
        decorated = self.cls.decorator_when_bound()(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('decorator_when_bound', decoratable_function),
            mock.call('wrapper', 43, kw1=1),
            mock.call('decoratable_function', 43, kw1=1),
        ])

    def test_instance_with_empty_brackets(self, mock_test_log):
        decorated = self.instance.decorator_when_bound()(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('decorator_when_bound', decoratable_function),
            mock.call('wrapper', 43, kw1=1),
            mock.call('decoratable_function', 43, kw1=1),
        ])

    def test_class_with_args(self, mock_test_log):
        decorated = self.cls.decorator_when_bound(42, kw0=0)(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('decorator_when_bound', decoratable_function, 42, kw0=0),
            mock.call('wrapper', 43, kw1=1),
            mock.call('decoratable_function', 43, kw1=1),
        ])

    def test_instance_with_args(self, mock_test_log):
        decorated = self.instance.decorator_when_bound(42, kw0=0)(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('decorator_when_bound', decoratable_function, 42, kw0=0),
            mock.call('wrapper', 43, kw1=1),
            mock.call('decoratable_function', 43, kw1=1),
        ])


class _DecoratorArg(object):
    pass


def _custom_is_decoratable_object(obj):
    return default_is_decoratable_object(obj) and obj is not _DecoratorArg


class TestIsDecoratableObjectCallback(TestCase):
    @mock.patch('decorator_args.default_is_decoratable_object', wraps=default_is_decoratable_object)
    def test_decorator_arg_detected_as_decoratable_object_by_default_is_decoratable_object(
            self, mock_default_is_decoratable_object):
        decorated_decorator = optional_decorator_args(non_wrapped_decorator)
        # Since we pass only a single positional argument to the decorator it will call the
        # default is_decoratable_object() that returns True because _DecoratorArg is a class.
        # This means that decorated_decorator() will treat _DecoratorArg as a decoratable object
        # and not as its arguments.
        decorated = decorated_decorator(_DecoratorArg)
        mock_default_is_decoratable_object.assert_called_once_with(_DecoratorArg)
        self.assertIs(decorated, _DecoratorArg)

    @mock.patch(__name__ + '.test_log')
    @mock.patch(__name__ + '._custom_is_decoratable_object', wraps=_custom_is_decoratable_object)
    def test_decorator_arg_detected_as_arg_because_of_our_custom_is_decoratable_object_callback(
            self, mock_custom_is_decoratable_object, mock_test_log):
        decorator_with_optional_args = optional_decorator_args(is_decoratable_object=_custom_is_decoratable_object)(
            non_wrapped_decorator)
        parametrized_decorator = decorator_with_optional_args(_DecoratorArg)
        mock_custom_is_decoratable_object.assert_called_once_with(_DecoratorArg)
        self.assertIsNot(parametrized_decorator, _DecoratorArg)

        decorated = parametrized_decorator(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        mock_test_log.assert_has_calls([
            mock.call('non_wrapped_decorator', decoratable_function, _DecoratorArg),
            mock.call('decoratable_function', 43, kw1=1),
        ])


class TestParametrization(TestCase):
    def test_is_decoratable_object_must_be_none_when_optional_args_equals_false(self):
        self.assertRaisesRegexp(
            ValueError,
            re.escape('is_decoratable_object must be None when optional==False'),
            decorator_args(
                optional=False,
                is_decoratable_object=_custom_is_decoratable_object,
                keyword_only=False,
            ),
            non_wrapped_decorator,
        )

    def test_is_decoratable_object_must_be_none_when_keyword_only_args_equals_true(self):
        self.assertRaisesRegexp(
            ValueError,
            re.escape('is_decoratable_object must be None when keyword_only==True'),
            decorator_args(
                optional=True,
                is_decoratable_object=_custom_is_decoratable_object,
                keyword_only=True,
            ),
            non_wrapped_decorator,
        )


@mock.patch(__name__ + '.test_log')
class TestOptionalKeywordOnlyArgs(TestCase):
    def test_zero_positional_arg_without_empty_brackets(self, mock_test_log):
        decorated_decorator = optional_keyword_only_decorator_args(non_wrapped_decorator)
        decorated = decorated_decorator(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertEqual(decorated, decoratable_function)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', decoratable_function),
            mock.call('decoratable_function', 43, kw1=1)
        ])

    def test_zero_positional_arg_with_empty_brackets(self, mock_test_log):
        decorated_decorator = optional_keyword_only_decorator_args(non_wrapped_decorator)
        # empty brackets to pass no args to the decorator
        decorated = decorated_decorator()(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertEqual(decorated, decoratable_function)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', decoratable_function),
            mock.call('decoratable_function', 43, kw1=1)
        ])

    def test_one_positional_arg_is_treated_as_decoratable_object_regardless_of_its_type(self, mock_test_log):
        decorated_decorator = optional_keyword_only_decorator_args(non_wrapped_decorator)
        # decorated_decorator decorates the passed 1 instead of treating it as a decorator arg
        self.assertRaises(TypeError, decorated_decorator(1), decoratable_function)

    def test_two_or_more_positional_args_are_treated_as_error(self, mock_test_log):
        decorated_decorator = optional_keyword_only_decorator_args(non_wrapped_decorator)
        self.assertRaisesRegexp(TypeError, re.escape('This decorator receives only keyword arguments'),
                                decorated_decorator, 1, 2)
        self.assertRaisesRegexp(TypeError, re.escape('This decorator receives only keyword arguments'),
                                decorated_decorator, 1, 2, 3)

    def test_one_positional_arg_with_keyword_args_fails(self, mock_test_log):
        decorated_decorator = optional_keyword_only_decorator_args(non_wrapped_decorator)
        self.assertRaisesRegexp(TypeError, re.escape('This decorator receives only keyword arguments'),
                                decorated_decorator, 1, kw0=0)

    def test_kwonly_args_work(self, mock_test_log):
        decorated_decorator = optional_keyword_only_decorator_args(non_wrapped_decorator)
        # empty brackets to pass no args to the decorator
        decorated = decorated_decorator(kw5=5, kw6=6)(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertEqual(decorated, decoratable_function)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', decoratable_function, kw5=5, kw6=6),
            mock.call('decoratable_function', 43, kw1=1)
        ])


@mock.patch(__name__ + '.test_log')
class TestNonOptionalDecoratorArgs(TestCase):
    """ Testing the @decorator_args decorator with optional=False setting. """
    def test_zero_positional_arg_without_empty_brackets_fails(self, mock_test_log):
        decorated_decorator = decorator_args(non_wrapped_decorator)
        # Since the decorator arguments aren't optional decorated_decorator receives
        # decoratable_function as a decorator argument and not as a decoratable object.
        parametrized_decorator = decorated_decorator(decoratable_function)
        self.assertIsNot(parametrized_decorator, decoratable_function)

        decorated = parametrized_decorator(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertEqual(decorated, decoratable_function)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', decoratable_function, decoratable_function),
            mock.call('decoratable_function', 43, kw1=1)
        ])

    def test_zero_positional_arg_with_empty_brackets(self, mock_test_log):
        decorated_decorator = decorator_args(non_wrapped_decorator)
        decorated = decorated_decorator()(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertEqual(decorated, decoratable_function)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', decoratable_function),
            mock.call('decoratable_function', 43, kw1=1)
        ])

    def test_keyword_only_args(self, mock_test_log):
        decorated_decorator = decorator_args(keyword_only=True)(non_wrapped_decorator)
        decorated = decorated_decorator(kw2=2)(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertEqual(decorated, decoratable_function)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', decoratable_function, kw2=2),
            mock.call('decoratable_function', 43, kw1=1)
        ])

    def test_positional_args_fail_when_keyword_only_equals_true(self, mock_test_log):
        decorated_decorator = decorator_args(keyword_only=True)(non_wrapped_decorator)
        self.assertRaisesRegexp(
            TypeError,
            re.escape('This decorator receives only keyword arguments'),
            decorated_decorator,
            'positional_arg',
        )


class TestKeywordOnlyDecoratorArgs(TestCase):
    """ Testing the @keyword_only_decorator_args decorator. """
    def test_positional_args_fail(self):
        decorated_decorator = keyword_only_decorator_args(non_wrapped_decorator)
        self.assertRaisesRegexp(TypeError, re.escape('This decorator receives only keyword arguments'),
                                decorated_decorator, 'positional_argument')

    @mock.patch(__name__ + '.test_log')
    def test_keyword_args_work(self, mock_test_log):
        decorated_decorator = keyword_only_decorator_args(non_wrapped_decorator)
        decorated = decorated_decorator(kw2=2)(decoratable_function)
        result = decorated(43, kw1=1)
        self.assertEqual(result, 'result')
        self.assertEqual(decorated, decoratable_function)
        self.assertListEqual(mock_test_log.mock_calls, [
            mock.call('non_wrapped_decorator', decoratable_function, kw2=2),
            mock.call('decoratable_function', 43, kw1=1)
        ])
