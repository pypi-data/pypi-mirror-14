#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-pedantic-http-methods',
    description="Raises an exception when attempting to perform side effects "
        "in GET and HEAD HTTP methods.",
    version='1.0.3',
    url='https://chris-lamb.co.uk/projects/django-pedantic-http-methods',

    author='Chris Lamb',
    author_email='chris@chris-lamb.co.uk',
    license='BSD',

    packages=find_packages(),

    install_requires=(
        'Django>=1.8',
    ),
)
