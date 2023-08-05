#!/usr/bin/python

import os
from setuptools import setup

def get_long_description():
	return open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

setup(name='vesna-alhauthproxy',
      version='1.0.6',
      description='ALH authorization proxy for OMF',
      license='GPL',
      long_description=get_long_description(),
      author='Tomaz Solc',
      author_email='tomaz.solc@ijs.si',

      packages = [ 'vesna', 'vesna.omf' ],

      namespace_packages = [ 'vesna' ],

      entry_points = {
	      'console_scripts': [
		      'vesna_alh_auth_proxy=vesna.omf.proxy:main',
	      ]
      },

      data_files = [
	      ('/etc/init.d', ['vesna_alh_auth_proxy']),
      ],

      install_requires = [ 'vesna-alhtools', 'requests-unixsocket', 'python-daemon' ],

      test_suite = 'test',
)
