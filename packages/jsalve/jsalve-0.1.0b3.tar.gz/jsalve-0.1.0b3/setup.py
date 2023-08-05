#!/usr/bin/env python3
import os
from setuptools import setup, find_packages


def get_readme():
    return open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    author="Julio Gonzalez Altamirano",
    author_email='devjga@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
    ],
    description="JSON API utilities for Python applications.",
    install_requires=['django', 'inflection'],
    keywords="django rest json json-api jsonapi",
    license="MIT",
    long_description=get_readme(),
    name='jsalve',
    packages=find_packages(include=['jsalve', 'jsalve.*'], exclude=['tests', 'tests.*']),
    platforms=['Any'],
    url='https://github.com/symfonico/jsalve',
    version='0.1.0b3',
)
