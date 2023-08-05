from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='metcalculator',
    version='1.4.4',
    description='Calculate various meteorological parameters',
    url='www.metpod.co.uk',
    license='MIT',
    author='Mark Baker',
    author_email='mark2182@mac.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
          'gui_scripts': [
               'metcalculator = metcalculator.__main__:main'
          ]
    },
)
