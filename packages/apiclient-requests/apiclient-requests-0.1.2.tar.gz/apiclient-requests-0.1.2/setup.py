# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='apiclient-requests',
    version='0.1.2',
    packages=[
        'apiclient',
    ],
    author='Suraj Arya',
    author_email='suraj.p.arya@gmail.com',
    description='A simple python base package for building good api clients on',
    url='https://github.com/suraj-arya/apiclient-requests',
    license='MIT',

    install_requires=[
        "requests==2.5.1"
    ],
)
