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

import time

import numpy as np
from numpy import linalg as npla
from scipy import stats
from scipy import linalg as scila
from scipy import sparse

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

from UQToolbox import gPC as UQ
from UQToolbox import RandomSampling as RS
from SpectralToolbox import Spectral1D
from SpectralToolbox import SpectralND
from SpectralToolbox import SparseGrids

plt.close('all')
STORE_FIG = False
FORMATS = ['pdf','png','eps']

startTime = time.clock()

PROBLEM = 1
if PROBLEM == 2:
    KL_N1D = 40
PLOTTING = True

doMonteCarlo = True
doMonteCarlo_N = 1000

doLHC = True
doLHC_N = 1000

doSparseGrid = False
doSparseGrid_level = 3
doSparseGrid_convergence = False
doSparseGrid_convergence_level = range(1,5)

doGPC = True
doGPC_N = 6
doGPC_warnings = False
doGPC_interpolate = False
doGPC_interpolate_N = 40

doGPC_convergence = True
doGPC_convergence_orders = range(1,10)

doCollocation = True
doCollocation_N = 6
doCollocation_warnings = False
doCollocation_interpolate = False
doCollocation_interpolate_N = 40

doCollocation_convergence = True
doCollocation_convergence_orders = range(1,9)

'''
# Define parameters for deterministic part of the problem
'''
P = 20
PI = 40

poly1D = Spectral1D.Poly1D(Spectral1D.JACOBI,[0.0,0.0])
poly = SpectralND.PolyND([poly1D, poly1D])

(x,w) = poly.GaussLobattoQuadrature([P,P])
(xI,wI) = poly.GaussLobattoQuadrature([PI,PI])

time_ProblemDefinition_start = time.clock()
if PROBLEM == 1:
    
    '''
    # Define deterministic definition for the problem
    '''    
    class PoissonParameters:
        epsilon = 1.
    
    params = PoissonParameters()
    
    xspan = [0.0, 1.0]
    yspan = [0.0, 1.0]
    xScaled = (x+1.)/2.
    xIScaled = (xI+1.)/2.
    
    def f(x,y):
        return -np.exp(-( (x-0.5)**2.+(y-0.5)**2. )/0.01)
        # return -np.ones(x.shape)
    
    BC_dir = []
    BC_x_neu = []
    BC_y_neu = []
    
    def BC_dir_f(x,y):
        return 0. * x;
    
    def BC_neu_x_f(x,y):
        return 0. * x;
    
    BC_dir_idx = []
    BC_dir_idx += np.where(xScaled[:,0] == 0.)[0].tolist()
    BC_dir_idx += np.where(xScaled[:,1] == 0.)[0].tolist()
    BC_dir_idx += np.where(xScaled[:,1] == 1.)[0].tolist()
    BC_dir.append((BC_dir_idx,BC_dir_f))
    
    BC_neu_x_idx = []
    BC_neu_x_idx += np.where(xScaled[:,0] == 1.)[0].tolist()
    BC_x_neu.append((BC_neu_x_idx,BC_neu_x_f));
    
    '''
    # Define stochastic definitions for the problem
    # logNormal distribution
    '''
    beta_bar = 1.
    C = np.sqrt(10)
    mu_beta = np.log(beta_bar)
    sigma_beta = np.log(C)/2.85
    
    def betaFunc(xi):
        return np.exp(mu_beta + sigma_beta * xi)
    
    dists = [ stats.lognorm(sigma_beta, loc=0., scale=np.exp(mu_beta)) ]
    
    def paramUpdate(params,sample):
        params.epsilon = sample
        return params
    
    def kappa(x,y,params):
        return params * np.ones(x.shape)
    
    if doGPC or doCollocation:
        '''
        # Define parameters for Polynomial chaos
        '''
        gPC_polysType = [Spectral1D.HERMITEP_PROB]
        gPC_polysParams = [None]
        gPC_distsPoly = [ stats.norm(0.,1.) ]

elif PROBLEM == 2:
    '''
    # Model Gaussian random field with C(x1,x2)
    '''
    
    '''
    # Define deterministic definition for the problem
    '''
    xspan = [0.0, 1.0]
    yspan = [0.0, 1.0]
    
    def scalingFun(x,y):
        sc_x = (x+1.)/2.
        sc_y = (y+1.)/2.
        return (sc_x,sc_y)
    
    xScaled = np.zeros(x.shape)
    xIScaled = np.zeros(xI.shape)
    (xScaled[:,0],xScaled[:,1]) = scalingFun(x[:,0],x[:,1])
    (xIScaled[:,0],xIScaled[:,1]) = scalingFun(xI[:,0],xI[:,1])
    
    alpha = 0.01
    def f(x,y):
        return - np.exp( - (x-0.3)**2./alpha - (y-0.3)**2./alpha )
    
    BC_dir = []
    BC_x_neu = []
    BC_y_neu = []
    
    def BC_dir_f(x,y):
        return np.ones( x.shape );
    
    def BC_neu_x_f(x,y):
        return 0. * x;
    
    def BC_neu_y_f(x,y):
        return 0. * y;
    
    BC_dir_idx = []
    BC_dir_idx += np.where(xScaled[:,0] == 0.)[0].tolist()
    BC_dir_idx += np.where(xScaled[:,1] == 1.)[0].tolist()
    BC_dir.append((BC_dir_idx,BC_dir_f))
    
    BC_neu_x_idx = []
    BC_neu_x_idx += np.where(xScaled[:,0] == 1.)[0].tolist()
    BC_x_neu.append((BC_neu_x_idx,BC_neu_x_f));
    
    BC_neu_y_idx = []
    BC_neu_y_idx += np.where(xScaled[:,1] == 0.)[0].tolist()
    BC_y_neu.append((BC_neu_y_idx,BC_neu_y_f));
    
    '''
    # Define stochastic definitions for the problem
    '''
    class PoissonParameters:
        rv = []
        def __init__(self,N):
            self.rv = np.zeros(N)
    
    def paramUpdate(params,sample):
        for i in range(len(sample)):
            params.rv[i] = sample[i]
        return params
    
    a = 0.01
    def C(x1,x2):
        return np.exp(- np.abs(x1-x2)/a )
    
    def sFun(x):
        return (x+1.)/2.
    
    (KL_x,KL_val,KL_vec,var,KL_Nvar) = UQ.KLExpansion1D(C,KL_N1D,sFun)
    KL_val = KL_val[:KL_Nvar]
    KL_vec = KL_vec[:,:KL_Nvar]
    KL_N = len(KL_val)**2
    
    # KL_poly = Spectral1D.Poly1D(Spectral1D.JACOBI,[0.0,0.0])
    
    KL_vec_x = np.zeros((len(x[:,0].ravel()), KL_Nvar ))
    for i in range(KL_Nvar):
        KL_vec_x[:,i] = Spectral1D.LagrangeInterpolate(KL_x,KL_vec[:,i],x[:,0].ravel())
    
    KL_vec_y = np.zeros((len(x[:,1].ravel()), KL_Nvar ))
    for i in range(KL_Nvar):
        KL_vec_y[:,i] = Spectral1D.LagrangeInterpolate(KL_x,KL_vec[:,i],x[:,1].ravel())
    
    def kappa(x,y,params):
        K = np.zeros(x.shape)
        
        for i in range(len(KL_val)):
            for j in range(len(KL_val)):
                K += np.sqrt(KL_val[i]*KL_val[j]) * KL_vec_x[:,i] * KL_vec_y[:,j] * params.rv[i*len(KL_val)+j]
        
        return np.exp(-2.5 + K)
    
    params = PoissonParameters(len(KL_val)**2)
    
    dists = []
    for i in range(len(KL_val)**2):
        dists.append( stats.norm() )
    
    if doGPC or doCollocation:
        '''
        # Define parameters for Polynomial chaos
        '''
        gPC_polysType = []
        gPC_polysParams = []
        gPC_distsPoly = []
        for i in range(KL_N):
            gPC_polysType.append(Spectral1D.HERMITEP_PROB)
            gPC_polysParams.append(None)
            gPC_distsPoly.append(stats.norm(0.,1.))

time_ProblemDefinition_stop = time.clock()

if PLOTTING:
    plt.figure()
    plt.plot(xScaled[:,0],xScaled[:,1],'.')
    for BC_dir_idx,BC_dir_f in BC_dir:
        plt.plot(xScaled[BC_dir_idx,0],xScaled[BC_dir_idx,1],'.')
    for BC_neu_idx,BC_neu_f in BC_x_neu:
        plt.plot(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1],'.')
    for BC_neu_idx,BC_neu_f in BC_y_neu:
        plt.plot(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1],'.')

if doMonteCarlo:
    time_MC_start = time.clock()
    '''
    #############################################################################
    #############################################################################
    #                         Monte Carlo Method                                #
    #############################################################################
    '''
    totN = doMonteCarlo_N
    
    time_MC_ExperimentConstruction_start = time.clock()
    ''' Construct differential operator '''
    (x1D,w1D) = poly1D.GaussLobattoQuadrature(P)
    V1D = poly1D.GradVandermonde1D(x1D,P,0)
    Vx1D = poly1D.GradVandermonde1D(x1D,P,1)
    D1D = np.linalg.solve(V1D.T,Vx1D.T).T
    
    Dx1D = np.kron(D1D,np.eye(P+1))
    Dy1D = np.kron(np.eye(P+1),D1D)
    
    # Set Neumann bc
    Dx1D_neu = Dx1D.copy()
    for BC_neu_idx,BC_neu_f in BC_x_neu:
        Dx1D_neu[BC_neu_idx,:] = 0.0 
        Dx1D_neu[BC_neu_idx,BC_neu_idx] = BC_neu_f(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1])
    Dy1D_neu = Dy1D.copy()
    for BC_neu_idx,BC_neu_f in BC_y_neu:
        Dy1D_neu[BC_neu_idx,:] = 0.0 
        Dy1D_neu[BC_neu_idx,BC_neu_idx] = BC_neu_f(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1])
    
    F = f(xScaled[:,0],xScaled[:,1]) #/ poly1D.Gamma(0)**2.
    
    def poisson2D(params,pp):
        
        V = np.diag(kappa(xScaled[:,0],xScaled[:,1],params))
        
        # Construct L operator
        L = np.dot(Dx1D, np.dot(V,Dx1D_neu)) + np.dot(Dy1D, np.dot(V,Dy1D_neu))
        
        # Impose Dirichlet Boundary Conditions
        for BC_dir_idx,BC_dir_f in BC_dir:
            L[BC_dir_idx,:] = 0.
            L[BC_dir_idx,BC_dir_idx] = 1.
            F[BC_dir_idx] = BC_dir_f(xScaled[BC_dir_idx,0],xScaled[BC_dir_idx,1])
        
        # Sparsify
        L_sparse = sparse.coo_matrix(L)
        
        ''' Solve the system '''
        u = sparse.linalg.spsolve(L_sparse,F)
        
        return u
    
    # def action(sols,newSol):
    #     if len(sols) == 0:
    #         sols = [newSol]
    #     else:
    #         sols.append(newSol)
    #     return sols
    time_MC_ExperimentConstruction_stop = time.clock()
    
    ''' Run experiments '''
    time_MC_ExperimentRun_start = time.clock()
    Exp = RS.Experiments( poisson2D, None, dists )
    Exp.sample( totN )
    Exp.run()
    samples = Exp.get_samples()
    MC_sols = Exp.get_results()
    time_MC_ExperimentRun_stop = time.clock()
    time_MC_stop = time.clock()
    
    MC_mean = np.mean(np.array(MC_sols),0)
    MC_var = np.var(np.array(MC_sols),0)
    
    if PLOTTING:
        ''' Plot Mean and Variance '''
        fig = plt.figure(figsize=(14,7))
        ax = fig.add_subplot(1,2,1,projection='3d')
        X = xScaled[:,0].reshape((P+1,P+1))
        Y = xScaled[:,1].reshape((P+1,P+1))
        Z = MC_mean.reshape((P+1,P+1))
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        plt.title('MC Mean')
        ax = fig.add_subplot(1,2,2,projection='3d')
        ax = fig.gca(projection='3d')
        Z = MC_var.reshape((P+1,P+1))
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        plt.title('MC Var')
        
        ''' Plot Mean and Variance '''
        fig = plt.figure(figsize=(14,7))
        ax = fig.add_subplot(1,2,1)
        X = xScaled[:,0].reshape((P+1,P+1))
        Y = xScaled[:,1].reshape((P+1,P+1))
        Z = MC_mean.reshape((P+1,P+1))
        CS = ax.contour(X,Y,Z)
        plt.clabel(CS, inline=1, fontsize=10)
        plt.title('MC Mean')
        ax = fig.add_subplot(1,2,2)
        Z = MC_var.reshape((P+1,P+1))
        CS = ax.contour(X,Y,Z)
        plt.clabel(CS, inline=1, fontsize=10)
        plt.title('MC Var')
        
        ''' Plot histogram of solutions at x=(1,0.5) '''
        V2D = poly.GradVandermonde(x,[P,P],[0,0],usekron=False)
        
        xI = np.array([[1., 0.]])
        V2DI = poly.GradVandermonde(xI,[P,P],[0,0],usekron=False)
        
        uHat = npla.solve(V2D,np.array(MC_sols).T)
        uI = np.dot(V2DI,uHat)
        
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.hist(uI.flatten(),bins=20, normed=True)
        plt.xlabel('u(1,0.5)')
        plt.ylabel('Perc. of occurrences')
        plt.title('MC - Histogram')
        
#        if PROBLEM == 1:
        ''' Plot Mean and Variance at x=(1,0.5) convergence w.r.t. samples '''
        MC_mean_conv = np.array([np.mean(uI.flatten()[:i]) for i in range(totN)])
        MC_var_conv = np.array([np.var(uI.flatten()[:i]) for i in range(totN)])
        
        fig = plt.figure()
        ax = fig.add_subplot(2,1,1)
        plt.title("MC mean and variance convergence")
        ax.plot(range(totN), MC_mean_conv)
        plt.ylabel('Mean')
        ax.grid()
        ax = fig.add_subplot(2,1,2)
        ax.plot(range(totN), MC_var_conv)
        ax.grid()
        plt.xlabel('N')
        plt.ylabel('Var')

if doLHC:
    time_LHC_start = time.clock()
    '''
    #############################################################################
    #############################################################################
    #                         Monte Carlo Method                                #
    #############################################################################
    '''
    totN = doLHC_N
    
    time_LHC_ExperimentConstruction_start = time.clock()
    ''' Construct differential operator '''
    (x1D,w1D) = poly1D.GaussLobattoQuadrature(P)
    V1D = poly1D.GradVandermonde1D(x1D,P,0)
    Vx1D = poly1D.GradVandermonde1D(x1D,P,1)
    D1D = np.linalg.solve(V1D.T,Vx1D.T).T
    
    Dx1D = np.kron(D1D,np.eye(P+1))
    Dy1D = np.kron(np.eye(P+1),D1D)
    
    # Set Neumann bc
    Dx1D_neu = Dx1D.copy()
    for BC_neu_idx,BC_neu_f in BC_x_neu:
        Dx1D_neu[BC_neu_idx,:] = 0.0 
        Dx1D_neu[BC_neu_idx,BC_neu_idx] = BC_neu_f(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1])
    Dy1D_neu = Dy1D.copy()
    for BC_neu_idx,BC_neu_f in BC_y_neu:
        Dy1D_neu[BC_neu_idx,:] = 0.0 
        Dy1D_neu[BC_neu_idx,BC_neu_idx] = BC_neu_f(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1])
    
    F = f(xScaled[:,0],xScaled[:,1]) #/ poly1D.Gamma(0)**2.
    
    def poisson2D(params,pp):
        
        V = np.diag(kappa(xScaled[:,0],xScaled[:,1],params))
        
        # Construct L operator
        L = np.dot(Dx1D, np.dot(V,Dx1D_neu)) + np.dot(Dy1D, np.dot(V,Dy1D_neu))
        
        # Impose Dirichlet Boundary Conditions
        for BC_dir_idx,BC_dir_f in BC_dir:
            L[BC_dir_idx,:] = 0.
            L[BC_dir_idx,BC_dir_idx] = 1.
            F[BC_dir_idx] = BC_dir_f(xScaled[BC_dir_idx,0],xScaled[BC_dir_idx,1])
        
        # Sparsify
        L_sparse = sparse.coo_matrix(L)
        
        ''' Solve the system '''
        u = sparse.linalg.spsolve(L_sparse,F)
        
        return u
    
    def action(sols,newSol):
        if len(sols) == 0:
            sols = [newSol]
        else:
            sols.append(newSol)
        return sols
    time_LHC_ExperimentConstruction_stop = time.clock()
    
    ''' Run experiments '''
    time_LHC_ExperimentRun_start = time.clock()
    Exp = RS.Experiments( poisson2D, None, dists )
    Exp.sample( totN, 'lhc')
    Exp.run()
    samples = Exp.get_samples()
    LHC_sols = Exp.get_results()
    time_LHC_ExperimentRun_stop = time.clock()
    time_LHC_stop = time.clock()
    
    LHC_mean = np.mean(np.array(LHC_sols),0)
    LHC_var = np.var(np.array(LHC_sols),0)
    
    if PLOTTING:
        ''' Plot Mean and Variance '''
        fig = plt.figure(figsize=(14,7))
        ax = fig.add_subplot(1,2,1,projection='3d')
        X = xScaled[:,0].reshape((P+1,P+1))
        Y = xScaled[:,1].reshape((P+1,P+1))
        Z = LHC_mean.reshape((P+1,P+1))
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        plt.title('LHC Mean')
        ax = fig.add_subplot(1,2,2,projection='3d')
        ax = fig.gca(projection='3d')
        Z = LHC_var.reshape((P+1,P+1))
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        plt.title('LHC Var')
        
        ''' Plot Mean and Variance '''
        fig = plt.figure(figsize=(14,7))
        ax = fig.add_subplot(1,2,1)
        X = xScaled[:,0].reshape((P+1,P+1))
        Y = xScaled[:,1].reshape((P+1,P+1))
        Z = LHC_mean.reshape((P+1,P+1))
        CS = ax.contour(X,Y,Z)
        plt.clabel(CS, inline=1, fontsize=10)
        plt.title('LHC Mean')
        ax = fig.add_subplot(1,2,2)
        Z = LHC_var.reshape((P+1,P+1))
        CS = ax.contour(X,Y,Z)
        plt.clabel(CS, inline=1, fontsize=10)
        plt.title('LHC Var')
        
        ''' Plot histogram of solutions at x=(1,0.5) '''
        V2D = poly.GradVandermonde(x,[P,P],[0,0],usekron=False)
        
        xI = np.array([[1., 0.]])
        V2DI = poly.GradVandermonde(xI,[P,P],[0,0],usekron=False)
        
        uHat = npla.solve(V2D,np.array(LHC_sols).T)
        uI = np.dot(V2DI,uHat)
        
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.hist(uI.flatten(),bins=20, normed=True)
        plt.xlabel('u(1,0.5)')
        plt.ylabel('Perc. of occurrences')
        plt.title('LHC - Histogram')
        
#        if PROBLEM == 1:
        ''' Plot Mean and Variance at x=(1,0.5) convergence w.r.t. samples '''
        LHC_mean_conv = np.array([np.mean(uI.flatten()[:i]) for i in range(totN)])
        LHC_var_conv = np.array([np.var(uI.flatten()[:i]) for i in range(totN)])
        
        fig = plt.figure()
        ax = fig.add_subplot(2,1,1)
        plt.title("LHC mean and variance convergence")
        ax.plot(range(totN), LHC_mean_conv)
        plt.ylabel('Mean')
        ax.grid()
        ax = fig.add_subplot(2,1,2)
        ax.plot(range(totN), LHC_var_conv)
        ax.grid()
        plt.xlabel('N')
        plt.ylabel('Var')

if doGPC:
    time_gPC_start = time.clock()
    '''
    #############################################################################
    #############################################################################
    #                    Polynomial Chaos Expansion                             #
    #############################################################################
    '''
    
    time_gPC_StochasticAssembly_start = time.clock()
    
    gPC_polys = []
    for i in range(len(gPC_polysType)):
        gPC_polys.append(Spectral1D.Poly1D( gPC_polysType[i], gPC_polysParams[i] ))
    
    '''
    #############################################################################
    #                      Expansion of Uncertainty                             #
    #############################################################################
    '''
    dictionary = UQ.gPC_MultiIndex( dists, gPC_polys, gPC_distsPoly, doGPC_N, int(np.ceil(3./2. * doGPC_N)), warnings=doGPC_warnings)
    gPC_x = dictionary['x']
    gPC_w = dictionary['w']
    gPC_vals = dictionary['vals']
    gPC_V = dictionary['V']
    gPC_wI = dictionary['wI']
    gPC_VI = dictionary['VI']
    
    print "[BGN] gPC: Evaluate KL-expansion"
    vals = np.zeros((gPC_vals.shape[0],xScaled.shape[0]))
    counter = gPC_vals.shape[0]/100.
    for i in range(gPC_vals.shape[0]):
        if i > counter:
            counter += gPC_vals.shape[0]/100.
            print "\r%d%%" % (int(i/float(gPC_vals.shape[0])*100.)),
        vals[i,:] = kappa(xScaled[:,0],xScaled[:,1],gPC_vals[i,:])
    
    gPC_vals = vals
    print "\n[END] gPC: Evaluate KL-expansion"
    
    # Transform (NORMALIZED)
    #yHat = linalg.solve(V,vals)
    [gPC_yHat, gPC_res, gPC_rank, gPC_s]  = npla.lstsq(gPC_V,gPC_vals)
    
    '''
    #############################################################################
    #                      Setup gPC matrices                                   #
    #############################################################################
    '''
    gPC_NI = gPC_VI.shape[0]; # Number of collocation points for each dof of the dynamical system
    gPC_MI = gPC_VI.shape[1]; # Length of the expansion for each dof of the dynamical system
    
    '''  Compute the e matrix using the Vandermonde (NORMALIZED) matrix '''    
    print "[BGN] gPC: Computing gPC_E"    
    import itertools
    ''' Index function definition '''
    def gPC_idxF(l,i,j):
        def idx2(i,j,M):
            return (j-i) + i*M - sum([k for k in range(i)])
        return int( sum([idx2(gPC_MI-k,gPC_MI-k,gPC_MI-k) for k in range(l)]) + idx2(i-l,j-l,gPC_MI-l) )
    
    gPC_E_idx = list(itertools.combinations_with_replacement(range(gPC_MI),3))
    gPC_E = np.zeros(len(gPC_E_idx))
    counter = len(gPC_E_idx)/100.
    for l,(i,j,k) in enumerate(gPC_E_idx):
        if l > counter:
            counter += len(gPC_E_idx)/100.
            print "\r%d%%" % (int(l/float(len(gPC_E_idx))*100.)),
        gPC_E[l] = np.dot(gPC_VI[:,i]*gPC_VI[:,j]*gPC_VI[:,k],gPC_wI)
    print '\n'
    
    print "[END] gPC: Computing gPC_E"
    
    ''' Assemble the A matrix '''    
    print "[BGN] gPC: Computing gPC_tensor"
    NP = xScaled.shape[0]
    #    gPC_tensor = np.zeros((gPC_MI,gPC_MI))
    tensor = []
    row = []
    col = []
    for j in range(0,gPC_MI):
        for k in range(j,gPC_MI):
            tt = np.zeros(NP)
            for i in range(0,gPC_MI):
                idx = np.sort((i,j,k))
                tt += gPC_yHat[i,:] * gPC_E[gPC_idxF(idx[0],idx[1],idx[2])]
            tensor.append(tt)
            row.append( (j*NP + np.arange(NP,dtype=np.int)) )
            col.append( (k*NP + np.arange(NP,dtype=np.int)) )
    
    tensor = np.asarray(tensor)
    row = np.asarray(row)
    col = np.asarray(col)
    
    gPC_tensor = sparse.csr_matrix( (tensor.ravel(),(row.ravel(),col.ravel())) )
    
    gPC_tensor_diag = gPC_tensor.diagonal()
    gPC_tensor = gPC_tensor - sparse.csr_matrix((gPC_tensor_diag,(range(gPC_MI*NP),range(gPC_MI*NP))))
    gPC_tensor = gPC_tensor + gPC_tensor.transpose()
    gPC_tensor = gPC_tensor + sparse.csr_matrix((gPC_tensor_diag,(range(gPC_MI*NP),range(gPC_MI*NP))))
    
    print "[END] gPC: Computing gPC_tensor"
    
    time_gPC_StochasticAssembly_stop = time.clock()
    
    '''
    #############################################################################
    #             Setup Stochastic-Deterministic Solver                         #
    #############################################################################
    # Set up on top of the stochastic problem
    '''
    time_gPC_Assembly_start = time.clock()
    
    ''' Construct differential operator '''
    (x1D,w1D) = poly1D.GaussLobattoQuadrature(P)
    V1D = poly1D.GradVandermonde1D(x1D,P,0)
    Vx1D = poly1D.GradVandermonde1D(x1D,P,1)
    D1D = np.linalg.solve(V1D.T,Vx1D.T).T
    
    Dx1D = np.kron(D1D,np.eye(P+1))
    Dy1D = np.kron(np.eye(P+1),D1D)
    
    # Set Neumann bc
    Dx1D_neu = Dx1D.copy()
    for BC_neu_idx,BC_neu_f in BC_x_neu:
        Dx1D_neu[BC_neu_idx,:] = 0.0 
        Dx1D_neu[BC_neu_idx,BC_neu_idx] = BC_neu_f(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1])
    Dy1D_neu = Dy1D.copy()
    for BC_neu_idx,BC_neu_f in BC_y_neu:
        Dy1D_neu[BC_neu_idx,:] = 0.0 
        Dy1D_neu[BC_neu_idx,BC_neu_idx] = BC_neu_f(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1])
    
    # Construct deterministic operator matrix
    L_det = np.dot(Dx1D,Dx1D_neu) + np.dot(Dy1D,Dy1D_neu)
    
    # Set Dirichlet bc (on the deterministic operator matrix)
    for BC_dir_idx,BC_dir_f in BC_dir:
        L_det[BC_dir_idx,:] = 0.0
        L_det[BC_dir_idx,BC_dir_idx] = 1.0
    
    # Sparsify and Expand the deterministic operator
    L_det_sparse = sparse.csr_matrix(L_det)
    ID = sparse.identity(gPC_MI)
    L_det_exp_sparse = sparse.kron(ID,L_det_sparse)
    
    # Construct deterministic-stochastic operator
    L = gPC_tensor.dot(L_det_exp_sparse)
    
#    # Sparsify and Expand the Differentiation matrices to (M*(P+1)**2)x(M*(P+1)**2)
#    Dx1D_sparse = sparse.csr_matrix(Dx1D)
#    Dy1D_sparse = sparse.csr_matrix(Dy1D)
#    Dx1D_neu_sparse = sparse.csr_matrix(Dx1D_neu)
#    Dy1D_neu_sparse = sparse.csr_matrix(Dy1D_neu)
#    ID = sparse.identity(gPC_MI)
#    
#    Dx1D_exp_sparse = sparse.kron(ID,Dx1D_sparse)
#    Dy1D_exp_sparse = sparse.kron(ID,Dy1D_sparse)
#    Dx1D_neu_exp_sparse = sparse.kron(ID,Dx1D_neu_sparse)
#    Dy1D_neu_exp_sparse = sparse.kron(ID,Dy1D_neu_sparse)
#    
#    # Construct L operator
#    L = Dx1D_exp_sparse.dot( gPC_tensor.dot(Dx1D_neu_exp_sparse) ) + Dy1D_exp_sparse.dot( gPC_tensor.dot(Dy1D_neu_exp_sparse) )
    
    # Construct f 
    F = np.zeros(gPC_MI*(P+1)**2)
    F[:(P+1)**2] = f(xScaled[:,0],xScaled[:,1]) # / poly1D.Gamma(0)**2.
    
    # Impose Dirichlet Boundary Conditions
    def csr_row_set_nz_to_val(csr, row, value=0):
        """Set all nonzero elements (elements currently in the sparsity pattern)
        to the given value. Useful to set to 0 mostly.
        """
        if not isinstance(csr, sparse.csr_matrix):
            raise ValueError('Matrix given must be of CSR format.')
        csr.data[csr.indptr[row]:csr.indptr[row+1]] = value
    
    print "[BGN] gPC: Impose Dirichlet Boundary Conditions"
    for BC_dir_idx,BC_dir_f in BC_dir:
        ''' Main Stochastic Mode '''
        idxs = np.asarray(BC_dir_idx)
        for idx in idxs:
            csr_row_set_nz_to_val(L,idx,0.)
            L[idx,idx] = 1.
        F[idxs] = BC_dir_f(xScaled[BC_dir_idx,0],xScaled[BC_dir_idx,1])
        
        ''' Higher Stochastic Modes '''
        for i in range(1,gPC_MI):
            idxs = i*(P+1)**2 + np.asarray(BC_dir_idx)
            for idx in idxs:
                csr_row_set_nz_to_val(L,idx,0.)
                L[idx,idx] = 1.
            F[idxs] = 0.
            
    print "[END] gPC: Impose Dirichlet Boundary Conditions"
    time_gPC_Assembly_stop = time.clock()
    
    plt.figure(figsize=(6,5))
    plt.spy(L.todense()[:1000,:1000])
    if STORE_FIG:
        for ff in FORMATS:
            plt.savefig('figs/Example-Poisson-Spy.'+ff,format=ff)
    
    sp_ratio = len(L.nonzero()[0])/L.shape[0]**2.
    print("Sparsness ratio non-zero/total = %f" % (sp_ratio))
    
    ''' Solve the system '''
    time_gPC_Solve_start = time.clock()
    print "[BGN] gPC: Solving"
#    ''' Preconditioning (Block-Jacobi)'''
#    dd = gPC_tensor.diagonal()
#    gPC_tensor_diag = sparse.csr_matrix( (dd,(range(len(dd)),range(len(dd)))) )
#    P = Dx1D_exp_sparse.dot( gPC_tensor_diag.dot(Dx1D_neu_exp_sparse) ) + Dy1D_exp_sparse.dot( gPC_tensor_diag.dot(Dy1D_neu_exp_sparse) )
#    M_x = lambda x: sparse.linalg.spsolve(P, x)
#    M = sparse.linalg.LinearOperator((len(dd), len(dd)), M_x)
    ''' Preconditioning (ILU) '''
    L = sparse.csc_matrix(L) # Convert to csc matrix for efficiency
    L_ILU = sparse.linalg.spilu(L)
    M_x = lambda x: L_ILU.solve(x)
    M = sparse.linalg.LinearOperator(L.shape, M_x)
    ''' Solving '''
    (U,info) = sparse.linalg.bicgstab(L,F,maxiter=10000,M=M)
    if info != 0:
        print "Not converging solution"
    print "[END] gPC: Solving"
    time_gPC_Solve_stop = time.clock()
    time_gPC_stop = time.clock()
    
    Ush = U.reshape((gPC_MI,(P+1)**2))
    
    ''' Interpolate options '''
    if doGPC_interpolate:
        # Prepare matrices for interpolation
        V2D = np.kron(V1D,V1D)
        x1DI = np.linspace(-1,1,doGPC_interpolate_N)
        V1DI = poly1D.GradVandermonde1D(x1DI,P,0)
        V2DI = np.kron(V1DI,V1DI)
    
    ''' Compute Mean and Variance '''
    UMean = Ush[0,:]
    UVar = np.sum(Ush[1:,:]**2.,0)
    
    if PLOTTING:
        ''' Plot modes (Interpolate) '''
        fig = plt.figure(figsize=(14,8))
        for i in range(0,min(gPC_MI,6)):
            ax = fig.add_subplot(2,3,i+1, projection='3d')
            
            if not doGPC_interpolate:
                X = xScaled[:,0].reshape((P+1,P+1))
                Y = xScaled[:,1].reshape((P+1,P+1))
                Z = Ush[i,:].reshape((P+1,P+1))
            else:
                (X,Y) = np.meshgrid(x1DI,x1DI)
                X = X.T
                Y = Y.T
                UshI = np.dot(V2DI, npla.solve(V2D,Ush[i,:]))
                Z = UshI.reshape((doGPC_interpolate_N,doGPC_interpolate_N))
            surf = ax.plot_surface(X,Y,Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            plt.ticklabel_format(style='sci', axis='z', scilimits=(0,0))
            plt.title('Mode %d' % i)
        fig.tight_layout()
        if STORE_FIG:
            for ff in FORMATS:
                plt.savefig('figs/Example-Poisson-Modes.'+ff,format=ff)
        
        ''' Plot Mean and Variance (Interpolate) '''
        fig = plt.figure(figsize=(6,5))
        ax = fig.add_subplot(1,1,1,projection='3d')
        if not doGPC_interpolate:
            X = xScaled[:,0].reshape((P+1,P+1))
            Y = xScaled[:,1].reshape((P+1,P+1))
            Z = UMean.reshape((P+1,P+1))
        else:
            (X,Y) = np.meshgrid(x1DI,x1DI)
            X = X.T
            Y = Y.T
            UMeanI = np.dot(V2DI, npla.solve(V2D,UMean))
            Z = UMeanI.reshape((doGPC_interpolate_N,doGPC_interpolate_N))
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('E[u]')
        plt.ticklabel_format(style='sci', axis='z', scilimits=(0,0))
        fig.tight_layout()
        if STORE_FIG:
            for ff in FORMATS:
                plt.savefig('figs/Example-Poisson-Mean.'+ff,format=ff)

        fig = plt.figure(figsize=(6,5))
        ax = fig.add_subplot(1,1,1,projection='3d')
        if not doGPC_interpolate:
            ax = fig.gca(projection='3d')
            Z = UVar.reshape((P+1,P+1))
        else:
            (X,Y) = np.meshgrid(x1DI,x1DI)
            X = X.T
            Y = Y.T
            UVarI = np.dot(V2DI, npla.solve(V2D,UVar))
            Z = UVarI.reshape((doGPC_interpolate_N,doGPC_interpolate_N))
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('V[u]')
        plt.ticklabel_format(style='sci', axis='z', scilimits=(0,0))
        fig.tight_layout()
        if STORE_FIG:
            for ff in FORMATS:
                plt.savefig('figs/Example-Poisson-Var.'+ff,format=ff)
        
        if PROBLEM == 1:
            ''' Plot the PDF of the solutions at x=(1,0.5) 
            ''
            '' Interpolate the space coordinate at x=(1,0.5)
            '' Interpolate the random space (theta) at certain values
            ''
            '''
            
            # Spatial interpolation at x=(1,0.5) for all the modes
            xI = np.array([[1.,0.]])
            V2DI = poly.GradVandermonde(xI,[P,P],[0,0],usekron=False)
            V2D = np.kron(V1D,V1D)
            uI = np.dot(V2DI,npla.solve(V2D,Ush.T))
            
            # Stochastic interpolation at theta values
            pp = SpectralND.PolyND(gPC_polys)
            gPC_vals = gPC_distsPoly[0].rvs(100000)
            gPC_VI_theta = pp.GradVandermonde([gPC_vals],[doGPC_N],[0])
            
            # Interpolate
            f_theta = np.dot(gPC_VI_theta, uI.T)
            
            kernel = stats.gaussian_kde(f_theta.flatten())
            xtheta = np.linspace(0.,np.max(f_theta),100)
            
            fig = plt.figure()
            plt.plot(kernel(xtheta))
            plt.xlabel('u(1,0.5)')
            plt.ylabel('pdf')
            plt.title('gPC - approx PDF')
            plt.show(block=False)

if doSparseGrid:
    time_SparseGrid_start = time.clock()
    '''
    #############################################################################
    #############################################################################
    #                              Sparse Grid                                  #
    #############################################################################
    '''
    time_SparseGrid_ExperimentConstruction_start = time.clock()
    ''' Construct differential operator '''
    (x1D,w1D) = poly1D.GaussLobattoQuadrature(P)
    V1D = poly1D.GradVandermonde1D(x1D,P,0)
    Vx1D = poly1D.GradVandermonde1D(x1D,P,1)
    D1D = np.linalg.solve(V1D.T,Vx1D.T).T
    
    Dx1D = np.kron(D1D,np.eye(P+1))
    Dy1D = np.kron(np.eye(P+1),D1D)
    
    # Set Neumann bc
    Dx1D_neu = Dx1D.copy()
    for BC_neu_idx,BC_neu_f in BC_x_neu:
        Dx1D_neu[BC_neu_idx,:] = 0.0 
        Dx1D_neu[BC_neu_idx,BC_neu_idx] = BC_neu_f(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1])
    Dy1D_neu = Dy1D.copy()
    for BC_neu_idx,BC_neu_f in BC_y_neu:
        Dy1D_neu[BC_neu_idx,:] = 0.0 
        Dy1D_neu[BC_neu_idx,BC_neu_idx] = BC_neu_f(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1])
    
    F = f(xScaled[:,0],xScaled[:,1]) #/ poly1D.Gamma(0)**2.
    
    def poisson2D(params):
        
        V = np.diag(kappa(xScaled[:,0],xScaled[:,1],params))
        
        # Construct L operator
        L = np.dot(Dx1D, np.dot(V,Dx1D_neu)) + np.dot(Dy1D, np.dot(V,Dy1D_neu))
        
        # Impose Dirichlet Boundary Conditions
        for BC_dir_idx,BC_dir_f in BC_dir:
            L[BC_dir_idx,:] = 0.
            L[BC_dir_idx,BC_dir_idx] = 1.
            F[BC_dir_idx] = BC_dir_f(xScaled[BC_dir_idx,0],xScaled[BC_dir_idx,1])
        
        # Sparsify
        L_sparse = sparse.coo_matrix(L)
        
        ''' Solve the system '''
        u = sparse.linalg.spsolve(L_sparse,F)
        
        return u
    
    def action(sols,newSol):
        if len(sols) == 0:
            sols = [newSol]
        else:
            sols.append(newSol)
        return sols
    
    time_SparseGrid_ExperimentConstruction_stop = time.clock()
    
    time_SparseGrid_ExperimentRun_start = time.clock()
    ''' Construct sparse grid '''
    sg = SparseGrids.SparseGrid(SparseGrids.GQN,len(dists),doSparseGrid_level,sym=1)
    (SG_x,SG_w) = sg.sparseGrid()
    
    ''' Run Experiments '''
    sols = UQ.Experiments(poisson2D, SG_x, params, paramUpdate, action)
    sols = np.asarray(sols).T
    time_SparseGrid_ExperimentRun_stop = time.clock()
    time_SparseGrid_stop = time.clock()
    
    ''' Compute mean and variance '''
    SG_mean = np.dot(sols, SG_w)
    SG_var = np.dot(sols**2., SG_w) - SG_mean**2.
    
    if PLOTTING:
        ''' Plot Mean and Variance '''
        fig = plt.figure(figsize=(14,7))
        ax = fig.add_subplot(1,2,1,projection='3d')
        X = xScaled[:,0].reshape((P+1,P+1))
        Y = xScaled[:,1].reshape((P+1,P+1))
        Z = SG_mean.reshape((P+1,P+1))
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        plt.title('SG Mean')
        ax = fig.add_subplot(1,2,2,projection='3d')
        ax = fig.gca(projection='3d')
        Z = SG_var.reshape((P+1,P+1))
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        plt.title('SG Var')
        
        ''' Plot Mean and Variance '''
        fig = plt.figure(figsize=(14,7))
        ax = fig.add_subplot(1,2,1)
        X = xScaled[:,0].reshape((P+1,P+1))
        Y = xScaled[:,1].reshape((P+1,P+1))
        Z = SG_mean.reshape((P+1,P+1))
        CS = ax.contour(X,Y,Z)
        plt.clabel(CS, inline=1, fontsize=10)
        plt.title('SG Mean')
        ax = fig.add_subplot(1,2,2)
        Z = SG_var.reshape((P+1,P+1))
        CS = ax.contour(X,Y,Z)
        plt.clabel(CS, inline=1, fontsize=10)
        plt.title('SG Var')
        
        if PROBLEM == 1:
            ''' Plot histogram of solutions at x=(1,0.5) '''
            V2D = poly.GradVandermonde(x,[P,P],[0,0],usekron=False)
            
            xI = np.array([[1., 0.]])
            V2DI = poly.GradVandermonde(xI,[P,P],[0,0],usekron=False)
            
            uHat = npla.solve(V2D,np.array(sols))
            uI = np.dot(V2DI,uHat)
            
            fig = plt.figure()
            ax = fig.add_subplot(1,1,1)
            ax.hist(uI.flatten(),bins=20, normed=True)
            plt.xlabel('u(1,0.5)')
            plt.ylabel('Perc. of occurrences')
            plt.title('SG - Histogram')
    
if doSparseGrid_convergence:
    uI_mean = np.zeros(len(doSparseGrid_convergence_level))
    uI_var = np.zeros(len(doSparseGrid_convergence_level))
    SG_N = np.zeros(len(doSparseGrid_convergence_level),dtype=int)
    for i_level,level in enumerate(doSparseGrid_convergence_level):
        '''
        #############################################################################
        #############################################################################
        #                              Sparse Grid                                  #
        #############################################################################
        '''
        ''' Construct differential operator '''
        (x1D,w1D) = poly1D.GaussLobattoQuadrature(P)
        V1D = poly1D.GradVandermonde1D(x1D,P,0)
        Vx1D = poly1D.GradVandermonde1D(x1D,P,1)
        D1D = np.linalg.solve(V1D.T,Vx1D.T).T
        
        Dx1D = np.kron(D1D,np.eye(P+1))
        Dy1D = np.kron(np.eye(P+1),D1D)
        
        # Set Neumann bc
        Dx1D_neu = Dx1D.copy()
        for BC_neu_idx,BC_neu_f in BC_x_neu:
            Dx1D_neu[BC_neu_idx,:] = 0.0 
            Dx1D_neu[BC_neu_idx,BC_neu_idx] = BC_neu_f(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1])
        Dy1D_neu = Dy1D.copy()
        for BC_neu_idx,BC_neu_f in BC_y_neu:
            Dy1D_neu[BC_neu_idx,:] = 0.0 
            Dy1D_neu[BC_neu_idx,BC_neu_idx] = BC_neu_f(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1])
        
        F = f(xScaled[:,0],xScaled[:,1]) #/ poly1D.Gamma(0)**2.
        
        def poisson2D(params):
            
            V = np.diag(kappa(xScaled[:,0],xScaled[:,1],params))
            
            # Construct L operator
            L = np.dot(Dx1D, np.dot(V,Dx1D_neu)) + np.dot(Dy1D, np.dot(V,Dy1D_neu))
            
            # Impose Dirichlet Boundary Conditions
            for BC_dir_idx,BC_dir_f in BC_dir:
                L[BC_dir_idx,:] = 0.
                L[BC_dir_idx,BC_dir_idx] = 1.
                F[BC_dir_idx] = BC_dir_f(xScaled[BC_dir_idx,0],xScaled[BC_dir_idx,1])
            
            # Sparsify
            L_sparse = sparse.coo_matrix(L)
            
            ''' Solve the system '''
            u = sparse.linalg.spsolve(L_sparse,F)
            
            return u
        
        def action(sols,newSol):
            if len(sols) == 0:
                sols = [newSol]
            else:
                sols.append(newSol)
            return sols
        
        ''' Construct sparse grid '''
        sg = SparseGrids.SparseGrid(SparseGrids.GQN,len(dists),level,sym=1)
        (SG_x,SG_w) = sg.sparseGrid()
        
        ''' Run Experiments '''
        sols = UQ.Experiments(poisson2D, SG_x, params, paramUpdate, action)
        sols = np.asarray(sols).T
        
        ''' Compute mean and variance '''
        SG_mean = np.dot(sols, SG_w)
        SG_var = np.dot(sols**2., SG_w) - SG_mean**2.
        
        ''' Interpolate and store SG_mean and SG_var at (1,0.5) '''
        V2D = poly.GradVandermonde(x,[P,P],[0,0],usekron=False)
        xI = np.array([[1., 0.]])
        V2DI = poly.GradVandermonde(xI,[P,P],[0,0],usekron=False)
        uHat_mean = npla.solve(V2D,SG_mean)
        uHat_var = npla.solve(V2D,SG_var)
        uI_mean[i_level] = np.dot(V2DI,uHat_mean)
        uI_var[i_level] = np.dot(V2DI,uHat_var)
        SG_N[i_level] = SG_x.shape[0]
    
    fig = plt.figure()
    ax = fig.add_subplot(2,1,1)
    plt.title("SG mean and variance convergence")
    ax.plot(SG_N, uI_mean)
    plt.ylabel('Mean')
    ax.grid()
    ax = fig.add_subplot(2,1,2)
    ax.plot(SG_N, uI_var)
    ax.grid()
    plt.xlabel('N')
    plt.ylabel('Var')

if doGPC_convergence:
    gPC_pdf_est_N = 100000
    f_theta_vec = np.zeros((len(doGPC_convergence_orders),gPC_pdf_est_N))
    time_gPC_convergence = np.zeros((len(doGPC_convergence_orders),2))
    time_gPC_convergence_StochasticAssembly = np.zeros((len(doGPC_convergence_orders),2))
    time_gPC_convergence_Assembly = np.zeros((len(doGPC_convergence_orders),2))
    time_gPC_convergence_Solve = np.zeros((len(doGPC_convergence_orders),2))
    mean_gPC_convergence = []
    mean_err_gPC_convergence = np.zeros(len(doGPC_convergence_orders)-1)
    sp_ratio = np.zeros((len(doGPC_convergence_orders)))
    for doGPC_N,gPC_conv_i in zip(doGPC_convergence_orders, range(len(doGPC_convergence_orders))):
        time_gPC_convergence[gPC_conv_i,0] = time.clock()
        '''
        #############################################################################
        #############################################################################
        #                    Polynomial Chaos Expansion                             #
        #############################################################################
        '''
        time_gPC_convergence_StochasticAssembly[gPC_conv_i,0] = time.clock()
        
        gPC_polys = []
        for i in range(len(gPC_polysType)):
            gPC_polys.append(Spectral1D.Poly1D( gPC_polysType[i], gPC_polysParams[i] ))
        
        '''
        #############################################################################
        #                      Expansion of Uncertainty                             #
        #############################################################################
        '''
        dictionary = UQ.gPC_MultiIndex( dists, gPC_polys, gPC_distsPoly, doGPC_N, int(np.ceil(3./2. * doGPC_N)))
        gPC_x = dictionary['x']
        gPC_w = dictionary['w']
        gPC_vals = dictionary['vals']
        gPC_V = dictionary['V']
        gPC_wI = dictionary['wI']
        gPC_VI = dictionary['VI']
        
        print "[BGN] gPC: Evaluate KL-expansion"
        vals = np.zeros((gPC_vals.shape[0],xScaled.shape[0]))
        for i in range(gPC_vals.shape[0]):
            print "\r%d/%d" % (i,gPC_vals.shape[0]),
            vals[i,:] = kappa(xScaled[:,0],xScaled[:,1], gPC_vals[i,:])
        
        gPC_vals = vals
        print "\n[END] gPC: Evaluate KL-expansion"
        
        # Transform (NORMALIZED)
        #yHat = linalg.solve(V,vals)
        [gPC_yHat, gPC_res, gPC_rank, gPC_s]  = npla.lstsq(gPC_V,gPC_vals)
        
        '''
        #############################################################################
        #                      Setup gPC matrices                                   #
        #############################################################################
        '''
        gPC_NI = gPC_VI.shape[0]; # Number of collocation points for each dof of the dynamical system
        gPC_MI = gPC_VI.shape[1]; # Length of the expansion for each dof of the dynamical system
        
        '''  Compute the e matrix using the Vandermonde (NORMALIZED) matrix '''    
        print "[BGN] gPC: Computing gPC_E"    
        import itertools
        ''' Index function definition '''
        def gPC_idxF(l,i,j):
            def idx2(i,j,M):
                return (j-i) + i*M - sum([k for k in range(i)])
            return int( sum([idx2(gPC_MI-k,gPC_MI-k,gPC_MI-k) for k in range(l)]) + idx2(i-l,j-l,gPC_MI-l) )
        
        gPC_E_idx = list(itertools.combinations_with_replacement(range(gPC_MI),3))
        gPC_E = np.zeros(len(gPC_E_idx))
        for l,(i,j,k) in enumerate(gPC_E_idx):
            print "\r%d/%d" % (l,len(gPC_E_idx)),
            gPC_E[l] = np.dot(gPC_VI[:,i]*gPC_VI[:,j]*gPC_VI[:,k],gPC_wI)
        print '\n'
        
        print "[END] gPC: Computing gPC_E"
        
        ''' Assemble the A matrix '''    
        print "[BGN] gPC: Computing gPC_tensor"
        NP = xScaled.shape[0]
        #    gPC_tensor = np.zeros((gPC_MI,gPC_MI))
        tensor = []
        row = []
        col = []
        for j in range(0,gPC_MI):
            for k in range(j,gPC_MI):
                tt = np.zeros(NP)
                for i in range(0,gPC_MI):
                    idx = np.sort((i,j,k))
                    tt += gPC_yHat[i,:] * gPC_E[gPC_idxF(idx[0],idx[1],idx[2])]
                tensor.append(tt)
                row.append( (j*NP + np.arange(NP,dtype=np.int)) )
                col.append( (k*NP + np.arange(NP,dtype=np.int)) )
        
        tensor = np.asarray(tensor)
        row = np.asarray(row)
        col = np.asarray(col)
        
        gPC_tensor = sparse.csr_matrix( (tensor.ravel(),(row.ravel(),col.ravel())) )
        
        gPC_tensor_diag = gPC_tensor.diagonal()
        gPC_tensor = gPC_tensor - sparse.csr_matrix((gPC_tensor_diag,(range(gPC_MI*NP),range(gPC_MI*NP))))
        gPC_tensor = gPC_tensor + gPC_tensor.transpose()
        gPC_tensor = gPC_tensor + sparse.csr_matrix((gPC_tensor_diag,(range(gPC_MI*NP),range(gPC_MI*NP))))
        
        print "[END] gPC: Computing gPC_tensor"
        
        time_gPC_convergence_StochasticAssembly[gPC_conv_i,1] = time.clock()
        
        '''
        #############################################################################
        #             Setup Stochastic-Deterministic Solver                         #
        #############################################################################
        # Set up on top of the stochastic problem
        '''
        time_gPC_convergence_Assembly[gPC_conv_i,0] = time.clock()
        
        ''' Construct differential operator '''
        (x1D,w1D) = poly1D.GaussLobattoQuadrature(P)
        V1D = poly1D.GradVandermonde1D(x1D,P,0)
        Vx1D = poly1D.GradVandermonde1D(x1D,P,1)
        D1D = np.linalg.solve(V1D.T,Vx1D.T).T
        
        Dx1D = np.kron(D1D,np.eye(P+1))
        Dy1D = np.kron(np.eye(P+1),D1D)
        
        # Set Neumann bc
        Dx1D_neu = Dx1D.copy()
        for BC_neu_idx,BC_neu_f in BC_x_neu:
            Dx1D_neu[BC_neu_idx,:] = 0.0 
            Dx1D_neu[BC_neu_idx,BC_neu_idx] = BC_neu_f(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1])
        Dy1D_neu = Dy1D.copy()
        for BC_neu_idx,BC_neu_f in BC_y_neu:
            Dy1D_neu[BC_neu_idx,:] = 0.0 
            Dy1D_neu[BC_neu_idx,BC_neu_idx] = BC_neu_f(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1])
        
        # Sparsify and Expand the Differentiation matrices to (M*(P+1)**2)x(M*(P+1)**2)
        Dx1D_sparse = sparse.csr_matrix(Dx1D)
        Dy1D_sparse = sparse.csr_matrix(Dy1D)
        Dx1D_neu_sparse = sparse.csr_matrix(Dx1D_neu)
        Dy1D_neu_sparse = sparse.csr_matrix(Dy1D_neu)
        ID = sparse.identity(gPC_MI)
        
        Dx1D_exp_sparse = sparse.kron(ID,Dx1D_sparse)
        Dy1D_exp_sparse = sparse.kron(ID,Dy1D_sparse)
        Dx1D_neu_exp_sparse = sparse.kron(ID,Dx1D_neu_sparse)
        Dy1D_neu_exp_sparse = sparse.kron(ID,Dy1D_neu_sparse)
        
        # Construct L operator
        L = Dx1D_exp_sparse.dot( gPC_tensor.dot(Dx1D_neu_exp_sparse) ) + Dy1D_exp_sparse.dot( gPC_tensor.dot(Dy1D_neu_exp_sparse) )
        
        # Construct f 
        F = np.zeros(gPC_MI*(P+1)**2)
        F[:(P+1)**2] = f(xScaled[:,0],xScaled[:,1]) # / poly1D.Gamma(0)**2.
        
        # Impose Dirichlet Boundary Conditions
        def csr_row_set_nz_to_val(csr, row, value=0):
            """Set all nonzero elements (elements currently in the sparsity pattern)
            to the given value. Useful to set to 0 mostly.
            """
            if not isinstance(csr, sparse.csr_matrix):
                raise ValueError('Matrix given must be of CSR format.')
            csr.data[csr.indptr[row]:csr.indptr[row+1]] = value
        
        print "[BGN] gPC: Impose Dirichlet Boundary Conditions"
        for BC_dir_idx,BC_dir_f in BC_dir:
            for i in range(0,gPC_MI):
                idxs = i*(P+1)**2 + np.asarray(BC_dir_idx)
                for idx in idxs:
                    csr_row_set_nz_to_val(L,idx,0.)
                    L[idx,idx] = 1.
                F[idxs] = BC_dir_f(xScaled[BC_dir_idx,0],xScaled[BC_dir_idx,1])
                
        print "[END] gPC: Impose Dirichlet Boundary Conditions"
        
        time_gPC_convergence_Assembly[gPC_conv_i,1] = time.clock()
        
#        plt.figure()
#        plt.spy(L)
        
        sp_ratio[gPC_conv_i] = len(L.nonzero()[0])/L.shape[0]**2.
        print("Sparse ratio non-zero/total = %f" % (sp_ratio[gPC_conv_i]))
        
        ''' Solve the system '''
        time_gPC_convergence_Solve[gPC_conv_i,0] = time.clock()
        U = sparse.linalg.spsolve(L,F)
        time_gPC_convergence_Solve[gPC_conv_i,1] = time.clock()
        time_gPC_convergence[gPC_conv_i,1] = time.clock()
        
        Ush = U.reshape((gPC_MI,(P+1)**2))
        
        ''' Interpolate options '''
        if doGPC_interpolate:
            # Prepare matrices for interpolation
            V2D = np.kron(V1D,V1D)
            x1DI = np.linspace(-1,1,doGPC_interpolate_N)
            V1DI = poly1D.GradVandermonde1D(x1DI,P,0)
            V2DI = np.kron(V1DI,V1DI)
        
        ''' Compute Mean and Variance '''
        UMean = Ush[0,:]
        UVar = np.sum(Ush[1:,:]**2.,0)
        
        mean_gPC_convergence.append(UMean.copy())
        
        ''' Plot the PDF of the solutions at x=(1,0.5) 
        ''
        '' Interpolate the space coordinate at x=(1,0.5)
        '' Interpolate the random space (theta) at certain values
        ''
        '''
        
        # Spatial interpolation at x=(1,0.5) for all the modes
        xI = np.array([[1.,0.]])
        V2DI = poly.GradVandermonde(xI,[P,P],[0,0],usekron=False)
        uI = np.dot(V2DI,npla.solve(V2D,Ush.T))
        
        # Stochastic interpolation at theta values
        pp = SpectralND.PolyND(gPC_polys)
        gPC_vals = gPC_distsPoly[0].rvs(gPC_pdf_est_N)
        gPC_VI_theta = pp.GradVandermonde([gPC_vals],[doGPC_N],[0])
        
        # Interpolate
        f_theta_vec[gPC_conv_i,:] = np.dot(gPC_VI_theta, uI[0])
    
    for i in range(len(doGPC_convergence_orders)-1):
        mean_err_gPC_convergence[i] = npla.norm(mean_gPC_convergence[i].flatten() - mean_gPC_convergence[-1].flatten(),2)
    
    if PLOTTING:
        # Convergence of point pdf
        markers = ['-','--','-.',':']
        fig = plt.figure(figsize=(6,5))
        xtheta = np.linspace(0.,np.max(f_theta_vec),100)
        for i in range(len(doGPC_convergence_orders[:4])):
            kernel = stats.gaussian_kde(f_theta_vec[i,:].flatten())
            plt.plot(xtheta, kernel(xtheta), 'k'+markers[i], label='Ord = %d' % doGPC_convergence_orders[i])
            # plt.hist(f_theta_vec[i,:],bins=100,histtype='step',normed=True,label='Ord = %d' % doGPC_convergence_orders[i])
    #        plt.plot(f_theta_vec[i,:],PDF,'.-',label='Ord = %d' % doGPC_convergence_orders[i])
        plt.xlabel('u(1,0.5)')
        plt.ylabel('pdf')
        plt.legend()
        plt.show(False)
        if STORE_FIG:
            for ff in FORMATS:
                plt.savefig('figs/Example-Poisson-PDF.'+ff,format=ff)
        
        # Convergence error vs order and error vs cputime
        fig = plt.figure(figsize=(6,5))
        cpu_time = np.diff(time_gPC_convergence,axis=1)
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twiny()
        gPC_ln1 = ax1.loglog(doGPC_convergence_orders[:-1],mean_err_gPC_convergence,'ko-',label='gPC vs. order')
        ax1.set_xlabel("Log10 - Order - N eval.")
        ax1.set_ylabel("Log10(Err)")
        # ax2.set_xticks(doGPC_convergence_orders[:-1])
        # ax2.set_xticklabels([ "%.2f"%v for v in np.log10(cpu_time[:-1,0])])
        gPC_ln2 = ax2.loglog(cpu_time[:-1,0],mean_err_gPC_convergence,'ko--',label='gPC vs. CPU time')
        ax2.set_xlabel("Log10 - CPU time")
        if doMonteCarlo:
            space = np.logspace(0,np.log10(doMonteCarlo_N),40,dtype=int)
            mean_err_MC_convergence = np.zeros(len(space))
            for i,ii in enumerate(space):
                mean_err_MC_convergence[i] = npla.norm( mean_gPC_convergence[-1].flatten() - np.mean( np.asarray(MC_sols[:(ii+1)]), axis=0).flatten(), 2 )
            MC_ln1 = ax1.loglog(space,mean_err_MC_convergence,'k-',label='MC vs. N eval.')
            MC_ln2 = ax2.loglog(np.logspace(0.0,np.log10(time_MC_stop-time_MC_start),len(space)),mean_err_MC_convergence,'k--',label='MC vs. CPU time')
        if doLHC:
            space = np.logspace(0,np.log10(doLHC_N),40,dtype=int)
            mean_err_LHC_convergence = np.zeros(len(space))
            for i,ii in enumerate(space):
                mean_err_LHC_convergence[i] = npla.norm( mean_gPC_convergence[-1].flatten() - np.mean( np.asarray(LHC_sols[:(ii+1)]), axis=0).flatten(), 2 )
            LHC_ln1 = ax1.loglog(space,mean_err_LHC_convergence,'k^-',label='LHC vs. N eval.')
            LHC_ln2 = ax2.loglog(np.logspace(0.0,np.log10(time_LHC_stop-time_LHC_start),len(space)),mean_err_LHC_convergence,'k^--',label='LHC vs. CPU time')
        lns = gPC_ln1+gPC_ln2+MC_ln1+MC_ln2+LHC_ln1+LHC_ln2
        labs = [l.get_label() for l in lns]
        ax2.legend(lns, labs, loc='lower right')
        plt.show(False)
        if STORE_FIG:
            for ff in FORMATS:
                plt.savefig('figs/Example-Poisson-Convergence.'+ff,format=ff)

if doCollocation:
    time_Coll_start = time.clock()
    '''
    #############################################################################
    #############################################################################
    #                    Polynomial Chaos Expansion                             #
    #############################################################################
    '''
    
    time_Coll_Assembly_start = time.clock()
    
    Coll_polys = []
    for i in range(len(gPC_polysType)):
        Coll_polys.append(Spectral1D.Poly1D( gPC_polysType[i], gPC_polysParams[i] ))
    
    '''
    #############################################################################
    #                      Expansion of Uncertainty                             #
    #############################################################################
    '''
    dictionary = UQ.gPC_MultiIndex( dists, Coll_polys, gPC_distsPoly, doCollocation_N, int(np.ceil(3./2. * doCollocation_N)), warnings=doCollocation_warnings)
    Coll_x = dictionary['x']
    Coll_w = dictionary['w']
    Coll_vals = dictionary['vals']
    Coll_V = dictionary['V']
    Coll_wI = dictionary['wI']
    Coll_VI = dictionary['VI']
    Coll_NI = Coll_VI.shape[0]; # Number of collocation points for each dof of the dynamical system
    Coll_MI = Coll_VI.shape[1]; # Length of the expansion for each dof of the dynamical system
    
    ''' Construct differential operator '''
    (x1D,w1D) = poly1D.GaussLobattoQuadrature(P)
    V1D = poly1D.GradVandermonde1D(x1D,P,0)
    Vx1D = poly1D.GradVandermonde1D(x1D,P,1)
    D1D = np.linalg.solve(V1D.T,Vx1D.T).T
    
    Dx1D = np.kron(D1D,np.eye(P+1))
    Dy1D = np.kron(np.eye(P+1),D1D)
    
    # Set Neumann bc
    Dx1D_neu = Dx1D.copy()
    for BC_neu_idx,BC_neu_f in BC_x_neu:
        Dx1D_neu[BC_neu_idx,:] = 0.0 
        Dx1D_neu[BC_neu_idx,BC_neu_idx] = BC_neu_f(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1])
    Dy1D_neu = Dy1D.copy()
    for BC_neu_idx,BC_neu_f in BC_y_neu:
        Dy1D_neu[BC_neu_idx,:] = 0.0 
        Dy1D_neu[BC_neu_idx,BC_neu_idx] = BC_neu_f(xScaled[BC_neu_idx,0],xScaled[BC_neu_idx,1])
    
    F = f(xScaled[:,0],xScaled[:,1]) #/ poly1D.Gamma(0)**2.
    
    def poisson2D(params,pp):
        
        V = np.diag(kappa(xScaled[:,0],xScaled[:,1],params))
        
        # Construct L operator
        L = np.dot(Dx1D, np.dot(V,Dx1D_neu)) + np.dot(Dy1D, np.dot(V,Dy1D_neu))
        
        # Impose Dirichlet Boundary Conditions
        for BC_dir_idx,BC_dir_f in BC_dir:
            L[BC_dir_idx,:] = 0.
            L[BC_dir_idx,BC_dir_idx] = 1.
            F[BC_dir_idx] = BC_dir_f(xScaled[BC_dir_idx,0],xScaled[BC_dir_idx,1])
        
        # Sparsify
        L_sparse = sparse.coo_matrix(L)
        
        ''' Solve the system '''
        u = sparse.linalg.spsolve(L_sparse,F)
        
        return u

    time_Coll_Assembly_stop = time.clock()
    
    ''' Solve the system '''
    time_Coll_Solve_start = time.clock()
    print "[BGN] Coll: Solving"
    Coll_sols = [ poisson2D(Coll_vals[i,:],None) for i in range(len(Coll_vals)) ]
    time_Coll_Solve_stop = time.clock()
    time_Coll_stop = time.clock()
    
    Sols = np.asarray(Coll_sols)
    Ush = np.dot(Coll_V.T, Sols * Coll_w[:,np.newaxis] )
    
    ''' Interpolate options '''
    if doCollocation_interpolate:
        # Prepare matrices for interpolation
        V2D = np.kron(V1D,V1D)
        x1DI = np.linspace(-1,1,doCollocation_interpolate_N)
        V1DI = poly1D.GradVandermonde1D(x1DI,P,0)
        V2DI = np.kron(V1DI,V1DI)
    
    ''' Compute Mean and Variance '''
    UMean = Ush[0,:]
    UVar = np.sum(Ush[1:,:]**2.,0)
    
    if PLOTTING:
        ''' Plot Collocation (Interpolate) '''
        fig = plt.figure(figsize=(14,8))
        for i in range(0,min(Coll_MI,6)):
            ax = fig.add_subplot(2,3,i+1, projection='3d')
            
            if not doCollocation_interpolate:
                X = xScaled[:,0].reshape((P+1,P+1))
                Y = xScaled[:,1].reshape((P+1,P+1))
                Z = Sols[i,:].reshape((P+1,P+1))
            else:
                (X,Y) = np.meshgrid(x1DI,x1DI)
                X = X.T
                Y = Y.T
                SolsI = np.dot(V2DI, npla.solve(V2D,Ush[i,:]))
                Z = SolsI.reshape((doCollocation_interpolate_N,doCollocation_interpolate_N))
            surf = ax.plot_surface(X,Y,Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
            plt.ticklabel_format(style='sci', axis='z', scilimits=(0,0))
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            plt.title('Coll %d' % i)
        fig.tight_layout()
        if STORE_FIG:
            for ff in FORMATS:
                plt.savefig('figs/Example-Coll-Poisson-Points.'+ff,format=ff)
        
        ''' Plot Mean and Variance (Interpolate) '''
        fig = plt.figure(figsize=(6,5))
        ax = fig.add_subplot(1,1,1,projection='3d')
        if not doCollocation_interpolate:
            X = xScaled[:,0].reshape((P+1,P+1))
            Y = xScaled[:,1].reshape((P+1,P+1))
            Z = UMean.reshape((P+1,P+1))
        else:
            (X,Y) = np.meshgrid(x1DI,x1DI)
            X = X.T
            Y = Y.T
            UMeanI = np.dot(V2DI, npla.solve(V2D,UMean))
            Z = UMeanI.reshape((doCollocation_interpolate_N,doCollocation_interpolate_N))
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        plt.ticklabel_format(style='sci', axis='z', scilimits=(0,0))
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('E[u]')
        fig.tight_layout()
        if STORE_FIG:
            for ff in FORMATS:
                plt.savefig('figs/Example-Coll-Poisson-Mean.'+ff,format=ff)

        fig = plt.figure(figsize=(6,5))
        ax = fig.add_subplot(1,1,1,projection='3d')
        if not doCollocation_interpolate:
            ax = fig.gca(projection='3d')
            Z = UVar.reshape((P+1,P+1))
        else:
            (X,Y) = np.meshgrid(x1DI,x1DI)
            X = X.T
            Y = Y.T
            UVarI = np.dot(V2DI, npla.solve(V2D,UVar))
            Z = UVarI.reshape((doCollocation_interpolate_N,doCollocation_interpolate_N))
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        plt.ticklabel_format(style='sci', axis='z', scilimits=(0,0))
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('V[u]')
        fig.tight_layout()
        if STORE_FIG:
            for ff in FORMATS:
                plt.savefig('figs/Example-Coll-Poisson-Var.'+ff,format=ff)
        
        if PROBLEM == 1:
            ''' Plot the PDF of the solutions at x=(1,0.5) 
            ''
            '' Interpolate the space coordinate at x=(1,0.5)
            '' Interpolate the random space (theta) at certain values
            ''
            '''
            
            # Spatial interpolation at x=(1,0.5) for all the modes
            xI = np.array([[1.,0.]])
            V2DI = poly.GradVandermonde(xI,[P,P],[0,0],usekron=False)
            V2D = np.kron(V1D,V1D)
            uI = np.dot(V2DI,npla.solve(V2D,Ush.T))
            
            # Stochastic interpolation at theta values
            pp = SpectralND.PolyND(Coll_polys)
            Coll_vals = gPC_distsPoly[0].rvs(100000)
            Coll_VI_theta = pp.GradVandermonde([Coll_vals],[doCollocation_N],[0])
            
            # Interpolate
            f_theta = np.dot(Coll_VI_theta, uI.T)
            
            kernel = stats.gaussian_kde(f_theta.flatten())
            xtheta = np.linspace(0.,np.max(f_theta),100)
            
            fig = plt.figure()
            plt.plot(kernel(xtheta))
            plt.xlabel('u(1,0.5)')
            plt.ylabel('pdf')
            plt.title('Coll - approx PDF')
            plt.show(block=False)


if doCollocation_convergence:
    Coll_pdf_est_N = 100000
    f_theta_vec = np.zeros((len(doCollocation_convergence_orders),Coll_pdf_est_N))
    time_Coll_convergence = np.zeros((len(doCollocation_convergence_orders),2))
    time_Coll_convergence_StochasticAssembly = np.zeros((len(doCollocation_convergence_orders),2))
    time_Coll_convergence_Assembly = np.zeros((len(doCollocation_convergence_orders),2))
    time_Coll_convergence_Solve = np.zeros((len(doCollocation_convergence_orders),2))
    mean_Coll_convergence = []
    mean_err_Coll_convergence = np.zeros(len(doCollocation_convergence_orders)-1)
    sp_ratio = np.zeros((len(doCollocation_convergence_orders)))
    for doCollocation_N,Coll_conv_i in zip(doCollocation_convergence_orders, range(len(doCollocation_convergence_orders))):
        time_Coll_convergence[Coll_conv_i,0] = time.clock()
        '''
        #############################################################################
        #############################################################################
        #                    Polynomial Chaos Expansion                             #
        #############################################################################
        '''
        time_Coll_convergence_Assembly[Coll_conv_i,0] = time.clock()
        
        Coll_polys = []
        for i in range(len(gPC_polysType)):
            Coll_polys.append(Spectral1D.Poly1D( gPC_polysType[i], gPC_polysParams[i] ))
        
        '''
        #############################################################################
        #                      Expansion of Uncertainty                             #
        #############################################################################
        '''
        dictionary = UQ.gPC_MultiIndex( dists, Coll_polys, gPC_distsPoly, doCollocation_N, int(np.ceil(3./2. * doCollocation_N)))
        Coll_x = dictionary['x']
        Coll_w = dictionary['w']
        Coll_vals = dictionary['vals']
        Coll_V = dictionary['V']
        Coll_wI = dictionary['wI']
        Coll_VI = dictionary['VI']
        
        time_Coll_convergence_Assembly[Coll_conv_i,1] = time.clock()
                
        ''' Solve the system '''
        time_Coll_convergence_Solve[Coll_conv_i,0] = time.clock()
        Coll_sols = [ poisson2D(Coll_vals[i,:],None) for i in range(len(Coll_vals)) ]
        time_Coll_convergence_Solve[Coll_conv_i,1] = time.clock()
        time_Coll_convergence[Coll_conv_i,1] = time.clock()
        
        Sols = np.asarray(Coll_sols)
        Ush = np.dot(Coll_V.T, Sols * Coll_w[:,np.newaxis] )
        
        ''' Interpolate options '''
        if doCollocation_interpolate:
            # Prepare matrices for interpolation
            V2D = np.kron(V1D,V1D)
            x1DI = np.linspace(-1,1,doCollocation_interpolate_N)
            V1DI = poly1D.GradVandermonde1D(x1DI,P,0)
            V2DI = np.kron(V1DI,V1DI)
        
        ''' Compute Mean and Variance '''
        UMean = Ush[0,:]
        UVar = np.sum(Ush[1:,:]**2.,0)
        
        mean_Coll_convergence.append(UMean.copy())
        
        ''' Plot the PDF of the solutions at x=(1,0.5) 
        ''
        '' Interpolate the space coordinate at x=(1,0.5)
        '' Interpolate the random space (theta) at certain values
        ''
        '''
        
        # Spatial interpolation at x=(1,0.5) for all the modes
        xI = np.array([[1.,0.]])
        V2DI = poly.GradVandermonde(xI,[P,P],[0,0],usekron=False)
        uI = np.dot(V2DI,npla.solve(V2D,Ush.T))
        
        # Stochastic interpolation at theta values
        pp = SpectralND.PolyND(Coll_polys)
        Coll_vals = gPC_distsPoly[0].rvs(Coll_pdf_est_N)
        Coll_VI_theta = pp.GradVandermonde([Coll_vals],[doCollocation_N],[0])
        
        # Interpolate
        f_theta_vec[Coll_conv_i,:] = np.dot(Coll_VI_theta, uI[0])
    
    for i in range(len(doCollocation_convergence_orders)-1):
        mean_err_Coll_convergence[i] = npla.norm(mean_Coll_convergence[i].flatten() - mean_Coll_convergence[-1].flatten(),2)
    
    if PLOTTING:
        # Convergence of point pdf
        markers = ['-','--','-.',':']
        fig = plt.figure(figsize=(6,5))
        xtheta = np.linspace(0.,np.max(f_theta_vec),100)
        for i in range(len(doCollocation_convergence_orders[:4])):
            kernel = stats.gaussian_kde(f_theta_vec[i,:].flatten())
            plt.plot(xtheta, kernel(xtheta), 'k'+markers[i], label='Ord = %d' % doCollocation_convergence_orders[i])
            # plt.hist(f_theta_vec[i,:],bins=100,histtype='step',normed=True,label='Ord = %d' % doCollocation_convergence_orders[i])
    #        plt.plot(f_theta_vec[i,:],PDF,'.-',label='Ord = %d' % doCollocation_convergence_orders[i])
        plt.xlabel('u(1,0.5)')
        plt.ylabel('pdf')
        plt.legend()
        plt.show(False)
        if STORE_FIG:
            for ff in FORMATS:
                plt.savefig('figs/Example-Coll-Poisson-PDF.'+ff,format=ff)
        
        # Convergence error vs order and error vs cputime
        fig = plt.figure(figsize=(6,5))
        cpu_time = np.diff(time_Coll_convergence,axis=1)
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twiny()
        Coll_ln1 = ax1.loglog(doCollocation_convergence_orders[:-1],mean_err_Coll_convergence,'ko-',label='Coll vs. order')
        ax1.set_xlabel("Log10 - Order - N eval.")
        ax1.set_ylabel("Log10(Err)")
        # ax2.set_xticks(doCollocation_convergence_orders[:-1])
        # ax2.set_xticklabels([ "%.2f"%v for v in np.log10(cpu_time[:-1,0])])
        Coll_ln2 = ax2.loglog(cpu_time[:-1,0],mean_err_Coll_convergence,'ko--',label='Coll vs. CPU time')
        ax2.set_xlabel("Log10 - CPU time")
        lns = Coll_ln1+Coll_ln2
        if doMonteCarlo:
            space = np.logspace(0,np.log10(doMonteCarlo_N),40,dtype=int)
            mean_err_MC_convergence = np.zeros(len(space))
            for i,ii in enumerate(space):
                mean_err_MC_convergence[i] = npla.norm( mean_Coll_convergence[-1].flatten() - np.mean( np.asarray(MC_sols[:(ii+1)]), axis=0).flatten(), 2 )
            MC_ln1 = ax1.loglog(space,mean_err_MC_convergence,'k-',label='MC vs. N eval.')
            MC_ln2 = ax2.loglog(np.logspace(0.0,np.log10(time_MC_stop-time_MC_start),len(space)),mean_err_MC_convergence,'k--',label='MC vs. CPU time')
            lns += MC_ln1+MC_ln2
        if doLHC:
            space = np.logspace(0,np.log10(doLHC_N),40,dtype=int)
            mean_err_LHC_convergence = np.zeros(len(space))
            for i,ii in enumerate(space):
                mean_err_LHC_convergence[i] = npla.norm( mean_Coll_convergence[-1].flatten() - np.mean( np.asarray(LHC_sols[:(ii+1)]), axis=0).flatten(), 2 )
            LHC_ln1 = ax1.loglog(space,mean_err_LHC_convergence,'k^-',label='LHC vs. N eval.')
            LHC_ln2 = ax2.loglog(np.logspace(0.0,np.log10(time_LHC_stop-time_LHC_start),len(space)),mean_err_LHC_convergence,'k^--',label='LHC vs. CPU time')
            lns += LHC_ln1+LHC_ln2
        labs = [l.get_label() for l in lns]
        ax2.legend(lns, labs, loc='lower right')
        plt.show(False)
        if STORE_FIG:
            for ff in FORMATS:
                plt.savefig('figs/Example-Coll-Poisson-Convergence.'+ff,format=ff)

stopTime = time.clock()

print "CPU usage statistics"
print "[%.6fs] Problem Definition CPU time" % (time_ProblemDefinition_stop-time_ProblemDefinition_start)
if doMonteCarlo:
    print "\n=================================="
    print "[%.6fs] Monte Carlo Total CPU time" % (time_MC_stop-time_MC_start)
    print "\t [%.6fs] Experiment Construction CPU time" % (time_MC_ExperimentConstruction_stop-time_MC_ExperimentConstruction_start)
    print "\t [%.6fs] Experiment Running CPU time" % (time_MC_ExperimentRun_stop-time_MC_ExperimentRun_start)
if doLHC:
    print "\n=================================="
    print "[%.6fs] Latin Hyper Cube Total CPU time" % (time_LHC_stop-time_LHC_start)
    print "\t [%.6fs] Experiment Construction CPU time" % (time_LHC_ExperimentConstruction_stop-time_LHC_ExperimentConstruction_start)
    print "\t [%.6fs] Experiment Running CPU time" % (time_LHC_ExperimentRun_stop-time_LHC_ExperimentRun_start)
if doGPC:
    print "\n=================================="
    print "[%.6fs] gPC CPU time" % (time_gPC_stop-time_gPC_start)
    print "\t [%.6fs] gPC Stochastic Assembly CPU time" % (time_gPC_StochasticAssembly_stop-time_gPC_StochasticAssembly_start)
    print "\t [%.6fs] gPC General Assembly CPU time" % (time_gPC_Assembly_stop-time_gPC_Assembly_start)
    print "\t [%.6fs] gPC Solve CPU time" % (time_gPC_Solve_stop-time_gPC_Solve_start)
if doCollocation:
    print "\n=================================="
    print "[%.6fs] Coll CPU time" % (time_Coll_stop-time_Coll_start)
    print "\t [%.6fs] Coll General Assembly CPU time" % (time_Coll_Assembly_stop-time_Coll_Assembly_start)
    print "\t [%.6fs] Coll Solve CPU time" % (time_Coll_Solve_stop-time_Coll_Solve_start)
if doGPC_convergence:
    print "\n=================================="
    print "gPC Convergence Test"
    for i in range(len(doGPC_convergence_orders)):
        print "----------------------------------"
        print "Order: %d" % doGPC_convergence_orders[i]
        print "[%.6fs] gPC CPU time" % (time_gPC_convergence[i,1]-time_gPC_convergence[i,0])
        print "\t [%.6fs] gPC Stochastic Assembly CPU time" % (time_gPC_convergence_StochasticAssembly[i,1]-time_gPC_convergence_StochasticAssembly[i,0])
        print "\t [%.6fs] gPC General Assembly CPU time" % (time_gPC_convergence_Assembly[i,1]-time_gPC_convergence_Assembly[i,0])
        print "\t [%.6fs] gPC Solve CPU time" % (time_gPC_convergence_Solve[i,1]-time_gPC_convergence_Solve[i,0])
if doCollocation_convergence:
    print "\n=================================="
    print "Coll Convergence Test"
    for i in range(len(doCollocation_convergence_orders)):
        print "----------------------------------"
        print "Order: %d" % doCollocation_convergence_orders[i]
        print "[%.6fs] Coll CPU time" % (time_Coll_convergence[i,1]-time_Coll_convergence[i,0])
        print "\t [%.6fs] Coll General Assembly CPU time" % (time_Coll_convergence_Assembly[i,1]-time_Coll_convergence_Assembly[i,0])
        print "\t [%.6fs] Coll Solve CPU time" % (time_Coll_convergence_Solve[i,1]-time_Coll_convergence_Solve[i,0])
if doSparseGrid:
    print "[%.6fs] Sparse Grid Total CPU time" % (time_SparseGrid_stop-time_SparseGrid_start)
    print "\t [%.6fs] Experiment Construction CPU time" % (time_SparseGrid_ExperimentConstruction_stop-time_SparseGrid_ExperimentConstruction_start)
    print "\t [%.6fs] Experiment Running CPU time" % (time_SparseGrid_ExperimentRun_stop-time_SparseGrid_ExperimentRun_start)
