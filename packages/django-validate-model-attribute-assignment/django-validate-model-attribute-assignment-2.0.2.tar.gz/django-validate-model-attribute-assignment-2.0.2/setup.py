#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-validate-model-attribute-assignment',

    url="https://chris-lamb.co.uk/projects/django-validate-model-attribute-assignment",
    version='2.0.2',
    description="Prevent typos and other errors when assigning attributes to Django model instances",

    author="Chris Lamb",
    author_email="chris@chris-lamb.co.uk",
    license="BSD",

    packages=find_packages(),

    install_requires=(
        'Django>=1.8',
    ),
)
