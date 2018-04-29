# -*- coding: utf-8 -*-
import htmlPy
import json
import csv
import multiprocessing
from multiprocessing import Process, Value, Array
import time
import subprocess
import os
import datetime


class Backend(htmlPy.Object):
    # GUI callable functions have to be inside a class.
    # The class should be inherited from htmlPy.Object.

    TITLE = u'GSReg for Julia'
    JULIA_MIN_VER = int('062')
    OUTPUT_FILE_PREFIX = '_gsreg_results_'
    STEPS = 4
    JULIA_BINARY_FILE = 'JULIA_BINARY'
    GSREG_SCRIPT_FILE = 'gsreg_script.jl'
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

    julia_binary = 'julia'    


    step = 1

    working_directory = ''
    csv_filename = ''
    
    fieldnames = None
    data = None
    depvar = None
    expvars = None
    intercept = None
    outsample = None

    cpu_count = None
    observations_number = None
    criteria = None

    process = None
    finished = None

    def __init__(self, app):
        super(Backend, self).__init__()
        self.app = app

    def render(self, template, params={}):
        params.update({
            'title': self.TITLE,
            'step': self.step, 
            'steps': self.STEPS
        })
        self.app.template = (template, params)

    def get_available_outsample(self):
        return self.observations_number-len(self.expvars)-(1 if self.intercept else 0)-20 

    @htmlPy.Slot(str, result=str)
    def binary(self, json_data=None):
        form_data = json.loads(json_data)
        self.julia_binary = form_data['binary']    
        
        if self.julia_binary is not None and len(self.julia_binary) < 1:
            return

        if not self.julia_exists(self.app.script_path, self.julia_binary):
            self.render('select_julia.html', {'alert': {
                    'title': 'Julia executable',
                    'body': 'Wrong selected executable '
                }}
            )
            return

        if not self.julia_version_check(self.julia_binary, self.JULIA_MIN_VER):
            self.render('select_julia.html', {'alert': {
                    'title': 'Julia version',
                    'body': 'GSReg requires Julia version 0.6.2 or higher. Please update Julia.'
                }}
            )
            return

        file = open(self.app.base_dir+'/'+self.JULIA_BINARY_FILE, 'w') 
        file.write(self.julia_binary)
        file.close()
        self.check_requirements(self.julia_binary)

    @htmlPy.Slot()
    def check_requirements(self, julia_binary=None):
        if julia_binary is not None:
            self.julia_binary = julia_binary
        else:
            self.julia_binary = self.app.julia_binary

        self.finished = Value('B', False)
        self.step = 0
        self.render('requirements.html')

        self.process = Process(target=self.run_check_requirements, args=(self.finished,))
        self.process.start()

    def run_check_requirements(self, finished):
        cmd = self.julia_binary+' '+self.app.script_path+'julia/require_packages.jl'
        subprocess.call(cmd, shell=False)
        finished.value = True

    @htmlPy.Slot(result=str)
    def check_requirements_is_done(self):
        if self.finished.value:
            self.select_csv()    

    @htmlPy.Slot()
    def select_csv(self, alert=None):
        self.csv_filename = ''
        self.fieldnames = None
        self.step = 1
        self.render('select_csv.html', {
            'alert': alert
        })

    @htmlPy.Slot(str, result=str)
    def variables(self, json_data=None, alert=None):
        if json_data:
            form_data = json.loads(json_data)
        else:
            form_data = {}
        
        form_database_exists = not ('database' not in form_data or len(form_data['database']) == 0)

        if (not form_database_exists) and len(self.csv_filename) == 0:
            self.select_csv(alert={
                'title': 'CSV file required',
                'body': 'Please select you CSV file'
            })
            return

        if form_database_exists:
            self.csv_filename = form_data['database']

        self.working_directory = os.path.dirname(self.csv_filename)+'/'
        self.input_filename = os.path.basename(self.csv_filename)
        self.output_filename = os.path.splitext(self.input_filename)[0]+self.OUTPUT_FILE_PREFIX+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.csv'

        with open(self.csv_filename) as csvfile:
            reader = csv.DictReader(csvfile)
            self.fieldnames = reader.fieldnames      
            self.observations_number = sum(1 for line in csvfile)
            csvfile.close()

        self.step = 2
        self.render('variables.html', {
            'variables': self.fieldnames,
            'alert': alert
        })

    @htmlPy.Slot()
    def back_variables(self):
        self.variables()

    @htmlPy.Slot(str, result=str)
    def settings(self, json_data=None, alert=None):
        if json_data:
            form_data = json.loads(json_data)
        else:
            form_data = {}
        
        if 'depvar' not in form_data and not self.depvar:
            return
        if 'expvars' not in form_data and not self.expvars:
            return
        if 'intercept' not in form_data and not self.intercept:
            return
        
        self.depvar = form_data['depvar'] if 'depvar' in form_data else self.depvar 
        
        self.intercept = form_data['intercept'] if 'intercept' in form_data else self.intercept

        if 'expvars' in form_data:
            self.expvars = form_data['expvars']
        
        if len(self.expvars) == 0:
            self.variables(alert={
                'title': 'Missing explanatory variables',
                'body': 'Please select your explanatory variables'
            })
            return

        if 'expvars' in form_data:
            self.expvars = self.expvars.split(';')
        else: 
            self.expvars = ''       

        self.depvar = self.depvar.replace(' ', '_')
        self.intercept = True if self.intercept == 'on' or self.intercept == True else False
        self.cpu_count = multiprocessing.cpu_count()

        self.step = 3
        self.render('settings.html', {
            'cpu_count': self.cpu_count,
            'available_criteria': self.AVAILABLE_CRITERIA,
            'observations_number': self.observations_number,
            'available_outsample': self.get_available_outsample(),
            'alert': alert
        })
        
    @htmlPy.Slot()
    def back_settings(self):
        self.settings()

    @htmlPy.Slot(str, result=str)
    def output(self, json_data):
        if json_data:
            form_data = json.loads(json_data)
        else:
            form_data = {}

        if 'outsample' not in form_data and not self.outsample:
            return
        if 'criteria' not in form_data and not self.criteria:
            return
        if 'samesample' not in form_data and not self.samesample:
            return
        if 'threads' not in form_data and not self.threads:
            return
        
        self.outsample = form_data['outsample'] if 'outsample' in form_data else self.outsample
        self.outsample = int(self.outsample)

        self.criteria = form_data['criteria'] if 'criteria' in form_data else self.criteria
        if len(self.criteria) == 0:
            self.settings(alert={
                'title': 'Missing ordering criteria',
                'body': 'Please select your ordering criteria'
            })
            return

        self.criteria = self.criteria.split(';')
        self.criteria_symbols = [':' + criteria for criteria in self.criteria]

        self.threads = form_data['threads'] if 'threads' in form_data else self.threads
        self.threads = int(self.threads)

        self.samesample = form_data['samesample'] if 'samesample' in form_data else self.samesample
        self.samesample = True if self.samesample == 'on' or self.samesample==True else False
        
        if self.outsample < 0 or self.outsample > self.get_available_outsample():
            return

        if self.threads < 1 or self.threads > self.cpu_count:
            return

        self.execute()
        #self.step = 4
        #self.render('output.html', {})

    @htmlPy.Slot(str, result=str)
    def execute(self, json_data=None):
        self.finished = Value('B', False)

        #form_data = json.loads(json_data)        
        #self.output_file = form_data['output']
        
        self.step = 4
        self.render('execute.html', {})

        script = 'using CSV'+'\n'
        script+= 'using GSReg'+'\n'
        script+= 'data = CSV.read("'+self.csv_filename+'")'+'\n'
        script+= 'GSReg.gsreg("'+self.depvar+' '+' '.join(self.expvars)+'"'
        script+= ', data'
        script+= ', intercept='+'true' if self.intercept else 'false'
        if self.outsample > 0:
            script+= ', outsample='+str(self.outsample)
        script+= ', samesample='+'true' if self.samesample else 'false'
        script+= ', criteria=['+', '.join(self.criteria_symbols)+']'
        #script+= ', csv=''+self.output_file+'''
        script+= ', csv="'+self.working_directory+self.output_filename+'"'
        script+= ', ttest=true'
        script+= ')'
        
        file = open(self.app.base_dir+'/'+self.GSREG_SCRIPT_FILE, 'w') 
        file.write(script)
        file.close()

        self.process = Process(target=self.run_julia, args=(self.finished,))
        self.process.start()
        #self.done()

    def run_julia(self, finished):
        cmd = 'JULIA_NUM_THREADS='+str(self.threads)+' '+self.julia_binary+' '+self.app.base_dir+'/'+self.GSREG_SCRIPT_FILE
        subprocess.call(cmd, shell=False)
        finished.value = True

    @htmlPy.Slot(result=str)
    def is_done(self):
        if self.finished.value:
            self.done()

    @htmlPy.Slot()
    def done(self):
        os.remove(self.app.base_dir+'/'+self.GSREG_SCRIPT_FILE)
        with open(self.working_directory+self.output_filename) as csvfile:
            reader = csv.DictReader(csvfile)
            summary = next(reader)
        
        for key, value in summary.iteritems():
            try:
                if len(summary[key]) > 0: 
                    summary[key] = float(summary[key])
                else:
                    summary[key] = None
            except Exception as e:
                pass
        
        self.step=5
        self.render('done.html', {
            'output_file': self.working_directory+self.output_filename,
            'summary': summary,
            'data': self
        })

    @htmlPy.Slot()
    def exit_program(self):
        self.app.stop()

    def criteria_title(self, name):
        for criteria in self.AVAILABLE_CRITERIA:
            if criteria['name'] == name:
                return criteria['title']

    @staticmethod
    def julia_exists(script_path, julia_binary=None):
        if julia_binary is None:
            julia_binary = 'julia'
        
        exists = False
        try:
            exists = True if subprocess.call(['bash '+script_path+'bash/detect.sh '+julia_binary], shell=False) is 1 else False
        except Exception as e:
            exists = False
        return exists

    @staticmethod
    def julia_version(julia_binary):
        output = subprocess.check_output(julia_binary+' -v', shell=False)
        output = int(output.replace('\n', '').replace('.', '').replace('julia version ', ''))
        return output

    @staticmethod
    def julia_version_check(julia_binary, julia_min_ver):
        return Backend.julia_version(julia_binary) >= julia_min_ver
