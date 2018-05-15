#!/usr/bin/env python

import sys
from src.gsreg_manager import GSRegManager
from src.gsreg_wizard import GSRegWizard
from PyQt5 import QtWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    manager = GSRegManager()
    wizard = GSRegWizard(manager=manager)
    wizard.show()
    sys.exit(app.exec_())