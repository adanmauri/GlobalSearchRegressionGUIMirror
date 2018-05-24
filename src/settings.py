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
from PyQt5.QtWidgets import QWidget, QInputDialog, QLineEdit, QFileDialog, QListView

from core import AbstractPage, Color

class Settings(AbstractPage):
    TITLE = "Settings"
    STEP = 3

    def __init__(self, parent=None, manager=None, wizard=None):
        super(Settings, self).__init__(parent, manager, wizard)
        self.completed = False
        self.setCommitPage(True)
        self.setButtonText(QtWidgets.QWizard.CommitButton, "Run")

    def initializePage(self):
        self.cleanMainLayout()
        self.showSettings()

    def showSettings(self):
        self.outsample_validator = QIntValidator()
        self.outsample_validator.setBottom(0)
        self.outsample_validator.setTop(self.getAvailableOutsample())
        self.outsample_label = QtWidgets.QLabel()
        self.outsample_label.setText("Out-of-sample size")
        self.outsample_input = QtWidgets.QLineEdit()
        self.outsample_input.setObjectName("outsample_input")
        self.outsample_input.setStyleSheet(
            'QLineEdit#outsample_input {'
            '   font-size: 16px;'
            '   border: 2px solid '+Color.BLUE+';'
            '   border-radius: 0px;'
            '}'
            'QLineEdit#outsample_input:active {'
            '   border: 2px solid '+Color.DARKER_BLUE+';'
            '}'
        )
        self.outsample_input.setFixedWidth(265)
        self.outsample_input.setValidator(self.outsample_validator)
        self.outsample_input.setText(str(0))
        self.outsample_help_label = QtWidgets.QLabel()
        self.outsample_help_label.setText("Min: 0  |  Max: "+str(self.getAvailableOutsample()))
        self.outsample_help_label.setStyleSheet(
            'color: #666;'
            'font-size: 14px;'
        )
        self.outsample_layout = QtWidgets.QVBoxLayout()
        self.outsample_layout.setAlignment(Qt.AlignVCenter)
        self.outsample_layout.addWidget(self.outsample_label)
        self.outsample_layout.addWidget(self.outsample_input)
        self.outsample_layout.addWidget(self.outsample_help_label)

        self.samesample_label = QtWidgets.QLabel()
        self.samesample_label.setText("Force same sample")
        self.samesample_input = QtWidgets.QComboBox()
        self.samesample_input.setFixedWidth(200)
        self.samesample_input.addItems(['Yes', 'No'])
        self.samesample_input.setObjectName("samesample_input")
        self.samesample_input.setStyleSheet(
            'QComboBox#samesample_input {'
            '   background: '+Color.GREEN+';'
            '   color: #FFF;'
            '   font-size: 16px;'
            '   border: 2px solid '+Color.GREEN+';'
            '}'
            'QComboBox#samesample_input:item {'
            '   background: '+Color.DARKER_GREEN+';'
            '}'
            'QComboBox#samesample_input:item:selected {'
            '   background: '+Color.DARKEST_GREEN+';'
            '}'
            'QComboBox#samesample_input::drop-down {'
            '    subcontrol-origin: padding;'
            '    subcontrol-position: top right;'
            '    width: 15px;'
            ''
            '    border-left-width: 1px;'
            '    border-left-color: darkgray;'
            '    border-left-style: solid; /* just a single line */'
            '    border-top-right-radius: 3px; /* same radius as the QComboBox */'
            '    border-bottom-right-radius: 3px;'
            '}'
        )
        self.samesample_help_label = QtWidgets.QLabel()
        self.samesample_help_label.setText("")
        self.samesample_help_label.setStyleSheet(
            'color: #666;'
            'font-size: 14px;'
        )
        self.samesample_layout = QtWidgets.QVBoxLayout()
        self.samesample_layout.setAlignment(Qt.AlignVCenter)
        self.samesample_layout.addWidget(self.samesample_label)
        self.samesample_layout.addWidget(self.samesample_input)
        self.samesample_layout.addWidget(self.samesample_help_label)

        self.threads_validator = QIntValidator()
        self.threads_validator.setBottom(1)
        self.threads_validator.setTop(self.manager.cpu_count)
        self.threads_label = QtWidgets.QLabel()
        self.threads_label.setText("Number of threads")
        self.threads_input = QtWidgets.QLineEdit()
        self.threads_input.setText(str(self.manager.cpu_count))
        self.threads_input.setObjectName("threads_input")
        self.threads_input.setStyleSheet(
            'QLineEdit#threads_input {'
            '   font-size: 16px;'
            '   border: 2px solid '+Color.BLUE+';'
            '   border-radius: 0px;'
            '}'
            'QLineEdit#threads_input:active {'
            '   border: 2px solid '+Color.DARKER_BLUE+';'
            '}'
        )
        self.threads_input.setFixedWidth(200)
        self.threads_input.setValidator(self.threads_validator)
        self.threads_help_label = QtWidgets.QLabel()
        self.threads_help_label.setText("Min: 1  |  Max: "+str(self.manager.cpu_count))
        self.threads_help_label.setStyleSheet(
            'color: #666;'
            'font-size: 14px;'
        )
        self.threads_layout = QtWidgets.QVBoxLayout()
        self.threads_layout.setAlignment(Qt.AlignVCenter)
        self.threads_layout.addWidget(self.threads_label)
        self.threads_layout.addWidget(self.threads_input)
        self.threads_layout.addWidget(self.threads_help_label)

        self.criteria_label = QtWidgets.QLabel()
        self.criteria_label.setText("Ordering criteria")
        self.criteria_list_input = QListView()
        self.criteria_model = QStandardItemModel(self.criteria_list_input)
        self.criteria_items = []
        for i, fieldname in enumerate(self.manager.AVAILABLE_CRITERIA):
            item = QStandardItem(fieldname['title'])
            item.setCheckable(True)
            item.setEditable(False)
            self.criteria_items.append(item)
            self.criteria_model.appendRow(item)
        self.criteria_list_input.setModel(self.criteria_model)
        self.criteria_layout = QtWidgets.QVBoxLayout()
        self.criteria_layout.setAlignment(Qt.AlignVCenter)
        self.criteria_layout.addWidget(self.criteria_label)
        self.criteria_layout.addWidget(self.criteria_list_input)

        self.row1_layout = QtWidgets.QHBoxLayout()
        self.row1_layout.setAlignment(Qt.AlignVCenter)

        self.row2_layout = QtWidgets.QHBoxLayout()
        self.row2_layout.setAlignment(Qt.AlignVCenter)

        self.row1_layout.addLayout(self.outsample_layout)
        self.row1_layout.addLayout(self.samesample_layout)
        self.row1_layout.addLayout(self.threads_layout)

        self.row2_layout.addLayout(self.criteria_layout)

        self.central_layout = QtWidgets.QVBoxLayout()

        self.central_layout.addLayout(self.row1_layout)
        self.central_layout.addLayout(self.row2_layout)

        self.main_layout.addLayout(self.central_layout)

        self.outsample_input.textChanged.connect(self.outsampleChanged)
        self.samesample_input.currentIndexChanged.connect(self.samesampleChanged)
        self.threads_input.textChanged.connect(self.threadsChanged)
        self.criteria_list_input.clicked.connect(self.criteriaChanged)

        self.outsampleChanged(self.outsample_input.text())
        self.samesampleChanged(self.samesample_input.currentIndex())
        self.threadsChanged(self.threads_input.text())
        self.criteriaChanged(self.criteria_list_input.currentIndex())

        self.validateAll()

    def outsampleChanged(self, value):
        if len(value) > 0:
            self.manager.outsample = int(value)
            for item in self.criteria_items:
                if 'rmseout' == self.manager.criteria_name(item.text()):
                    if self.manager.outsample == 0:
                        item.setEnabled(False)
                        item.setCheckable(False)
                        item.setCheckState(QtCore.Qt.Unchecked)
                    else:
                        item.setEnabled(True)
                        item.setCheckable(True)
            self.criteriaChanged(0)
        else:
            self.manager.outsample = None
        self.validateAll()

    def samesampleChanged(self, index):
        self.manager.samesample = True if self.samesample_input.currentText() == 'Yes' else False
        self.validateAll()

    def threadsChanged(self, value):
        if len(value) > 0 and int(value) > 0:
            self.manager.threads = int(value)
        else:
            self.manager.threads = None
        self.validateAll()

    def criteriaChanged(self, index):
        self.manager.criteria = []
        for item in self.criteria_items:
            if item.checkState() == QtCore.Qt.Checked:
                self.manager.criteria.append(self.manager.criteria_name(item.text()))
        self.validateAll()        

    def validateAll(self):
        valid = True
        if self.manager.outsample is None:
            valid = valid and False
        if self.manager.threads is None:
            valid = valid and False
        if len(self.manager.criteria) == 0:
            valid = valid and False
        self.completed = valid
        self.completeChanged.emit()

    def getAvailableOutsample(self):
        return self.manager.observations_number-len(self.manager.expvars) - (1 if self.manager.intercept else 0) - 20 

    def isComplete(self):
        return self.completed
