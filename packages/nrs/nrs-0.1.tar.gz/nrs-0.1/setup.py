#!/usr/bin/env python

from setuptools import setup, Extension

bzlib = Extension('nrs.ext._bzlib', [
    'nrs/ext/bzlib.i',
    'nrs/ext/bzlib.c',
    'nrs/ext/decompress.c',
    'nrs/ext/huffman.c'
])

setup(name='nrs',
      version='0.1',
      description='NSIS Reversing Suite',
      author='isra17',
      author_email='isra017@gmail.com',
      url='https://github.com/isra17/nrs',
      packages=['nrs','nrs.ext'],

      install_requires=['future'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      ext_modules=[bzlib]
    )

