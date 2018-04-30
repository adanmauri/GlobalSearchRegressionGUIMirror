import sys
import os

from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from distutils.version import LooseVersion, StrictVersion

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
        self.manager.step = 0

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

        self.setProgress()
        self.setTitle()
        self.prev_button.hide()
        self.next_button.hide()
        self.resized.connect(self.updateWindow)

    def setProgress(self):
        self.progress.setMaximum(self.manager.steps)
        self.progress.setValue(self.manager.step)

    def setTitle(self):
        self.page_step.setText("Step "+str(self.manager.step)+": ")
        self.page_title.setText(self.title)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)

    def horizontalCenter(self, widget, parent=None):
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
            self.horizontalCenter(self.container)
            self.minimumHeight(self.container)

    def link(self, linkStr):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(linkStr))

    def setNavButtons(self):
        self.prev_button.show()
        self.next_button.show()
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
            self.next_button.setStyleSheet("visibility: hidden;")

    def startLoading(self):
        self.loading_anim = QMovie(self.manager.getImage('loading.gif'))
        self.loading_label = QLabel()
        self.loading_label.setMovie(self.loading_anim)
        self.loading_label.setMinimumSize(680,200)
        self.loading_label.setMaximumSize(680,200)
        self.loading_label.setAlignment(QtCore.Qt.AlignCenter)
        self.step_layout.addWidget(self.loading_label)
        self.horizontalCenter(self.loading_label, self.container)
        self.loading_anim.start()

    def stopLoading(self):
        self.loading_label.hide()

    def prev(self):
        pass

    def next(self):
        pass

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

class QIComboBox(QtWidgets.QComboBox):
    def __init__(self,parent=None):
        super(QIComboBox, self).__init__(parent)

class GSRegManager():
    title = u'GSReg GUI'
    julia_executable_config = "JULIA_EXECUTABLE"
    min_julia_version = "0.6.2"
    base_path = None
    static_path = None
    img_path = None
    font_path = None
    steps = 5
    step = 0

    julia_executable = None

    def __init__(self, static_path = None):
        self.base_path = os.getcwd()+'/'
        if static_path is None:
            static_path = 'static/'
        self.static_path = self.base_path+static_path
        self.img_path = self.static_path+'img/' 
        self.font_path = self.static_path+'fonts/' 
        self.scripts_path = self.base_path+'scripts/' 
        self.getJuliaExecutableConfig()

    def getImage(self, filename):
        return self.img_path+filename

    def getFont(self, filename):
        return self.img_path+filename

    def getJuliaExecutableConfig(self):
        try:
            self.getJuliaExecutable()
        except Exception as a:
            self.setJuliaExecutable("julia")

    def getJuliaExecutable(self):
        file = open(self.base_path+'/'+self.julia_executable_config, "r") 
        self.julia_executable=file.read()
        file.close()

    def setJuliaExecutable(self, julia_executable):
        self.julia_executable = julia_executable
        file = open(self.base_path+'/'+self.julia_executable_config, "w")
        file.write(self.julia_executable)
        file.close()

class GSRegGuiStep0(Window):
    manager = None
    ui = "templates/step1.ui"
    next = True
    title = None

    def  __init__(self, manager, parent=None):
        super(GSRegGuiStep0, self).__init__(manager, parent)
        self.stepDispatcher()

    def stepDispatcher(self):
        if self.manager.step == 0:
            self.step0()
        elif self.manager.step == 1:
            self.step1()

    def prev(self):
        self.manager.step = self.manager.step-1
        self.stepDispatcher()

    def next(self):
        self.manager.step = self.manager.step+1
        self.stepDispatcher()

    """
    STEP 0
    """
    description_layout = None
    find_julia_layout = None
    julia_found = False
    def step0(self):
        self.title = "Select Julia executable"
        self.setProgress()
        self.setTitle()
        self.startLoading()
        self.detectJulia()

    def detectJulia(self):       
        command = self.manager.julia_executable
        args =  ['-v']
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.onDetectJuliaFinished)
        self.process.start(command, args)
        self.process.waitForFinished()
        self.stopLoading()
        if not self.julia_found:
            self.findJulia()

    def onDetectJuliaFinished(self):
        self.julia_found = True
        self.manager.julia_version = str(self.process.readAllStandardOutput().split('\n')[0]).replace("julia version ", "")
        if LooseVersion(self.manager.julia_version) < LooseVersion(self.manager.min_julia_version):
            self.stopLoading()
            self.findJulia()
        else:
            self.detectRequirements()

    def findJulia(self):
        self.stopLoading()
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

    def detectRequirements(self):
        self.startLoading()
        command = self.manager.julia_executable
        args =  [self.manager.scripts_path+"require_packages.jl"]
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.onDetectRequirementsFinished)
        self.process.start(command, args)
        self.process.waitForFinished()

    def onDetectRequirementsFinished(self):
        print "adads"
        self.cleanStep0()
        self.next()

    def removeFindJulia(self):
        self.cleanStep0()

    def findJuliaDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self,"Select Julia executable", "","All Files (*)", options=options)
        if filename:
            self.manager.setJuliaExecutable(filename) 
            self.cleanStep0()
            self.detectJulia()

    def cleanStep0(self):
        self.clearLayout(self.description_layout)
        self.clearLayout(self.find_julia_layout)
        self.stopLoading()

    def step1(self):
        self.title = "Load your database"
        self.setProgress()
        self.setTitle()

