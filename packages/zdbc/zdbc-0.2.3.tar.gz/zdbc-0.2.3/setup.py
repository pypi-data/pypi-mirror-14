#!/usr/bin/env python

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='zdbc',
      version='0.2.3',
      description='Zscheile DataBase Management',
      author='Erik Kai Alain Zscheile',
      author_email='erik.zscheile.ytrizja@gmail.com',
      license='GPL-3',
      packages=['zdbc'],
      entry_points = {
          'console_scripts': [
              'zdbc=zdbc.cmdzdbc:main'
            ],
        },
      )
