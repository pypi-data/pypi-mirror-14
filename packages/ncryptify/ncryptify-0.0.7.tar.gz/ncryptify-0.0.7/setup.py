#!/usr/bin/env python

from distutils.core import setup

requirements=['bson>=0.4.1', 'requests>=2.2.1', 'pyjwt>=1.4.0', 'cryptography>=1.0.2', 'validators>=0.8',
              'bottle>=0.12.8', 'bottle_beaker>=0.1.0', 'python_slugify>=1.1.4', 'beaker>=1.7.0',
              'jinja2>=2.8', 'uuid>=1.30']

setup(name='ncryptify',
      version='0.0.7',
      description='ncryptify client library',
      long_description='Client library for the ncryptify service',
      author='SafeNet Labs',
      author_email='support@ncryptify.com',
      url='https://www.ncryptify.com',
      license='MIT',
      packages=['ncryptify'],
      install_requires=requirements
      )

