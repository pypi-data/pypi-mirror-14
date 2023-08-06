#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pip.req import parse_requirements

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [str(ir.req) for ir in parse_requirements('requirements.txt', session=False)]

test_requirements = [str(ir.req) for ir in parse_requirements('requirements_dev.txt', session=False)]

setup(
    name='yagocd',
    version='0.1.1',
    description="Yet another Python client for ThoughtWorks GOCD REST API.",
    long_description=readme + '\n\n' + history,
    author="Grigory Chernyshev",
    author_email='systray@yandex.ru',
    url='https://github.com/grundic/yagocd',
    packages=[
        'yagocd',
    ],
    package_dir={'yagocd': 'yagocd'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='yagocd',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
