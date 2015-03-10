#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

from setuptools import setup, find_packages
from distutils.core import setup
import os

os.chdir('./modules')

setup(
    name='QSTools',

    version='1.0',

    description='Tools for controlling the QuickSchools API and GUI.',

    author='Rick Nagy (QuickSchools.com)',

    url='https://github.com/br1ckb0t/QSTools',

    packages=['qs'],

    install_requires=[
        'unidecode>=0.04.17',
        'reindent>=0.1.1',
        'requests>=2.5.3',
        'chardet>=2.3.0',
        'nose>=1.3.3'
    ],
)
