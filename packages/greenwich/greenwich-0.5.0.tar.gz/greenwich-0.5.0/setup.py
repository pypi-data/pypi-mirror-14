#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# FIXME: use "gdal-config --cflags" to introspect the directory containing
# headers. Patch here to avoid the need for "MAKEFLAGS=... pip install", but
# this should eventually to in upstream GDAL setup.py.
setup(name='greenwich',
      version='0.5.0',
      description='A GDAL wrapper with Python conveniences',
      long_description=open('README.rst').read(),
      author='Brian Galey',
      author_email='bkgaley@gmail.com',
      url='https://github.com/bkg/greenwich',
      packages=['greenwich'],
      install_requires=['GDAL', 'numpy', 'Pillow'],
      license='BSD',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
      ],
      test_suite='tests')
