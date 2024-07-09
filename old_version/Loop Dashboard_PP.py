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
from tkinter import *
from tkinter.ttk import *
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
DEBUG = True

LastName = "*"
patient_db = get_current("PatientDB")
# mrn = ['RT2022-96-HN-ML-1706', 'RT2022-97-HN-ML-1706', 'RT2022-98-HN-ML-1706', 'RT2022-99-HN-ML-1706']
# mrn = ['RT2022-96-HN-ML-1706']
#mrn = ['2140837', '7052693','2002997','2172254','2241507','zz_00017','2032916','2204934','4616301','2747795']
mrn = ['zz_00017']
# mrn = ['HN_ML_642']
# plan_names = ['ManualPlan', 'ClinicalML']
# plan_names = ['A1PHH', 'ML_plan']
plan_names = ['A1Pclin_mod' , 'Protons_5mm_3%_unaltered','Protons_4mm_3%_v3','Protons_3mm_3%_v3','Protons_2mm_3%_v3' ]
photon_ref_plan_name = 'A1PMediastinum'
script_path = Path().absolute()



for index in range(len(mrn)):
    # get patient from the database
    info = patient_db.QueryPatientInfo(Filter = {'IsImmutable':False, 'IsPhantom':False, 'PatientID':mrn[index]}, UseIndexService=True)     
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
                        exec(open(script_path / 'optionmenu_PP.py').read())
    else:
        print('ERROR - Patient not found : ' + mrn[index])

