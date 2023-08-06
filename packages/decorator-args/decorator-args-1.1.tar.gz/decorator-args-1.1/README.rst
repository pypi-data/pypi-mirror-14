==============
decorator-args
==============

Optional/required/keyword-only decorator arguments made easy.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


.. image:: https://img.shields.io/travis/pasztorpisti/decorator-args.svg?style=flat
    :target: https://travis-ci.org/pasztorpisti/decorator-args
    :alt: build

.. image:: https://img.shields.io/codacy/0e4f7e6a2823485ba20496c7c96a42e7/master.svg?style=flat
    :target: https://www.codacy.com/app/pasztorpisti/decorator-args
    :alt: code quality

.. image:: https://landscape.io/github/pasztorpisti/decorator-args/master/landscape.svg?style=flat
    :target: https://landscape.io/github/pasztorpisti/decorator-args/master
    :alt: code health

.. image:: https://img.shields.io/coveralls/pasztorpisti/decorator-args/master.svg?style=flat
    :target: https://coveralls.io/r/pasztorpisti/decorator-args?branch=master
    :alt: coverage

.. image:: https://img.shields.io/pypi/v/decorator-args.svg?style=flat
    :target: https://pypi.python.org/pypi/decorator-args
    :alt: pypi

.. image:: https://img.shields.io/github/tag/pasztorpisti/decorator-args.svg?style=flat
    :target: https://github.com/pasztorpisti/decorator-args
    :alt: github

.. image:: https://img.shields.io/github/license/pasztorpisti/decorator-args.svg?style=flat
    :target: https://github.com/pasztorpisti/decorator-args/blob/master/LICENSE.txt
    :alt: license: MIT


This mini-library is far from being revolutionary or essential but its features may come in handy for some.
It is a chaotic set of ideas and features that I don't really feel to be rock solid but I think it isn't an
unforgivable guilt to release it to the wild. In worst case you can open a "Please destruct this code/library"
issue on its github page.


.. contents::


Installation
============

.. code-block:: sh

    pip install decorator-args

Alternatively you can download the distribution from the following places:

- https://pypi.python.org/pypi/decorator-args#downloads
- https://github.com/pasztorpisti/decorator-args/releases


Usage
=====


Problem to solve
----------------

The following code snippet shows two examples:

1. Applying a decorator called ``argless``  without any arguments.
2. Applying a decorator called ``argful`` that receives arguments before applying it.

.. code-block:: python

    #1
    @argless
    def decorated_function():
        ...

    #2
    @argful('arg1_value', arg2='arg2_value')
    def decorated_function():
        ...


This library tries to make it easier to implement decorators that receive arguments (like ``argful_decorator`` above).
Besides this it has some related extra features to offer (optional and keyword-only decorator args).


How this library helps
----------------------

The previously used ``argful`` decorator can be implemented in countless ways but the two most standard ways to do it
without this library looks like this:

1. "Inception-style" implementation as a function:

.. code-block:: python

    def argful(arg1, arg2='arg2_default'):
        # TODO: Validate and pre-process decorator args as early as possible for easier debugging
        def decorate(decoratable):
            @functools.wraps(decoratable)
            def wrapper(*args, **kwargs):
                # TODO: Manipulate the input and output of the wrapped
                # decoratable object and use arg1 and arg2 if you want...
                return decoratable(*args, **kwargs)
            return wrapper
        return decorate


2. Implementation as a class:

.. code-block:: python

    class argful(object):
        def __init__(self, arg1, arg2='arg2_default'):
            # TODO: Validate and pre-process decorator args as early as possible for easier debugging
            self.arg1 = arg1
            self.arg2 = arg2

        def __call__(self, decoratable):
            @functools.wraps(decoratable)
            def wrapper(*args, **kwargs)
                # TODO: Manipulate the input and output of the wrapped
                # decoratable object and use self.arg1 and self.arg2 if you want...
                return decoratable(*args, **kwargs)
            return wrapper


The ``decorator_args.decorator_args`` decorator provided by this library can remove a level of indirection from the
"Inception-style" implementation seen in example #1 making the code simpler and more readable:

.. code-block:: python

    from decorator_args import decorator_args


    @decorator_args
    def argful(decoratable, arg1, arg2='arg2_default'):
        @functools.wraps(decoratable)
        def wrapper(*args, **kwargs):
            # TODO: Manipulate the input and output of the wrapped
            # decoratable object and use arg1 and arg2 if you want...
            return decoratable(*args, **kwargs)
        return wrapper


At the same time this library offers the following extra features:

- It can force keyword-only argument passing for your decorator. In some cases this is desirable because it can make
  code easier to read and understand:

.. code-block:: python

    # Decorator implementation with keyword-only decorator arguments:
    @decorator_args(keyword_only=True)
    def argful(decoratable, arg1, arg2='arg2_default'):
        ...


    # This would fail with a ``TypeError('This decorator receives only keyword arguments')``
    @argful('arg1_value', arg2='arg2_value')
    def decorated_function():
        ...


    # This is OK because all args are passed as keyword args
    @argful(arg1='arg1_value', arg2='arg2_value')
    def decorated_function():
        ...

- If your decorator doesn't have required arguments and you use the ``optional`` feature of this library than you can
  apply your decorator without an argument list when you don't want to pass any args to it:

.. code-block:: python

    # Decorator implementation with optional argument list:
    # Note that our decorator doesn't have required args other than the decoratable object:
    @decorator_args(optional=True)
    def argful(decoratable, arg1='arg1_default', arg2='arg2_default'):
        ...


    # This works because of using `optional=True` above:
    @argful
    def decorated_function():
        ...


    # This would work even without `optional=True` in our decorator implementation:
    @argful()
    def decorated_function():
        ...


    # Of course passing actual args also works as expected:
    @argful('arg1_value', 'arg2_value')
    def decorated_function():
        ...


Library interface
=================

The library offers a ``decorator_args.decorator_args`` decorator that is the main "workhorse" of the library and a
set of other decorators that are just convenience helpers around the previously mentioned main decorator.
Syntax-wise the arguments of these decorators are optional and keyword-only.


Main "entrypoint"
-----------------

decorator_args.\ **decorator_args**\ *(\*, keyword_only=False, optional=False, is_decoratable_object=None)*

    The main decorator of the library. All other decorators are just convenience helpers based on this one.

    - ``keyword_only``: Makes the arguments of your decorator keyword-only. Passing any positional arguments to your
      decorator will result in a ``TypeError`` with an appropriate error message.
    - ``optional``: ``optional=True`` allows you to write ``@your_decorator`` instead of ``@your_decorator()``.
      When you apply your decorator without passing any args to it you can omit the empty brackets
      that specify the empty decorator argument list.
    - ``is_decoratable_object``: This argument can be used only when ``keyword_only=False`` and ``optional=True``.
      When the argument list of your decorator is optional and you apply your decorator by passing only a single
      positional argument to the decorator this library has hard time to decide whether that single positional argument
      is an optional decorator argument or a decoratable object. This decision is made by the library function
      ``decorator_args.default_is_decoratable_object(obj)`` function which returns ``True`` if the given single
      positional argument is a function, method, or class. This default behavior is good in most of the cases when
      your decorator receives only simple arguments like integers, strings, bools, etc... However if your decorator
      can receive a single positional argument that can be a function, method, or class, then the default behavior
      isn't suitable. There are several workarounds to this problem, one of them is providing your own
      ``is_decoratable_object(obj)`` implementation through the currently documented decorator argument. You probably
      have additional info to make an accurate distinction between decorator arguments and decoratable objects to
      provide a working ``is_decoratable_object(obj)`` implementation.

      In such pathological edge-cases you can also use the following workarounds besides the previously documented
      custom ``is_decoratable_object(obj)`` implementation:

        - When you apply your decorator with only a single argument that is a function/method/class you can
          pass the argument as a keyword-argument. This way it will be detected as a decorator argument for sure.
          This is however just a dirty hack that still leaves chance for the users of your decorator to make an
          error. This can result in long debugging sessions.
        - You can make your optional arguments keyword-only with ``keyword_only=True``.
          This completely eliminates the problem.
        - Don't make the argument list of this decorator optional. With a required decorator argument list this
          problem isn't present.


Helpers: convenience API
------------------------

The convenience API provides a set of decorators that are just "wrappers" around the main
``decorator_args.decorator_args`` decorator. These convenience decorators just bind some of the main decorator
arguments to some constants.


decorator_args.\ **optional_decorator_args**\ *(\*, keyword_only=False, is_decoratable_object=None)*

    Works just like the main ``decorator_args.decorator_args`` decorator with ``optional=True``.

decorator_args.\ **keyword_only_decorator_args**\ *(\*, optional=False)*

    Works just like the main ``decorator_args.decorator_args`` decorator with ``keyword_only=True``.

decorator_args.\ **optional_keyword_only_decorator_args**\ *()*

    Works just like the main ``decorator_args.decorator_args`` decorator with ``optional=True`` and
    ``keyword_only=True``.


Implementing your decorators in a "twisted" way
===============================================

The tricky implementation of the library ensures that the decorators provided by this library can be applied to your
decorators even in some exotic cases:

    - `When your decorator is a bound instance/class/static method`_
    - `When your decorator is a bound __call__ magic (instance)method`_


When your decorator is a bound instance/class/static method
-----------------------------------------------------------

.. code-block:: python

    class AnyClass(object):
        @decorator_args
        def decorator_when_bound(self, decoratable, arg1, arg2):
            ...

        # It is important to apply @decorator_args after @classmethod!
        @decorator_args
        @classmethod
        def decorator_when_bound_2(cls, decoratable, arg1, arg2):
            ...

        # It is important to apply @decorator_args after @statimethod!
        @decorator_args
        @staticmethod
        def decorator_when_bound_3(decoratable, arg1, arg2):
            ...


    any_class_instance = AnyClass()

    decorator_with_args = any_class_instance.decorator_when_bound
    decorator_with_args_2 = AnyClass.decorator_when_bound_2
    decorator_with_args_3a = any_class_instance.decorator_when_bound_3
    decorator_with_args_3b = AnyClass.decorator_when_bound_3


When your decorator is a bound __call__ magic (instance)method
--------------------------------------------------------------

.. code-block:: python

    class AnyClass(object):
        @decorator_args
        def __call__(self, decoratable, arg1, arg2):
            ...


    # Because of the syntactic sugar provided by python it is as simple as:
    decorator_with_args = AnyClass()
