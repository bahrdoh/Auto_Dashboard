from connect import *
from tkinter import *
from tkinter.ttk import *
from new_window import *
import numpy as np
import pickle
import os
import copy
import sys
import csv
import re
from pathlib import Path

patient = get_current('Patient')

# Setting up storage paths
user_name = os.getlogin()
user_name.replace(" ", "_")
baseline_storage_path = Path('\\\\zkh\\appdata\\Raystation\\Research\\ML\\\Dashboard\\baseline-storage\\')
baseline_storage_file = str(baseline_storage_path / patient.PatientID) + '.pickle'

# Make the tkinter window with different option-menus
master = Tk()

Tumorlocation = ['Pharynx', 'Oral cavity', 'Larynx and others']  # all the baseline complication options
Baseline_xerostomie = ['Not at all', 'A little', 'Quite bad']
Baseline_dysfagie = ['Grade 0-1', 'Grade 2', 'Grade 3-4']

variable2 = StringVar(master)
variable3 = StringVar(master)
variable4 = StringVar(master)

# Try to load existing baseline values, or set default values
try:
    with open(baseline_storage_file, 'rb') as handle:
        base_values = pickle.load(handle)
except FileNotFoundError:
    base_values = ['Pharynx', 'Not at all', 'Grade 0-1']

variable2.set(base_values[0])  # retrieve the base complication values that were chosen
variable3.set(base_values[1])
variable4.set(base_values[2])

# Labels to indicate what you are actually choosing
Label(master, text="select a tumour site").grid(row=1, column=1)
Label(master, text="select the baseline xerostomia").grid(row=2, column=1)
Label(master, text="select the baseline dysfagia").grid(row=3, column=1)

OptionMenu(master, variable2, base_values[0], *Tumorlocation).grid(row=1, column=2)
OptionMenu(master, variable3, base_values[1], *Baseline_xerostomie).grid(row=2, column=2)
OptionMenu(master, variable4, base_values[2], *Baseline_dysfagie).grid(row=3, column=2)

# Function to save baseline values
def save_baseline_values():
    baseline_values = [variable2.get(), variable3.get(), variable4.get()]
    with open(baseline_storage_file, 'wb') as handle:
        pickle.dump(baseline_values, handle)
    print('Baseline values saved to:', baseline_storage_file)
    master.quit()

# Button to save the selected values
Button(master, text="Save", command=save_baseline_values).grid(row=4, column=1, columnspan=2)

mainloop()
