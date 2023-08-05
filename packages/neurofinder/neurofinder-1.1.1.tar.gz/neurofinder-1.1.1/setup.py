#!/usr/bin/env python

from setuptools import setup, find_packages

version = '1.1.1'

required = open('requirements.txt').read().split('\n')

setup(
    name='neurofinder',
    version=version,
    description='evaluate neuron finding algorithms',
    author='freeman-lab',
    author_email='the.freeman.lab@gmail.com',
    url='https://github.com/freeman-lab/neurofinder-python',
    packages=find_packages(),
    install_requires=required,
    entry_points = {"console_scripts": ['neurofinder = neurofinder.cli:cli']},
    long_description='See ' + 'https://github.com/freeman-lab/neurofinder-python',
    license='MIT'
)
