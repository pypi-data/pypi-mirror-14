#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-staticfiles-dotd',

    url="https://chris-lamb.co.uk/projects/django-staticfiles-dotd",
    version='1.3.1',
    description="Django staticfiles adaptor to concatentate .d-style"
        " directories",

    author="Chris Lamb",
    author_email="chris@chris-lamb.co.uk",
    license="BSD",

    packages=find_packages(),
    install_requires=(
        'Django>=1.9.0',
        'monkeypatch==0.1rc3',
    ),
)
