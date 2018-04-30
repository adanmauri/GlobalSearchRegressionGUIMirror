import sys
from gsreg_gui import *

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    manager = GSRegManager()
    wizard = GSRegGuiStep0(manager)
    wizard.show()
    sys.exit(app.exec_())