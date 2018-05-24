from PyQt5.QtWidgets import QApplication, QWidget
import sys
import os
import time
import csv

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
        script+= 'data = CSV.read("'+self.manager.working_directory+self.manager.input_filename+'")'+'\n'
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
        self.hideLoading()
        os.remove(self.manager.root_path+self.manager.GSREG_BASH_FILE)
        os.remove(self.manager.root_path+self.manager.GSREG_SCRIPT_FILE)
        self.STEP = 5

        self.cleanMainLayout()
        self.setTitle(step=5, title='Done!')
        self.setProgressBar()

        self.completed = True
        self.completeChanged.emit()

        with open(self.manager.working_directory+self.manager.output_filename) as csvfile:
            reader = csv.DictReader(csvfile)
            self.fieldnames = reader.fieldnames   
            for row in reader:   
                self.best_model = row
                break
            csvfile.close()
        
        self.results_layout = QtWidgets.QVBoxLayout()
        self.set_result_title(self.results_layout)
        self.set_dependent_variable(self.results_layout)
        self.set_headers(self.results_layout)
        self.set_line(self.results_layout)
        self.set_main_output(self.results_layout)
        self.set_line(self.results_layout)
        self.set_mod_stats(self.results_layout)
        self.set_line(self.results_layout)

        self.main_layout.addLayout(self.results_layout)

        self.description_layout = QtWidgets.QVBoxLayout()
        self.description_layout.setAlignment(Qt.AlignTop)
        self.description_text = QtWidgets.QTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.description_text.setStyleSheet("font-size: 18px; margin-right: 15px; margin-top: 10px;")
        self.description_text.setText("A CSV file with all-subsets results has been saved at: "+self.manager.working_directory+self.manager.output_filename)
        self.description_text.setFixedWidth(680)

        self.description_layout.addWidget(self.description_text)

        self.results_layout.addLayout(self.description_layout)


    def set_result_title(self, results_layout):
        title_layout = QtWidgets.QVBoxLayout()
        title_layout.setAlignment(Qt.AlignVCenter)
        titlew_layout = QtWidgets.QHBoxLayout()
        titlew_layout.addLayout(title_layout)
        title_text = QtWidgets.QLabel()
        title_text.setFixedWidth(680)
        title_text.setStyleSheet("margin-top: 20px; color: #34495e; font-size: 18px; border-top: 2px solid #34495e; border-bottom: 2px solid #34495e;")
        title_text.setText("Best model results")
        title_text.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_text)
        results_layout.addLayout(titlew_layout)
    
    def set_dependent_variable(self, results_layout):
        none_layout = QtWidgets.QVBoxLayout()
        dp_layout = QtWidgets.QVBoxLayout()
        wapper_layout = QtWidgets.QHBoxLayout()
        wapper_layout.addLayout(none_layout)
        wapper_layout.addLayout(dp_layout)

        none_text = QtWidgets.QLabel()
        none_text.setFixedWidth(340)
        none_text.setStyleSheet("margin-top: 20px; font-size: 14px;")
        none_text.setText("")
        none_layout.addWidget(none_text)

        dp_text = QtWidgets.QLabel()
        dp_text.setStyleSheet("margin-top: 20px; border-bottom: 1px solid #34495e;")
        dp_text.setText("Dependent variable: "+self.manager.depvar)
        dp_text.setAlignment(Qt.AlignLeft)
        dp_layout.addWidget(dp_text)
        results_layout.addLayout(wapper_layout)
    
    def set_headers(self, results_layout):
        cov_layout = QtWidgets.QVBoxLayout()
        coef_layout = QtWidgets.QVBoxLayout()
        std_layout = QtWidgets.QVBoxLayout()
        ttest_layout = QtWidgets.QVBoxLayout()

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addLayout(cov_layout)
        header_layout.addLayout(coef_layout)
        header_layout.addLayout(std_layout)
        header_layout.addLayout(ttest_layout)

        cov_text = QtWidgets.QLabel()
        cov_text.setFixedWidth(330)
        cov_text.setStyleSheet("margin-top: 10px; ")
        cov_text.setText("Selected covariates")
        cov_layout.addWidget(cov_text)

        coef_text = QtWidgets.QLabel()
        coef_text.setFixedWidth(105)
        coef_text.setStyleSheet("margin-top: 10px;")
        coef_text.setText("Coef.")
        coef_layout.addWidget(coef_text)

        std_text = QtWidgets.QLabel()
        std_text.setFixedWidth(105)
        std_text.setStyleSheet("margin-top: 10px;")
        std_text.setText("Std.")
        std_layout.addWidget(std_text)

        ttest_text = QtWidgets.QLabel()
        ttest_text.setFixedWidth(105)
        ttest_text.setStyleSheet("margin-top: 10px;")
        ttest_text.setText("t-test")
        ttest_layout.addWidget(ttest_text)

        results_layout.addLayout(header_layout)
    
    def set_line(self, results_layout):
        cov_layout = QtWidgets.QVBoxLayout()
        coef_layout = QtWidgets.QVBoxLayout()
        std_layout = QtWidgets.QVBoxLayout()
        ttest_layout = QtWidgets.QVBoxLayout()

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addLayout(cov_layout)
        header_layout.addLayout(coef_layout)
        header_layout.addLayout(std_layout)
        header_layout.addLayout(ttest_layout)

        line_widget = QtWidgets.QLabel()
        line_widget.setStyleSheet("border-top: 1px solid #34495e;")
        line_widget.setFixedWidth(680)
        line_widget.setFixedHeight(2)

        line_widget.setText("")
        cov_layout.addWidget(line_widget)

        results_layout.addLayout(header_layout)

    def set_main_output(self, results_layout):
        expvars = self.manager.expvars
        if '_cons_b' in self.best_model and len(self.best_model["_cons_b"]) > 0:
            expvars.append('_cons')

        for expvar in self.manager.expvars:
            if expvar+'_b' in self.best_model and len(self.best_model[expvar+"_b"]) > 0:
                cov_layout = QtWidgets.QVBoxLayout()
                coef_layout = QtWidgets.QVBoxLayout()
                std_layout = QtWidgets.QVBoxLayout()
                ttest_layout = QtWidgets.QVBoxLayout()

                header_layout = QtWidgets.QHBoxLayout()
                header_layout.addLayout(cov_layout)
                header_layout.addLayout(coef_layout)
                header_layout.addLayout(std_layout)
                header_layout.addLayout(ttest_layout)

                cov_text = QtWidgets.QLineEdit()
                cov_text.setFrame(False)
                cov_text.setReadOnly(True)
                cov_text.setFixedWidth(330)
                cov_text.setStyleSheet("padding-left: 5px;")
                cov_text.setText(expvar)
                cov_layout.addWidget(cov_text)

                coef_text = QtWidgets.QLineEdit()
                coef_text.setFrame(False)
                coef_text.setReadOnly(True)
                coef_text.setFixedWidth(105)
                coef_text.setStyleSheet("")
                coef_text.setText(str(round(float(self.best_model[expvar+"_b"]), 6)))
                coef_layout.addWidget(coef_text)

                std_text = QtWidgets.QLineEdit()
                std_text.setFrame(False)
                std_text.setReadOnly(True)
                std_text.setFixedWidth(105)
                std_text.setStyleSheet("")
                std_text.setText(str(round(float(self.best_model[expvar+"_b"])/float(self.best_model[expvar+"_t"]), 6)))
                std_layout.addWidget(std_text)

                ttest_text = QtWidgets.QLineEdit()
                ttest_text.setFrame(False)
                ttest_text.setReadOnly(True)
                ttest_text.setFixedWidth(105)
                ttest_text.setStyleSheet("")
                ttest_text.setText(str(round(float(self.best_model[expvar+"_t"]), 6)))
                ttest_layout.addWidget(ttest_text)

                results_layout.addLayout(header_layout)

    def set_mod_stats(self, results_layout):
        self.set_mod_stat(results_layout, 'Observations', str(self.manager.observations_number))
        self.set_mod_stat(results_layout, 'Adjusted R2', str(round(float(self.best_model['r2adj']), 6)))
        self.set_mod_stat(results_layout, 'F-statistic', str(round(float(self.best_model['F']), 6)))

        for criteria in self.manager.criteria:
            if criteria in self.best_model and len(self.best_model[criteria]) > 0 and criteria != "r2adj":
                self.set_mod_stat(results_layout, self.manager.criteria_title(criteria), str(round(float(self.best_model[criteria]), 6)))

                
    def set_mod_stat(self, results_layout, name, value):
        name_layout = QtWidgets.QVBoxLayout()
        value_layout = QtWidgets.QVBoxLayout()
        
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addLayout(name_layout)
        header_layout.addLayout(value_layout)

        name_text = QtWidgets.QLineEdit()
        name_text.setFrame(False)
        name_text.setReadOnly(True)
        name_text.setStyleSheet("padding-left: 5px;")
        name_text.setText(name)
        name_layout.addWidget(name_text)

        value_text = QtWidgets.QLineEdit()
        value_text.setFrame(False)
        value_text.setReadOnly(True)
        value_text.setStyleSheet("")
        value_text.setText(value)
        value_layout.addWidget(value_text)

        results_layout.addLayout(header_layout)

    def isComplete(self):
        return self.completed
