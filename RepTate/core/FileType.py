import numpy as np
import logging
#from Table import *
from File import *
from DataTable import *

class TXTColumnFile(object):
	
    """Basic class for text-column based data files
    
    Columns should be separated by espaces or tabs
    BASIC Structure of FILE:
    LINE    CONTENTS
    0       Param1=434;Param2=4355;
    1       # Header line and/or comments [OPTIONAL, ANY NUMBER OF HEADER LINES IS POSSIBLE]
    2       col1 col2 col3 [NAMES OF COLUMNS, OPTIONAL]
    3       4343 434.5 535e-434 [DATA, ONLY NUMBERS ALLOWED]

    The following examples can be declared with the line:
    ftype=TXTColumnFile("LVE files", "tts", "LVE files", ['w','G\'','G\'\''], ['Mw','T'], ['rad/s','Pa','Pa'])
    
    EXAMPLE 1: columns line, no header lines
    C1=8.77210163229153;C2=114.03;Rho0=0.928;C3=0.61;T=-35;CTg=14.65;dx12=0;isof=true;Mw=634.5;chem=PI;PDI=1.03;
    w                           G'                          G''                        T                            g
    4.29882628773180E-0008      1.44001856995549E+0002      3.70207627600662E+0003     -3.30000000000000E-0003      0.00000000000000E+0000     
    6.30767835406968E-0008      2.56947504513849E+0002      5.39032089470917E+0003      3.14760000000000E-0004      0.00000000000000E+0000     
    9.25946098215800E-0008      4.87031807130633E+0002      7.86538338583378E+0003     -1.01000000000000E-0002      0.00000000000000E+0000     

    EXAMPLE 2: Neither columns line nor header lines
    C1=8.77210163229153;C2=114.03;Rho0=0.928;C3=0.61;T=-35;CTg=14.65;dx12=0;isof=true;Mw=23.4;chem=PI;PDI=1.03;
    2.42782390212358E-0003      2.11182193155015E+0001      1.72559181398615E+0003      1.25000000000000E-0003      0.00000000000000E+0000     
    3.56351666244471E-0003      4.30476548641552E+0001      2.53490824331357E+0003      1.48400000000000E-0002      0.00000000000000E+0000     

    EXAMPLE 3: 2 Header lines, no column line 
    T=160;chem=PE;
    # Header 1
    # Header 2
    4.23333e-05 1.05E+00 2.96E+01
    6.7e-05 2.02E+00 3.97E+01 
    
    EXAMPLE 4: 2 Header lines + column line
    T=160;chem=PE;
    # Header 1
    # Header 2
    w G' G''
    4.23333e-05 1.05E+00 2.96E+01
    6.7e-05 2.02E+00 3.97E+01 
    """    
    def __init__(self, name='TXTColumn', extension='txt', 
                 description='Generic text file with columns', 
                 col_names=[], basic_file_parameters=[], col_units=[]):
        """Constructor
           col_names: list with names of columns to read
           basic_file_parameters: list with file parameters that should always be included in the header line
           col_units: TO DO
        """
        self.name=name
        self.extension=extension
        self.description=description
        self.col_names_line=0
        self.first_data_line = 0
        self.col_names=col_names
        self.col_index=list(range(len(self.col_names)))
        self.basic_file_parameters=basic_file_parameters # Those that will show by default in the dataset
        self.col_units=col_units
        self.logger = logging.getLogger('ReptateLogger')

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
        
    def get_parameters(self, line, file):
        items=line.split(';')
        file.file_parameters={}
        for i in range(len(items)):
            par=items[i].split('=')
            if len(par)>1:
                if (self.is_number(par[1])):
                    file.file_parameters[par[0]]=float(par[1])
                else:
                    file.file_parameters[par[0]]=par[1]
                
    def find_col_names_and_first_data_lines(self, lines, file):
        colnameline=0
        firstdata=0
        for i in range(1,len(lines)):
            if all(x in lines[i] for x in self.col_names):
                # Column names line found
                colnameline=i
            elif all(self.is_number(x) for x in lines[i].split()):
                # Data lines have been found 
                firstdata=i
                break
            else:
                # Otherwise, this must be a header line
                file.header_lines.append(lines[i])
        return colnameline, firstdata   
                
    def read_file(self, filename, parent_dataset, ax):
        file=File(filename, self, parent_dataset, ax)
        f = open(filename, "r")
        lines=f.readlines()
        
        self.get_parameters(lines[0], file)
        self.col_names_line, self.first_data_line = self.find_col_names_and_first_data_lines(lines, file)
    
        self.col_index=[]
        if (self.col_names_line>0):
            items=lines[self.col_names_line].split()
            for col in self.col_names:
                for j in range(len(items)):
                    if (col==items[j]):
                        self.col_index.append(int(j))
                        break
        else:
            self.col_index=list(range(len(self.col_names)))

        file.data_table.num_columns=len(self.col_index)
        rawdata=[]
        for i in range(self.first_data_line, len(lines)):
            items=lines[i].split()
            for j in self.col_index:
                rawdata.append(float(items[j]))
        file.data_table.num_rows=int(len(rawdata)/file.data_table.num_columns)
        file.data_table.data = np.reshape(rawdata,newshape=(file.data_table.num_rows, file.data_table.num_columns))        

        return file

    
