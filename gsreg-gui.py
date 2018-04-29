import htmlPy
import os
import subprocess
from backend import Backend
from PySide import QtGui, QtCore
# --windowed 
# --onefile

#from os.path import expanduser

#home = expanduser("~")

#print home

#exit()

app = htmlPy.AppGUI(title=Backend.TITLE, plugins=True, maximized=True, allow_overwrite=True, developer_mode=False)
app.base_dir = os.path.abspath(os.path.dirname(__file__))
app.static_path = os.path.join(app.base_dir, "static/")
app.template_path = os.path.join(app.base_dir, "templates/")
app.script_path = os.path.join(app.base_dir, "scripts/")
app.window.setWindowIcon(QtGui.QIcon(app.static_path + "img/gsreg_appicon.png"))
app.bind(Backend(app))

try:
    file = open(app.base_dir+'/'+Backend.JULIA_BINARY_FILE, "r") 
    app.julia_binary=file.read()
    file.close()
except Exception as a:
    app.julia_binary="julias"
    file = open(app.base_dir+'/'+Backend.JULIA_BINARY_FILE, "w")
    file.write(app.julia_binary)
    file.close()

if Backend.julia_exists(app.script_path, app.julia_binary):
    app.template = ("pre_requirements.html", {
        "step": 0,
        "steps": Backend.STEPS,
        "title": Backend.TITLE
    })
else:
    app.template = ("select_julia.html", {
        "step": 0,
        "steps": Backend.STEPS,
        "title": Backend.TITLE 
    })

if __name__ == "__main__":
    app.start()
    app.exec_()
    sys.exit(app.exec_())