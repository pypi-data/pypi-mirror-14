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

import numpy as np
import scipy.special as scsp
import scipy.stats as stats
from matplotlib import pyplot as plt
from SpectralToolbox import Spectral1D
from UQToolbox import CutANOVA
import UQToolbox.RandomSampling as RS

DIM = 8
pp = Spectral1D.Poly1D(Spectral1D.JACOBI,[0.,0.])
polys = [pp for i in range(DIM)]
Ns = [6 for i in range(DIM)]
cut_order = 2
X_cut = np.zeros((1,len(polys)))

tol = 2. * np.spacing(1)

cut_HDMR = CutANOVA.CutHDMR(polys,Ns,cut_order,X_cut,tol)

def fun(X,params=None):
    a = np.asarray([0., 1.,4.5, 9., 99., 99., 99., 99.]);
    if len(X.shape) == 1:
        Y = np.prod( (np.abs(4.*X - 2.) + a)/(1. + a) );
    elif len(X.shape) == 2:
        Y = np.prod( (np.abs(4.*X - 2.) + a)/(1. + a) , 1);
    return Y

def transformFunc(X):
    # from [-1,1] to [0,1]
    return (X+1.)/2.

# Evaluate f on the cutHDMR grid
print "N. eval = %d" % np.sum( [scsp.binom(DIM,i) * Ns[0]**i for i in range(cut_order+1)] )
cut_HDMR.evaluateFun(fun,transformFunc)
print "End evaluation"

print "Start HDMR computation"
# Compute the cutHDMR
cut_HDMR.computeCutHDMR()

# Compute the ANOVA-HDMR
cut_HDMR.computeANOVA_HDMR()
print "End HDMR computation"

# Compute an estimate for the total variance (using Monte Carlo)
dists = [stats.uniform(0,1) for i in xrange(DIM)]
exp_lhc = RS.Experiments(fun,None,dists,False)
exp_lhc.sample(2000, method='lhc')
exp_lhc.run()
MC_vals = np.asarray(exp_lhc.get_samples())
MC_exp = np.asarray(exp_lhc.get_results())
MC_mean = np.mean(MC_exp)
MC_var = np.var(MC_exp)
plt.figure()
plt.subplot(2,1,1)
plt.plot(np.array([np.mean(MC_exp[:i]) for i in range(len(MC_exp))]))
plt.subplot(2,1,2)
plt.plot(np.array([np.var(MC_exp[:i]) for i in range(len(MC_exp))]))

# Compute individual variances
D = []
for level_grids in cut_HDMR.grids:
    D_level = []
    for grid in level_grids:
        D_level.append( np.dot(grid.ANOVA_HDMR_vals**2., grid.WF) )
    D.append(D_level)
Var_ANOVA = np.sum(D[1]) + np.sum(D[2])
print "TotVar/Var_Anova = %f" % (Var_ANOVA/MC_var)

# Compute Total variances per component
TV = np.zeros(DIM)
for idx in range(DIM):
    for level, level_idxs in enumerate(cut_HDMR.idxs):
        for j, idxs in enumerate(level_idxs):
            if idx in idxs:
                TV[idx] += D[level][j]
TS = TV/MC_var
print "N     TV       TS"
for i,grid in enumerate(cut_HDMR.grids[1]):
    print "%2d    %.4f   %.4f" % (i+1, TV[i], TS[i])

plt.figure()
plt.pie(TS/np.sum(TS),labels=["x%d"%(i+1) for i in range(DIM)])
plt.show(False)
