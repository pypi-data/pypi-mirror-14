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

test_requirements = [
    "pytest"
]

setup(
    name='config_edit',
    version='0.0.1',
    description="Library to work with config files of various applications",
    long_description=readme + '\n\n' + history,
    author="Hamza Sheikh",
    author_email='code@codeghar.com',
    url='https://github.com/hamzasheikh/config_edit',
    packages=[
        'config_edit',
    ],
    package_dir={'config_edit':
                 'config_edit'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='config_edit',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
