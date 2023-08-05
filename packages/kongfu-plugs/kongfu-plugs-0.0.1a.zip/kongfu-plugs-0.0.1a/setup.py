__doc__ = """
=====================
Plugs Introduction
=====================
:Author: Uniyes.com
.. contents::
About Plugs
----------------
Plugs is a collection project for kongfu project. So you can use any app of it
to compose your project.
License
------------
Plugs is released under MIT license. Of cause if there are some third party
apps not written by Uniyes.com, it'll under the license of itself.
"""

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
    # note: no find_packges function in distutils

with open('README.rst') as file_readme:
    readme = file_readme.read()

setup(name='kongfu-plugs',
      version='0.0.1a',
      description='Plugs is a collection project for kongfu project',
      long_description=readme,
      author='Uniyes.com',
      author_email='company@Uniyes.com',
      license='MIT',
      url='https://git.oschina.net/uniyes/kongfu-plugs',
      keywords='please don\'t use this library for anything',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      zip_safe=False,
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',

      ],
)