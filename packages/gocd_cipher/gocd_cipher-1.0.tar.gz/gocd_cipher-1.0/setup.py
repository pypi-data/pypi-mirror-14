#!/usr/bin/env python

from distutils.core import setup

setup(name='gocd_cipher',
      version='1.0',
      description='A tool to encrypt, decrypt and recypher secrets encrypted with GoCD\'s inbuilt encryption utility',
      author='Connor Shearwood',
      author_email='connor.shearwood@springer.com',
      packages=['gocd_cipher'],
      install_requires=[
          "PyCrypto"
      ],
      entry_points={
          'console_scripts': ['gocd_cipher=gocd_cipher.utility:utility'],
      }
 )
