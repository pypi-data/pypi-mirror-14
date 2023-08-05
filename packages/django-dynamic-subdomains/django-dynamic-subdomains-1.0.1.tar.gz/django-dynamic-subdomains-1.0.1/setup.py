#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-dynamic-subdomains',
    description="Dynamic and static subdomain support for Django.",
    version='1.0.1',
    url='https://chris-lamb.co.uk/projects/django-dynamic-subdomains/',

    author="Chris Lamb",
    author_email='chris@chris-lamb.co.uk',
    license='BSD',

    packages=find_packages(),

    install_requires=(
        'Django>=1.8',
        'monkeypatch==0.1rc3',
    ),
)
