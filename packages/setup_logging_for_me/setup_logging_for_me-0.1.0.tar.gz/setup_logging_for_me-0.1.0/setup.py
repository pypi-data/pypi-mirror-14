#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]


setup(
    name='setup_logging_for_me',
    version='0.1.0',
    description="I never remember how to do basic config",
    long_description=readme + '\n\n' + history,
    author="Javier Andrés Mansilla",
    author_email='javimansilla@gmail.com',
    url='https://github.com/jmansilla/setup_logging_for_me',
    packages=[
        'setup_logging_for_me',
    ],
    package_dir={'setup_logging_for_me':
                 'setup_logging_for_me'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='setup_logging_for_me',
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
)
