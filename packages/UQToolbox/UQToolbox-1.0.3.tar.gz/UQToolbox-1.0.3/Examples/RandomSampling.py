# -*- coding: utf-8 -*-

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


import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import UQToolbox.RandomSampling as RS

params = dict( tspan = [0.,1.],
               nt = 100 )
    
def f(X,params):
    # y(t) = b * exp(-a*t)
    # In the following X[0] = a, X[1] = b
    # Note: all the "imports" must be declared inside this function
    # in order for UQToolbox to work with mpi
    import numpy as np
    tspan = params['tspan']
    nt = params['nt']
    T = np.linspace( tspan[0], tspan[1], nt )
    return X[1] * np.exp( - X[0] * T )


# Optional storage information
store_file = 'rs.pkl'
store_freq = 100 # Every how many simulations to store

# Optional running information
maxprocs = 1 # number of mpi threads to be used

# Distribution of (a,b)
dists = [ stats.uniform(.5,.5),    # a ~ U([0.5, 1.0])
          stats.uniform(.25,.5) ]  # b ~ U([0.25, 0.75])

# Number of experiments
N = 1000

# The experiment object
experiments = RS.RandomExperiments( f, params,
                                    dists,
                                    marshal_f = True, # Store definition of f
                                    store_file = store_file )

# Test Sobol sequence
experiments.sample( N, 'sobol' ) # Create the qmc samples. Other options are 'mc' or 'lhc'

# Plot samples
ns = np.asarray( experiments.get_new_samples() ) # Sample points on which the function has not been evaluated yet
plt.figure()
plt.plot( ns[:,0], ns[:,1], '.' )
plt.show(False)

print "N samples to be evaluated: %d" % len( experiments.get_new_samples() )

# Evaluate function on samples
print "Running experiments"
experiments.run( maxprocs, store_freq=store_freq )

print "N samples to be evaluated: %d" % len( experiments.get_new_samples() )
print "N samples already evaluated: %d" % len( experiments.get_samples() )

# Evaluate mean and variance
results = np.asarray( experiments.get_results() )
mean = np.mean( results, axis=0 )
var = np.var( results, axis=0 )

# Plot mean, var and first 2 realizations
tspan = params['tspan']
nt = params['nt']
T = np.linspace( tspan[0], tspan[1], nt )

plt.figure()
for i in range(2):
    plt.plot(T, results[i,:])

plt.plot(T, mean, 'k', linewidth=2.,label='mean')
plt.plot(T, mean + np.sqrt(var), '--k', linewidth=2.,label='std')
plt.plot(T, mean - np.sqrt(var), '--k', linewidth=2.)
plt.legend()
plt.show(False)
