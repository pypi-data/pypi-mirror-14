#!/usr/bin/env python

#
# This file is part of UQToolbox.
#
# UQToolbox is free software: you can redistribute it and/or modify
# it under the terms of the LGNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# UQToolbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LGNU Lesser General Public License for more details.
#
# You should have received a copy of the LGNU Lesser General Public License
# along with UQToolbox.  If not, see <http://www.gnu.org/licenses/>.
#
# DTU UQ Library
# Copyright (C) 2014 The Technical University of Denmark
# Scientific Computing Section
# Department of Applied Mathematics and Computer Science
#
# Author: Daniele Bigoni
#


import os.path
import sys, re
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import pip

global include_dirs
include_dirs = []

deps_list = ['numpy', 'orthpol', 'scipy',
             'Sphinx', 'sphinxcontrib-bibtex',
             'SpectralToolbox', 'prettytable']
if "--without-mpi4py" in sys.argv:
    idx = sys.argv.index('--without-mpi4py')
    del sys.argv[idx]
else:
    deps_list.extend(['mpi4py', 'mpi_map'])

def deps_install():
    for package in deps_list:
        print("[DEPENDENCY] Installing %s" % package)
        try:
            pip.main(['install', '--no-binary', ':all:', '--upgrade', package])
        except Exception as e:
            print("[Error] Unable to install %s using pip." +
                  "Please read the instructions for " +
                  "manual installation... Exiting" % package)
            raise e
            exit(2)

class UQToolbox_install(install):
    def run(self):
        deps_install()
        import numpy as np
        include_dirs.append(np.get_include())
        install.run(self)

class UQToolbox_develop(develop):
    def run(self):
        deps_install()
        import numpy as np
        include_dirs.append(np.get_include())
        develop.run(self)

local_path = os.path.split(os.path.realpath(__file__))[0]
version_file = os.path.join(local_path, 'UQToolbox/_version.py')
version_strline = open(version_file).read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, version_strline, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (version_file,))

setup(name = "UQToolbox",
      version = version,
      packages=find_packages(),
      include_package_data=True,
      scripts=[],
      url="http://www2.compute.dtu.dk/~dabi/",
      author = "Daniele Bigoni",
      author_email = "dabi@dtu.dk",
      license="COPYING.LESSER",
      description="Tools for Uncertainty Quantification",
      long_description=open("README.txt").read(),
      zip_safe = False,                      # For Debug purposes
      cmdclass={'install': UQToolbox_install,
                'develop': UQToolbox_develop},
      include_dirs=include_dirs
      )
