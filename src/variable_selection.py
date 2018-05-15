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

class VariableSelection(AbstractPage):
    TITLE = "Variable selection"
    STEP = 2

    def __init__(self, parent=None, manager=None, wizard=None):
        super(VariableSelection, self).__init__(parent, manager, wizard)
        self.completed = False

    def initializePage(self):
        self.cleanMainLayout()
        self.showDefineVariables()

    def showDefineVariables(self):
        self.variables_layout = QtWidgets.QVBoxLayout()

        self.dep_int_variables_layout = QtWidgets.QHBoxLayout()
        self.exp_variables_layout = QtWidgets.QVBoxLayout()

        self.dependent_variable_layout = QtWidgets.QVBoxLayout()
        self.intercept_variable_layout = QtWidgets.QVBoxLayout()
        
        self.dep_int_variables_layout.addLayout(self.dependent_variable_layout)
        self.dep_int_variables_layout.addLayout(self.intercept_variable_layout)

        self.dependent_variable_label = QtWidgets.QLabel()
        self.dependent_variable_label.setText("Dependent variable")
        self.dependent_variable_input = QtWidgets.QComboBox()
        self.dependent_variable_input.addItems(self.manager.fieldnames)
        self.dependent_variable_input.setObjectName("dependent_variable_input")
        self.dependent_variable_input.setStyleSheet(
            'QComboBox#dependent_variable_input {'
            '   background: '+Color.GREEN+';'
            '   color: #FFF;'
            '   font-size: 16px;'
            '   border: 2px solid '+Color.GREEN+';'
            '}'
            'QComboBox#dependent_variable_input:item {'
            '   background: '+Color.DARKER_GREEN+';'
            '}'
            'QComboBox#dependent_variable_input:item:selected {'
            '   background: '+Color.DARKEST_GREEN+';'
            '}'
            'QComboBox#dependent_variable_input::drop-down {'
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

        self.dependent_variable_layout.addWidget(self.dependent_variable_label)
        self.dependent_variable_layout.addWidget(self.dependent_variable_input)

        self.intercept_variable_label = QtWidgets.QLabel()
        self.intercept_variable_label.setText("Include intecept")
        self.intercept_variable_input = QtWidgets.QComboBox()
        self.intercept_variable_input.addItems(['Yes', 'No'])
        self.intercept_variable_input.setObjectName("intercept_variable_input")
        self.intercept_variable_input.setStyleSheet(
            'QComboBox#intercept_variable_input {'
            '   background: '+Color.GREEN+';'
            '   color: #FFF;'
            '   font-size: 16px;'
            '   border: 2px solid '+Color.GREEN+';'
            '}'
            'QComboBox#intercept_variable_input:item {'
            '   background: '+Color.DARKER_GREEN+';'
            '}'
            'QComboBox#intercept_variable_input:item:selected {'
            '   background: '+Color.DARKEST_GREEN+';'
            '}'
            'QComboBox#intercept_variable_input::drop-down {'
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
        self.intercept_variable_layout.addWidget(self.intercept_variable_label)
        self.intercept_variable_layout.addWidget(self.intercept_variable_input)

        self.explanatory_variables_label = QtWidgets.QLabel()
        self.explanatory_variables_label.setText("Explanatory variables")
        self.explanatory_list_input = QListView()
        self.explanatory_model = QStandardItemModel(self.explanatory_list_input)
        self.explanatory_items = []
        for i, fieldname in enumerate(self.manager.fieldnames):
            item = QStandardItem(fieldname)
            item.setCheckable(True)
            item.setEditable(False)
            self.explanatory_items.append(item)
            self.explanatory_model.appendRow(item)
        self.explanatory_list_input.setModel(self.explanatory_model)
        self.explanatory_variables_button = QtWidgets.QPushButton()
        self.explanatory_variables_button.setObjectName("explanatory_variables_button")
        self.explanatory_variables_button.setText("Select all")
        self.explanatory_variables_button.setStyleSheet(
            'QPushButton#explanatory_variables_button {'
            '   background: '+Color.RED+';'
            '   color: #FFF;'
            '   font-size: 20px;'
            '   border: 0;'
            '   margin-top:20px;'
            '}'
            'QPushButton#explanatory_variables_button:hover {'
            '   background: '+Color.DARKER_RED+';'
            '}'
            'QPushButton#explanatory_variables_button:pressed {'
            '   background: '+Color.DARKEST_RED+';'
            '}'
        )
        self.exp_variables_layout.addWidget(self.explanatory_variables_label)
        self.exp_variables_layout.addWidget(self.explanatory_list_input)
        self.exp_variables_layout.addWidget(self.explanatory_variables_button)
    
        self.variables_layout.addLayout(self.dep_int_variables_layout)
        self.variables_layout.addLayout(self.exp_variables_layout)
        self.main_layout.addLayout(self.variables_layout)

        self.dependent_variable_input.currentIndexChanged.connect(self.dependentSelectChanged)
        self.intercept_variable_input.currentIndexChanged.connect(self.interceptSelectChanged)
        self.explanatory_list_input.clicked.connect(self.explanatorySelectChanged)

        self.dependentSelectChanged(self.dependent_variable_input.currentIndex())
        self.interceptSelectChanged(self.intercept_variable_input.currentIndex())
        self.explanatorySelectChanged(self.dependent_variable_input.currentIndex())

        self.explanatory_variables_button.clicked.connect(self.selectAllClick)

    def dependentSelectChanged(self, index):
        self.manager.depvar = self.manager.fieldnames[index]
        for item in self.explanatory_items:
            item.setEnabled(True)
            item.setCheckable(True)
        self.explanatory_items[index].setEnabled(False)
        self.explanatory_items[index].setCheckable(False)
        self.explanatory_items[index].setCheckState(QtCore.Qt.Unchecked)
        self.explanatorySelectChanged(index)

    def interceptSelectChanged(self, index):
        self.manager.intercept = True if self.intercept_variable_input.currentText() == 'Yes' else False

    def explanatorySelectChanged(self, index):
        self.manager.expvars = []
        for item in self.explanatory_items:
            if item.checkState() == QtCore.Qt.Checked:
                self.manager.expvars.append(item.text())        
        if self.isAllExplanatoryChecked():
            self.explanatory_variables_button.setText("Unselect all")
        else:
            self.explanatory_variables_button.setText("Select all")
        if len(self.manager.expvars) > 0:
            self.completed = True
        else:
            self.completed = False
        self.completeChanged.emit()

    def selectAllClick(self):
        state = QtCore.Qt.Checked if not self.isAllExplanatoryChecked() else QtCore.Qt.Unchecked
        for item in self.explanatory_items:
            if item.isEnabled():
                item.setCheckState(state)
        self.explanatorySelectChanged(0)

    def isAllExplanatoryChecked(self):
        count = 1
        for item in self.explanatory_items:
            if item.checkState() == QtCore.Qt.Checked and item.isEnabled():
                count = count + 1
        return count == len(self.explanatory_items)

    def isComplete(self):
        return self.completed
