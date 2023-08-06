# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='decorator-args',
    version='1.0',
    description='Optional/required/keyword-only decorator arguments made easy.',
    keywords='optional required keyword only decorator arguments args',

    url='https://github.com/pasztorpisti/decorator-args',

    license='MIT',

    author='István Pásztor',
    author_email='pasztorpisti@gmail.com',

    classifiers=[
        'License :: OSI Approved :: MIT License',

        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    py_modules=['decorator_args'],
    test_suite='tests',
    tests_require=['mock'],
)
