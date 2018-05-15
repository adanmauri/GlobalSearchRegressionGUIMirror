from PyQt5.QtWidgets import QApplication, QWidget
import sys
import os


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

class SelectExecutable(AbstractPage):
    TITLE = "Select Julia executable"
    STEP = 0
    completed = None

    def  __init__(self, parent=None, manager=None, wizard=None):
        super(SelectExecutable, self).__init__(parent, manager, wizard)
        self.setCommitPage(True)
        self.completed = False
        self.setProgressBar()
        self.setButtonText(QtWidgets.QWizard.CommitButton, "Select")

    def initializePage(self):
        self.detectJulia()

    def detectJulia(self, selected=False):
        self.setTitle(step=False, title='Checking requirements')
        self.showLoading()
        self.process = QtCore.QProcess()
        self.process.start(self.manager.julia_binary+' -v')
        self.process.waitForFinished(msecs=1000)

        if self.process.exitCode() != 0:
            if selected:
                self.showInvalidBinaryMessage()
            self.showFindJulia()
        else:    
            julia_version = str(self.process.readAllStandardOutput())
            if julia_version.find('julia version') == -1:
                if selected:
                    self.showInvalidBinaryMessage()
                self.showFindJulia()
            else:
                julia_version = julia_version.replace('\n', '').replace('julia version ', '')
                if not self.manager.validate_julia_version(julia_version):
                    self.showOldBinaryMessage()
                    self.showFindJulia()
                else:
                    self.updateRequirements()

    def updateRequirements(self):
        self.setTitle(step=False, title='Updating Julia requirements')
        self.process = QtCore.QProcess()
        self.process.finished.connect(self.updateRequirementsCallback)
        self.process.start(self.manager.julia_binary+' '+self.manager.getScript('require_packages.jl'))

    def updateRequirementsCallback(self):
        self.completed = True
        self.completeChanged.emit()
        self.wizard.next()

    def showInvalidBinaryMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Your selected file does not appears to be a valid Julia executable.")
        msg.setWindowTitle("Invalid Julia executable")
        retval = msg.exec_()

    def showOldBinaryMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        version = self.manager.MIN_JULIA_VERSION
        if self.manager.MIN_JULIA_VERSION[0] == '^':
            version = self.manager.MIN_JULIA_VERSION[1:]+' or higher'

        msg.setText("Your selected Julia executable is older than required ("+version+").")
        msg.setWindowTitle("Old Julia version")
        retval = msg.exec_()

    def showFindJulia(self):
        version = self.manager.MIN_JULIA_VERSION
        if self.manager.MIN_JULIA_VERSION[0] == '^':
            version = self.manager.MIN_JULIA_VERSION[1:]+' or higher'

        self.hideLoading()
        self.setTitle(step=False, title="Select Julia executable")
        self.description_layout = QtWidgets.QVBoxLayout()
        self.description_text = QtWidgets.QLabel()
        self.description_text.setStyleSheet("color: #34495e; font-size: 18px;")
        self.description_text.setText("Is Julia "+version+" already installed? If yes, please, indicate the Julia executable. Otherwise, install Julia and restart this application.")
        self.description_text.setWordWrap(True)
        self.description_text.setFixedWidth(680)
        self.description_text.setFixedHeight(45)
        
        self.how_to = QtWidgets.QLabel()
        self.how_to.setStyleSheet("color: #34495e; font-size: 18px;")
        self.how_to.linkActivated.connect(self.link)
        self.how_to.setText('How to install Julia [<a style="color: #60ad51;" href="https://julialang.org/downloads/platform.html"]>https://julialang.org/downloads/platform.html</a>]')
        self.how_to.setWordWrap(True)
        self.how_to.setFixedWidth(680)
        self.how_to.setFixedHeight(40)
        
        self.description_layout.addWidget(self.description_text)
        self.description_layout.addWidget(self.how_to)

        self.find_julia_button = QtWidgets.QPushButton()
        self.find_julia_button.setText("Find Julia executable")
        self.find_julia_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.find_julia_button.clicked.connect(self.findJuliaDialog)
        self.find_julia_button.setObjectName("find_julia_button")
        self.find_julia_button.setStyleSheet(
            'QPushButton#find_julia_button {'
            '   background: '+Color.RED+';'
            '   color: #FFF;'
            '   font-size: 20px;'
            '   border: 0;'
            '   margin-top:20px;'
            '}'
            'QPushButton#find_julia_button:hover {'
            '   background: '+Color.DARKER_RED+';'
            '}'
            'QPushButton#find_julia_button:pressed {'
            '   background: '+Color.DARKEST_RED+';'
            '}'
        )
        self.description_layout.addWidget(self.find_julia_button)
        self.main_layout.addLayout(self.description_layout)

    def findJuliaDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self,"Select Julia executable", "","All Files (*)", options=options)
        if filename:
            self.manager.setJuliaBinary(filename)
            self.detectJulia(selected=True)

    def isComplete(self):
        return self.completed

    def isCommitPage(self):
        return True
