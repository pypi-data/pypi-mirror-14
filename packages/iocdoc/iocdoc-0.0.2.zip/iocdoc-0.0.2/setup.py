#!/usr/bin/env python

# Copyright (c) 2009 - 2015, UChicago Argonne, LLC.
# See LICENSE file for details.


from setuptools import setup, find_packages
import os
import re
import sys
import versioneer

# pull in some definitions from the package's __init__.py file
sys.path.insert(0, os.path.join('src', ))
import iocdoc

requires = iocdoc.__requires__
packages = find_packages()
verbose=1
long_description = open('README.rst', 'r').read()


setup (
    name             = iocdoc.__package_name__,        # iocdoc
    license          = iocdoc.__license__,
    version          = versioneer.get_version(),
    cmdclass         = versioneer.get_cmdclass(),
    description      = iocdoc.__description__,
    long_description = long_description,
    author           = iocdoc.__author_name__,
    author_email     = iocdoc.__author_email__,
    url              = iocdoc.__url__,
    download_url     = iocdoc.__download_url__,
    keywords         = iocdoc.__keywords__,
    install_requires = requires,
    platforms        = 'any',
    package_dir      = {'': 'src'},
    #packages         = find_packages(),
    packages         = [str(iocdoc.__package_name__), ],
    package_data     = dict(iocdoc=['resources/*', 'LICENSE', ]),
    classifiers      = iocdoc.__classifiers__,
    entry_points={
       # create & install console_scripts in <python>/bin
       'console_scripts': ['iocdoc = iocdoc.ioc:main'],
       #'gui_scripts': ['iocdoc = iocdoc:main'],
       },
      )
