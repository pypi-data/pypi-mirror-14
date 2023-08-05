==================================
Uncertainty Quantification Toolbox
==================================

This is a collection of tools for Uncertainty Quantification

Features:
 - Sampling methods (Monte Carlo, Latin Hypercube, Quasi Monte Carlo) with MPI support
 - Tools for Generalized Polynomial Chaos
 - Probabilistic Collocation Method
 - Multi-element Probabilistic Collocation Method
 - High Dimensional Model Representation
 - ANOVA
 - Global Sensitivity (Total Sensitivity Indices)
 - Model reduction (Karhunen–Loève expansion)

Requirements
============
Some parts of the software require the `SpectralToolbox <https://pypi.python.org/pypi/SpectralToolbox/>`_. The package has automatically MPI support through `mpi4py <https://pypi.python.org/pypi/mpi4py/>`_ and `mpi_map <https://pypi.python.org/pypi/mpi_map/>`_.

Installation
============
Install running:

    $ pip install UQToolbox

Some users might want to install the toolbox *without MPI* support. This is possible, but not through the ``pip`` command:

     $ pip install --download="/pth/to/downloaded/files" UQToolbox

     $ cd /pth/to/downloaded/files

     $ tar xzf UQToolbox-x.x.x.tar.gz

     $ cd UQToolbox-x.x.x

     $ python setup.py install --without-mpi4py

Test Installation
=================
You can test whether all the functionalities work by running the unit tests.

    >>> import UQToolbox
    >>> UQToolbox.RunUnitTests(maxprocs=None,PLOTTING=True)

where ``maxprocs`` defines the number of processors to be used if MPI support is activated. Be patient. The number of unit tests grows with the number of functionalities implemented in the software.
