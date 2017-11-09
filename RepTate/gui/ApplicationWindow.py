import sys
import os
import logging
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import seaborn as sns   
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_pdf import PdfPages
import itertools
import Symbols_rc
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtWidgets import QToolBar, QToolButton, QMenu, QFileDialog, QMessageBox, QInputDialog, QLineEdit
#from DataSet import *
from QDataSet import *
from DataFiles import *
from DataSetItem import *
from Application import *
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
Ui_AppWindow, QMainWindow = loadUiType('gui/ApplicationWindow.ui')

class ApplicationWindow(Application, QMainWindow, Ui_AppWindow):
    def __init__(self, name='Application Template', parent=None):
        print("ApplicationWindow.__init__(self) called")
        super(ApplicationWindow, self).__init__(name, parent)
        print("ApplicationWindow.__init__(self) ended")

        if CmdBase.mode!=CmdMode.GUI:
            return
        
        QMainWindow.__init__(self)
        Ui_AppWindow.__init__(self)

        self.setupUi(self)
        self.logger = logging.getLogger('ReptateLogger')
        self.name = name
        self.parent_application = parent
        self.canvas = 0
        self.files = {}
        self.tab_count = 0
        #self.views={} # we use 'views' of Application.py
       
        # Accept Drag and drop events
        self.setAcceptDrops(True)

        # DataSet Tabs behaviour ##########
        self.DataSettabWidget.setTabsClosable(True)
        self.DataSettabWidget.setUsesScrollButtons(True)
        self.DataSettabWidget.setMovable(True)
        
        ################
        # SETUP TOOLBARS
        # Data Inspector Toolbar
        tb = QToolBar()
        tb.setIconSize(QtCore.QSize(24,24))
        tb.addAction(self.actionCopy)
        tb.addAction(self.actionPaste)
        tb.addAction(self.actionShiftVertically)
        tb.addAction(self.actionShiftHorizontally)
        self.LayoutDataInspector.insertWidget(0, tb)
        
        # Dataset Toolbar
        tb = QToolBar()
        tb.setIconSize(QtCore.QSize(24,24))
        tb.addAction(self.actionNew_Empty_Dataset)
        tb.addAction(self.actionNew_Dataset_From_File)
        tb.addAction(self.actionView_All_Sets)
        tbut = QToolButton()
        tbut.setPopupMode(QToolButton.MenuButtonPopup)
        tbut.setDefaultAction(self.actionData_Representation)
        menu=QMenu()
        menu.addAction(self.actionShow_Small_Symbols)
        menu.addAction(self.actionShow_Large_Symbols)
        tbut.setMenu(menu)
        tb.addWidget(tbut)
        #
        tb.addAction(self.actionReload_Data)
        tbut = QToolButton()
        tbut.setPopupMode(QToolButton.MenuButtonPopup)
        tbut.setDefaultAction(self.actionShow_Limits)
        menu=QMenu()
        menu.addAction(self.actionNo_Limits)
        menu.addAction(self.actionVertical_Limits)
        menu.addAction(self.actionHorizontal_Limits)
        menu.addAction(self.actionBoth_Limits)
        tbut.setMenu(menu)
        tb.addWidget(tbut)
        #
        tb.addAction(self.actionInspect_Data)
        tb.addAction(self.actionPrint)
        self.ViewDataTheoryLayout.insertWidget(1, tb)
        self.ViewDataTheorydockWidget.Width=500
        self.ViewDataTheorydockWidget.setTitleBarWidget(QWidget())                

        # Tests TableWidget
        self.tableWidget.setRowCount(30)
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setHorizontalHeaderLabels(['x','y','z','a','b','c','d','e','f','g'])

        # Hide Data Inspector
        self.DataInspectordockWidget.hide()

        # PLOT Style
        # sns.set_style("white")
        # sns.set_style("ticks")
        # #plt.style.use('seaborn-talk')
        # #plt.style.use('seaborn-paper')
        # plt.style.use('seaborn-poster')
        # self.figure=plt.figure()
        # self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        # sns.despine() # Remove up and right side of plot box
        # LEGEND STUFF
        leg=plt.legend(loc='upper left', frameon=True, ncol=2)
        if leg:
            leg.draggable()
                
        # EVENT HANDLING
        #connection_id = self.figure.canvas.mpl_connect('button_press_event', self.onclick)
        connection_id = self.figure.canvas.mpl_connect('resize_event', self.resizeplot)
        #connection_id = self.figure.canvas.mpl_connect('motion_notify_event', self.on_plot_hover)   
        connection_id = self.actionPrint.triggered.connect(self.printPlot)
        connection_id = self.actionInspect_Data.triggered.connect(self.showDataInspector)
        connection_id = self.actionNew_Empty_Dataset.triggered.connect(self.createNew_Empty_Dataset)
        connection_id = self.actionNew_Dataset_From_File.triggered.connect(self.openDataset)
       # connection_id = self.actionNew_Dataset_From_File.triggered.connect(self.createNew_Dataset_From_File)
        connection_id = self.actionReload_Data.triggered.connect(self.DEBUG_populate_current_Dataset_with_random_data)

        connection_id = self.actionShow_Small_Symbols.triggered.connect(self.Small_Symbols)
        connection_id = self.actionShow_Large_Symbols.triggered.connect(self.Large_Symbols)

        connection_id = self.actionNo_Limits.triggered.connect(self.No_Limits)
        connection_id = self.actionVertical_Limits.triggered.connect(self.Vertical_Limits)
        connection_id = self.actionHorizontal_Limits.triggered.connect(self.Horizontal_Limits)
        connection_id = self.actionBoth_Limits.triggered.connect(self.Both_Limits)
            
        connection_id = self.viewComboBox.currentIndexChanged.connect(self.Change_View)

        connection_id = self.DataSettabWidget.tabCloseRequested.connect(self.close_tab_handler)
        connection_id = self.DataSettabWidget.tabBarDoubleClicked.connect(self.mouse_Double_Click_Event)

        # TEST GET CLICKABLE OBJECTS ON THE X AXIS
        #xaxis = self.ax.get_xticklabels()
        #print (xaxis)
    
    def mouse_Double_Click_Event(self, index):
        print("double click")
        old_name = self.DataSettabWidget.currentWidget().name
        new_tab_name, success = QInputDialog.getText (
                self, "Change Name",
                "Insert New Tab Name",
                QLineEdit.Normal,
                old_name)
        if (success and new_tab_name!=""):
            self.DataSettabWidget.setTabText(index, new_tab_name)
            self.DataSettabWidget.currentWidget().name = new_tab_name
            self.datasets[new_tab_name] = self.datasets[old_name]
            self.datasets.pop(old_name)

    
    def close_tab_handler(self, index):
        print("tab %s is closing"%index)
        self.ax.cla()
        self.DataSettabWidget.removeTab(index)
        
    def Change_View(self):
        current_dataset = self.DataSettabWidget.currentWidget()
        if (current_dataset==None):
            return
        
        #clear plot window before replotting in new view
        self.ax.cla()
        
        # what does that do? Nothing it seems.
        nitems = current_dataset.DataSettreeWidget.topLevelItemCount()
        for i in range(nitems):
            item = current_dataset.DataSettreeWidget.topLevelItem(i)
        ####

        view = self.views[self.viewComboBox.currentText()] 
        # for dt in self.files.values():
        #     x, y, success = view.view_proc(dt.data_table, dt.file_parameters)
        #     current_dataset.series = self.ax.scatter(x, y, label=dt.file_name_short)
        #     self.canvas.draw()

    def populateViews(self):
        for i in self.views:
            #add keys of 'views' dict to the list of views avaliable 
            self.viewComboBox.addItem(i) 

    def dragEnterEvent(self, e):      
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore() 

    def dropEvent(self, e):
        reptatelogger = logging.getLogger('ReptateLogger')
        paths_to_open = []
        for url in e.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isfile(path):
                paths_to_open.append(path)

        if (self.DataSettabWidget.count()==0):
            self.createNew_Empty_Dataset()
        ds_name = self.DataSettabWidget.currentWidget().name
        ds = self.datasets[ds_name]
        print("paths_to_open: ", paths_to_open)
        success, newtabs, ext = ds.do_open(paths_to_open)
        print("Success: ", success, success==True)
        if success==True:
            for df in newtabs:
                self.addTableToCurrentDataSet(df, ext)
        else:
            QMessageBox.about(self, "Open", success)

    def addTableToCurrentDataSet(self, dt, ext):
        ds = self.DataSettabWidget.currentWidget()
        lnew = []
        for param in self.filetypes[ext].basic_file_parameters[:]:
            try:
                lnew.append(str(dt.file_parameters[param]))
            except KeyError as e:
                message = "Parameter %s not found in file\n '%s'.\nValue set to 0"%(e, dt.file_name_short)
                QMessageBox.warning(self, 'Header', message)
                lnew.append(str(0))

        lnew.insert(0, dt.file_name_short)
        newitem = DataSetItem(ds.DataSettreeWidget, lnew, )
        newitem.setCheckState(0, 2)
        
        #root.setIcon(0, QIcon(':/Icons/Images/symbols/'+pname+str(i+1)+'.ico'))
        ds.do_plot()
        # view = self.current_view
        # x, y, success = view.view_proc(dt.data_table, dt.file_parameters)
        # newitem.series=self.ax.scatter(x, y, label=dt.file_name_short)
        self.canvas.draw()


    def No_Limits(self):
        self.actionShow_Limits.setIcon(self.actionNo_Limits.icon())

    def Vertical_Limits(self):
        self.actionShow_Limits.setIcon(self.actionVertical_Limits.icon())

    def Horizontal_Limits(self):
        self.actionShow_Limits.setIcon(self.actionHorizontal_Limits.icon())

    def Both_Limits(self):
        self.actionShow_Limits.setIcon(self.actionBoth_Limits.icon())
        
    def Small_Symbols(self):
        self.actionData_Representation.setIcon(self.actionShow_Small_Symbols.icon())
    
    def Large_Symbols(self):
        self.actionData_Representation.setIcon(self.actionShow_Large_Symbols.icon())
    
    def DEBUG_populate_current_Dataset_with_random_data(self):
        # Plot some random walks
        num_lines=10
        num_points=200
        #palette = itertools.cycle(sns.color_palette("Set1",n_colors=num_lines, desat=.5)) 
        #palette = itertools.cycle(sns.color_palette("Blues_d",n_colors=num_lines)) 
        pname="default" # nipy_spectral gist_ncar gist_rainbow Dark2 cool, afmhot, hsl, husl, deep, muted, bright, pastel, dark, colorblind, viridis
        #palette = itertools.cycle(sns.color_palette(pname,num_lines)) 
        palette=itertools.cycle(((0,0,0),(1.0,0,0),(0,1.0,0),(0,0,1.0),(1.0,1.0,0),(1.0,0,1.0),(0,1.0,1.0),(0.5,0,0),(0,0.5,0),(0,0,0.5),(0.5,0.5,0),(0.5,0,0.5),(0,0.5,0.5),(0.25,0,0),(0,0.25,0),(0,0,0.25),(0.25,0.25,0),(0.25,0,0.25),(0,0.25,0.25)))
        markerlst = itertools.cycle(('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd')) 
        linelst = itertools.cycle((':', '-', '-.', '--'))

        # Add New tab to DataSettabWidget
        if (self.DataSettabWidget.count()==0): return
        ds=self.DataSettabWidget.currentWidget()
        
        nold = ds.DataSettreeWidget.topLevelItemCount()
        for i in range(nold):
            marker=next(markerlst)
            edgecolors=next(palette)

        for i in range(num_lines):
            root = DataSetItem(ds.DataSettreeWidget, ['Line %02d'%(i+nold), "%g"%np.sin(i), "%g"%(1-1/(i+1))])
            root.setCheckState(0, 2)
            root.setIcon(0, QIcon(':/Icons/Images/symbols/'+pname+str(i+1)+'.ico'))
            
            x=np.arange(num_points)
            y=np.cumsum(np.random.randn(num_points))
            
            # DIFFERENT STYLES
            # JUST LINES
            #self.ax.plot(y, color=next(palette), label='Line %d'%i)
            # LINES with DIFFERENT STYLES, BLACK
            #self.ax.plot(y, linestyle=next(linelst), color='black', label='Line %d'%i)
            # LINES with DIFFERENT STYLES, DIFFERENT COLORS
            #self.ax.plot(y, linestyle=next(linelst), color=next(palette), label='Line %d'%i)
            # LINES WITH FILLED SYMBOLS
            #self.ax.plot(y, color=next(palette), marker=next(markerlst), label='Line %d'%i)
            # LINES WITH FILLED SYMBOLS WITH BLACK BORDERS
            #c=next(palette)
            #self.ax.plot(y, color=c, marker=next(markerlst), ms=12, markerfacecolor=c, markeredgewidth=1, markeredgecolor='black', label='Line %d'%i)
            # EMPTY SYMBOLS 
           
            #root.series=self.ax.scatter(x, y, marker=next(markerlst), s=120, facecolors='none', edgecolors=next(palette), linewidths=1, label='Line %02d'%(i+nold))

            
            # EMPTY BLACK AND WHITE SYMBOLS 
            #self.ax.scatter(x, y, marker=next(markerlst), s=120, facecolors='none', edgecolors='black', label='Line %d'%i)
            # FILLED SYMBOLS with Black borders
            #self.ax.scatter(x, y, marker=next(markerlst), s=120, facecolors=next(palette), edgecolors='black', label='Line %d'%i)
            #root = QTreeWidgetItem(ds.DataSettreeWidget, ['Line %d'%i, "%g"%np.sin(i), "%g"%(1-1/(i+1))])

           
                        
        # LEGEND STUFF
        leg=plt.legend(loc='upper left', frameon=True, ncol=2)
        if leg:
            leg.draggable()
            
        # LIMITS AND AXIS LABELS
        # TODO: Need to define a Units module to handle this!!!
        self.ax.set_xlim(0, num_points)
        self.ax.set_xlabel("t (s)")
        self.ax.set_ylabel("r (m)")
    
        plt.tight_layout(pad=1.2)
        self.canvas.draw()
        
    def createNew_Empty_Dataset(self):
        # Add New empty tab to DataSettabWidget
        ind = self.tab_count + 1
        self.tab_count += 1
        ds_name = 'DataSet' + '%d'%ind
        ds = QDataSet(name=ds_name, parent=self)
        self.datasets[ds_name] = ds
        self.DataSettabWidget.addTab(ds, ds_name) 
        #Set the new tab the active tab
        self.DataSettabWidget.setCurrentIndex(ind - 1)
       
        dfile=list(self.filetypes.values())[0] 
        dataset_header=dfile.basic_file_parameters[:]
        dataset_header.insert(0, "File")
        ds.DataSettreeWidget.setHeaderItem(QTreeWidgetItem(dataset_header))   
        hd=ds.DataSettreeWidget.header()
        w=ds.DataSettreeWidget.width()
        w/=hd.count()
        for i in range(hd.count()):
            hd.resizeSection(i, w)
            #hd.setTextAlignment(i, Qt.AlignHCenter)
    
    
    #################################
    # VB: browse and select file to open
    def openDataset(self):
        self.logger.debug("in openDataset")
        if (self.DataSettabWidget.count()==0):
            self.createNew_Empty_Dataset()
        ds_name = self.DataSettabWidget.currentWidget().name
        ds = self.datasets[ds_name]

        if self.filetypes!={}:
            # should be of form, e.g., "LVE (*.tts *.osc);;Text file (*.txt)"
            allowed_ext = self.name.rstrip("0123456789") + " ("        
            for ext in self.filetypes:
                allowed_ext = allowed_ext + "*.%s "%ext
            allowed_ext = allowed_ext + ")"
        paths_to_open = self.openFileNamesDialog(allowed_ext)
        if not paths_to_open:
            return
        
        self.logger.debug(paths_to_open)
        success, newtabs, ext = ds.do_open(paths_to_open)
        if success:
            for df in newtabs:
                self.addTableToCurrentDataSet(df, ext)
        else:
            QMessageBox.about(self, "Open", success)

        # for path in paths_to_open:
        #     split_file = path.split('.')
        #     file_ext = split_file[len(split_file)-1]
        #     if not file_ext in self.filetypes:
        #         QMessageBox.warning(self, 'Open Data File', 'Incorect File Extension\nExpected: %s'%(" or ".join(self.filetypes.keys())))
        #         return


                # if (self.DataSettabWidget.count()==0):
                #     self.createNew_Empty_Dataset()
                # ds_name = self.DataSettabWidget.TabText()
                # ds = self.datasets[ds_name]
                # ft = self.filetypes[file_ext]
                # ds.open_files(path, ft)
                # dt = .read_file(path, self, self.ax)
                # # self.files[dt.file_name_short] = dt
                # self.current_file = dt
                # self.addTableToCurrentDataSet(dt)
                # # file_ext='gt'
                # # dt = self.files[file_ext].read_file(f)
                # # self.logger.debug("set dt = ...")
                # # self.addTableToCurrentDataSet(dt)
            # else:
            #     #QMessageBox.about(self, "Title", "Message")
   
    def openFileNamesDialog(self, ext_filter="All Files (*)"):  
        # file browser window  
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_start = "data/"
        dilogue_name = "Open"
        selected_files, _ = QFileDialog.getOpenFileNames(self, dilogue_name, dir_start, ext_filter, options=options)
        return selected_files
    # def warningMessageBox(self, message):
    #     msg = QMessageBox.warning(self, "bal", "bil")
    #     self.logger.debug("ouiuoiu")
    #     #msg.setText(message)
    #     #msg.exec_()



    #####################################   
            
            

    # def createNew_Dataset_From_File(self):
    #     # Add New empty tab to DataSettabWidget
    #     ind=self.DataSettabWidget.count()+1
    #     ds = DataSet()
    #     self.DataSettabWidget.addTab(ds, 'DataSet'+'%d'%ind)
    #     #Set the new tab the active tab
    #     self.DataSettabWidget.setCurrentIndex(ind-1)
        
    #     dfile=list(self.files.values())[0] 
    #     dataset_header=dfile.basic_file_parameters[:]
    #     dataset_header.insert(0, "File")
    #     ds.DataSettreeWidget.setHeaderItem(QTreeWidgetItem(dataset_header))   
    #     hd=ds.DataSettreeWidget.header()
    #     w=ds.DataSettreeWidget.width()
    #     w/=hd.count()
    #     for i in range(hd.count()):
    #         hd.resizeSection(i, w)
    #         #hd.setTextAlignment(i, Qt.AlignHCenter)

    def showDataInspector(self):
        if self.DataInspectordockWidget.isHidden():
            self.DataInspectordockWidget.show()
        else:
            self.DataInspectordockWidget.hide()
        
    def printPlot(self):
        fileName = QFileDialog.getSaveFileName(self,
            "Export plot", "", "Image (*.png);;PDF (*.pdf);; Postscript (*.ps);; EPS (*.eps);; Vector graphics (*.svg)");
        # TODO: Set DPI, FILETYPE, etc
        plt.savefig(fileName[0])
        
    def on_plot_hover(self, event):
        pass
        
    def onclick(self, event):
        if event.dblclick:
            pickedtick = event.artist
            print(event)
            print(pickedtick)

    def resizeplot(self, event):
        # TIGHT LAYOUT in order to view axes and everything
        plt.tight_layout(pad=1.2)
