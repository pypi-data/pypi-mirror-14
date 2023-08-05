#!/usr/bin/env python

from distutils.core import setup

setup(
    name='mujoco-py',
    version='0.2.4',
    description='Python wrapper for Mojoco',
    author='OpenAI',
    packages=['mujoco_py'],
    package_data={
        'mujoco_py': ['vendor/*/*/*']
    },
    install_requires=[
        'PyOpenGL>=3.1.0',
        'numpy>=1.10.4'
    ],
    tests_requires=[
        'nose2'
    ]
)
