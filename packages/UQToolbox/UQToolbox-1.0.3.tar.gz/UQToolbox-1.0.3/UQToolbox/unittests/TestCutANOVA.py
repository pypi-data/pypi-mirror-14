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

import sys
import numpy as np
import numpy.linalg as npla
import scipy.stats as stats
try:
    import cPickle as pkl
except ImportError:
    import pickle as pkl
from SpectralToolbox import Spectral1D
from UQToolbox import CutANOVA
import UQToolbox.RandomSampling as RS
from UQToolbox.unittests.auxiliary import bcolors

def print_ok(string):
    print(bcolors.OKGREEN + "[SUCCESS] " + string + bcolors.ENDC)

def print_fail(string,msg=''):
    print(bcolors.FAIL + "[FAILED] " + string + bcolors.ENDC)
    if msg != '':
        print(bcolors.FAIL + msg + bcolors.ENDC)

def run(maxprocs=None, PLOTTING=True):
    if PLOTTING:
        import matplotlib.pyplot as plt

    store_freq = 100
    out_file = 'sensitivity.pkl'
        
    DIM = 8                                           # number of uncertainties
    dists = [stats.uniform(0,1) for i in range(DIM)] # Distributions

    params = dict( a = np.asarray([0., 1.,4.5, 9., 99., 99., 99., 99.]) )
    def fun(X,params):
        a = params['a']
        if len(X.shape) == 1:
            Y = np.prod( (np.abs(4.*X - 2.) + a)/(1. + a) );
        elif len(X.shape) == 2:
            Y = np.prod( (np.abs(4.*X - 2.) + a)/(1. + a) , 1);
        return Y

    poly_order = 6  # Polynomial chaos order (MUST BE EVEN)
    cut_order = 2
    
    # Polynomial construction for the distribution at hand
    pp = Spectral1D.generate(Spectral1D.JACOBI,[0.,0.])
    polys = [pp for i in range(DIM)]
    dists_polys = [ stats.uniform(-1,2) ] * DIM # orthogonality distribution for JACOBBI(0,0) polynomials (used for scaling).
    orders = [poly_order for i in range(DIM)] # Isotropic expansion (equal for all params)
    X_cut = np.zeros((1,len(polys))) # Anchor point (usually the central one)
    tol = 5. * np.spacing(1) # Internal tolerance for the construction of the nested grids

    cut_HDMR = CutANOVA.CutHDMR( fun, params,
                                 dists, dists_polys, polys,
                                 orders, cut_order, X_cut, tol,
                                 marshal_f = False,
                                 store_file = out_file )
    print_ok("UQToolbox.CutANOVA: CutHDMR construction")

    # Evaluate f on the cutHDMR grid
    print("Evaluation: %d/%d" % (len(cut_HDMR.get_results()), len(cut_HDMR.get_results())+len(cut_HDMR.get_new_samples())))

    cut_HDMR.run( maxprocs, store_freq )
    print_ok("UQToolbox.CutANOVA: CutHDMR evaluation")

    print("Start HDMR computation - cut-HDMR")
    # Compute the cutHDMR
    cut_HDMR.computeCutHDMR()

    print("Start HDMR computation - ANOVA-HDMR")
    # Compute the ANOVA-HDMR
    cut_HDMR.computeANOVA_HDMR()
    print("End HDMR computation")

    print_ok("UQToolbox.CutANOVA: CutHDMR computation")

    # Compute an estimate for the total variance (using Latin Hyper Cube)
    exp_lhc = RS.Experiments(fun,params,dists,False)
    exp_lhc.sample(2000, method='lhc')
    exp_lhc.run()
    MC_exp = np.asarray(exp_lhc.get_results())
    MC_mean = np.mean(MC_exp)
    MC_var = np.var(MC_exp)
    if PLOTTING:
        plt.figure()
        plt.subplot(2,1,1)
        plt.plot(np.array([np.mean(MC_exp[:i]) for i in range(len(MC_exp))]))
        plt.subplot(2,1,2)
        plt.plot(np.array([np.var(MC_exp[:i]) for i in range(len(MC_exp))]))
    print_ok("UQToolbox.CutANOVA: Total variance evaluation")

    # Compute individual variances
    D = []
    for level_grids in cut_HDMR.grids:
        D_level = []
        for grid in level_grids:
            D_level.append( np.dot(grid.ANOVA_HDMR_vals**2., grid.WF) )
        D.append(D_level)
    Var_ANOVA = np.sum( [ np.sum(sd) for sd in D[1:] ] )
    print("Variance ANOVA: %f" % Var_ANOVA)
    print("VarANOVA/TotVar = %f" % (Var_ANOVA/MC_var))

    # Compute Total variances per component
    TV = np.zeros(DIM)
    for idx in range(DIM):
        for level, level_idxs in enumerate(cut_HDMR.idxs):
            for j, idxs in enumerate(level_idxs):
                if idx in idxs:
                    TV[idx] += D[level][j]
    TS = TV/MC_var
    print("N     TV       TS")
    for i,grid in enumerate(cut_HDMR.grids[1]):
        print("%2d    %.4f   %.4f" % (i+1, TV[i], TS[i]))

    print_ok("UQToolbox.CutANOVA: TSI calculation")

    if PLOTTING:
        plt.figure()
        plt.pie(TS/np.sum(TS),labels=["x%d"%(i+1) for i in range(DIM)])
        plt.show(False)


if __name__ == "__main__":
    # Number of processors to be used, defined as an additional arguement 
    # $ python TestKL.py N
    if len(sys.argv) == 2:
        maxprocs = int(sys.argv[1])
    else:
        maxprocs = None

    run(maxprocs)
