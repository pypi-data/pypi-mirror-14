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

__all__ = ['object_store','Driver']

import os
try:
    import cPickle as pkl
except ImportError:
    import pickle as pkl
import shutil
import sys
import warnings
import logging
import marshal, types
import time
import datetime
import numpy as np
from numpy import linalg as la
from numpy import random
from scipy import stats
from UQToolbox.sobol_lib import i4_sobol_generate
try:
    import mpi_map
    MPI_SUPPORT = True
except ImportError:
    MPI_SUPPORT = False

def object_store(path,obj):
    """ Used to store any object in the library.

    :param string path: path pointing to the location where to store the data
    :param object obj: a pickleable object

    """
    if os.path.isfile(path):
        # If the file already exists, make a safety copy
        shutil.copyfile(path, path+".old")
    ff = open(path,'wb')
    pkl.dump(obj,ff)
    ff.close()

class Driver(object):
    """ This class is devoted to the sampling from a multi dimensional distribution and the evaluation of a function `f` on it.
    
    :param function f: the function representing the experiment
    :param object params: parameters to be passed to the function ``f`` (pickable)
    :param list dists: list of distributions, instance of ``scipy.stats``
    :param bool marshal_f: whether to marshal the function ``f`` or not.
    :param str store_file: file path where to store the computed values
    """

    logger = logging.getLogger(__name__)
    logger.propagate = False
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s %(levelname)s:%(name)s: %(message)s",
                                  "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
        
    def __init__(self, f, params, marshal_f=True, store_file=""):

        self.f = None
        
        self.params = None
        self.f_code = None
        self.new_samples = []
        self.samples = []
        self.results = []
        self.store_file = ""
    
        self.serialize_list = ['new_samples','samples','results','f_code','params','store_file','serialize_list']
        
        self.set_f(f)
        self.set_params(params)
        self.store_file = store_file

    def __getstate__(self):
        return dict( [ (tag, getattr( self, tag )) for tag in self.serialize_list ] )

    def __setstate__(self,state,f = None, dists=None):
        for tag in state.keys():
            setattr(self, tag, state[tag])
        # Reset additional parameters
        if f == None: self.reset_f_marshal()
        else: self.set_f(f)
        
    def reset(self):
        self.samples = []
        self.new_samples = []
        self.results = []
    
    def set_f(self, f, marshal_f=True):
        self.f = f
        if self.f != None and marshal_f:
            self.f_code = marshal.dumps(self.f.__code__)
    
    def reset_f_marshal(self):
        if self.f_code != None:
            code = marshal.loads(self.f_code)
            self.f = types.FunctionType(code, globals(), "f")
        else:
            warnings.warn("UQToolbox.RandomSampling.Experiments: The Experiments has not function code to un-marshal. The function is undefined. Define it using UQToolbox.RandomSampling.Experiments.set_f", RuntimeWarning)
    
    def set_params(self, params):
        self.params = params
    
    def get_params(self):
        return self.params
        
    def get_new_samples(self):
        """
        :returns: the list of samples for which the experiment have not been evaluated yet.
        """
        return self.new_samples
    
    def get_samples(self):
        """
        :returns: the list of samples for which the experiment have been evaluated already.
        """
        return self.samples
    
    def get_results(self):
        """
        :returns: the list of results of the evaluation of ``f`` on the samples.
        """
        return self.results
    
    def store(self):
        if self.store_file != "":
            object_store(self.store_file, self)    
    
    def run (self, maxprocs=None, store_freq=None):
        """ Evaluate the function ``f`` on the samples.
        
        :param int maxprocs: the maximum number of processors available
        :param int store_freq: number of evaluations to be executed before storing. If ``maxprocs`` > 1 then the object is store every ``store_freq*maxprocs`` evaluations.
        """
        if maxprocs != None and not MPI_SUPPORT:
            warnings.warn("UQToolbox.RandomSampling.Experiments.run: MPI is not supported. The jobs will be run without it.", RuntimeWarning)
        
        if maxprocs == None or not MPI_SUPPORT:
            maxprocs = 1
        
        if store_freq == None:
            store_freq = len(self.new_samples)
        
        # Split the samples into chuncks of store_freq*maxprocs size
        chunk_size = store_freq*maxprocs
        ns = [ chunk_size ] * ( len(self.new_samples) // chunk_size )
        ns.append( len(self.new_samples) % chunk_size )
        for i in range(1,len(ns)): ns[i] += ns[i-1]
        ns.insert(0,0)
        slists = [ self.new_samples[ns[i]:ns[i+1]] for i in range(0, len(ns)-1 ) ]

        for slist in slists:
            start_time = time.time()
            if maxprocs == 1:
                for sample in slist:
                    self.results.append( self.f( sample, self.params ) )
            else:
                self.results.extend( mpi_map.mpi_map(self.f, slist, self.params, maxprocs) )
            stop_time = time.time()
            elapsed_time = stop_time-start_time
                        
            for sample in slist:
                self.samples.append(sample)
                self.new_samples.remove(sample)

            if len(slist) > 0:
                est_time = (elapsed_time/len(slist)) * len(self.new_samples)
                self.logger.info(
                    "Completed: %d/%d \t Est. Time: %s" % (
                        len(self.samples),
                        len(self.samples)+len(self.new_samples),
                        datetime.timedelta(seconds=est_time)
                    ))
                self.store()
