from connect import *
import pickle
import os
from pathlib import Path


patient = get_current('Patient')
# Setting up storage paths
user_name = os.getlogin()
user_name.replace(" ", "_")
baseline_storage_path = Path('\\\\zkh\\appdata\\Raystation\\Research\\ML\\\Dashboard\\baseline-storage\\')
baseline_storage_file = str(baseline_storage_path / patient.PatientID) + '.pickle'

# Function to load and print baseline values
def show_baseline_values():
    try:
        with open(baseline_storage_file, 'rb') as handle:
            baseline_values = pickle.load(handle)
        print(f"Tumor Location: {baseline_values[0]}")
        print(f"Xerostomia: {baseline_values[1]}")
        print(f"Dysphagia: {baseline_values[2]}")
    except FileNotFoundError:
        print("Baseline data not found.")

# Load and print the baseline values
show_baseline_values()
