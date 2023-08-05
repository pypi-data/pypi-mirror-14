#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'fitsio',
]

test_requirements = [
    'pytest',
    'numpy',
]

setup(
    name='fitsiochunked',
    version='0.0.5',
    description="Package to efficiently read large fits arrays in object by object",
    long_description=readme,
    author="Simon Walker",
    author_email='s.r.walker101@googlemail.com',
    url='https://github.com/mindriot101/fitsiochunked',
    py_modules=['fitsiochunked'],
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='fitsiochunked',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='testing',
    tests_require=test_requirements,
    setup_requires=['pytest-runner'],
)
