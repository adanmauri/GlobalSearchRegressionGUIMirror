from PyQt5.QtWidgets import QApplication, QWidget
import sys
import os

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtCore, QtWidgets
 
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QInputDialog, QLineEdit, QFileDialog


class Window(QMainWindow):
    resized = QtCore.pyqtSignal()
    widget = None
    prev_step = None
    next_step = None
    def  __init__(self, manager, parent=None):
        super(Window, self).__init__(parent=parent)
        #ui = Ui_MainWindow()
        #ui.setupUi(self)
        self.manager = manager

        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont(self.manager.getFont("lato/lato-regular.ttf"))
        your_ttf_font = QFont("Lato")
        #qp.setFont(your_ttf_font)

        self.showMaximized()
        self.setMinimumSize(750, 16777215)
        self.setWindowTitle(self.manager.title)

        self.ui = uic.loadUi(self.ui, self)
        self.container.setMinimumWidth(680)
        self.container.setMaximumWidth(680)
        self.main_layout.setGeometry(QtCore.QRect(10,10,50,50))

        self.gsreg_logotype.setPixmap(QtGui.QPixmap(self.manager.getImage('gsreg_logotype.png')))
        self.julia_logotype.setMaximumSize(200,110)
        self.julia_logotype.setPixmap(QtGui.QPixmap(self.manager.getImage('julia_logotype.png')))
        self.julia_logotype.setMaximumSize(200,110)
        self.progress.setFixedHeight(12)

        self.header_line.setStyleSheet("border: 2px solid #e7e9ec;")

        self.page_step.setFont(QFont("lato-regular", 18, QFont.Bold))
        self.page_step.setStyleSheet("font-weight: 700; color: #333;")
        self.page_step.setFixedWidth(110)
        self.page_step.setFixedHeight(100)
        self.page_title.setFont(QFont("lato-regular", 18, QFont.Bold))
        self.page_title.setStyleSheet("font-weight: 700; color: #666;")
        self.page_title.setFixedHeight(100)

        self.setTitle()
        self.resized.connect(self.updateWindow)

    def setTitle(self):
        self.page_step.setText("Step "+str(self.step)+": ")
        self.page_title.setText(self.title)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)

    def verticalCenter(self, widget, parent=None):
        if parent is None:
            parent = self
        #widget.move(QApplication.desktop().screen().rect().center()- widget.rect().center())
        widget.move((parent.width() / 2)-widget.width()/2, 0)

    def minimumHeight(self, widget, parent=None):
        if parent is None:
            parent = self
        widget.setMinimumHeight(parent.height())

    def updateWindow(self):
        if self.container is not None:
            self.verticalCenter(self.container)
            self.minimumHeight(self.container)

    def link(self, linkStr):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(linkStr))

    def setNavButtons(self):
        if self.prev_step is not None:
            self.prev_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.prev_button.clicked.connect(self.prev)
            self.prev_button.setMaximumSize(200,200)
        else:
            self.prev_button.setStyleSheet("visibility: hidden;")
        
        if self.next_step is not None:
            self.next_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.next_button.clicked.connect(self.next)
            self.next_button.setMaximumSize(200,200)
        else:
            self.next_button.hide()

    def prev(self):
        pass

    def next(self):
        pass

class QIComboBox(QtWidgets.QComboBox):
    def __init__(self,parent=None):
        super(QIComboBox, self).__init__(parent)

class GSRegManager():
    title = u'GSReg GUI'
    root_path = None
    static_path = None
    img_path = None
    font_path = None

    def __init__(self, static_path = None):
        self.root_path = os.getcwd()+'/'
        if static_path is None:
            static_path = 'static/'
        self.static_path = self.root_path+static_path
        self.img_path = self.static_path+'img/' 
        self.font_path = self.static_path+'fonts/' 

    def getImage(self, filename):
        return self.img_path+filename

    def getFont(self, filename):
        return self.img_path+filename

class GSRegGuiStep0(Window):
    manager = None
    ui = "templates/step1.ui"
    title = "Select Julia executable"
    step = 0

    def  __init__(self, manager, parent=None):
        super(GSRegGuiStep0, self).__init__(manager, parent)

        self.description_layout = QtWidgets.QVBoxLayout()
        self.find_julia_layout = QtWidgets.QVBoxLayout()

        self.step_layout.addLayout(self.description_layout)
        self.step_layout.addLayout(self.find_julia_layout)

        self.description_text = QtWidgets.QLabel()
        self.description_text.setStyleSheet("color: #34495e; font-size: 18px;")
        self.description_text.setText("Is Julia already installed? If yes, please, indicate the Julia executable. Otherwise, install Julia and restart this application.")
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
        self.find_julia_button.setObjectName("find_julia_button")
        self.find_julia_button.setStyleSheet(""+
            "QPushButton#find_julia_button {"
            "   background: #cc5c5c;"+
            "   font-size: 20px;"
            "}"+
            "QPushButton#find_julia_button:hover {"
            "   background: #cc3333;"
            "}"
        )
        self.find_julia_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.find_julia_button.clicked.connect(self.findJuliaDialog)
        self.find_julia_layout.addWidget(self.find_julia_button)

        self.next_step = GSRegGuiStep1(manager, parent=self)
        self.next_step.hide()

        self.setNavButtons()

    def findJuliaDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self,"Select Julia executable", "","All Files (*)", options=options)
        if filename:
            self.julia_executable = filename
 
    def next(self):
        #valida_algo
        self.next_step.show()
        self.hide()
 
class GSRegGuiStep1(Window):
    manager = None
    ui = "templates/step1.ui"
    title = "Load your database"
    step = 1

    def  __init__(self, manager, parent=None):
        super(GSRegGuiStep1, self).__init__(manager, parent)
  
class Page2(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.label1 = QtWidgets.QLabel()
        self.label2 = QtWidgets.QLabel()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        self.setLayout(layout)
 
    def initializePage(self):
        self.label1.setText("Example text")
        self.label2.setText("Example text")


