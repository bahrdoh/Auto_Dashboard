from connect import *
from tkinter import *
from tkinter.ttk import *
from new_window_Ilse import *
import numpy as np
import pickle
import os
import copy
import sys
import csv
import re
from pathlib import Path

case = get_current('Case')
patient = get_current('Patient')


ROI_NAMES = ['CTV_7000', 'CTV_5425', 'BODY', 'BaseOfTongue', 'Brain', 'BrainStem', 'Cerebellum', 'Cerebrum',
             'Cochlea_L', 'Cochlea_R', 'Crico', 'Esophagus_Cerv', 'GlotticArea', 
             'Lacrimal_L', 'Lacrimal_R', 'non-NTCP-OARs_out', 'OpticNerve_L', 'OpticNerve_R', 'OralCavity_Ext', 'OralCavity_inPTV70_07', 'OralCavity_inPTV54_07', 
             'Parotid_L', 'ParotidL_inPTV70_07','ParotidL_inPTV54_07','Parotid_R', 'ParotidR_inPTV70_05', 'ParotidR_inPTV54_05', 'PCM_Inf', 'PCMInf_inPTV70_07',
             'PCMInf_inPTV54_07', 'PCM_Med', 'PCMMed_inPTV70_05','PCMMed_inPTV54_05', 'PCM_Sup','PCMSup_inPTV70_05','PCMSup_inPTV54_05', 'Submandibular_L', 
             'SubmandibularL_inPTV70_05', 'SubmandibularL_inPTV54_05', 'Submandibular_R', 'SubmandibularR_inPTV70_05', 'SubmandibularL_inPTV54_05', 'SpinalCord', 'Supraglottic', 'Thyroid']
             
'''doses of the nominal plan'''            
def get_doses(plan, roi_names):    
    ROI_doses = []
    ROI_names = []
    ROI_evaluation = []
    total_dose = plan.TreatmentCourse.TotalDose
    for roi_names in ROI_NAMES:
        try:                                                                        #The try except is here because not all patients have all the ROI's in the list
            total_dose.GetDoseStatistic(RoiName = roi_names, DoseType='Average')
        except: 
            pass
        else:
            ROI_doses.append(round(total_dose.GetDoseStatistic(RoiName = roi_names, DoseType='Average')))
            ROI_names.append(roi_names)
    max_width_ROI = max(len(x) for x in ROI_names) #The length of the longest ROI name, will come in handy later
    return ROI_names, ROI_doses, max_width_ROI

'''This function will check if a plan has a scenario group. If it does not have a scenario group it will give an assertion error'''
def get_scenario_group(case, plan): 
    rssgs = case.TreatmentDelivery.RadiationSetScenarioGroups
    scenario_group=None
    for sg in rssgs:
        if sg.ReferencedRadiationSet.BeamSetIdentifier() == plan.BeamSets[0].BeamSetIdentifier():
            scenario_group=sg
    assert(scenario_group!=None)
    return scenario_group

'''The voxelwise worst values of the clinical goals cannot be retrieved form RayStation directly, however the dose data of each individual scenario can be retrieved.
This function flattens (makes it a vector) all those dose values and puts them in the same list beneath each other.
Then it finds the lowest and highest value in each column. This is the voxelwise min and voxelwise max data'''     
def compute_voxelwise_min_max(group):
    scenario_doses=[]
    i=0
    for scenario in group.DiscreteFractionDoseScenarios:
        dose = scenario.DoseValues.DoseData
        scenario_doses.append(dose.flatten('C'))
        i += 1
    voxelwise_min = np.min(scenario_doses, axis=0)
    voxelwise_max= np.max(scenario_doses, axis=0)
    return voxelwise_min, voxelwise_max

'''This function creates the vox worst plans.
If the voxelwise worst plans already exist it calculates the new dose data and puts that in the existing voxelwise worst plans
If the voxelwise worst plans do not exist yet it copies the normal plan and puts the voxelwise worst data in there'''
def create_vox_worst_plans(case, plan, plan_name):
    scenario_group = get_scenario_group(case, plan)
    voxelwise_min, voxelwise_max = compute_voxelwise_min_max(scenario_group)
    
    new_plan_name_min = 'vwmin_' + plan_name
    new_plan_name_max = 'vwmax_' + plan_name
    existing_names = [p.Name for p in case.TreatmentPlans]
    
    if new_plan_name_min not in existing_names:
        case.CopyPlan(PlanName=plan_name, NewPlanName=new_plan_name_min)
        case.CopyPlan(PlanName=plan_name, NewPlanName=new_plan_name_max)
        new_plan_min = case.TreatmentPlans[new_plan_name_min]
        new_plan_max = case.TreatmentPlans[new_plan_name_max]
        new_bs_min = new_plan_min.BeamSets[0]
        new_bs_max = new_plan_max.BeamSets[0]
        try:
            new_bs_min.FractionDose.SetDoseValues(Dose=voxelwise_min, CalculationInfo='')
            new_bs_max.FractionDose.SetDoseValues(Dose=voxelwise_max, CalculationInfo='')
        except:
            # For RayStation versions before 11B
            new_bs_min.FractionDose.SetDoseValues(Array=voxelwise_min, CalculationInfo='')
            new_bs_max.FractionDose.SetDoseValues(Array=voxelwise_max, CalculationInfo='')       
    else:
        new_plan_min = case.TreatmentPlans[new_plan_name_min]
        new_plan_max = case.TreatmentPlans[new_plan_name_max]
        new_bs_min = new_plan_min.BeamSets[0]
        new_bs_max = new_plan_max.BeamSets[0]
        try:
            new_bs_min.FractionDose.SetDoseValues(Dose=voxelwise_min, CalculationInfo='')
            new_bs_max.FractionDose.SetDoseValues(Dose=voxelwise_max, CalculationInfo='')     
        except:
            new_bs_min.FractionDose.SetDoseValues(Array=voxelwise_min, CalculationInfo='')
            new_bs_max.FractionDose.SetDoseValues(Array=voxelwise_max, CalculationInfo='')
        
    return new_plan_min, new_plan_max

''''This function checks if new voxelwise worst plans need to be made'''
def find_latest_vox_worst_plans(case, plan):
    plan_name = plan.Name
    new_plan_name_min = 'vwmin_' + plan_name
    new_plan_name_max = 'vwmax_' + plan_name
    existing_names = [p.Name for p in case.TreatmentPlans]
    
    if new_plan_name_min not in existing_names: #If no voxelwise worst plans exist yet, make them
        new_plan_min, new_plan_max = create_vox_worst_plans(case, plan, plan_name)
    else:
        latest_plan_min = case.TreatmentPlans[new_plan_name_min]
        latest_plan_max = case.TreatmentPlans[new_plan_name_max]
        try: #try to find the latest save times of the voxelwise worst plans and the normal plan. If the plans are not saved yet, the timestamps don't exist, hence the "try-except"
            time_latest_plan_min = latest_plan_min.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
            time_latest_optimization = plan.PlanOptimizations[len(plan.PlanOptimizations)-1].OptimizedBeamSets[0].ModificationInfo.ModificationTime
        except:
            time_latest_plan_min = []
            time_latest_optimization = []
        if time_latest_optimization and time_latest_plan_min:   #An empty list will be evaluated as false and go to the else clause.
            if time_latest_plan_min > time_latest_optimization: #If the latest voxel worst plans are more recently made than the latest optimization of the plan, use the most recent voxelwise worst plans.
                new_plan_min = latest_plan_min
                new_plan_max = latest_plan_max
            else:
                new_plan_min, new_plan_max = create_vox_worst_plans(case, plan, plan_name)
        else:
            new_plan_min, new_plan_max = create_vox_worst_plans(case, plan, plan_name) 
    return new_plan_min, new_plan_max        
   
'''This function calculates a robust equivalent for the conformity index'''  
def conformity_index(plan, dosevalue, roi_name):
    try: # the "try-except" is there for if there is already the same clinical goal an error will occur.
        plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName = roi_name, GoalCriteria = "AtLeast", GoalType = "ConformityIndex", AcceptanceLevel = 1, ParameterValue = dosevalue)
        x = len(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
        conformity_index = round(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[x-1].GetClinicalGoalValue(), 3) #This works because the last evaluation function that's added will also be the last in the list of evaluation functions.
    except:
        x = len(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
        for i in range(x): # The following evaluation function is guaranteed to exist otherwise the "try" statement would have worked
            if plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[i].PlanningGoal.ParameterValue == dosevalue and plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[i].PlanningGoal.Type == 'ConformityIndex':
                conformity_index = round(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[i].GetClinicalGoalValue(), 3)
                return conformity_index          
    return conformity_index

'''This function calculates a robust homogeneity index'''  
def homogeneity_index(plan, fractionvalue, roi_name):
    try: # the "try-except" is there for if there is already the same clinical goal an error will occur.
        plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=roi_name, GoalCriteria="AtLeast", GoalType="HomogeneityIndex", AcceptanceLevel=1, ParameterValue=fractionvalue)
        x = len(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
        homogeneity_index = round(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[x-1].GetClinicalGoalValue(), 4) #This works because the last evaluation function that's added will also be the last in the list of evaluation functions.
    except:
        x = len(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
        for i in range(x): # The following evaluation function is guaranteed to exist otherwise the "try" statement would have worked
            if plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[i].PlanningGoal.ParameterValue == fractionvalue and plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[i].PlanningGoal.Type == 'HomogeneityIndex':
                homogeneity_index = round(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[i].GetClinicalGoalValue(), 4)
                return homogeneity_index          
    return homogeneity_index


'''This fucntion calculates predicted OAR doses also known as 'The Makbule tool'''
def calculate_oar_prediction(plan):
        """
        Calculates predicted OAR doses
        """                          
        _oralcavityB = [1.481, 0.641, 0.558] # constant, VOLUMEperc_in70_07,  VOLUMEperc_in54out70_07
        _oralcavityLow = [0.906, 0.610, 0.473] # 95% confidence interval lower bound
        _oralcavityUp = [2.056, 0.672, 0.643]   # 95% confidence interval upper bound      
        oral_cavity_rois = ['OralCavity_Ext', 'OralCavity_inPTV70_07', 'OralCavity_inPTV54_07'] # ROIs 
        oral_cavity_coefs = [_oralcavityB, _oralcavityLow, _oralcavityUp] # Coeffcients
        oral_cavity_predictions = [] # Empty list for ROI

        _pcmsupB = [6.442, 0.643, 0.468] 
        _pcmsupLow = [5.243, 0.624, 0.438] 
        _pcmsupUp = [7.640, 0.661, 0.497]        
        pcmsup_rois = ['PCM_Sup','PCMSup_inPTV70_05','PCMSup_inPTV54_05']
        pcmsup_coefs = [_pcmsupB, _pcmsupLow, _pcmsupUp]
        pcmsup_predictions = []

        _pcmmedB = [9.890, 0.597, 0.393] 
        _pcmmedLow = [8.183, 0.573, 0.622] 
        _pcmmedUp = [11.597, 0.622, 0.430]        
        pcmmed_rois = ['PCM_Med','PCMMed_inPTV70_05','PCMMed_inPTV54_05']
        pcmmed_coefs = [_pcmmedB, _pcmmedLow, _pcmmedUp]
        pcmmed_predictions = []

        _pcminfB = [3.952, 0.641, 0.373] 
        _pcminfLow = [1.989, 0.619, 0.321] 
        _pcminfUp = [5.916, 0.663, 0.425]        
        pcminf_rois = ['PCM_Inf','PCMInf_inPTV70_07','PCMInf_inPTV54_07']
        pcminf_coefs = [_pcminfB, _pcminfLow, _pcminfUp]
        pcminf_predictions = []

        _parotidlB = [1.121, 0.606, 0.513] 
        _parotidlLow = [0.196, 0.582, 0.465] 
        _parotidlUp = [2.045, 0.630, 0.560]        
        parotidl_rois = ['Parotid_L','ParotidL_inPTV70_07','ParotidL_inPTV54_07']
        parotidl_coefs = [_parotidlB, _parotidlLow, _parotidlUp]
        parotidl_predictions = []

        _parotidrB = [3.063, 0.639, 0.602] 
        _parotidrLow = [2.206, 0.613, 0.544] 
        _parotidrUp = [3.919, 0.665, 0.661]        
        parotidr_rois = ['Parotid_R','ParotidR_inPTV70_05','ParotidR_inPTV54_05']
        parotidr_coefs = [_parotidrB, _parotidrLow, _parotidrUp]
        parotidr_predictions = []

        _submandibularlB = [10.117, 0.571, 0.450] 
        _submandibularlLow = [8.291, 0.547, 0.416] 
        _submandibularlUp = [11.943, 0.596, 0.483]        
        submandibularl_rois = ['Submandibular_L','SubmandibularL_inPTV70_05','SubmandibularL_inPTV54_05']
        submandibularl_coefs = [_submandibularlB, _submandibularlLow, _submandibularlUp]
        submandibularl_predictions = []

        _submandibularrB = [8.808, 0.585, 0.465] 
        _submandibularrLow = [7.237, 0.565, 0.434] 
        _submandibularrUp = [10.379, 0.605, 0.496]        
        submandibularr_rois = ['Submandibular_R','SubmandibularR_inPTV70_05','SubmandibularR_inPTV54_05']
        submandibularr_coefs = [_submandibularrB, _submandibularrLow, _submandibularrUp]
        submandibularr_predictions = []
        
        roi_volumes = []
        for i  in ROI_NAMES:                       
            if i == 'OralCavity_Ext': # ROI aangeven
                for j in range (len(oral_cavity_rois)):
                    try: 
                        roi_volume = plan.TreatmentCourse.TotalDose.GetDoseGridRoi(RoiName=oral_cavity_rois[j]).RoiVolumeDistribution.TotalVolume 
                    except: 
                        roi_volume = 0
                    roi_volumes.append(roi_volume)
                coefs = oral_cavity_coefs # ROI aangeven
                for k in range(len(coefs)):
                    try:
                        dose_pred = round((coefs[k][0] + coefs[k][1] * roi_volumes[1]/roi_volumes[0]*100 + \
                                              coefs[k][2] * (roi_volumes[2]-roi_volumes[1])/ roi_volumes[0]*100) *100) 
                    except:
                        dose_pred = 0
                    oral_cavity_predictions.append(dose_pred)
                roi_volumes = []
            elif i == 'PCM_Sup': 
                for j in range (len(pcmsup_rois)):
                    try:
                        roi_volume = plan.TreatmentCourse.TotalDose.GetDoseGridRoi(RoiName=pcmsup_rois[j]).RoiVolumeDistribution.TotalVolume
                    except: 
                        roi_volume = 0                   
                    roi_volumes.append(roi_volume)
                coefs = pcmsup_coefs 
                for k in range(len(coefs)):
                    try:
                        dose_pred = round((coefs[k][0] + coefs[k][1] * roi_volumes[1]/roi_volumes[0]*100 + \
                                          coefs[k][2] * (roi_volumes[2]-roi_volumes[1])/ roi_volumes[0]*100) *100) 
                    except:
                        dose_pred = 0
                    pcmsup_predictions.append(dose_pred) 
                roi_volumes = []
            elif i == 'PCM_Med': 
                for j in range (len(pcmmed_rois)):
                    try: 
                        roi_volume = plan.TreatmentCourse.TotalDose.GetDoseGridRoi(RoiName=pcmmed_rois[j]).RoiVolumeDistribution.TotalVolume
                    except: 
                        roi_volume = 0
                    roi_volumes.append(roi_volume)
                coefs = pcmmed_coefs 
                for k in range(len(coefs)):
                    try:
                        dose_pred = round((coefs[k][0] + coefs[k][1] * roi_volumes[1]/roi_volumes[0]*100 + \
                                          coefs[k][2] * (roi_volumes[2]-roi_volumes[1])/ roi_volumes[0]*100) *100) 
                    except:
                        dose_pred = 0
                    pcmmed_predictions.append(dose_pred)
                roi_volumes = []
            elif i == 'PCM_Inf': 
                for j in range (len(pcminf_rois)):
                    try: 
                        roi_volume = plan.TreatmentCourse.TotalDose.GetDoseGridRoi(RoiName=pcminf_rois[j]).RoiVolumeDistribution.TotalVolume 
                    except: 
                        roi_volume = 0                    
                    roi_volumes.append(roi_volume)
                coefs = pcminf_coefs 
                for k in range(len(coefs)):
                    try:
                        dose_pred = round((coefs[k][0] + coefs[k][1] * roi_volumes[1]/roi_volumes[0]*100 + \
                                          coefs[k][2] * (roi_volumes[2]-roi_volumes[1])/ roi_volumes[0]*100) *100) 
                    except:
                        dose_pred = 0                    
                    pcminf_predictions.append(dose_pred)  
                roi_volumes = []
            elif i == 'Parotid_L': 
                for j in range (len(parotidl_rois)):
                    try: 
                        roi_volume = plan.TreatmentCourse.TotalDose.GetDoseGridRoi(RoiName=parotidl_rois[j]).RoiVolumeDistribution.TotalVolume 
                    except: 
                        roi_volume = 0
                        print ('ROI is leeg')
                    roi_volumes.append(roi_volume)
                coefs = parotidl_coefs 
                for k in range(len(coefs)):
                    try:
                        dose_pred = round((coefs[k][0] + coefs[k][1] * roi_volumes[1]/roi_volumes[0]*100 + \
                                          coefs[k][2] * (roi_volumes[2]-roi_volumes[1])/ roi_volumes[0]*100) *100) 
                    except:
                        dose_pred = 0
                    parotidl_predictions.append(dose_pred) 
                roi_volumes = []
            elif i == 'Parotid_R': 
                for j in range (len(parotidr_rois)):
                    try:
                        roi_volume = plan.TreatmentCourse.TotalDose.GetDoseGridRoi(RoiName=parotidr_rois[j]).RoiVolumeDistribution.TotalVolume 
                    except: 
                        roi_volume = 0                    
                    roi_volumes.append(roi_volume)
                coefs = parotidr_coefs 
                for k in range(len(coefs)):
                    try:
                        dose_pred = round((coefs[k][0] + coefs[k][1] * roi_volumes[1]/roi_volumes[0]*100 + \
                                          coefs[k][2] * (roi_volumes[2]-roi_volumes[1])/ roi_volumes[0]*100) *100) 
                    except:
                        dose_pred = 0
                    parotidr_predictions.append(dose_pred)
                roi_volumes = []
            elif i == 'Submandibular_L': 
                for j in range (len(submandibularl_rois)):
                    try: 
                        roi_volume = plan.TreatmentCourse.TotalDose.GetDoseGridRoi(RoiName=submandibularl_rois[j]).RoiVolumeDistribution.TotalVolume
                    except: 
                        roi_volume = 0
                    roi_volumes.append(roi_volume)
                coefs = submandibularl_coefs 
                for k in range(len(coefs)):
                    try:
                        dose_pred = round((coefs[k][0] + coefs[k][1] * roi_volumes[1]/roi_volumes[0]*100 + \
                                          coefs[k][2] * (roi_volumes[2]-roi_volumes[1])/ roi_volumes[0]*100) *100) 
                    except:
                        dose_pred = 0                   
                    submandibularl_predictions.append(dose_pred)  
                roi_volumes = []
            elif i == 'Submandibular_R': # ROI aangeven
                for j in range (len(submandibularr_rois)):
                    try:
                        roi_volume = plan.TreatmentCourse.TotalDose.GetDoseGridRoi(RoiName=submandibularr_rois[j]).RoiVolumeDistribution.TotalVolume
                    except: 
                        roi_volume = 0                    
                    roi_volumes.append(roi_volume)
                coefs = submandibularr_coefs 
                for k in range(len(coefs)):
                    try:
                        dose_pred = round((coefs[k][0] + coefs[k][1] * roi_volumes[1]/roi_volumes[0]*100 + \
                                          coefs[k][2] * (roi_volumes[2]-roi_volumes[1])/ roi_volumes[0]*100) *100) 
                    except:
                        dose_pred = 0
                    submandibularr_predictions.append(dose_pred)  
                roi_volumes = []
        return oral_cavity_predictions, pcmsup_predictions, pcmmed_predictions, pcminf_predictions, parotidl_predictions, parotidr_predictions, submandibularl_predictions, submandibularr_predictions

'''This fucntion calculates grade 2 and grade 3 dysphagia based on the DSS and an earlier script made by Ilse van Bruggen'''
def calculate_ntcp_dys(plan, tumorlocation, dysfagie):
        """
        Calculates dysphagia
        """   
        baseline_dysphagia2 = 0
        baseline_dysphagia3 = 0
        tumorlocation2 = 0
        tumorlocation3 = 0
        if tumorlocation == 'Pharynx':
            tumorlocation2 = -0.6281
            tumorlocation3 = 0.0387
        elif tumorlocation == 'Larynx and others':
            tumorlocation2 = -0.7711
            tumorlocation3 = -0.5303
        else:
            pass
        
        if dysfagie == 'Grade 2':
            baseline_dysphagia2 = 0.9382
            baseline_dysphagia3 = 0.5738
        elif dysfagie == 'Grade 3-4':
            baseline_dysphagia2 = 1.2900
            baseline_dysphagia3 = 1.4718
        else:
            pass

        
        _dysphagia2 = {'constant': -4.0536,
              'Davg oral cavity': 0.0300/100,
              'Davg PCM superior': 0.0236/100,
              'Davg PCM medius': 0.0095/100,
              'Davg PCM inferior': 0.0133/100}

        _dysphagia3 = {'constant': -7.6174,
              'Davg oral cavity': 0.0259/100,
              'Davg PCM superior': 0.0203/100,
              'Davg PCM medius': 0.0303/100,
              'Davg PCM inferior': 0.0341/100}
              
        all_rois = case.PatientModel.RegionsOfInterest
        roi_names = [x.Name for x in all_rois]
        
        '''If one of the following structures is not present the dose value "nan" will be assigned. That way the calculation will continue without flagging an error and simply presenting the final answer as "nan" '''
        if "OralCavity_Ext" not in roi_names or "PCM_Sup" not in roi_names or "PCM_Med" not in roi_names or "PCM_Inf" not in roi_names:
            oral_cav_avg_dose = float('nan')
            pcm_sup_avg_dose = float('nan')
            pcm_med_avg_dose = float('nan')
            pcm_inf_avg_dose = float('nan')
        else:
            oral_cav_avg_dose = plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName="OralCavity_Ext", DoseType="Average")    
            pcm_sup_avg_dose = plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName="PCM_Sup", DoseType="Average")
            pcm_med_avg_dose = plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName="PCM_Med", DoseType="Average")
            pcm_inf_avg_dose = plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName="PCM_Inf", DoseType="Average")  

        # Calculate risk of dysphagia        
        lp2 = _dysphagia2['constant'] + \
             _dysphagia2['Davg oral cavity'] * oral_cav_avg_dose + \
             _dysphagia2['Davg PCM superior'] * pcm_sup_avg_dose + \
             _dysphagia2['Davg PCM medius'] * pcm_med_avg_dose + \
             _dysphagia2['Davg PCM inferior'] * pcm_inf_avg_dose + \
             baseline_dysphagia2 + \
             tumorlocation2

        grade_2 = (1 / (1 + 2.718281828459045**(-lp2)))*100
    
        lp3 = _dysphagia3['constant'] + \
             _dysphagia3['Davg oral cavity'] * oral_cav_avg_dose + \
             _dysphagia3['Davg PCM superior'] * pcm_sup_avg_dose + \
             _dysphagia3['Davg PCM medius'] * pcm_med_avg_dose + \
             _dysphagia3['Davg PCM inferior'] * pcm_inf_avg_dose + \
             baseline_dysphagia3 + \
             tumorlocation3 
        
        grade_3 = (1 / (1 + 2.718281828459045**(-lp3)))*100
                               
        return grade_2, grade_3


'''This function will return grade 2 and 3 xerostomia based on the DSS and an earlier script made by Ilse van Bruggen'''
def calculate_ntcp_xero(case, plan, xerostomie):
        """
        Calculates xerostomia
        """              
        baseline_xerostomia2 = 0
        baseline_xerostomia3 = 0
        if xerostomie == 'A little':
            baseline_xerostomia2 = 0.4950
            baseline_xerostomia3 = 0.4249
        elif xerostomie == 'Quite bad':
            baseline_xerostomia2 = 1.2070
            baseline_xerostomia3 = 1.0361
        
        _xerostomia2 = {'constant': -2.2951,
               'Davg parotid left': 0.0996,
               'Davg parotid right': 0.0996,
               'Davg submandibular left': 0.0182/100,
               'Davg submandibular right': 0.0182/100}

        _xerostomia3 = {'constant': -3.7286,
               'Davg parotid left': 0.0855,
               'Davg parotid right': 0.0855,
               'Davg submandibular left': 0.0156/100,
               'Davg submandibular right': 0.0156/100}

        all_rois = case.PatientModel.RegionsOfInterest
        roi_names = [x.Name for x in all_rois]
        

        '''If one of the following structures is not present the dose value "nan" will be assigned. That way the calculation will continue without flagging an error and simply presenting the final answer as "nan". 
        If only one of the submandibular glands is missing the calculation can continue by using the dose on the other submandibular gland, if both are missing "nan" will be assigned.'''
        if "Parotid_L" not in roi_names or "Parotid_R" not in roi_names:
            parotid_left_avg_dose = float('nan')
            parotid_right_avg_dose = float('nan')
        else:    
            parotid_left_avg_dose = plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName="Parotid_L", DoseType="Average")
            parotid_right_avg_dose = plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName="Parotid_R", DoseType="Average")

        if 'Submandibular_L' not in roi_names and 'Submandibular_R' not in roi_names:  
            submandibular_avg_dose = float('nan')
        elif 'Submandibular_L' not in roi_names:
            submandibular_avg_dose = plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName="Submandibular_R", DoseType="Average")
        elif 'Submandibular_R' not in roi_names:
            submandibular_avg_dose = plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName="Submandibular_L", DoseType="Average")
        else:    
            submandibular_left_avg_dose = plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName="Submandibular_L", DoseType="Average")
            submandibular_right_avg_dose = plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName="Submandibular_R", DoseType="Average")  
            submandibular_left_volume = plan.TreatmentCourse.TotalDose.GetDoseGridRoi(RoiName="Submandibular_L").RoiVolumeDistribution.TotalVolume
            submandibular_right_volume = plan.TreatmentCourse.TotalDose.GetDoseGridRoi(RoiName="Submandibular_R").RoiVolumeDistribution.TotalVolume
            submandibular_avg_dose = (submandibular_left_avg_dose*submandibular_left_volume + submandibular_right_avg_dose*submandibular_right_volume)/(submandibular_left_volume + submandibular_right_volume)    
       
        # Calculate risk of xerostomia    
        lp2 = _xerostomia2['constant'] + \
            _xerostomia2['Davg parotid left'] * (parotid_left_avg_dose/100)**0.5 + \
            _xerostomia2['Davg parotid right'] * (parotid_right_avg_dose/100)**0.5 + \
            _xerostomia2['Davg submandibular left'] * submandibular_avg_dose + \
            baseline_xerostomia2
        
        lp3 = _xerostomia3['constant'] + \
            _xerostomia3['Davg parotid left'] * (parotid_left_avg_dose/100)**0.5 + \
            _xerostomia3['Davg parotid right'] * (parotid_right_avg_dose/100)**0.5 + \
            _xerostomia3['Davg submandibular left'] * submandibular_avg_dose + \
            baseline_xerostomia3

        grade_2 = 1 / (1 + 2.718281828459045**(-lp2))*100  
        grade_3 = 1 / (1 + 2.718281828459045**(-lp3))*100          
        
        return grade_2, grade_3 
      

'''This function calculates the difference between the dysphagia and xerostomia between a photon plan and a proton plan.'''        
def delta_NTCP(grade_2_dysphagia_proton, grade_3_dysphagia_proton, grade_2_dysphagia_photon, grade_3_dysphagia_photon, grade_2_xerostomia_proton, grade_3_xerostomia_proton, grade_2_xerostomia_photon, grade_3_xerostomia_photon):
    
    delta_grade_2_dysphagia = grade_2_dysphagia_photon - grade_2_dysphagia_proton
    delta_grade_3_dysphagia = grade_3_dysphagia_photon - grade_3_dysphagia_proton
    delta_grade_2_xerostomia = grade_2_xerostomia_photon - grade_2_xerostomia_proton
    delta_grade_3_xerostomia = grade_3_xerostomia_photon - grade_3_xerostomia_proton
    sum_NTCP_grade_2 = round(delta_grade_2_dysphagia + delta_grade_2_xerostomia, 1)
    sum_NTCP_grade_3 = round(delta_grade_3_dysphagia + delta_grade_3_xerostomia, 1)
    delta_grade_2_dysphagia = round(delta_grade_2_dysphagia, 1)  #rounding after the sum to avoid rounding errors
    delta_grade_3_dysphagia = round(delta_grade_3_dysphagia, 1)
    delta_grade_2_xerostomia = round(delta_grade_2_xerostomia, 1)
    delta_grade_3_xerostomia = round(delta_grade_3_xerostomia, 1)

    return delta_grade_2_dysphagia, delta_grade_2_xerostomia, delta_grade_3_dysphagia, delta_grade_3_xerostomia, sum_NTCP_grade_2, sum_NTCP_grade_3
        

'''This function returns if the plans have passed evaluation functions (true/false) and returns the actual value of the clinical goal.
This is done nominaly and for the voxelwise worst plans.'''
def clinical_goal_evaluations(plan, new_plan_min, new_plan_max):
        x = len(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
        clinical_goal_passed = []
        clinical_goal_ROI = []
        clinical_goal_value = []
        clinical_goal_nom_passed = []
        clinical_goal_nom = []
        evaluation_functions = plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions
        evaluation_functions_min = new_plan_min.TreatmentCourse.EvaluationSetup.EvaluationFunctions
        evaluation_functions_max = new_plan_max.TreatmentCourse.EvaluationSetup.EvaluationFunctions
        for i in range(x):
                clinical_goal_ROI.append(evaluation_functions[i].ForRegionOfInterest.Name)
                clinical_goal_nom_passed.append(evaluation_functions[i].EvaluateClinicalGoal())
                clinical_goal_nom.append(evaluation_functions[i].GetClinicalGoalValue())
                if evaluation_functions[i].PlanningGoal.GoalCriteria == 'AtLeast':                  #for the voxelwise worst plans a distinction between the "At least" and "At most" goals is important. The "at least" goals should be evaluated over the voxelwise minimum plan
                    clinical_goal_passed.append(evaluation_functions_min[i].EvaluateClinicalGoal())
                    clinical_goal_value.append(evaluation_functions_min[i].GetClinicalGoalValue()) 
                else:
                    clinical_goal_passed.append(evaluation_functions_max[i].EvaluateClinicalGoal())
                    clinical_goal_value.append(evaluation_functions_max[i].GetClinicalGoalValue())
        max_width_clinical_goal_ROI = max(len(x) for x in clinical_goal_ROI)
        return clinical_goal_passed, clinical_goal_ROI, clinical_goal_value, clinical_goal_nom_passed, clinical_goal_nom, max_width_clinical_goal_ROI, 


'''This function adds the right units to the clinical goal values from the previous function and also returns the complete clinical goal'''
def clinical_goal_evaluations_to_string(plan, clinical_goal_value):
        x = len(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
        evaluation_functions = plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions
        clinical_goal = []
        clinical_goal_value_string = []
        for i in range(x):
            if evaluation_functions[i].PlanningGoal.Type == 'DoseAtAbsoluteVolume':
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' ' + str(round(evaluation_functions[i].PlanningGoal.AcceptanceLevel)) + ' cGy (RBE) dose at ' + str(round(evaluation_functions[i].PlanningGoal.ParameterValue)) + ' cm\u00b3 volume')
                clinical_goal_value_string.append(str(round(clinical_goal_value[i])) + ' cGy (RBE)')
            elif evaluation_functions[i].PlanningGoal.Type == 'DoseAtVolume':
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' ' + str(round(evaluation_functions[i].PlanningGoal.AcceptanceLevel)) + ' cGy (RBE) dose at ' + str(evaluation_functions[i].PlanningGoal.ParameterValue*100) + ' % volume')
                clinical_goal_value_string.append(str(round(clinical_goal_value[i])) + ' cGy (RBE)')
            elif evaluation_functions[i].PlanningGoal.Type == 'AverageDose':
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' ' + str(round(evaluation_functions[i].PlanningGoal.AcceptanceLevel)) + ' cGy (RBE) average dose')
                clinical_goal_value_string.append(str(round(clinical_goal_value[i])) + ' cGy (RBE)')
            elif evaluation_functions[i].PlanningGoal.Type == 'VolumeAtDose':    
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' ' + str(evaluation_functions[i].PlanningGoal.AcceptanceLevel*100) + ' % volume at ' + str(round(evaluation_functions[i].PlanningGoal.ParameterValue)) + ' cGy (RBE) dose')
                clinical_goal_value_string.append(str(round(clinical_goal_value[i]*100, 4)) + ' %')
            elif evaluation_functions[i].PlanningGoal.Type == 'AbsoluteVolumeAtDose':    
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' ' + str(round(evaluation_functions[i].PlanningGoal.AcceptanceLevel)) + ' cm\u00b3 volume at ' + str(round(evaluation_functions[i].PlanningGoal.ParameterValue)) + ' cGy (RBE) dose')
                clinical_goal_value_string.append(str(round(clinical_goal_value[i], 4)) + ' cm\u00b3 ')
            elif evaluation_functions[i].PlanningGoal.Type == 'ConformityIndex':    
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' a conformity index of ' + str(evaluation_functions[i].PlanningGoal.AcceptanceLevel) + ' at ' + str(round(evaluation_functions[i].PlanningGoal.ParameterValue)) + ' cGy (RBE) isodose')    
                clinical_goal_value_string.append('N/A')  #Because a homogeneity index cannot be calculated robustly
            elif evaluation_functions[i].PlanningGoal.Type == 'HomogeneityIndex':    
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' a homogeneity index of ' + str(evaluation_functions[i].PlanningGoal.AcceptanceLevel) + ' at ' + str(evaluation_functions[i].PlanningGoal.ParameterValue*100) + ' % volume')
                clinical_goal_value_string.append('N/A')  #Because a conformity index cannot be calculated robustly
            else:
                clinical_goal.append('unknown clinical goal')
                clinical_goal_value_string.append('N/A') 
            
        return clinical_goal, clinical_goal_value_string

'''This function is almost the same as the previous one except for the CI and HI indeces, because nominaly they can be calculated.'''
def clinical_goal_evaluations_to_string_nominal(plan, clinical_goal_value):
        x = len(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
        evaluation_functions = plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions
        clinical_goal = []
        clinical_goal_value_string = []
        for i in range(x):
            if evaluation_functions[i].PlanningGoal.Type == 'DoseAtAbsoluteVolume':
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' ' + str(round(evaluation_functions[i].PlanningGoal.AcceptanceLevel)) + ' cGy (RBE) dose at ' + str(evaluation_functions[i].PlanningGoal.ParameterValue) + ' cm\u00b3 volume')
                clinical_goal_value_string.append(str(round(clinical_goal_value[i])) + ' cGy (RBE)')
            elif evaluation_functions[i].PlanningGoal.Type == 'DoseAtVolume':
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' ' + str(round(evaluation_functions[i].PlanningGoal.AcceptanceLevel)) + ' cGy (RBE) dose at ' + str(evaluation_functions[i].PlanningGoal.ParameterValue*100) + ' % volume')
                clinical_goal_value_string.append(str(round(clinical_goal_value[i])) + ' cGy (RBE)')
            elif evaluation_functions[i].PlanningGoal.Type == 'AverageDose':
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' ' + str(round(evaluation_functions[i].PlanningGoal.AcceptanceLevel)) + ' cGy (RBE) average dose')
                clinical_goal_value_string.append(str(round(clinical_goal_value[i])) + ' cGy (RBE)')
            elif evaluation_functions[i].PlanningGoal.Type == 'VolumeAtDose':    
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' ' + str(round(evaluation_functions[i].PlanningGoal.AcceptanceLevel*100)) + ' % volume at ' + str(round(evaluation_functions[i].PlanningGoal.ParameterValue)) + ' cGy (RBE) dose')
                clinical_goal_value_string.append(str(round(clinical_goal_value[i]*100, 4)) + ' %')
            elif evaluation_functions[i].PlanningGoal.Type == 'AbsoluteVolumeAtDose':    
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' ' + str(round(evaluation_functions[i].PlanningGoal.AcceptanceLevel)) + ' cm\u00b3 volume at ' + str(round(evaluation_functions[i].PlanningGoal.ParameterValue)) + ' cGy (RBE) dose')
                clinical_goal_value_string.append(str(round(clinical_goal_value[i], 4)) + ' cm\u00b3 ')
            elif evaluation_functions[i].PlanningGoal.Type == 'ConformityIndex':    
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' a conformity index of ' + str(evaluation_functions[i].PlanningGoal.AcceptanceLevel) + ' at ' + str(round(evaluation_functions[i].PlanningGoal.ParameterValue)) + ' cGy (RBE) isodose')    
                clinical_goal_value_string.append(str(round(clinical_goal_value[i], 4)))
            elif evaluation_functions[i].PlanningGoal.Type == 'HomogeneityIndex':    
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' a homogeneity index of ' + str(evaluation_functions[i].PlanningGoal.AcceptanceLevel) + ' at ' + str(evaluation_functions[i].PlanningGoal.ParameterValue*100) + ' % volume')
                clinical_goal_value_string.append(str(round(clinical_goal_value[i], 4)))
            else:
                clinical_goal.append('unknown clinical goal')
                clinical_goal_value_string.append('N/A') 
            
        return clinical_goal, clinical_goal_value_string


'''I think this function has become obsolete (the previous functions should do I think), but I will not test it because of time constraints.
It can not be simply be removed because it is called in the "new_window" script.'''
def clinical_goal_evaluations_photon(plan):
        x = len(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
        evaluation_functions = plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions
        clinical_goal_ROI = []
        clinical_goal = []
        clinical_goal_value = []
        clinical_goal_nominal = []
        clinical_goal_passed = []
        for i in range(x):
            clinical_goal_ROI.append(evaluation_functions[i].ForRegionOfInterest.Name)
            clinical_goal_passed.append(evaluation_functions[i].EvaluateClinicalGoal())
            if evaluation_functions[i].PlanningGoal.Type == 'DoseAtAbsoluteVolume':
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' ' + str(evaluation_functions[i].PlanningGoal.AcceptanceLevel) + ' cGy (RBE) dose at ' + str(evaluation_functions[i].PlanningGoal.ParameterValue) + ' cm\u00b3 volume')    
                clinical_goal_value.append(round(evaluation_functions[i].GetClinicalGoalValue()))
                clinical_goal_nominal.append(str(clinical_goal_value[i]) + ' cGy (RBE)')
            elif evaluation_functions[i].PlanningGoal.Type == 'DoseAtVolume':
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' ' + str(evaluation_functions[i].PlanningGoal.AcceptanceLevel) + ' cGy (RBE) dose at ' + str(evaluation_functions[i].PlanningGoal.ParameterValue*100) + ' % volume')
                clinical_goal_value.append(round(evaluation_functions[i].GetClinicalGoalValue()))
                clinical_goal_nominal.append(str(clinical_goal_value[i]) + ' cGy (RBE)')
            elif evaluation_functions[i].PlanningGoal.Type == 'AverageDose':
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' ' + str(evaluation_functions[i].PlanningGoal.AcceptanceLevel) + ' cGy (RBE) average dose')     
                clinical_goal_value.append(round(evaluation_functions[i].GetClinicalGoalValue()))
                clinical_goal_nominal.append(str(clinical_goal_value[i]) + ' cGy (RBE)')
            elif evaluation_functions[i].PlanningGoal.Type == 'VolumeAtDose':    
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' ' + str(evaluation_functions[i].PlanningGoal.AcceptanceLevel*100) + ' % volume at ' + str(evaluation_functions[i].PlanningGoal.ParameterValue) + ' cGy (RBE) dose')               
                clinical_goal_value.append(round(evaluation_functions[i].GetClinicalGoalValue(), 4))
                clinical_goal_nominal.append(str(clinical_goal_value[i]*100) + ' %')
            elif evaluation_functions[i].PlanningGoal.Type == 'AbsoluteVolumeAtDose':    
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' ' + str(evaluation_functions[i].PlanningGoal.AcceptanceLevel) + ' cm\u00b3 volume at ' + str(evaluation_functions[i].PlanningGoal.ParameterValue) + ' cGy (RBE) dose')               
                clinical_goal_value.append(round(evaluation_functions[i].GetClinicalGoalValue(), 4))
                clinical_goal_nominal.append(str(clinical_goal_value[i]) + ' cm\u00b3')
            elif evaluation_functions[i].PlanningGoal.Type == 'ConformityIndex':    
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' a conformity index of ' + str(evaluation_functions[i].PlanningGoal.AcceptanceLevel) + ' at ' + str(evaluation_functions[i].PlanningGoal.ParameterValue) + ' cGy (RBE) isodose')                    
                clinical_goal_value.append(round(evaluation_functions[i].GetClinicalGoalValue(), 4))
                clinical_goal_nominal.append(str(clinical_goal_value[i]))
            elif evaluation_functions[i].PlanningGoal.Type == 'HomogeneityIndex':    
                clinical_goal.append(evaluation_functions[i].PlanningGoal.GoalCriteria + ' a homogeneity index of ' + str(evaluation_functions[i].PlanningGoal.AcceptanceLevel) + ' at ' + str(evaluation_functions[i].PlanningGoal.ParameterValue*100) + ' % volume')               
                clinical_goal_value.append(round(evaluation_functions[i].GetClinicalGoalValue(), 4))
                clinical_goal_nominal.append(str(clinical_goal_value[i]))
            else:
                clinical_goal.append('unknown clinical goal')
                clinical_goal_value.append(float('nan'))
                clinical_goal_nominal.append('N/A')
        
        max_width_clinical_goal_ROI = max(len(x) for x in clinical_goal_ROI)
        max_width_clinical_goal = max(len(x) for x in clinical_goal)
        return clinical_goal_passed, clinical_goal_ROI, clinical_goal, clinical_goal_value, clinical_goal_nominal, max_width_clinical_goal_ROI, max_width_clinical_goal

'''Define path'''
# dashboard_storage_path = Path('\\\\zkh\\appdata\\Raystation\\Research\\ML\\Erik and Roel\\erik\\scripts\\dashboard_Hielke\\dashboard-storage\\')
# dashboard_storage_path = Path('\\\\zkh\\appdata\\Raystation\\Research\\ML\\Erik and Roel\\erik\\scripts\\dashboard_Hielke\\dashboard-storage\\')
user_name = os.getlogin()
user_name.replace(" ","_")
dashboard_storage_path = Path('\\\\zkh\\appdata\\Raystation\\Research\\ML\\Dashboard\\dashboard-storage\\' ) / user_name
print(dashboard_storage_path)
dashboard_storage_path.mkdir(mode=0o777, parents=True, exist_ok=True)
baseline_storage_path = Path('\\\\zkh\\appdata\\Raystation\\Research\\ML\\\Dashboard\\baseline-storage\\')
script_path = Path().absolute()

print(dashboard_storage_path)
print(baseline_storage_path)
print(script_path)


'''Open the other script that works in conjunction with this one'''
#exec(open("\\\\zkh\\appdata\\Raystation\\Research\\ML\\Hielke\\scripts\\new_window.py").read())
# exec(open("\\\\zkh\\appdata\\Raystation\\Research\\ML\\Erik and Roel\\erik\\scripts\\dashboard_Hielke\\ver_2.0\\new_window.py").read())
exec(open(script_path / 'new_window_Ilse.py').read())

'''Make the tkinter window with different option-menus'''
master = Tk()

Tumorlocation = ['Pharynx', 'Oral cavity', 'Larynx and others'] #all the baseline complication options
Baseline_xerostomie = ['Not at all', 'A little', 'Quite bad']
Baseline_dysfagie = ['Grade 0-1', 'Grade 2', 'Grade 3-4']

variable = StringVar(master) #setting the variables for the optionmenus
variable1 = StringVar(master)
variable2 = StringVar(master)
variable3 = StringVar(master)
variable4 = StringVar(master)
variable5 = StringVar(master)

baseline_storage_file = str(baseline_storage_path / patient.PatientID) + '.pickle'

try: #if the baseline values are already stored open them and set them as the basevalues, else set them to the standard settings
    with open( baseline_storage_file, 'rb') as handle:
        print('Read patient baseline from : ' + baseline_storage_file)
        base_values = pickle.load(handle) 
except:
    print('Baseline data not found : ' + baseline_storage_file)
    base_values = ['Pharynx', 'Not at all', 'Grade 0-1']


select_plan = [x.Name for x in case.TreatmentPlans]  #all plans to choose from
select_plan_2 = ['no plan']                          #in the second option menu "no plan" will be the default option   
select_plan_2 += [x.Name for x in case.TreatmentPlans]
select_plan_NTCP_comparison = []
for x in case.TreatmentPlans:
    if x.BeamSets[0].Modality == 'Photons':         #for the NTCP comparison only a photon plan can be chosen
        select_plan_NTCP_comparison.append(x.Name)

'''Labels to indicate what you are actualy choosing'''  
Label(master, text = "select a plan").grid(row = 1, column = 1)
Label(master, text = "select another plan").grid(row = 2, column = 1)
Label(master, text = '').grid(row = 3, column = 1)
Label(master, text = "select a tumour site").grid(row = 4, column = 1)
Label(master, text = "select the baseline xerostomia").grid(row = 5, column = 1)
Label(master, text = "select the baseline dysfagia").grid(row = 6, column = 1)
Label(master, text = '').grid(row = 7, column = 1)
Label(master, text = "select a photon plan NTCP for NTCP comparison").grid(row = 8, column = 1)

'''This function defines which dashboard should be created based on the modalities of the plans that are chosen.'''
def different_dashboards(var, index, mode):
    if case.TreatmentPlans[variable.get()].BeamSets[0].Modality == 'Protons' and variable1.get() == "no plan":   
        button = Button(master, text = "ok", command = create_new_window_proton).grid(row = 9, column = 1)
    elif case.TreatmentPlans[variable.get()].BeamSets[0].Modality == 'Photons' and variable1.get() == 'no plan':
        button = Button(master, text = "ok", command = create_new_window_photon).grid(row = 9, column = 1)
    elif case.TreatmentPlans[variable.get()].BeamSets[0].Modality == 'Protons' and case.TreatmentPlans[variable1.get()].BeamSets[0].Modality == 'Protons':
        button = Button(master, text = 'ok', command = create_new_window_proton_proton).grid(row = 9, column = 1) 
    elif case.TreatmentPlans[variable.get()].BeamSets[0].Modality == 'Photons' and case.TreatmentPlans[variable1.get()].BeamSets[0].Modality == 'Photons':
        button = Button(master, text = 'ok', command = create_new_window_photon_photon).grid(row = 9, column = 1)    
    else:
        button = Button(master, text = 'ok', command = create_new_window_proton_photon).grid(row = 9, column = 1)

'''putting the trace before the optionmenu gives rise to some error in the execution details, but does not interfere with the functioning of the code,
whereas putting them behind the optionmenus causes the "Ok" button only to appear after a change in a menu was made.'''       
variable.trace('w', different_dashboards)   
variable1.trace('w', different_dashboards)

global plan_name
global photon_ref_plan_name
all_data = []
plan_info = []

try:
    print('In optionmenu, the plan_name is : ' + plan_name)
    without_gui = True
except:
    without_gui = False
    plan_name = select_plan[0]
    photon_ref_plan_name = 'A1FHH'

variable.set(plan_name)
variable2.set(base_values[0]) #retrieve the base complication values that were chosen
variable3.set(base_values[1])
variable4.set(base_values[2])
variable5.set(photon_ref_plan_name)
print('Plan name in optionmenu ' + variable.get())

if without_gui:
    if case.TreatmentPlans[plan_name].BeamSets[0].Modality == 'Photons':
        print('create_new_window_photon()')
        create_new_window_photon()
    else:
        create_new_window_proton()
    
else:
    OptionMenu(master, variable, variable.get(), *select_plan).grid(row = 1, column = 2)
    OptionMenu(master, variable1, select_plan_2[0], *select_plan_2).grid(row = 2, column = 2)
    OptionMenu(master, variable2, base_values[0], *Tumorlocation).grid(row = 4, column = 2)
    OptionMenu(master, variable3, base_values[1], *Baseline_xerostomie).grid(row = 5, column = 2)
    OptionMenu(master, variable4, base_values[2], *Baseline_dysfagie).grid(row = 6, column = 2)
    OptionMenu(master, variable5, variable5.get(), *select_plan_NTCP_comparison).grid(row = 8, column = 2)

    mainloop()

# OptionMenu(master, variable, select_plan[0], *select_plan).grid(row = 1, column = 2)
# OptionMenu(master, variable1, select_plan_2[0], *select_plan_2).grid(row = 2, column = 2)
# OptionMenu(master, variable2, base_values[0], *Tumorlocation).grid(row = 4, column = 2)
# OptionMenu(master, variable3, base_values[1], *Baseline_xerostomie).grid(row = 5, column = 2)
# OptionMenu(master, variable4, base_values[2], *Baseline_dysfagie).grid(row = 6, column = 2)
# OptionMenu(master, variable5, 'A1FHH', *select_plan_2).grid(row = 8, column = 2)

