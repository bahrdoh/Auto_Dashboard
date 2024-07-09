#!/usr/bin/env python
"""
Dose statistics export to SQL with loop patient Db script for Raystation
"""

__project__ = "LoopDb_Use_PlanName"
__author__ = "r.g.j.kierkelsn@umcg.nl"
__copyright__ = "Copyright UMCG 2015-2017, UMC Groningen -The Netherlands "
__version__ = "61.0.0"

from connect import *
# from optionmenu import *
from tkinter.ttk import *
from tkinter import *
import numpy as np
import pickle
import os
import copy
import sys
import csv
import re
from pathlib import Path
import locale

locale.setlocale(locale.LC_ALL, '') # Use locale with decimal point for csv export

all_data = []
plan_info = []
DEBUG = False 

LastName = "*"
patient_db = get_current("PatientDB") 
mrn = ['HN_ML_P_752', 'HN_ML_P_753']
plan_names = ['A1PHH', 'X_ML_plan'] 
photon_ref_plan_name = 'A1FHH'
script_path = Path().absolute()



for index in range(len(mrn)):
    # get patient from the database
    info = patient_db.QueryPatientInfo(Filter = {'IsImmutable':False, 'IsPhantom':False, 'PatientID':f'^{mrn[index] }$'}, UseIndexService=True)    
    print(len(info))

    if len(info) == 1:
        if DEBUG:
            patient = get_current("Patient")
        else:
            patient = patient_db.LoadPatient(PatientInfo = info[0], AllowPatientUpgrade=True)
        for case in patient.Cases:            
            case.SetCurrent()           
            for plan_name in plan_names:
                print('Loop Dashboard plan_name : ' + plan_name)
                for plan in case.TreatmentPlans: 
                    print('Loop Dashboard case.TreatmentPlan : ' + plan.Name)
                    if plan.Name.lower() == plan_name.lower():
                        exec(open(script_path / 'optionmenu_Ilse_OARs.py').read())
    else:
        print('ERROR - Patient not found : ' + mrn[index])

