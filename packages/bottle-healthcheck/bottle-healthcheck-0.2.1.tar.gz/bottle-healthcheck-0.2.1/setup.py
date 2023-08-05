#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='bottle-healthcheck',
      version='0.2.1',
      description='Adds healthcheck endpoints to Bottle apps',
      author='Frank Stratton',
      author_email='frank@runscope.com',
      maintainer='Iuri de Silvio',
      maintainer_email='iurisilvio@gmail.com',
      url='https://github.com/iurisilvio/bottle-healthcheck',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      license='MIT',
      platforms='any',
      install_requires=[],
      test_requires=['bottle', 'webtest'],
      test_suite='test_healthcheck',
      classifiers=('Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Bottle',
                   'Programming Language :: Python'))
