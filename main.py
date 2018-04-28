import htmlPy
import os
from backend import Backend
import subprocess

app = htmlPy.AppGUI(title=Backend.title, developer_mode=True)
app.maximized = True

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.static_path = os.path.join(BASE_DIR, "static/")
app.template_path = os.path.join(BASE_DIR, "templates/")

app.bind(Backend(app))

try:
    file = open("JULIA_BINARY", "r") 
    app.JULIA_BINARY=file.read()
    file.close()
except Exception as a:
    app.JULIA_BINARY = None

if Backend.julia_exists(app.JULIA_BINARY):
    app.template = ("pre_requirements.html", {
        "step": 0,
        "steps": Backend.steps,
        "title": Backend.title
    })
else:
    app.template = ("select_julia.html", {
        "step": 0,
        "steps": Backend.steps,
        "title": Backend.title 
    })

if __name__ == "__main__":
    app.start()
