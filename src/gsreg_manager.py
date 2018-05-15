import sys
import os
import sip
import platform
from distutils.version import LooseVersion, StrictVersion
import multiprocessing

class GSRegManager():
    TITLE = u'GSReg GUI'
    JULIA_BINARY_FILE = 'JULIA_BINARY'
    GSREG_SCRIPT_FILE = 'gsreg_script.jl'
    GSREG_BASH_FILE = 'gsreg_script.sh'

    STEPS = 5
    MIN_JULIA_VERSION = '^0.6.2'
    OUTPUT_FILE_PREFIX = '_gsreg_results_'

    AVAILABLE_CRITERIA = [
        {
            'name': 'r2adj',
            'title': 'Adjusted R2',
        },
        {
            'name': 'bic',
            'title': 'BIC',
        },
        {
            'name': 'aic',
            'title': 'AIC',
        },
        {
            'name': 'aicc',
            'title': 'AIC Corrected',
        },
        {
            'name': 'cp',
            'title': "Mallows's Cp",
        },
        {
            'name': 'rmse',
            'title': 'RMSE In',
        },
        {
            'name': 'rmseout',
            'title': 'RMSE Out',
        }
    ]

    root_path = None
    static_path = None
    img_path = None
    font_path = None

    platform = None
    cpu_count = None

    step = None

    julia_binary = None
    input_filename = None
    output_filename = None
    working_directory = None
    fieldnames = None
    observations_number = None

    depvar = None
    expvars = []
    intercept = False
    outsample = None
    samesample = None
    threads = None
    criteria = None

    def __init__(self, static_path = None):
        #self.root_path = os.getcwd()+'/'
        self.root_path = os.path.abspath(os.path.dirname(__file__))+'/'
        self.root_path = self.root_path+'../'
        if static_path is None:
            static_path = 'assets/'
        self.static_path = self.root_path+static_path
        self.img_path = self.static_path+'img/' 
        self.font_path = self.static_path+'fonts/'
        self.templates_path = self.root_path+'templates/'
        self.scripts_path = self.root_path+'scripts/' 
        self.setupPlatform()
        self.setupJuliaBinary()
        self.step = 0
        self.cpu_count = multiprocessing.cpu_count()

    def setupPlatform(self):
        self.platform = platform.system()

    def setupJuliaBinary(self):
        try:
            self.getJuliaBinary()
        except Exception as a:
            print a
            self.setJuliaBinary("julia")

    def setJuliaBinary(self, julia_binary):
        self.julia_binary=julia_binary
        file = open(self.root_path+self.JULIA_BINARY_FILE, "w")
        file.write(self.julia_binary)
        file.close()

    def getJuliaBinary(self):
        file = open(self.root_path+self.JULIA_BINARY_FILE, "r") 
        self.julia_binary=file.read()
        file.close()

    def getImage(self, filename):
        return self.img_path+filename

    def getFont(self, filename):
        return self.img_path+filename

    def getTemplate(self, filename):
        return self.templates_path+filename

    def getScript(self, filename):
        return self.scripts_path+filename
        
    def validate_julia_version(self, julia_version):
        if (self.MIN_JULIA_VERSION[0] == "^"):
            return LooseVersion(self.MIN_JULIA_VERSION[1:]) <= LooseVersion(julia_version)
        else:
            return LooseVersion(self.MIN_JULIA_VERSION) == LooseVersion(version)

    def criteria_title(self, name):
        for criteria in self.AVAILABLE_CRITERIA:
            if criteria['name'] == name:
                return criteria['title']

    def criteria_name(self, title):
        for criteria in self.AVAILABLE_CRITERIA:
            if criteria['title'] == title:
                return criteria['name']
