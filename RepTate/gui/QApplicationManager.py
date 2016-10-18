import os
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication

from ApplicationManager import *
from QAboutReptate import *

path = os.path.dirname(os.path.abspath(__file__))
Ui_MainWindow, QMainWindow = loadUiType(os.path.join(path,'ReptateMainWindow.ui'))

class QApplicationManager(QMainWindow, Ui_MainWindow, ApplicationManager):
    """ Main Reptate window and application manager"""    
    
    def __init__(self, parent=None):
        super(QApplicationManager, self).__init__(parent)
        self.setupUi(self)

        # Hide console and project navigation
        self.ConsoledockWidget.hide()
        self.ProjectdockWidget.hide()

        # Connect actions
        # Generate action buttons from dict of available applications
        #self.actionTest.triggered.connect(self.new_test_window)
        #self.actionReact.triggered.connect(self.new_react_window)
        #self.actionMWD.triggered.connect(self.new_mwd_window)
        #self.actionTTS.triggered.connect(self.new_tts_window)
        #self.actionLVE.triggered.connect(self.new_lve_window)
        #self.actionNLVE.triggered.connect(self.new_nlve_window)
        #self.actionGt.triggered.connect(self.new_gt_window)
        #self.actionCreep.triggered.connect(self.new_creep_window)
        #self.actionSANS.triggered.connect(self.new_sans_window)
        self.actionProject.triggered.connect(self.switch_project_view_hide)
        self.actionConsole.triggered.connect(self.switch_console_view_hide)
        self.ApplicationtabWidget.tabCloseRequested.connect(self.close_tab)        
        self.ApplicationtabWidget.currentChanged.connect(self.tab_changed)
        #self.Projecttree.itemSelectionChanged.connect(self.treeChanged)
        
        self.actionAbout_Qt.triggered.connect(QApplication.aboutQt)
        self.actionAbout.triggered.connect(self.show_about)
        
        # CONSOLE WINDOW (need to integrate it with cmd commands)
        #self.text_edit = Console(self)
        #this is how you pass in locals to the interpreter
        #self.text_edit.initInterpreter(locals()) 
        #self.verticalLayout.addWidget(self.text_edit)

    def show_about(self):
        """ Show about window"""
        dlg = AboutWindow(self)
        dlg.show()        

    def switch_project_view_hide(self):
        """View or hide the project navigation window """
        if (self.ProjectdockWidget.isHidden()):
            self.ProjectdockWidget.show()
        else:
            self.ProjectdockWidget.hide()

    def switch_console_view_hide(self):
       """Show or hide the console window"""
       if (self.ConsoledockWidget.isHidden()):
            self.ConsoledockWidget.show()
            #self.text_edit.setFocus()
       else:
            self.ConsoledockWidget.hide()

    def tab_changed(self, index):
        """Capture when the active application has changed"""
        #appname = self.ApplicationtabWidget.widget(index).windowTitle
        #items = self.Projecttree.findItems(appname, Qt.MatchContains)
        #self.Projecttree.setCurrentItem(items[0])
        pass

    def tree_changed(self):
        """Capture when the active application has changed in the application navigator"""
        #print("HELLO")
        #appname = self.Projecttree.currentItem.text(0)
        #print(index, appname)
        pass

    def close_tab(self, index):
        #appname = self.ApplicationtabWidget.widget(index).windowTitle
        #print(appname)
        #print(self.appdict[appname])
        #self.Projecttree.removeItemWidget(self.appdict[appname],0)
        
        self.ApplicationtabWidget.removeTab(index)