#!/usr/bin/env python

#
# This file is part of TensorToolbox.
#
# TensorToolbox is free software: you can redistribute it and/or modify
# it under the terms of the LGNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TensorToolbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LGNU Lesser General Public License for more details.
#
# You should have received a copy of the LGNU Lesser General Public License
# along with TensorToolbox.  If not, see <http://www.gnu.org/licenses/>.
#
# DTU UQ Library
# Copyright (C) 2014-2016 The Technical University of Denmark
# Scientific Computing Section
# Department of Applied Mathematics and Computer Science
#
# Author: Daniele Bigoni
#

import os.path
import sys, getopt, re
from setuptools import setup, find_packages
import pip

def deps_install(package):
    try:
        pip.main(['install', '--no-binary', 'all', package])
    except Exception as e:
        print("Unable to install %s using pip. \
              Please read the instructions for \
              manual installation.. Exiting" % package)
        exit(2)

deps_install('Cython')
deps_install('numpy')
deps_install('scipy')
deps_install('SpectralToolbox')
deps_install('Sphinx')
deps_install('prettytable')
deps_install('h5py')
deps_install('matplotlib')
deps_install('UQToolbox')
deps_install('mpi4py')
deps_install('mpi_map')

import numpy as np

local_path = os.path.split(os.path.realpath(__file__))[0]
version_file = os.path.join(local_path, 'TensorToolbox/_version.py')
version_strline = open(version_file).read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, version_strline, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (version_file,))

setup(name = "TensorToolbox",
      version = version,
      packages=find_packages(),
      include_package_data=True,
      scripts=["scripts/TensorToolboxUpV030"],
      url="http://www.limitcycle.it/dabi/",
      author = "Daniele Bigoni",
      author_email = "dabi@limitcycle.it",
      license="COPYING.LESSER",
      description="Tools for the decomposition of tensors",
      long_description=open("README.txt").read(),
      zip_safe = False,         # I need this for MPI purposes
      include_dirs=[np.get_include()]
      )
