from setuptools import setup, find_packages
from os import path
import codecs
import os
import re

here = path.abspath(path.dirname(__file__))

setup(
    name='metarmonitor',
    version='0.7.9',
    description='Monitor METAR and TAF reports',
    url='www.metpod.co.uk',
    license='MIT',
    author='Mark Baker',
    author_email='mark2182@mac.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['pillow', 'requests', 'twilio', 'apscheduler'],
    package_data={
        '': ['images/*.gif'],
    },
    entry_points={
          'gui_scripts': [
               'metarmonitor = metarmonitor.__main__:main'
          ]
    },
)
