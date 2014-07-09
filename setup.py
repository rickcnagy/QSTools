#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

from distutils.core import setup
import os

os.chdir('./modules')

setup(
    name='QSTools',
    version='1.0',
    description='A suite of tools for programmatically interacting with the QuickSchools API and GUI.',
    author='Rick Nagy (QuickSchools.com)',
    url='https://github.com/br1ckb0t/QSTools',
    packages=['qs'])
