from PyQt5.QtWidgets import QApplication, QWidget
import sys
import os
import sip
import platform
from distutils.version import LooseVersion, StrictVersion

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtCore, QtWidgets
 
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QInputDialog, QLineEdit, QFileDialog

from src.select_executable import SelectExecutable
from src.load_database import LoadDatabase

class MainWindow(QMainWindow):
    STEP_CLASSES = [
        'SelectExecutable',
        'LoadDatabase'
    ]
    
    manager = None
    step = None
    widget = None

    def  __init__(self, manager):
        super(MainWindow, self).__init__()
        self.manager = manager
        self.stepSelector()

    def stepSelector(self):
        self.widget = self.STEP_CLASSES[self.manager.step](manager)
