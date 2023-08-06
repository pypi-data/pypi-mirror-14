# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='apio',
    author='Jesús Arroyo Torrens',
    email='jesus.jkhlg@gmail.com',
    version='0.1',
    packages=['apio', 'examples'],
    package_data={
        'apio': ['SConstruct',
                 'packages/*.py',
                 'packages/*.rules'],
        'examples': ['*/*']
    },
    include_package_data=True,
    install_requires=[
        'click',
        'requests'
    ],
    entry_points={
        'console_scripts': ['apio=apio:cli']
    },
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                 'Programming Language :: Python']
)
