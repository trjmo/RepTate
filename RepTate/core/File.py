# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module File

Module that defines a basic File, with headers, columns and data.

""" 
import os
from FileType import *
from DataTable import *

class File(object):
    """Basic class that describes elements of a DataSet"""

    def __init__(self, file_name="", file_type=None, parent_dataset=None, ax=None):
        """ Constructor:
            file_name: Full path
            file_name_short: Just the file name
            header_lines: 
        """
        self.file_full_path = os.path.abspath(file_name)
        tmpname = self.file_full_path.split(os.sep)
        tmpname = tmpname[len(tmpname)-1]
        lst = tmpname.split('.')
        short = '.'.join(lst[:-1])      
        self.file_name_short = short
        self.file_type = file_type
        self.parent_dataset = parent_dataset
        self.ax = ax

        #plot attributes
        self.marker = None
        self.color = None
        self.filled = None
        self.size = None

        self.header_lines=[]
        self.file_parameters={}
        self.active = True
        self.data_table = DataTable(ax)
        
    def __str__(self):
        return '%s: %s' % (self.file_full_path, self.file_parameters)