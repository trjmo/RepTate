# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module DataTable

Module for the actual object that contains the data, both for experiments and theory. 

""" 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class DataTable(object):
    """Class that stores data and series"""
    MAX_NUM_SERIES=3

    def __init__(self, ax=None):
        """Constructor"""
        self.num_columns=0
        self.num_rows=0
        self.column_names=[]
        self.column_units=[]
        self.data=np.zeros((self.num_rows, self.num_columns))
        self.series=[]
        for i in range(self.MAX_NUM_SERIES): 
            ss = ax.plot([], [], label='')
            self.series.append(ss[0])

    def __str__(self):
        """
        .. todo:: Refine this. It doesn't work
        """
        return self.data