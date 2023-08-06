#!/usr/bin/env python

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='pytest-pride',
    license='MIT',
    description='Minitest-style test colors',
    author='Devon Meunier',
    author_email='devon.meunier@gmail.com',
    url='https://github.com/meunierd/pytest-pride',
    long_description=read("README.md"),
    version='0.1.2',
    py_modules=['pytest_pride'],
    entry_points={'pytest11': ['pride = pytest_pride']},
    install_requires=['pytest>=2.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ]
)
