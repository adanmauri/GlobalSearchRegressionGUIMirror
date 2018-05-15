from PyQt5.QtWidgets import QApplication, QWidget
import sys
import os
import datetime
import csv

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtCore, QtWidgets, QtGui
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QInputDialog, QLineEdit, QFileDialog

from core import AbstractPage, Color

class LoadDatabase(AbstractPage):
    TITLE = "Load your database"
    STEP = 1
    summary_text = None
    def __init__(self, parent=None, manager=None, wizard=None):
        super(LoadDatabase, self).__init__(parent, manager, wizard)
        self.completed = False

    def initializePage(self):
        self.showLoadDatabase()

    def showLoadDatabase(self):
        self.description_layout = QtWidgets.QVBoxLayout()
        self.description_text = QtWidgets.QLabel()
        self.description_text.setStyleSheet("color: #34495e; font-size: 18px;")
        self.description_text.setText("You should select a Comma-separated values (CSV) file, where the first row is expected to contain the variable names (column headers). In this version, variables with string values will not be available for calculation.")
        self.description_text.setWordWrap(True)
        self.description_text.setFixedWidth(680)
        self.description_text.setFixedHeight(70)
        self.description_layout.addWidget(self.description_text)

        self.load_database_button = QtWidgets.QPushButton()
        self.load_database_button.setText("Load your database")
        self.load_database_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.load_database_button.clicked.connect(self.loadDatabaseDialog)
        self.load_database_button.setObjectName("load_database_button")
        self.load_database_button.setStyleSheet(
            'QPushButton#load_database_button {'
            '   background: '+Color.RED+';'
            '   color: #FFF;'
            '   font-size: 20px;'
            '   border: 0;'
            '   margin-top:20px;'
            '}'
            'QPushButton#load_database_button:hover {'
            '   background: '+Color.DARKER_RED+';'
            '}'
            'QPushButton#load_database_button:pressed {'
            '   background: '+Color.DARKEST_RED+';'
            '}'
        )

        self.description_layout.addWidget(self.load_database_button)
        self.main_layout.addLayout(self.description_layout)

    def loadDatabaseDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self,"Select your database", "","CSV Files (*.csv)", options=options)
        if filename:
            self.csv_filename = filename
            self.loadDatabase()
    
    def loadDatabase(self):
        self.manager.input_filename = os.path.basename(self.csv_filename)
        self.manager.working_directory = os.path.dirname(self.csv_filename)+'/'
        self.manager.output_filename = os.path.splitext(self.manager.input_filename)[0]+self.manager.OUTPUT_FILE_PREFIX+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.csv'

        with open(self.csv_filename) as csvfile:
            reader = csv.DictReader(csvfile)
            self.manager.fieldnames = reader.fieldnames      
            self.manager.observations_number = sum(1 for line in csvfile)
            csvfile.close()

        if self.summary_text is None:
            self.summary_text = QtWidgets.QLabel()
            self.summary_text.setStyleSheet("margin-top:5px; color: #34495e; font-size: 18px;")
            self.summary_text.setWordWrap(True)
            self.summary_text.setFixedWidth(680)
            self.description_layout.addWidget(self.summary_text)

            self.variables_number = QtWidgets.QLabel()
            self.variables_number.setStyleSheet("margin-top:5px; color: #34495e; font-size: 18px;")
            self.variables_number.setWordWrap(True)
            self.variables_number.setFixedWidth(680)
            self.description_layout.addWidget(self.variables_number)

            self.observations_number = QtWidgets.QLabel()
            self.observations_number.setStyleSheet("margin-top:10px; color: #34495e; font-size: 18px;")
            self.observations_number.setWordWrap(True)
            self.observations_number.setFixedWidth(680)
            self.description_layout.addWidget(self.observations_number)

        self.summary_text.setText("Filename: "+self.csv_filename)
        self.variables_number.setText("Number of variables: "+str(len(self.manager.fieldnames)))
        self.observations_number.setText("Number of observations: "+str(self.manager.observations_number))
        self.completed = True
        self.completeChanged.emit()
    
    def isComplete(self):
        return self.completed
