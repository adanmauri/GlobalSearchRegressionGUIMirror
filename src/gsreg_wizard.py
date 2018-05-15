#!/usr/bin/env python

from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtCore, QtWidgets, QtGui

from src.select_executable import SelectExecutable
from src.load_database import LoadDatabase
from src.variable_selection import VariableSelection
from src.settings import Settings
from src.running import Running

class GSRegWizard(QtWidgets.QWizard):
    PAGES = [
        'SelectExecutable',
        'LoadDatabase',
        'VariableSelection',
        'Settings',
        'Running'
    ]
    
    manager = None
    
    def __init__(self, parent=None, manager=None):
        super(GSRegWizard, self).__init__(parent)
        self.manager = manager
        self.setUI()
        self.setPages()

    def setUI(self):
        font_db = QtGui.QFontDatabase()
        font_id = font_db.addApplicationFont(self.manager.getFont("lato/lato-regular.ttf"))
        your_ttf_font = QtGui.QFont("Lato")

        self.showMaximized()
        self.setMinimumSize(750, 750)
        self.setWindowTitle(self.manager.TITLE)

        self.setStyleSheet(
            'background: #ffffff;'
        )

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)

    def setPages(self):
        for page in self.PAGES:
            self.addPage(eval(page)(self, manager=self.manager, wizard=self))
    
