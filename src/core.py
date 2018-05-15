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

class Color():
    GREEN = '#60ad51'
    DARKER_GREEN = '#228a22'
    DARKEST_GREEN = '#1a6d1a'

    BLUE = '#6682e0'
    DARKER_BLUE = '#3a5fcc'
    DARKEST_BLUE = '#2d4ba3'
   
    RED = '#cc5c5c'
    DARKER_RED = '#ad4c4c'
    DARKEST_RED = '#7f2323'

class AbstractPage(QtWidgets.QWizardPage):    
    ui = "widget.ui"
    STEP = None
    PREV_STEP = None
    NEXT_STEP = 1
    resized = QtCore.pyqtSignal()
    loading = None

    def  __init__(self, parent=None, manager=None, wizard=None):
        super(AbstractPage, self).__init__(parent=None)
        self.manager = manager
        self.wizard = wizard
        self.setUI()
        self.setProgressBar()
        self.setTitle()

    def setUI(self):
        uic.loadUi(self.manager.getTemplate(self.ui), self)

        self.wrapper_layout.setGeometry(QtCore.QRect(10,10,50,50))

        # Main Widget 
        self.main_widget.setMinimumWidth(680)
        self.main_widget.setMaximumWidth(680)

        # Logotypes
        self.gsreg_logotype.setPixmap(QtGui.QPixmap(self.manager.getImage('gsreg_logotype.png')))
        self.gsreg_logotype.setAlignment(Qt.AlignRight)
        self.gsreg_logotype.setAlignment(Qt.AlignVCenter)
        self.gsreg_logotype.setFixedHeight(90)
        self.gsreg_logotype.setFixedWidth(340)
        self.julia_logotype.setPixmap(QtGui.QPixmap(self.manager.getImage('julia_logotype.png')))
        self.julia_logotype.setAlignment(Qt.AlignLeft)
        self.julia_logotype.setAlignment(Qt.AlignVCenter)
        self.julia_logotype.setFixedHeight(90)
        self.julia_logotype.setFixedWidth(330)

        # Header Line
        self.header_line.setStyleSheet("border: 2px solid #e7e9ec;")

        # Progress Bar
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setMaximum(self.manager.STEPS)
        self.progress_bar.setStyleSheet(
            'QProgressBar {'
            '   border-color: 0;'
            '   background: #ebedef;'
            '}'
            'QProgressBar:horizontal {'
            '   border-radius: 5px;'
            '}'
            'QProgressBar::chunk {'
            '   background: '+Color.RED+';'
            '   border-radius: 5px;'
            '}'
        )

        # Page Step
        self.step_label.setFont(QFont("lato-regular", 18, QFont.Bold))
        self.step_label.setStyleSheet("font-weight: 700; color: #333;")
        self.step_label.setFixedWidth(110)
        self.step_label.setFixedHeight(100)
        self.step_label.setFixedHeight(50)
        self.title_label.setFont(QFont("lato-regular", 18, QFont.Bold))
        self.title_label.setStyleSheet("font-weight: 700; color: #666;")
        self.title_label.setFixedHeight(50)

        # Window
        self.resized.connect(self.updateWindow)

    def setProgressBar(self):
        if self.STEP is not None or self.STEP is not False:
            self.progress_bar.setValue(self.STEP)
        
    def setTitle(self, step=None, title=None):
        if (step is None or step is not False) and (self.STEP is not None or self.STEP is not False):
            step = self.STEP
        else:
            step = None

        if step is not None:
            self.step_label.setText("Step "+str(step)+": ")
            self.step_label.show()
        else:
            self.step_label.hide()

        if title is None:
            title = self.TITLE
        self.title_label.setText(title)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(AbstractPage, self).resizeEvent(event)

    def verticalCenter(self, widget, parent=None):
        if parent is None:
            parent = self
        widget.move((parent.width() / 2)-widget.width()/2, 0)

    def minimumHeight(self, widget, parent=None):
        if parent is None:
            parent = self
        widget.setMinimumHeight(parent.height())
    
    def updateWindow(self):
        if self.main_widget is not None:
            self.verticalCenter(self.main_widget)
            self.minimumHeight(self.main_widget)
    
    def link(self, linkStr):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(linkStr))

    def showLoading(self):
        self.cleanMainLayout()    
        loading = QtGui.QMovie(self.manager.getImage('loading.gif'))
        self.loading_label = QtWidgets.QLabel()
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setMovie(loading)
        loading.start()
        self.main_layout.addWidget(self.loading_label)

    def hideLoading(self):
        self.cleanMainLayout()    
        if self.loading_label is not None:
            self.main_layout.removeWidget(self.loading_label)
            sip.delete(self.loading_label)
            self.loading_label = None

    def cleanMainLayout(self):
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if self.main_layout.widget():
                self.main_layout.widget().deleteLater()
