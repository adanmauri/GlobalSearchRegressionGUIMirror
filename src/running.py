from PyQt5.QtWidgets import QApplication, QWidget
import sys
import os
import time

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtCore, QtWidgets
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QInputDialog, QLineEdit, QFileDialog

from core import AbstractPage, Color

class Running(AbstractPage):
    TITLE = "Running GSReg"
    STEP = 4
    completed = False

    def  __init__(self, parent=None, manager=None, wizard=None):
        super(Running, self).__init__(parent, manager, wizard)
        self.setCommitPage(True)
        self.completed = False
        self.setProgressBar()

    def initializePage(self):
        self.cleanMainLayout()
        self.runGSReg()

    def runGSReg(self, selected=False):
        self.showLoading()

        script = 'using CSV'+'\n'
        script+= 'using GSReg'+'\n'
        script+= 'data = CSV.read("'+self.manager.input_filename+'")'+'\n'
        script+= 'GSReg.gsreg("'+self.manager.depvar+' '+' '.join(self.manager.expvars)+'"'
        script+= ', data'
        script+= ', intercept='+'true' if self.manager.intercept else 'false'
        if self.manager.outsample > 0:
            script+= ', outsample='+str(self.manager.outsample)
        script+= ', samesample='+'true' if self.manager.samesample else 'false'
        script+= ', criteria=[:'+', :'.join(self.manager.criteria)+']'
        #script+= ', csv=''+self.output_file+'''
        script+= ', csv="'+self.manager.working_directory+self.manager.output_filename+'"'
        script+= ', ttest=true'
        script+= ')'
               
        file = open(self.manager.root_path+self.manager.GSREG_SCRIPT_FILE, 'w') 
        file.write(script)
        file.close()
        
        bash = '#!/bin/bash'+'\n'
        bash+= 'JULIA_NUM_THREADS='+str(self.manager.threads)+' '+self.manager.julia_binary+' '+self.manager.GSREG_SCRIPT_FILE

        file = open(self.manager.root_path+self.manager.GSREG_BASH_FILE, 'w') 
        file.write(bash)
        file.close()

        self.process = QtCore.QProcess()
        self.process.finished.connect(self.done)
        self.process.start('bash', [self.manager.root_path+self.manager.GSREG_BASH_FILE])

    def done(self):
        os.remove(self.manager.root_path+self.manager.GSREG_BASH_FILE)
        os.remove(self.manager.root_path+self.manager.GSREG_SCRIPT_FILE)
        self.cleanMainLayout()
        self.setTitle(step=5, title='Done!')
        self.completed = True
        self.completeChanged.emit()

        self.description_layout = QtWidgets.QVBoxLayout()
        self.description_text = QtWidgets.QLabel()
        self.description_text.setStyleSheet("color: #34495e; font-size: 18px;")
        self.description_text.setText("A CSV file with all-subsets results has been saved at: "+self.manager.working_directory+self.manager.output_filename)
        self.description_text.setWordWrap(True)
        self.description_text.setFixedWidth(680)
        self.description_text.setFixedHeight(45)
        self.description_layout.addWidget(self.description_text)
        self.main_layout.addLayout(self.description_layout)

    def isComplete(self):
        return self.completed
