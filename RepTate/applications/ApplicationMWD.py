# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module ApplicationMWD

Module for handling Molecular weight distributions from GPC experiments.

""" 
from Application import *
from QApplicationWindow import *
import numpy as np
from TheoryDiscrMWD import TheoryDiscrMWD
#from TheoryMaxwellModes import TheoryMaxwellModesTime


class ApplicationMWD(CmdBase):
    """
    Application to analyze Molecular Weight distributions
    
    .. todo:: IS IT NECESSARY TO KEEP TWO SEPARATE APPLICATIONS FOR REACT AND FOR MWD???
    """
    name="MWD"
    description="Experimental Molecular weight distributions"
    def __new__(cls, name="LVE", parent = None):
        return GUIApplicationMWD(name, parent) if (CmdBase.mode==CmdMode.GUI) else CLApplicationMWD(name, parent)

class BaseApplicationMWD:    
    def __init__(self, name="MWD", parent = None):
        super().__init__(name, parent)

        # VIEWS
        self.views["W(M)"]=View("W(M)", "Molecular weight distribution", "M", "W(M)", "g/mol", "-", True, False, self.viewWM, 1, ["W(M)"])
        self.current_view=self.views["W(M)"]

        # FILES
        ftype=TXTColumnFile("React Files", "reac", "Relaxation modulus", ['M','W(logM)', 'g', 'br/1000C'], ['Mn','Mw','PDI'], ["g/mol", '-'])
        self.filetypes[ftype.extension]=ftype
        ftype=TXTColumnFile("GPC Files", "gpc", "Molecular Weight Distribution", ['M','W(logM)'], ['Mn','Mw','PDI'], ["g/mol", '-'])
        #ftype=TXTColumnFile("GPC Files", "gpc", "Molecular Weight Distribution", ['M','W(logM)'], [], ['kDa', '-'])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        self.theories[TheoryDiscrMWD.thname] = TheoryDiscrMWD
        #self.theories[TheoryMaxwellModesTime.thname]=TheoryMaxwellModesTime

    def viewWM(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        max_y = np.max(dt.data[:, 1])
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]/max_y
        return x, y, True

class CLApplicationMWD(BaseApplicationMWD, Application):    
    def __init__(self, name="MWD", parent = None):
        super().__init__(name, parent)

class GUIApplicationMWD(BaseApplicationMWD, QApplicationWindow):    
    def __init__(self, name="MWD", parent = None):
        super().__init__(name, parent)
        self.populate_views() #populate the view ComboBox
