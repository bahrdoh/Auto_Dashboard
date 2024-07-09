import locale
from datetime import date

def float_to_string(value):
    value_as_string = locale.format_string('%.8e', value)
    return value_as_string

def store_patient_baseline(baseline): 
    print('Store patient baseline in :' + baseline_storage_file)
    with open(baseline_storage_file, 'wb') as handle:
            pickle.dump(baseline, handle, protocol=pickle.HIGHEST_PROTOCOL)

def append_dashboard_data(data, filename): 
    print('Store dashboard in :' + filename)
    try:
        with open(filename , 'a', newline = '', encoding='utf-8-sig') as file:  # utf-8-sig enables greek letters to be written to the csv
            writer = csv.writer(file, delimiter = ';')            # without the colon delimiter all data would be put in one cell in Excel   
            writer.writerows(data)   
        return
    except:
        print('Could not write dashboard to : ' + filename)

def store_dashboard_data(data, filename): 
    print('Store dashboard in :' + filename)
    try:
        with open(filename , 'w', newline = '', encoding='utf-8-sig') as file:  # utf-8-sig enables greek letters to be written to the csv
            writer = csv.writer(file, delimiter = ';')                          # without the colon delimiter all data would be put in one cell in Excel   
            writer.writerows(data)   
        return
    except:
        print('Could not write dashboard to : ' + filename)

def add_line(line):
    # print(plan_info)
    all_data.append(line)

def create_new_window_proton():
    master.withdraw()   #close the first tkinter window
    window = Toplevel(master, background = '#2c2c2c') #open the dashboard window
    
    plan_name = variable.get()  #get the name of the proton plan that was chosen
    print('Plan name in create new window proton' + plan_name)
    
    if DEBUG:
        print(locale.localeconv())
        print('Example export of one-and-a-half : ', float_to_string(3.0/2))
        # exit()
    if without_gui:
        print('No gui')

        
    plan = case.TreatmentPlans[plan_name] #get the plan associated with that plan name
    photon_plan_name = variable5.get() #get the name of the proton plan that was chosen for NTCP comparison
    photon_plan = case.TreatmentPlans[photon_plan_name]  #get the photon plan associated with that plan name
    
    nominal_plan = get_doses(plan, ROI_NAMES) #get all the nominal doses

    new_plan_min, new_plan_max = find_latest_vox_worst_plans(case, plan) #find the latest vox worst plans or make them

    clinical_goal_passed, clinical_goal_ROI, clinical_goal_value, clinical_goal_nom_passed, clinical_goal_nom, max_width_clinical_goal_ROI = clinical_goal_evaluations(plan, new_plan_min, new_plan_max) 
    clinical_goal, clinical_goal_value_string = clinical_goal_evaluations_to_string(plan, clinical_goal_value)
    unused1, clinical_goal_nominal = clinical_goal_evaluations_to_string_nominal(plan, clinical_goal_nom)
    
    max_width_clinical_goal = max(len(x) for x in clinical_goal)

    '''text labels'''

    Label(window, text = 'Nominal plan (average dose in cGy)', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'center', width = nominal_plan[2] + 16).grid(row = 1, column = 2, columnspan = 2)
    Label(window, text = 'Robust evaluation', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = max_width_clinical_goal + max_width_clinical_goal_ROI + 21, anchor = 'center').grid(row = 1, column = 5, columnspan = 4)
    Label(window, text = 'ROI/POI', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = max_width_clinical_goal_ROI + 5).grid(row = 3, column = 5)
    Label(window, text = 'Clinical goal', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = max_width_clinical_goal).grid(row = 3, column = 6)
    Label(window, text = 'Voxelwise worst', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = 16).grid(row = 3, column = 7)
    Label(window, text = 'Nominal result', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = 16).grid(row = 3, column = 8)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = 1, column = 1)       # These 'empty' labels add some empty space, otherwise everything is put right beside each other
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = 1, column = 12)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = 6, column = 4)
    
    '''clinical goals and their values'''
    
    x = len(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
    for i in range(x):
        Label(window, text = clinical_goal_ROI[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = max_width_clinical_goal_ROI + 5, border = 0.4, relief = 'solid').grid(row = i + 4, column = 5)
        Label(window, text = clinical_goal[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = max_width_clinical_goal, border = 0.4, relief = 'solid').grid(row = i + 4, column = 6)
        if clinical_goal_passed[i] == True: #give the text a green color when the goal was passed.
            Label(window, text = clinical_goal_value_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#62de87', anchor = 'w', width = 16, border = 0.4, relief = 'solid').grid(row = i + 4, column = 7)     
        else: #give the goal a red color when it was not passed.
            Label(window, text = clinical_goal_value_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#f26a52', anchor = 'w', width = 16, border = 0.4, relief = 'solid').grid(row = i + 4, column = 7)
        if clinical_goal_nom_passed[i] == True:
            Label(window, text = clinical_goal_nominal[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#62de87', anchor = 'w',  width = 16, border = 0.4, relief = 'solid').grid(row = i + 4, column = 8)
        else:
            Label(window, text = clinical_goal_nominal[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#f26a52', anchor = 'w',  width = 16, border = 0.4, relief = 'solid').grid(row = i + 4, column = 8)


    '''Dose values of ROI's'''

    y = len(nominal_plan[0]) 
    for i in range(y):
        Label(window, text = nominal_plan[0][i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = nominal_plan[2] + 4, border  = 0.4, relief = 'solid').grid(row = i + 3, column = 2)
        Label(window, text = str(nominal_plan[1][i]), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = 12, border  = 0.4, relief = 'solid').grid(row = i + 3, column = 3)
    
    '''Robust conformity index'''
    
    conformity_index_7000 = conformity_index(new_plan_min, 0.94*7000, 'CTV_7000') 
    conformity_index_5425 = conformity_index(new_plan_min, 0.94*5425, 'CTV_5425')    
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w').grid(row = 4, column = 9)
    Label(window, text = 'Conformity index CTV_7000', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 27).grid(row = 1, column = 10)    
    Label(window, text = 'Conformity index CTV_5425', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 27).grid(row = 2, column = 10)
    Label(window, text = str(conformity_index_7000), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid', width = 20).grid(row = 1, column = 11)    
    Label(window, text = str(conformity_index_5425), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid', width = 20).grid(row = 2, column = 11)

    '''NTCP'''
    
    chosen_tumorlocation = variable2.get() #retrieve the base complication values that were chosen
    chosen_xerostomie = variable3.get()
    chosen_dysfagie = variable4.get()
    print('baseline choices : ' + str([chosen_tumorlocation, chosen_xerostomie, chosen_dysfagie]))

    grade_2_dysphagia_proton, grade_3_dysphagia_proton = calculate_ntcp_dys(plan, chosen_tumorlocation, chosen_dysfagie) #calculate dyphagia, xerostomia and the difference between photon and proton plans
    grade_2_dysphagia_photon, grade_3_dysphagia_photon = calculate_ntcp_dys(photon_plan, chosen_tumorlocation, chosen_dysfagie)
    grade_2_xerostomia_proton, grade_3_xerostomia_proton = calculate_ntcp_xero(case, plan, chosen_xerostomie)
    grade_2_xerostomia_photon, grade_3_xerostomia_photon = calculate_ntcp_xero(case, photon_plan, chosen_xerostomie)
        
    delta_ntcp = delta_NTCP(grade_2_dysphagia_proton, grade_3_dysphagia_proton, grade_2_dysphagia_photon, grade_3_dysphagia_photon, grade_2_xerostomia_proton, grade_3_xerostomia_proton, grade_2_xerostomia_photon, grade_3_xerostomia_photon)   
    
    
    Label(window, text = 'NTCP', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid', width = 27).grid(row = 6, column = 10, columnspan = 4, sticky = 'ew')
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11), border  = 0.4, relief = 'solid', width = 27).grid(row = 7, column = 10)
    Label(window, text = 'Grade 2 Dysphagia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 27).grid(row = 8, column = 10)
    Label(window, text = 'Grade 2 Xerostomia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 27).grid(row = 9, column = 10)
    Label(window, text = 'Grade 3 Dysphagia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 27).grid(row = 10, column = 10)
    Label(window, text = 'Grade 3 Xerostomia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 27).grid(row = 11, column = 10)
    Label(window, text = '\u03a3 graad 2', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 27).grid(row = 12, column = 10)
    Label(window, text = '\u03a3 graad 3', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 27).grid(row = 13, column = 10)
    Label(window, text = 'NTCP ' + photon_plan_name, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 7, column = 11)
    Label(window, text = str(round(grade_2_dysphagia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 8, column = 11)
    Label(window, text = str(round(grade_2_xerostomia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 9, column = 11)
    Label(window, text = str(round(grade_3_dysphagia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 10, column = 11)
    Label(window, text = str(round(grade_3_xerostomia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 11, column = 11)
    Label(window, text = 'NTCP ' + plan_name, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 7, column = 12)
    Label(window, text = str(round(grade_2_dysphagia_proton, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 8, column = 12)
    Label(window, text = str(round(grade_2_xerostomia_proton, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 9, column = 12)
    Label(window, text = str(round(grade_3_dysphagia_proton, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 10, column = 12)
    Label(window, text = str(round(grade_3_xerostomia_proton, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 11, column = 12)
    Label(window, text = '\u0394 NTCP', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 10).grid(row = 7, column = 13)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = 6, column = 14)
    
    for i in range(len(delta_ntcp)):
        if np.isnan(delta_ntcp[i]) == True: #if the value is "nan" put in the text 'N/A'
            Label(window, text = 'N/A', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 10).grid(row = i + 8, column = 13)
        else:
            if delta_ntcp[i] >= 0: 
                Label(window, text = str(delta_ntcp[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 10).grid(row = i + 8, column = 13)
            else:
                Label(window, text = str(delta_ntcp[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border  = 0.4, relief = 'solid', width = 10).grid(row = i + 8, column = 13)
    
    ''' Volume ROIs '''
    oral_cavity_predictions, pcmsup_predictions, pcmmed_predictions, pcminf_predictions, parotidl_predictions, parotidr_predictions, submandibularl_predictions, submandibularr_predictions = calculate_oar_prediction(plan) #Ilse
    
    
    '''Storing patient baseline'''
    store_patient_baseline([chosen_tumorlocation, chosen_xerostomie, chosen_dysfagie])              
   
    '''Storing the data'''  # storing the whole dashboard might also work by using postscript but I have not looked into it.
                            # Storing the data in a pandas dataframe might also be a nice solution, but the module is not installed
    try: #the modification times do not always exist, hence the "try except"
        plan_mod_time = plan.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
    except:
        plan_mod_time = "Unknown"
    try:
        photon_plan_mod_time = photon_plan.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
    except:
        photon_plan_mod_time = "Unknown"
    
    plan_info = [patient.Name, patient.PatientID, plan_name, str(plan_mod_time), photon_plan_name, str(photon_plan_mod_time)]
    
    ntcp_labels = ['Grade 2 Dysphagia', 'Grade 2 Xerostomia', 'Grade 3 Dysphagia', 'Grade 3 Xerostomia', '\u03a3 grade 2', '\u03a3 grade 3']
    ntcp_photon = [round(grade_2_dysphagia_photon, 1), round(grade_2_xerostomia_photon, 1), round(grade_3_dysphagia_photon, 1), round(grade_3_xerostomia_photon, 1)]  # The None's are inserted to ensure that lists are the same length where needed
    ntcp_proton = [round(grade_2_dysphagia_proton, 1), round(grade_2_xerostomia_proton, 1), round(grade_3_dysphagia_proton, 1), round(grade_3_xerostomia_proton, 1)]
    
    predicted_labels = ['predicted_dmean', 'predicted_95lower', 'predicted_95upper'] #Ilse  

    for i in range(len(oral_cavity_predictions)):   # x and y are the lenghts of the seperate lists
        add_line(plan_info + ['OralCavity_Ext', 'nominal', predicted_labels[i],  float_to_string(oral_cavity_predictions[i]),'cGy (RBE)']) #Ilse
        add_line(plan_info + ['PCM_Sup', 'nominal', predicted_labels[i],  float_to_string(pcmsup_predictions[i]),'cGy (RBE)']) 
        add_line(plan_info + ['PCM_Med', 'nominal', predicted_labels[i],  float_to_string(pcmmed_predictions[i]),'cGy (RBE)']) 
        add_line(plan_info + ['PCM_Inf', 'nominal', predicted_labels[i],  float_to_string(pcminf_predictions[i]),'cGy (RBE)'])     
        add_line(plan_info + ['Parotid_L', 'nominal', predicted_labels[i],  float_to_string(parotidl_predictions[i]),'cGy (RBE)']) 
        add_line(plan_info + ['Parotid_R', 'nominal', predicted_labels[i],  float_to_string(parotidr_predictions[i]),'cGy (RBE)']) 
        add_line(plan_info + ['Submandibular_L', 'nominal', predicted_labels[i],  float_to_string(submandibularl_predictions[i]),'cGy (RBE)']) 
        add_line(plan_info + ['Submandibular_R', 'nominal', predicted_labels[i],  float_to_string(submandibularr_predictions[i]),'cGy (RBE)']) 
      
    for i in range(len(nominal_plan[0])):   # x and y are the lenghts of the seperate lists
        add_line(plan_info + [nominal_plan[0][i],'nominal','Average dose', float_to_string(nominal_plan[1][i]),'cGy (RBE)' ])
        
    for i in range(len(clinical_goal_ROI)):   # x and y are the lenghts of the seperate lists
        add_line(plan_info + [clinical_goal_ROI[i], 'nominal', clinical_goal[i], float_to_string(clinical_goal_nom[i]), 'unit', clinical_goal_nom_passed[i]])
        add_line(plan_info + [clinical_goal_ROI[i], 'voxelwise worst', clinical_goal[i], float_to_string(clinical_goal_value[i]), 'unit', clinical_goal_passed[i]])       
  
    for i in range(len(ntcp_photon)):   # x and y are the lenghts of the seperate lists
        # add_line(plan_info + [ntcp_labels[i], 'nominal', ntcp_labels[i],  ntcp_photon[i]])
        add_line(plan_info + [ntcp_labels[i], 'nominal', ntcp_labels[i],  float_to_string(ntcp_proton[i])])
        add_line(plan_info + [ntcp_labels[i], 'nominal', '\u0394' + ntcp_labels[i],  float_to_string(delta_ntcp[i])])
        # Reminder (keep for future reference) : \u0394 = delta character \u03a3 sum/sigma character'


    # for i in range(y):   # x and y are the lenghts of the seperate lists
         # all_data.nominal_plan[0][i]
         
    add_line(plan_info + ['CTV_7000', 'voxelwise worst', 'Conformity index CTV_7000',   float_to_string(conformity_index_7000)])
    add_line(plan_info + ['CTV_5425', 'voxelwise worst', 'Conformity index CTV_5425',   float_to_string(conformity_index_5425)])    
    
    dashboard_storage_file = str(dashboard_storage_path / patient.PatientID) + '_' + plan_name + '.csv'
    
    todays_date = date.today()
    date_prefix = '%02d%02d%02d' % (todays_date.year, todays_date.month, todays_date.day)
    dashboard_all_data_file = str(dashboard_storage_path / (date_prefix + '_ML_HN_research_all_data' + '.csv'))

    '''Buttons'''
    data_headers = [['Patient Name','Patient ID', 'Plan name', 'Plan time', 'Photon plan name', 'Photon plan time', 'ROI', 'Eval Dose', 'Parameter', 'Value', 'Unit', 'Goal Pass'], None]

    if without_gui:
        store_dashboard_data(data_headers, dashboard_storage_file)
        append_dashboard_data(all_data, dashboard_storage_file)  
        if not os.path.exists(str(dashboard_all_data_file)): 
            print('New file : ' + dashboard_all_data_file) 
            store_dashboard_data(data_headers, dashboard_all_data_file)
        append_dashboard_data(all_data, dashboard_all_data_file)
        master.destroy()
    else:
        Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 4, column = 2)
        Button(window, text="Close", command = master.destroy).grid(row = y + 5, column = 2)        
        Button(window, text='save', command = store_dashboard_data(all_data, dashboard_storage_file)).grid(row = y + 5, column = 4)
        Button(window, text='save and close', command = lambda:[store_dashboard_data(all_data, dashboard_storage_file), master.destroy()]).grid(row = y + 5, column = 6)
        Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 6, column = 1) 


def create_new_window_photon():
    master.withdraw()
    window = Toplevel(master, background = '#2c2c2c')
    
    plan_name = variable.get()
    plan = case.TreatmentPlans[plan_name]
    photon_plan_name = variable5.get()
    photon_plan = case.TreatmentPlans[photon_plan_name]  
    
    clinical_goal_passed, clinical_goal_ROI, clinical_goal, clinical_goal_value, clinical_goal_nom, max_width_clinical_goal_ROI, max_width_clinical_goal = clinical_goal_evaluations_photon(plan)
    # print(clinical_goal_passed, clinical_goal_ROI, clinical_goal, clinical_goal_value, clinical_goal_nom, max_width_clinical_goal_ROI, max_width_clinical_goal)
    
    # '''Text labels'''
    
    Label(window, text = 'Nominal plan (average dose in cGy)', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid').grid(row = 1, column = 2, columnspan = 2, sticky = 'ew')
    Label(window, text = 'Clinical goal evaluation', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', anchor = 'center').grid(row = 1, column = 5, columnspan = 4, sticky = 'ew')
    Label(window, text = 'ROI/POI', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = max_width_clinical_goal_ROI + 5).grid(row = 3, column = 5)
    Label(window, text = 'Clinical goal', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = max_width_clinical_goal).grid(row = 3, column = 6)
    Label(window, text = 'Nominal result', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = 16).grid(row = 3, column = 7)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = 1, column = 1)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = 1, column = 4)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = 2, column = 5, columnspan = 3)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = 1, column = 8)

    '''clinical goals and their values'''

    x = len(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
    for i in range(x): 
        Label(window, text = clinical_goal_ROI[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = max_width_clinical_goal_ROI + 5, border = 0.4, relief = 'solid').grid(row = i + 4, column = 5)
        Label(window, text = clinical_goal[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = max_width_clinical_goal, border = 0.4, relief = 'solid').grid(row = i + 4, column = 6)
        if clinical_goal_passed[i] == True:
            Label(window, text = clinical_goal_nom[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#62de87', anchor = 'w', width = 16, border = 0.4, relief = 'solid').grid(row = i + 4, column = 7)
        else:
            Label(window, text = clinical_goal_nom[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#f26a52', anchor = 'w', width = 16, border = 0.4, relief = 'solid').grid(row = i + 4, column = 7)
 
    '''Dose values of ROI's'''
    
    nominal_plan = get_doses(plan, ROI_NAMES)
    y = len(nominal_plan[0])
    for i in range(y):
        Label(window, text = nominal_plan[0][i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = nominal_plan[2] + 4, border  = 0.4, relief = 'solid').grid(row = i + 3, column = 2)
        Label(window, text = str(nominal_plan[1][i]), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = 12, border  = 0.4, relief = 'solid').grid(row = i + 3, column = 3)
 
    '''NTCP'''
 
    chosen_tumorlocation = variable2.get()
    chosen_xerostomie = variable3.get()
    chosen_dysfagie = variable4.get()
    grade_2_dysphagia_proton, grade_3_dysphagia_proton = calculate_ntcp_dys(plan, chosen_tumorlocation, chosen_dysfagie)
    grade_2_dysphagia_photon, grade_3_dysphagia_photon = calculate_ntcp_dys(photon_plan, chosen_tumorlocation, chosen_dysfagie)
    grade_2_xerostomia_proton, grade_3_xerostomia_proton = calculate_ntcp_xero(case, plan, chosen_xerostomie)
    grade_2_xerostomia_photon, grade_3_xerostomia_photon = calculate_ntcp_xero(case, photon_plan, chosen_xerostomie)
        
    delta_ntcp = delta_NTCP(grade_2_dysphagia_proton, grade_3_dysphagia_proton, grade_2_dysphagia_photon, grade_3_dysphagia_photon, grade_2_xerostomia_proton, grade_3_xerostomia_proton, grade_2_xerostomia_photon, grade_3_xerostomia_photon)

    if not without_gui:
        Label(window, text = 'NTCP', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid', width = 27).grid(row = 6, column = 9, columnspan = 4, sticky = 'ew')
        Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11), border  = 0.4, relief = 'solid', width = 20).grid(row = 7, column = 9)
        Label(window, text = 'Grade 2 Dysphagia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 8, column = 9)
        Label(window, text = 'Grade 2 Xerostomia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 9, column = 9)
        Label(window, text = 'Grade 3 Dysphagia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 10, column = 9)
        Label(window, text = 'Grade 3 Xerostomia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 11, column = 9)
        Label(window, text = '\u03a3 grade 2', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 12, column = 9)
        Label(window, text = '\u03a3 grade 3', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 13, column = 9)
        Label(window, text = 'NTCP ' + photon_plan_name, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 7, column = 10)
        Label(window, text = str(round(grade_2_dysphagia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 8, column = 10)
        Label(window, text = str(round(grade_2_xerostomia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 9, column = 10)
        Label(window, text = str(round(grade_3_dysphagia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 10, column = 10)
        Label(window, text = str(round(grade_3_xerostomia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 11, column = 10)
        Label(window, text = 'NTCP ' + plan_name, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 7, column = 11)
        Label(window, text = str(round(grade_2_dysphagia_proton, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 8, column = 11)
        Label(window, text = str(round(grade_2_xerostomia_proton, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 9, column = 11)
        Label(window, text = str(round(grade_3_dysphagia_proton, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 10, column = 11)
        Label(window, text = str(round(grade_3_xerostomia_proton, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 20).grid(row = 11, column = 11)
        Label(window, text = '\u0394 NTCP', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 10).grid(row = 7, column = 12)
        Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = 6, column = 13)
    
    if not without_gui:   
        for i in range(len(delta_ntcp)):
            if np.isnan(delta_ntcp[i]) == True:
                Label(window, text = 'NA', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 10).grid(row = i + 8, column = 12)
            else:
                if delta_ntcp[i] >= 0: 
                    Label(window, text = str(delta_ntcp[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 10).grid(row = i + 8, column = 12)
                else:
                    Label(window, text = str(delta_ntcp[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border  = 0.4, relief = 'solid', width = 10).grid(row = i + 8, column = 12)
    
    '''Storing patient baseline'''
    print('baseline choices : ' + str([chosen_tumorlocation, chosen_xerostomie, chosen_dysfagie]))
    store_patient_baseline([chosen_tumorlocation, chosen_xerostomie, chosen_dysfagie])              
                
    '''Storing the data'''

    try:
        plan_mod_time = plan.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
    except:
        plan_mod_time = "Unknown"
    try:
        photon_plan_mod_time = photon_plan.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
    except:
        photon_plan_mod_time = "Unknown"
    
    plan_info = [patient.Name, patient.PatientID, plan_name, str(plan_mod_time), photon_plan_name, str(photon_plan_mod_time)]
    
    ntcp_labels = ['Grade 2 Dysphagia', 'Grade 2 Xerostomia', 'Grade 3 Dysphagia', 'Grade 3 Xerostomia', '\u03a3 grade 2', '\u03a3 grade 3']
    ntcp_photon = [round(grade_2_dysphagia_photon, 1), round(grade_2_xerostomia_photon, 1), round(grade_3_dysphagia_photon, 1), round(grade_3_xerostomia_photon, 1), None, None] # The None's are inserted to ensure that lists are the same length where needed
    ntcp_proton = [round(grade_2_dysphagia_proton, 1), round(grade_2_xerostomia_proton, 1), round(grade_3_dysphagia_proton, 1), round(grade_3_xerostomia_proton, 1), None, None]
    data_headers = [['Patient Name','Patient ID', 'Plan name', 'Plan time', 'Photon plan name', 'Photon plan time', 'ROI', 'Eval Dose', 'Parameter', 'Value', 'Unit', 'Goal Pass'], None]
           
    for i in range(len(nominal_plan[0])):   # x and y are the lenghts of the seperate lists
        add_line(plan_info + [nominal_plan[0][i],'nominal','Average dose', float_to_string(nominal_plan[1][i]),'cGy (RBE)' ])
        
    for i in range(len(clinical_goal_ROI)):   # x and y are the lenghts of the seperate lists
        add_line(plan_info + [clinical_goal_ROI[i], 'nominal', clinical_goal[i], float_to_string(clinical_goal_value[i]), 'unit', clinical_goal_passed[i]])
        # add_line(plan_info + [clinical_goal_ROI[i], 'voxelwise worst', clinical_goal[i], float_to_string(clinical_goal_value[i]), 'unit', clinical_goal_passed[i]])    
# print(clinical_goal_passed, clinical_goal_ROI, clinical_goal, clinical_goal_value, clinical_goal_nom, max_width_clinical_goal_ROI, max_width_clinical_goal)
# [True, True, True, True, True, True, True, True, True, True, True, False, False, True, True, True] 
# ['SpinalCord', 'Cerebellum', 'Parotid_R', 'Parotid_L', 'BrainStem', 'PTV_7000_eval', 'PTV_5425_eval', 'PTV_7000', 'PTV_7000', 'Cochlea_L', 'Cochlea_R', 'Submandibular_L', 'Submandibular_R', 'Cerebrum', 'PTV_5425', 'PTV_7000'] 
# ['AtMost 5000.0 cGy (RBE) dose at 0.1 cm³ volume', 'AtMost 5000.0 cGy (RBE) dose at 0.1 cm³ volume', 'AtMost 2600.0 cGy (RBE) average dose', 'AtMost 2600.0 cGy (RBE) average dose', 'AtMost 5600.0 cGy (RBE) dose at 0.1 cm³ volume', 'AtLeast 98.0 % volume at 6650.0 cGy (RBE) dose', 'AtLeast 98.0 % volume at 5154.0 cGy (RBE) dose', 'AtLeast 6950.0 cGy (RBE) average dose', 'AtMost 7050.0 cGy (RBE) average dose', 'AtMost 4500.0 cGy (RBE) dose at 0.0 cm³ volume', 'AtMost 4500.0 cGy (RBE) dose at 0.0 cm³ volume', 'AtMost 4000.0 cGy (RBE) average dose', 'AtMost 4000.0 cGy (RBE) average dose', 'AtMost 5000.0 cGy (RBE) dose at 0.1 cm³ volume', 'AtLeast 98.0 % volume at 5154.0 cGy (RBE) dose', 'AtLeast 98.0 % volume at 6650.0 cGy (RBE) dose'] 
# [4422, 3155, 2363, 1957, 2083, 0.99, 1.0, 7025, 7025, 333, 376, 4894, 7007, 317, 1.0, 0.99] 
# ['4422 cGy (RBE)', '3155 cGy (RBE)', '2363 cGy (RBE)', '1957 cGy (RBE)', '2083 cGy (RBE)', '99.0 %', '100.0 %', '7025 cGy (RBE)', '7025 cGy (RBE)', '333 cGy (RBE)', '376 cGy (RBE)', '4894 cGy (RBE)', '7007 cGy (RBE)', '317 cGy (RBE)', '100.0 %', '99.0 %'] 15 46
# use last line to capture the unit, or modify get clinical goal        
  
    for i in range(len(ntcp_photon)):   # x and y are the lenghts of the seperate lists
        # add_line(plan_info + [ntcp_labels[i], 'nominal', ntcp_labels[i],  ntcp_photon[i]])
        # print('[ntcp_labels[i] nominal ntcp_labels[i],  float_to_string(ntcp_photon[i])]', [ ntcp_labels[i],  ntcp_photon[i]])
        # print(str(ntcp_labels[i]).encode('utf-8-sig'))
        # print(str(ntcp_photon[i]))
        try:
            add_line(plan_info + [ntcp_labels[i], 'nominal', ntcp_labels[i],  float_to_string(ntcp_photon[i])])
            add_line(plan_info + [ntcp_labels[i], 'nominal', '\u0394' + ntcp_labels[i],  float_to_string(delta_ntcp[i])])
        except:
            pass
        # Reminder (keep for future reference) : \u0394 = delta character \u03a3 sum/sigma character'


    '''Conformity index PTVs'''
    
    conformity_index_7000 = conformity_index(plan, 0.95*7000, 'PTV_7000_eval') 
    conformity_index_5425 = conformity_index(plan, 0.95*5425, 'PTV_5425_eval')    

    add_line(plan_info + ['PTV_7000_eval', 'nominal', 'Conformity index PTV_7000_eval',   float_to_string(conformity_index_7000)])
    add_line(plan_info + ['PTV_5425_eval', 'nominal', 'Conformity index PTV_P425_eval',   float_to_string(conformity_index_5425)])    

    '''Homogeneity index PTVs'''
    
    homogeneity_index_7000 = homogeneity_index(plan, 0.98, 'PTV_7000_eval') 
    homogeneity_index_5425 = homogeneity_index(plan, 0.98, 'PTV_5425_eval')    

    add_line(plan_info + ['PTV_7000_eval', 'nominal', 'Homogeneity index PTV_7000_eval',   float_to_string(homogeneity_index_7000)])
    add_line(plan_info + ['PTV_5425_eval', 'nominal', 'Homogeneity index PTV_5425_eval',   float_to_string(homogeneity_index_5425)])    

    dashboard_storage_file = str(dashboard_storage_path / patient.PatientID) + '_' + plan_name + '.csv'
    todays_date = date.today()
    date_prefix = '%02d%02d%02d' % (todays_date.year, todays_date.month, todays_date.day)
    dashboard_all_data_file = str(dashboard_storage_path / (date_prefix + '_ML_HN_research_all_data' + '.csv'))

    if without_gui:
        store_dashboard_data(data_headers, dashboard_storage_file)
        append_dashboard_data(all_data, dashboard_storage_file)  
        if not os.path.exists(str(dashboard_all_data_file)): 
            print('New file : ' + dashboard_all_data_file) 
            store_dashboard_data(data_headers, dashboard_all_data_file)
        append_dashboard_data(all_data, dashboard_all_data_file)
        master.destroy()
    else:
        Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 4, column = 2)
        Button(window, text="Close", command = master.destroy).grid(row = y + 5, column = 2)        
        Button(window, text='save', command = store_dashboard_data(all_data, dashboard_storage_file)).grid(row = y + 5, column = 4)
        Button(window, text='save and close', command = lambda:[store_dashboard_data(all_data, dashboard_storage_file), master.destroy()]).grid(row = y + 5, column = 6)
        Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 6, column = 1) 
 
    # Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 4, column = 2)
    # Button(window, text="close", command = master.destroy).grid(row = y + 5, column = 2)
    # Button(window, text='save', command = store_dashboard_data(all_data, dashboard_storage_file)).grid(row = y + 5, column = 4)
    # Button(window, text='save and close', command = lambda:[store_dashboard_data(all_data, dashboard_storage_file), master.destroy()]).grid(row = y + 5, column = 6)
    # Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 6, column = 1)



def create_new_window_proton_proton():       
    master.withdraw()
    root = Toplevel(master, background = '#2c2c2c')
    root.geometry('1400x1000')
    root.state('zoomed')
    
    '''It is not possible to add a scrollbar to the grid in the toplevel window.
    The workaround is to open a frame (in which you can scroll) on a canvas and display that canvas on the toplevel window.'''
    def onFrameConfigure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    style = Style()
    style.configure('TFrame', background = '#2c2c2c')
    
    canvas = Canvas(root, background = '#2c2c2c') #make the canvas
    window = Frame(canvas, style = 'TFrame') #make the frame
    scrollbar_ver = Scrollbar(root, orient="vertical", command=canvas.yview)  #add the scrollbars to the canvas
    scrollbar_hor = Scrollbar(root, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand = scrollbar_ver.set) #determine what the scrollbar should do
    canvas.configure(xscrollcommand = scrollbar_hor.set)
    scrollbar_ver.pack(side="right", fill="y") #place the actual scrollbar
    scrollbar_hor.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True) 
    canvas.create_window((4,4), window=window, anchor="nw")

    window.bind("<Configure>", lambda event, canvas = canvas: onFrameConfigure(canvas))
    

    plan_name1 = variable.get()
    plan_name2 = variable1.get()
    photon_plan_name = variable5.get()
    plan1 = case.TreatmentPlans[plan_name1]
    plan2 = case.TreatmentPlans[plan_name2]
    photon_plan = case.TreatmentPlans[photon_plan_name]  
    nominal_plan1 = get_doses(plan1, ROI_NAMES)
    nominal_plan2 = get_doses(plan2, ROI_NAMES)
    y = len(nominal_plan1[0])
    
    new_plan1_min, new_plan1_max = find_latest_vox_worst_plans(case, plan1)
    new_plan2_min, new_plan2_max = find_latest_vox_worst_plans(case, plan2)
    
    clinical_goal_passed1, clinical_goal_ROI1, clinical_goal_value1, clinical_goal_nom_passed1, clinical_goal_nom1, max_width_clinical_goal_ROI1 = clinical_goal_evaluations(plan1, new_plan1_min, new_plan1_max)
    clinical_goal1, clinical_goal_value_string1 = clinical_goal_evaluations_to_string(plan1, clinical_goal_value1)
    clinical_goal_passed2, clinical_goal_ROI2, clinical_goal_value2, clinical_goal_nom_passed2, clinical_goal_nom2, max_width_clinical_goal_ROI2 = clinical_goal_evaluations(plan2, new_plan2_min, new_plan2_max)
    clinical_goal2, clinical_goal_value_string2 = clinical_goal_evaluations_to_string(plan2, clinical_goal_value2)
    
    unused, clinical_goal_nominal1 = clinical_goal_evaluations_to_string_nominal(plan1, clinical_goal_nom1)
    unused, clinical_goal_nominal2 = clinical_goal_evaluations_to_string_nominal(plan2, clinical_goal_nom2)
    
    delta_clinical_goal_value = [x - y for x, y in zip(clinical_goal_value1, clinical_goal_value2)] 
    delta_clinical_goal_nominal = [x - y for x,y in zip(clinical_goal_nom1, clinical_goal_nom2)]
    unused, delta_clinical_goal_value_string = clinical_goal_evaluations_to_string(plan1, delta_clinical_goal_value)
    unused, delta_clinical_goal_nominal_string = clinical_goal_evaluations_to_string_nominal(plan1, delta_clinical_goal_nominal)
    
    max_width_clinical_goal1 = max(len(x) for x in clinical_goal1)
    

    '''Text labels'''

    Label(window, text = 'Nominal plan (average dose in cGy)', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'center', width = nominal_plan1[2] + 30).grid(row = 1, column = 2, columnspan = 4)
    Label(window, text = 'ROI/POI', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'w', width = nominal_plan1[2] + 4).grid(row = 3, column = 2)
    Label(window, text = plan_name1, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'w', width = 12).grid(row = 3, column = 3, sticky = 'ew')
    Label(window, text = plan_name2, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'w', width = 12).grid(row = 3, column = 4, sticky = 'ew')
    Label(window, text = '\u0394', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'center', width = 12).grid(row = 3, column = 5, sticky = 'ew')
    Label(window, text = 'Robust evaluation ' + plan_name1, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', anchor = 'center').grid(row = y + 6, column = 2, columnspan = 6, sticky = 'ew')
    Label(window, text = 'Robust evaluation ' + plan_name2, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', anchor = 'center').grid(row = y + 6, column = 9, columnspan = 2, sticky = 'ew')
    Label(window, text = plan_name1 + ' - ' + plan_name2, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', anchor = 'center').grid(row = y + 6, column = 12, columnspan = 2, sticky = 'ew')
    Label(window, text = 'ROI/POI', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = nominal_plan1[2] + 4).grid(row = y + 8, column = 2)
    Label(window, text = 'Clinical goal', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', anchor = 'center').grid(row = y + 8, column = 3, columnspan = 3, sticky = 'ew')
    Label(window, text = 'Voxelwise worst', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid').grid(row = y + 8, column = 6, sticky = 'ew')
    Label(window, text = 'Voxelwise worst', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = 16).grid(row = y + 8, column = 9)
    Label(window, text = 'Nominal result', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = 16).grid(row = y + 8, column = 7)
    Label(window, text = 'Nominal result', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = 16).grid(row = y + 8, column = 10)
    Label(window, text = '\u0394 voxelwise worst', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = 16).grid(row = y + 8, column = 12)
    Label(window, text = '\u0394 nominal result', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = 16).grid(row = y + 8, column = 13)
    
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = 1, column = 1)       # These 'empty' labels add some empty space, otherwise everything is put right beside each other
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = 2, column = 2)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 4, column = 2)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 5, column = 2)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 5, column = 8)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 5, column = 11)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 7, column = 2)
    

    '''Dose values of ROI's'''

    delta_nominal_plan1_plan2 = [elem1 - elem2 for (elem1, elem2) in zip(nominal_plan1[1], nominal_plan2[1])]
    for i in range(y):
        Label(window, text = nominal_plan1[0][i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = nominal_plan1[2] + 4, border  = 0.4, relief = 'solid').grid(row = i + 4, column = 2)
        Label(window, text = str(nominal_plan1[1][i]), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = 12, border  = 0.4, relief = 'solid').grid(row = i + 4, column = 3, sticky = 'ew')
        Label(window, text = str(nominal_plan2[1][i]), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = 12, border  = 0.4, relief = 'solid').grid(row = i + 4, column = 4, sticky = 'ew')
        if delta_nominal_plan1_plan2[i] >= 0: 
            Label(window, text = str(delta_nominal_plan1_plan2[i]), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = 12, border  = 0.4, relief = 'solid').grid(row = i + 4, column = 5, sticky = 'ew')
        else:
            Label(window, text = str(delta_nominal_plan1_plan2[i]), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', width = 12, border  = 0.4, relief = 'solid').grid(row = i + 4, column = 5, sticky = 'ew')
 
 
    '''clinical goals and their values plan 1'''
    
    x = len(plan1.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
    for i in range(x): 
        Label(window, text = clinical_goal_ROI1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = nominal_plan1[2] + 4, border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 2)
        Label(window, text = clinical_goal1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 3, columnspan = 3, sticky = 'ew')
        if clinical_goal_passed1[i] == True:
            Label(window, text = clinical_goal_value_string1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#62de87', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 6, sticky = 'ew')
        else:
            Label(window, text = clinical_goal_value_string1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#f26a52', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 6, sticky = 'ew')
        if clinical_goal_nom_passed1[i] == True:
            Label(window, text = clinical_goal_nominal1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#62de87', anchor = 'w',  width = 16, border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 7)
        else:
            Label(window, text = clinical_goal_nominal1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#f26a52', anchor = 'w',  width = 16, border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 7)
    
    '''clinical goals and their values plan 2'''
 
    z = len(plan2.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
    for i in range(z): 
        Label(window, text = clinical_goal_nominal2[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 10, sticky = 'ew')
        if clinical_goal_passed2[i] == True:
            Label(window, text = clinical_goal_value_string2[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#62de87', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 9, sticky = 'ew')
        else:
            Label(window, text = clinical_goal_value_string2[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#f26a52', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 9, sticky = 'ew')
        if clinical_goal_nom_passed1[i] == True:
            Label(window, text = clinical_goal_nominal2[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#62de87', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 10, sticky = 'ew')
        else:
            Label(window, text = clinical_goal_nominal2[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#f26a52', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 10, sticky = 'ew')
    
    

    '''delta clinical goals'''
    
    for i in range(max(x,z)):  #the "if else" tree is there in case both plans do not have the same amount of clinical goals (more likely to happen when comparing a photon and proton plan)
        if i < x and i < z:
            if plan1.TreatmentCourse.EvaluationSetup.EvaluationFunctions[i].PlanningGoal.GoalCriteria == 'AtMost':
                if delta_clinical_goal_value[i] < 0:
                    Label(window, text = delta_clinical_goal_value_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 12, sticky = 'ew')
                else:
                    Label(window, text = delta_clinical_goal_value_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 12, sticky = 'ew')
                if delta_clinical_goal_nominal[i] < 0:
                    Label(window, text = delta_clinical_goal_nominal_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 13, sticky = 'ew')
                else:
                    Label(window, text = delta_clinical_goal_nominal_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 13, sticky = 'ew')
            else:
                if delta_clinical_goal_value[i] > 0:
                    Label(window, text = delta_clinical_goal_value_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 12, sticky = 'ew')
                else:
                    Label(window, text = delta_clinical_goal_value_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 12, sticky = 'ew')
                if delta_clinical_goal_nominal[i] > 0:
                    Label(window, text = delta_clinical_goal_nominal_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 13, sticky = 'ew')
                else:
                    Label(window, text = delta_clinical_goal_nominal_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 13, sticky = 'ew')
        else:
            Label(window, text = 'NA', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 9, column = 13, sticky = 'ew')
 
    '''NTCP'''
 
    chosen_tumorlocation = variable2.get()
    chosen_xerostomie = variable3.get()
    chosen_dysfagie = variable4.get()
    grade_2_dysphagia_proton1, grade_3_dysphagia_proton1 = calculate_ntcp_dys(plan1, chosen_tumorlocation, chosen_dysfagie)
    grade_2_dysphagia_proton2, grade_3_dysphagia_proton2 = calculate_ntcp_dys(plan2, chosen_tumorlocation, chosen_dysfagie)
    grade_2_dysphagia_photon, grade_3_dysphagia_photon = calculate_ntcp_dys(photon_plan, chosen_tumorlocation, chosen_dysfagie)
    grade_2_xerostomia_proton1, grade_3_xerostomia_proton1 = calculate_ntcp_xero(case, plan1, chosen_xerostomie)
    grade_2_xerostomia_proton2, grade_3_xerostomia_proton2 = calculate_ntcp_xero(case, plan2, chosen_xerostomie)
    grade_2_xerostomia_photon, grade_3_xerostomia_photon = calculate_ntcp_xero(case, photon_plan, chosen_xerostomie)
        
    delta_ntcp1 = delta_NTCP(grade_2_dysphagia_proton1, grade_3_dysphagia_proton1, grade_2_dysphagia_photon, grade_3_dysphagia_photon, grade_2_xerostomia_proton1, grade_3_xerostomia_proton1, grade_2_xerostomia_photon, grade_3_xerostomia_photon)  
    delta_ntcp2 = delta_NTCP(grade_2_dysphagia_proton2, grade_3_dysphagia_proton2, grade_2_dysphagia_photon, grade_3_dysphagia_photon, grade_2_xerostomia_proton2, grade_3_xerostomia_proton2, grade_2_xerostomia_photon, grade_3_xerostomia_photon)
    
    
    Label(window, text = 'NTCP', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 12, column = 2, columnspan = 6, sticky = 'ew')
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11), border  = 0.4, relief = 'solid', width = nominal_plan1[2] + 4).grid(row = x + y + 13, column = 2)
    Label(window, text = 'Grade 2 Dysphagia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = nominal_plan1[2] + 4).grid(row = x + y + 14, column = 2)
    Label(window, text = 'Grade 2 Xerostomia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = nominal_plan1[2] + 4).grid(row = x + y + 15, column = 2)
    Label(window, text = 'Grade 3 Dysphagia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = nominal_plan1[2] + 4).grid(row = x + y + 16, column = 2)
    Label(window, text = 'Grade 3 Xerostomia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = nominal_plan1[2] + 4).grid(row = x + y + 17, column = 2)
    Label(window, text = '\u03a3 graad 2', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = nominal_plan1[2] + 4).grid(row = x + y + 18, column = 2)
    Label(window, text = '\u03a3 graad 3', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = nominal_plan1[2] + 4).grid(row = x + y + 19, column = 2)
    Label(window, text = 'NTCP ' + photon_plan_name, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 13, column = 3, sticky = 'ew')
    Label(window, text = str(round(grade_2_dysphagia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 14, column = 3, sticky = 'ew')
    Label(window, text = str(round(grade_2_xerostomia_photon,1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 15, column = 3, sticky = 'ew')
    Label(window, text = str(round(grade_3_dysphagia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 16, column = 3, sticky = 'ew')
    Label(window, text = str(round(grade_3_xerostomia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 17, column = 3, sticky = 'ew')
    Label(window, text = 'NTCP ' + plan_name1, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 13, column = 4, sticky = 'ew')
    Label(window, text = str(round(grade_2_dysphagia_proton1, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 14, column = 4, sticky = 'ew')
    Label(window, text = str(round(grade_2_xerostomia_proton1, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 15, column = 4, sticky = 'ew')
    Label(window, text = str(round(grade_3_dysphagia_proton1, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 16, column = 4, sticky = 'ew')
    Label(window, text = str(round(grade_3_xerostomia_proton1, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 17, column = 4, sticky = 'ew')
    Label(window, text = 'NTCP ' + plan_name2, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 13, column = 5, sticky = 'ew')
    Label(window, text = str(round(grade_2_dysphagia_proton2, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 14, column = 5, sticky = 'ew')
    Label(window, text = str(round(grade_2_xerostomia_proton2, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 15, column = 5, sticky = 'ew')
    Label(window, text = str(round(grade_3_dysphagia_proton2, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 16, column = 5, sticky = 'ew')
    Label(window, text = str(round(grade_3_xerostomia_proton2, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 17, column = 5, sticky = 'ew')
    Label(window, text = photon_plan_name + ' - ' + plan_name1, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 13, column = 6, sticky = 'ew')
    Label(window, text = photon_plan_name + ' - ' + plan_name2, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 10).grid(row = x + y + 13, column = 7, sticky = 'ew')
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = x + y + 10, column = 2)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = x + y + 11, column = 2)
    
    
    for i in range(len(delta_ntcp1)):
        if np.isnan(delta_ntcp1[i]) == True:
            Label(window, text = 'N/A', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 14, column = 6, sticky = 'ew')
            Label(window, text = 'N/A', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 14, column = 7, sticky = 'ew')
        else:
            if delta_ntcp1[i] >= 0: 
                Label(window, text = str(delta_ntcp1[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 14, column = 6, sticky = 'ew')
            else:
                Label(window, text = str(delta_ntcp1[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 14, column = 6, sticky = 'ew')
            
            if delta_ntcp2[i] >= 0: 
                Label(window, text = str(delta_ntcp2[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 14, column = 7, sticky = 'ew')
            else:
                Label(window, text = str(delta_ntcp2[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 14, column = 7, sticky = 'ew')    
    
 
    '''Robust conformity index'''
    
    conformity_index_7000_1 = conformity_index(new_plan1_min, 7000, 'CTV_7000') 
    conformity_index_5425_1 = conformity_index(new_plan1_min, 5425, 'CTV_5425')   
    conformity_index_7000_2 = conformity_index(new_plan2_min, 7000, 'CTV_7000') 
    conformity_index_5425_2 = conformity_index(new_plan2_min, 5425, 'CTV_5425')
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = x + y + 20, column = 2)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11), border  = 0.4, relief = 'solid').grid(row = x + y + 22, column = 2, sticky = 'ew')
    Label(window, text = 'Robust conformity index', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 21, column = 2, columnspan = 4, sticky = 'ew')    
    Label(window, text = plan_name1, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 22, column = 3, sticky = 'ew')
    Label(window, text = plan_name2, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 22, column = 4, sticky = 'ew')
    Label(window, text = '\u0394', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 22, column = 5, sticky = 'ew')
    Label(window, text = 'CI CTV_7000', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 23, column = 2, sticky = 'ew')    
    Label(window, text = 'CI CTV_5425', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 24, column = 2, sticky = 'ew')
    Label(window, text = str(conformity_index_7000_1), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 23, column = 3, sticky = 'ew')    
    Label(window, text = str(conformity_index_5425_1), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 24, column = 3, sticky = 'ew') 
    Label(window, text = str(conformity_index_7000_2), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 23, column = 4, sticky = 'ew')    
    Label(window, text = str(conformity_index_5425_2), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 24, column = 4, sticky = 'ew')
    if conformity_index_7000_1 - conformity_index_7000_2 < 0:
        Label(window, text = str(round(conformity_index_7000_1 - conformity_index_7000_2, 2)), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 23, column = 5, sticky = 'ew')
    else:
        Label(window, text = str(round(conformity_index_7000_1 - conformity_index_7000_2, 2)), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 23, column = 5, sticky = 'ew')
        
    if conformity_index_5425_1 - conformity_index_5425_2 < 0:
        Label(window, text = str(round(conformity_index_5425_1 - conformity_index_5425_2, 2)), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 24, column = 5, sticky = 'ew')
    else:
        Label(window, text = str(round(conformity_index_5425_1 - conformity_index_5425_2, 2)), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 24, column = 5, sticky = 'ew')    
        
        
    '''Storing patient baseline'''
    store_patient_baseline([chosen_tumorlocation, chosen_xerostomie, chosen_dysfagie])              
            
   
    '''Storing the data''' 

    try:
        plan_mod_time1 = plan.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
    except:
        plan_mod_time1 = "Unknown"
    try:
        plan_mod_time2 = plan2.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
    except:
        plan_mod_time2 = "Unknown"
    try:
        photon_plan_mod_time = photon_plan.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
    except:
        photon_plan_mod_time = photon_plan.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
               
    ntcp_labels = ['Grade 2 Dysphagia', 'Grade 2 Xerostomia', 'Grade 3 Dysphagia', 'Grade 3 Xerostomia', '\u03a3 grade 2', '\u03a3 grade 3']    
    ntcp_photon = [round(grade_2_dysphagia_photon, 1), round(grade_2_xerostomia_photon, 1), round(grade_3_dysphagia_photon, 1), round(grade_3_xerostomia_photon, 1), None, None]     
    ntcp_proton1 = [round(grade_2_dysphagia_proton1, 1), round(grade_2_xerostomia_proton1, 1), round(grade_3_dysphagia_proton1, 1), round(grade_3_xerostomia_proton1, 1), None, None]    
    ntcp_proton2 = [round(grade_2_dysphagia_proton2, 1), round(grade_2_xerostomia_proton2, 1), round(grade_3_dysphagia_proton2, 1), round(grade_3_xerostomia_proton2, 1), None, None]    
    all_data = [['Patient name:  ' + patient.Name, None, None, None, None, None, 'Patient ID:  ' + patient.PatientID],
                [None],
                [plan_name1 + ' last stored at:  ' + str(plan_mod_time1)],
                [plan_name2 + ' last stored at:  ' + str(plan_mod_time2)],
                [photon_plan_name + ' last stored at:  ' + str(photon_plan_mod_time)],
                [None],
                ['Nominal plan', None, None, None, None, None, 'Robust evaluation', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'NTCP'],     
                [None],
                [None, None, plan_name1, plan_name2, None, None, None, None, None, None, None, None, None, plan_name1, None, None, None, plan_name2, None, None, None, plan_name1 + ' - ' + plan_name2, None, None, None, None, None, None, photon_plan_name, plan_name1, plan_name2, 
                photon_plan_name + ' - ' + plan_name1, None, photon_plan_name + ' - ' + plan_name2, None, None],
                ['ROI/POI', None, 'Dose', 'Dose', '\u0394 Dose', None, 'ROI/POI', None, 'Clinical Goal', None, None, None, None, 'Voxelwise worst', None, 'Nominal result', None, 'Voxelwise worst', None, 'Nominal result', None, '\u0394 Voxelwise worst', None, '\u0394 Nominal result',
                None, None, None, None, 'NTCP', 'NTCP', 'NTCP', '\u0394 NTCP', None, '\u0394 NTCP']]
    
    '''Maybe there is a better way of doing this instead of making this monstrosity, but I'm not sure'''
    for i in range(max(x,y,z)):
        if i < 6:               # tacit assumption that there are six or more clinical goals or ROIs ---> the index i will be out of range otherwise.
            if i < x and i < y and i < z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], 
                None, clinical_goal_value_string2[i], None, clinical_goal_nominal2[i], None, delta_clinical_goal_value_string[i], None, delta_clinical_goal_nominal_string[i], None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_proton1[i], ntcp_proton2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i < x and i < y and i >= z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], 
                None, None, None, None, None, None, None, None, None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_proton1[i], ntcp_proton2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i < x and i >= y and i < z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], 
                None, clinical_goal_value_string2[i], None, clinical_goal_nominal2[i], None, delta_clinical_goal_value_string[i], None, delta_clinical_goal_nominal_string[i], None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_proton1[i], ntcp_proton2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i < x and i >= y and i >= z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], 
                None, None, None, None, None, None, None, None, None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_proton1[i], ntcp_proton2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i >= x and i < y and i < z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None,  None, None, None, None, 
                None, clinical_goal_value_string2[i], None, clinical_goal_nominal2[i], None, None, None, None, None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_proton1[i], ntcp_proton2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i >= x and i < y and i >= z:     
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, None, None, None, None, None, None,  None, None, None, None, 
                None, None, None, None, None, None, None, None, None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_proton1[i], ntcp_proton2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i >= x and i >= y and i < z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None,  None, None, None, None, 
                None, clinical_goal_value_string2[i], None, clinical_goal_nominal2[i], None, None, None, None, None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_proton1[i], ntcp_proton2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
        else:
            if i < x and i < y and i < z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], 
                None, clinical_goal_value_string2[i], None, clinical_goal_nominal2[i], None, delta_clinical_goal_value_string[i], None, delta_clinical_goal_nominal_string[i], None, None])
            elif i < x and i < y and i >= z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], 
                None, None])
            elif i < x and i >= y and i < z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], 
                None, clinical_goal_value_string2[i], None, clinical_goal_nominal2[i], None, delta_clinical_goal_value_string[i], None, delta_clinical_goal_nominal_string[i], None, None])
            elif i < x and i >= y and i >= z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], None, None])
            elif i >= x and i < y and i < z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None,  None, None, None, None, 
                None, clinical_goal_value_string2[i], None, clinical_goal_nominal2[i], None, None])
            elif i >= x and i < y and i >= z:     
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, None])
            elif i >= x and i >= y and i < z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None,  None, None, None, None, None, clinical_goal_value_string2[i], None, clinical_goal_nominal2[i], None, None])

        
    all_data.append([None])    
    all_data.append([None])    
    all_data.append([None, None, None, plan_name1, plan_name2, '\u0394'])  
    all_data.append(['Conformity index CTV_7000', None, None, conformity_index_7000_1, conformity_index_7000_2, round(conformity_index_7000_1 - conformity_index_7000_2, 2)])
    all_data.append(['Conformity index CTV_5425', None, None, conformity_index_5425_1, conformity_index_5425_2, round(conformity_index_5425_1 - conformity_index_5425_2, 2)])

    dashboard_storage_file = str(dashboard_storage_path / patient.PatientID) + '_' + plan_name1 + '_' + plan_name2  
    # store_dashboard_data(all_data, dashboard_storage_file)
    
    # def store_dashboard_data(all_data, dashboard_storage_file): 
        # # outputpath = '\\\\zkh\\appdata\\Raystation\\Research\\ML\\Erik and Roel\\erik\\scripts\\dashboard_Hielke\\dashboard-storage\\'
        # filename = patient.PatientID + '_' + plan_name1 + '_' + plan_name2  
        # with open(dashboard_storage_path + filename + '.csv', 'w', newline = '', encoding='utf-8-sig') as file:  # utf-8-sig enables greek letters to be written to the csv
                    # writer = csv.writer(file, delimiter = ';')                                       # without the colon delimiter all data would be put in one cell in Excel   
                    # writer.writerows(all_data)
                    # writer.writerow([None])
                    # writer.writerow([None])
                    # writer.writerow([None, None, None, plan_name1, plan_name2, '\u0394'])
                    # writer.writerow(['Conformity index CTV_7000', None, None, conformity_index_7000_1, conformity_index_7000_2, round(conformity_index_7000_1 - conformity_index_7000_2, 2)])
                    # writer.writerow(['Conformity index CTV_5425', None, None, conformity_index_5425_1, conformity_index_5425_2, round(conformity_index_5425_1 - conformity_index_5425_2, 2)])
        # return     
        
    '''Buttons'''
    
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = x + y + 25, column = 2)
    Button(window, text="Close", command = master.destroy).grid(row = x + y + 26, column = 2)        
    Button(window, text='save', command = store_dashboard_data(all_data, dashboard_storage_file)).grid(row = x + y + 26, column = 4)
    Button(window, text='save and close', command = lambda:[store_dashboard_data(all_data, dashboard_storage_file), master.destroy()]).grid(row = x + y + 26, column = 6)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = x + y + 27, column = 1)     
        
        
    
def create_new_window_proton_photon():    
    master.withdraw()
    root = Toplevel(master, background = '#2c2c2c')
    root.geometry('1400x1000')
    root.state('zoomed')
    
    def onFrameConfigure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    style = Style()
    style.configure('TFrame', background = '#2c2c2c')
    
    canvas = Canvas(root, background = '#2c2c2c')
    window = Frame(canvas, style = 'TFrame')
    scrollbar_ver = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar_hor = Scrollbar(root, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand = scrollbar_ver.set)
    canvas.configure(xscrollcommand = scrollbar_hor.set)
    scrollbar_ver.pack(side="right", fill="y")
    scrollbar_hor.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4,4), window=window, anchor="nw")

    window.bind("<Configure>", lambda event, canvas = canvas: onFrameConfigure(canvas))
    
    if case.TreatmentPlans[variable.get()].BeamSets[0].Modality == 'Protons':
        plan_name1 = variable.get()
        plan_name2 = variable1.get()
    else:
        plan_name1 = variable1.get()
        plan_name2 = variable.get()
    
    photon_plan_name = variable5.get()
    plan1 = case.TreatmentPlans[plan_name1]
    plan2 = case.TreatmentPlans[plan_name2]
    photon_plan = case.TreatmentPlans[photon_plan_name]  
    nominal_plan1 = get_doses(plan1, ROI_NAMES)
    nominal_plan2 = get_doses(plan2, ROI_NAMES)
    y = len(nominal_plan1[0])

    #only applicable to the proton plan
    new_plan1_min, new_plan1_max = find_latest_vox_worst_plans(case, plan1) 
    
    clinical_goal_passed1, clinical_goal_ROI1, clinical_goal_value1, clinical_goal_nom_passed1, clinical_goal_nom1, max_width_clinical_goal_ROI1 = clinical_goal_evaluations(plan1, new_plan1_min, new_plan1_max)
    clinical_goal1, clinical_goal_value_string1 = clinical_goal_evaluations_to_string(plan1, clinical_goal_value1)
    unused1, clinical_goal_nominal1 = clinical_goal_evaluations_to_string_nominal(plan1, clinical_goal_nom1)
    
    max_width_clinical_goal1 = max(len(x) for x in clinical_goal1)
    
    #for the photon plan:
    clinical_goal_passed2, clinical_goal_ROI2, clinical_goal2, clinical_goal_value2, clinical_goal_nominal2, max_width_clinical_goal_ROI2, max_width_clinical_goal2 = clinical_goal_evaluations_photon(plan2) 
    
    max_width_clinical_goal2 = max(len(x) for x in clinical_goal2)
    
    #Difference between plans
    delta_clinical_goal_nominal = [x - y for x,y in zip(clinical_goal_nom1, clinical_goal_value2)]
    try:
        unused, delta_clinical_goal_nominal_string = clinical_goal_evaluations_to_string_nominal(plan1, delta_clinical_goal_nominal)
    except: 
        unused, delta_clinical_goal_nominal_string = clinical_goal_evaluations_to_string_nominal(plan2, delta_clinical_goal_nominal)
    
    '''Text labels'''

    Label(window, text = 'Nominal plan (average dose in cGy)', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'center', width = nominal_plan1[2] + 30).grid(row = 1, column = 2, columnspan = 4)
    Label(window, text = 'ROI/POI', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'w').grid(row = 3, column = 2, sticky = 'ew')
    Label(window, text = plan_name1, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'w', width = 12).grid(row = 3, column = 3, sticky = 'ew')
    Label(window, text = plan_name2, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'w', width = 12).grid(row = 3, column = 4, sticky = 'ew')
    Label(window, text = '\u0394', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'center', width = 12).grid(row = 3, column = 5, sticky = 'ew')
    Label(window, text = 'Clinical goal evaluation', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', anchor = 'center').grid(row = y + 6, column = 2, columnspan = 6, sticky = 'ew')
    Label(window, text = 'Note: photon plans and proton plans can often not be directly compared', background = '#FF9300', font = ('TkDefaultFont', 11), border = 0.4, relief = 'solid', anchor = 'center').grid(row = y + 6, column = 9, columnspan = 3, sticky = 'ew')
    Label(window, text = 'ROI/POI', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid').grid(row = y + 9, column = 2, sticky = 'ew')
    Label(window, text = 'ROI/POI', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid').grid(row = y + 9, column = 9, sticky = 'ew')
    Label(window, text = 'Clinical goal', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', anchor = 'center').grid(row = y + 9, column = 3, columnspan = 3, sticky = 'ew')
    Label(window, text = 'Clinical goal', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', anchor = 'center', width = max_width_clinical_goal2).grid(row = y + 9, column = 10)
    Label(window, text = plan_name1, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', anchor = 'center').grid(row = y + 8, column = 2, columnspan = 6, sticky = 'ew')
    Label(window, text = plan_name2, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', anchor = 'center').grid(row = y + 8, column = 9, columnspan = 3, sticky = 'ew')
    Label(window, text = 'Voxelwise worst', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid').grid(row = y + 9, column = 6, sticky = 'ew')
    Label(window, text = 'Nominal result', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = 16).grid(row = y + 9, column = 7)
    Label(window, text = 'Nominal result', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = 16).grid(row = y + 9, column = 11)
    Label(window, text = '\u0394 nominal result', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = 16).grid(row = y + 9, column = 13)
    
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = 1, column = 1)       # These 'empty' labels add some empty space, otherwise everything is put right beside each other
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = 2, column = 2)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 4, column = 2)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 5, column = 2)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 5, column = 8)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 5, column = 12)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 7, column = 14)
    
    
    '''Dose values of ROI's'''

    delta_nominal_plan1_plan2 = [elem1 - elem2 for (elem1, elem2) in zip(nominal_plan1[1], nominal_plan2[1])]
    for i in range(y):
        Label(window, text = nominal_plan1[0][i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + 4, column = 2, sticky = 'ew')
        Label(window, text = str(nominal_plan1[1][i]), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = 12, border  = 0.4, relief = 'solid').grid(row = i + 4, column = 3, sticky = 'ew')
        Label(window, text = str(nominal_plan2[1][i]), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = 12, border  = 0.4, relief = 'solid').grid(row = i + 4, column = 4, sticky = 'ew')
        if delta_nominal_plan1_plan2[i] >= 0: 
            Label(window, text = str(delta_nominal_plan1_plan2[i]), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = 12, border  = 0.4, relief = 'solid').grid(row = i + 4, column = 5, sticky = 'ew')
        else:
            Label(window, text = str(delta_nominal_plan1_plan2[i]), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', width = 12, border  = 0.4, relief = 'solid').grid(row = i + 4, column = 5, sticky = 'ew')
            
            
    '''clinical goals and their values plan 1'''

    x = len(plan1.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
    for i in range(x): 
        Label(window, text = clinical_goal_ROI1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 2, sticky = 'ew')
        Label(window, text = clinical_goal1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 3, columnspan = 3, sticky = 'ew')       
        if clinical_goal_passed1[i] == True:
            Label(window, text = clinical_goal_value_string1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#62de87', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 6, sticky = 'ew')
        else:
            Label(window, text = clinical_goal_value_string1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#f26a52', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 6, sticky = 'ew')
        if clinical_goal_nom_passed1[i] == True:
            Label(window, text = clinical_goal_nominal1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#62de87', anchor = 'w',  width = 16, border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 7)    
        else:        
            Label(window, text = clinical_goal_nominal1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#f26a52', anchor = 'w',  width = 16, border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 7) 
            
    '''clinical goals and their values plan 2'''

    z = len(plan2.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
    for i in range(z): 
        Label(window, text = clinical_goal_ROI2[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 9, sticky = 'ew')
        Label(window, text = clinical_goal2[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 10, sticky = 'ew')
        if clinical_goal_passed2[i] == True:
            Label(window, text = clinical_goal_nominal2[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#62de87', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 11, sticky = 'ew')
        else:
            Label(window, text = clinical_goal_nominal2[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#f26a52', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 11, sticky = 'ew')        
            
                   
    '''delta clinical goals'''

    for i in range(max(x,z)): #The number of clinical goals is likely to differ, this "if else" tree makes sure that's no problem
        if i < x and i < z:
            if plan1.TreatmentCourse.EvaluationSetup.EvaluationFunctions[i].PlanningGoal.GoalCriteria == 'AtMost':
                if delta_clinical_goal_nominal[i] < 0:
                    Label(window, text = delta_clinical_goal_nominal_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 13, sticky = 'ew')
                else:
                    Label(window, text = delta_clinical_goal_nominal_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 13, sticky = 'ew')
            else:
                if delta_clinical_goal_nominal[i] > 0:
                    Label(window, text = delta_clinical_goal_nominal_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 13, sticky = 'ew')
                else:
                    Label(window, text = delta_clinical_goal_nominal_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 13, sticky = 'ew')   
        else:
            Label(window, text = 'NA', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 13, sticky = 'ew')
            
    
    '''NTCP'''
 
    chosen_tumorlocation = variable2.get()
    chosen_xerostomie = variable3.get()
    chosen_dysfagie = variable4.get()
    grade_2_dysphagia_plan1, grade_3_dysphagia_plan1 = calculate_ntcp_dys(plan1, chosen_tumorlocation, chosen_dysfagie)
    grade_2_dysphagia_plan2, grade_3_dysphagia_plan2 = calculate_ntcp_dys(plan2, chosen_tumorlocation, chosen_dysfagie)
    grade_2_dysphagia_photon, grade_3_dysphagia_photon = calculate_ntcp_dys(photon_plan, chosen_tumorlocation, chosen_dysfagie)
    grade_2_xerostomia_plan1, grade_3_xerostomia_plan1 = calculate_ntcp_xero(case, plan1, chosen_xerostomie)
    grade_2_xerostomia_plan2, grade_3_xerostomia_plan2 = calculate_ntcp_xero(case, plan2, chosen_xerostomie)
    grade_2_xerostomia_photon, grade_3_xerostomia_photon = calculate_ntcp_xero(case, photon_plan, chosen_xerostomie)
        
    delta_ntcp1 = delta_NTCP(grade_2_dysphagia_plan1, grade_3_dysphagia_plan1, grade_2_dysphagia_photon, grade_3_dysphagia_photon, grade_2_xerostomia_plan1, grade_3_xerostomia_plan1, grade_2_xerostomia_photon, grade_3_xerostomia_photon)  
    delta_ntcp2 = delta_NTCP(grade_2_dysphagia_plan2, grade_3_dysphagia_plan2, grade_2_dysphagia_photon, grade_3_dysphagia_photon, grade_2_xerostomia_plan2, grade_3_xerostomia_plan2, grade_2_xerostomia_photon, grade_3_xerostomia_photon)
    
    
    Label(window, text = 'NTCP', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 13, column = 2, columnspan = 6, sticky = 'ew')
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11), border  = 0.4, relief = 'solid').grid(row = x + y + 14, column = 2, sticky = 'ew')
    Label(window, text = 'Grade 2 Dysphagia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 15, column = 2, sticky = 'ew')
    Label(window, text = 'Grade 2 Xerostomia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 16, column = 2, sticky = 'ew')
    Label(window, text = 'Grade 3 Dysphagia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 17, column = 2, sticky = 'ew')
    Label(window, text = 'Grade 3 Xerostomia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 18, column = 2, sticky = 'ew')
    Label(window, text = '\u03a3 graad 2', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 19, column = 2, sticky = 'ew')
    Label(window, text = '\u03a3 graad 3', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 20, column = 2, sticky = 'ew')
    Label(window, text = 'NTCP ' + photon_plan_name, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 14, column = 3, sticky = 'ew')
    Label(window, text = str(round(grade_2_dysphagia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 15, column = 3, sticky = 'ew')
    Label(window, text = str(round(grade_2_xerostomia_photon,1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 16, column = 3, sticky = 'ew')
    Label(window, text = str(round(grade_3_dysphagia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 17, column = 3, sticky = 'ew')
    Label(window, text = str(round(grade_3_xerostomia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 18, column = 3, sticky = 'ew')
    Label(window, text = 'NTCP ' + plan_name1, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 14, column = 4, sticky = 'ew')
    Label(window, text = str(round(grade_2_dysphagia_plan1, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 15, column = 4, sticky = 'ew')
    Label(window, text = str(round(grade_2_xerostomia_plan1, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 16, column = 4, sticky = 'ew')
    Label(window, text = str(round(grade_3_dysphagia_plan1, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 17, column = 4, sticky = 'ew')
    Label(window, text = str(round(grade_3_xerostomia_plan1, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 18, column = 4, sticky = 'ew')
    Label(window, text = 'NTCP ' + plan_name2, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 14, column = 5, sticky = 'ew')
    Label(window, text = str(round(grade_2_dysphagia_plan2, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 15, column = 5, sticky = 'ew')
    Label(window, text = str(round(grade_2_xerostomia_plan2, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 16, column = 5, sticky = 'ew')
    Label(window, text = str(round(grade_3_dysphagia_plan2, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 17, column = 5, sticky = 'ew')
    Label(window, text = str(round(grade_3_xerostomia_plan2, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 18, column = 5, sticky = 'ew')
    Label(window, text = photon_plan_name + ' - ' + plan_name1, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 14, column = 6, sticky = 'ew')
    Label(window, text = photon_plan_name + ' - ' + plan_name2, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid', width = 10).grid(row = x + y + 14, column = 7, sticky = 'ew')
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = x + y + 11, column = 2)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = x + y + 12, column = 2)
    
    
    for i in range(len(delta_ntcp1)):
        if np.isnan(delta_ntcp1[i]) == True:
            Label(window, text = 'N/A', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 15, column = 6, sticky = 'ew')
            Label(window, text = 'N/A', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 15, column = 7, sticky = 'ew')
        else:
            if delta_ntcp1[i] >= 0: 
                Label(window, text = str(delta_ntcp1[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 15, column = 6, sticky = 'ew')
            else:
                Label(window, text = str(delta_ntcp1[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 15, column = 6, sticky = 'ew')
            
            if delta_ntcp2[i] >= 0: 
                Label(window, text = str(delta_ntcp2[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 15, column = 7, sticky = 'ew')
            else:
                Label(window, text = str(delta_ntcp2[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 15, column = 7, sticky = 'ew')             
                
                
    '''Robust conformity index'''
    
    conformity_index_7000 = conformity_index(new_plan1_min, 0.94*7000, 'CTV_7000') 
    conformity_index_5425 = conformity_index(new_plan1_min, 0.94*5425, 'CTV_5425')   
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = x + y + 21, column = 2)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = x + y + 22, column = 2)
    Label(window, text = 'Robust conformity index', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 23, column = 2, columnspan = 2, sticky = 'ew')    
    Label(window, text = plan_name1, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 24, column = 2, columnspan = 2, sticky = 'ew')
    Label(window, text = 'CI CTV_7000', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 25, column = 2, sticky = 'ew')    
    Label(window, text = 'CI CTV_5425', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 26, column = 2, sticky = 'ew')
    Label(window, text = str(conformity_index_7000), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 25, column = 3, sticky = 'ew')    
    Label(window, text = str(conformity_index_5425), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 26, column = 3, sticky = 'ew') 
    
    '''Storing patient baseline'''
    store_patient_baseline([chosen_tumorlocation, chosen_xerostomie, chosen_dysfagie])              

            
    '''Store the data'''
    
    try:
        plan_mod_time1 = plan.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
    except:
        plan_mod_time1 = "Unknown"
    try:
        plan_mod_time2 = plan.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
    except:
        plan_mod_time2 = "Unknown"
    try:
        photon_plan_mod_time = photon_plan.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
    except:
        photon_plan_mod_time = photon_plan.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
               
    ntcp_labels = ['Grade 2 Dysphagia', 'Grade 2 Xerostomia', 'Grade 3 Dysphagia', 'Grade 3 Xerostomia', '\u03a3 grade 2', '\u03a3 grade 3']    
    ntcp_photon = [round(grade_2_dysphagia_photon, 1), round(grade_2_xerostomia_photon, 1), round(grade_3_dysphagia_photon, 1), round(grade_3_xerostomia_photon, 1), None, None]     
    ntcp_plan1 = [round(grade_2_dysphagia_plan1, 1), round(grade_2_xerostomia_plan1, 1), round(grade_3_dysphagia_plan1, 1), round(grade_3_xerostomia_plan1, 1), None, None]    
    ntcp_plan2 = [round(grade_2_dysphagia_plan2, 1), round(grade_2_xerostomia_plan2, 1), round(grade_3_dysphagia_plan2, 1), round(grade_3_xerostomia_plan2, 1), None, None]    
    
    all_data = [['Patient name:  ' + patient.Name, None, None, None, None, None, 'Patient ID:  ' + patient.PatientID],
                [None],
                [plan_name1 + ' last stored at:  ' + str(plan_mod_time1)],
                [plan_name2 + ' last stored at:  ' + str(plan_mod_time2)],
                [photon_plan_name + ' last stored at:  ' + str(photon_plan_mod_time)],
                [None],
                ['Nominal plan', None, None, None, None, None, 'Clinical goal evaluation', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'NTCP'],     
                [None],
                [None, None, plan_name1, plan_name2, None, None, plan_name1, None, None, None, None, None, None, None, None, None, None, None, plan_name2, None, None, None, None, None, None, None, None, None, None, None, None, None, 
                photon_plan_name, plan_name1, plan_name2, photon_plan_name + ' - ' + plan_name1, None, photon_plan_name + ' - ' + plan_name2, None, None],
                ['ROI/POI', None, 'Dose', 'Dose', '\u0394 Dose', None, 'ROI/POI', None, 'Clinical Goal', None, None, None, None, 'Voxelwise worst', None, 'Nominal result', None, None, 'ROI/POI', None, 'Clinical Goal', None, None, None, None,
                'Nominal result', None, '\u0394 Nominal result', None, None, None, None, 'NTCP', 'NTCP', 'NTCP', '\u0394 NTCP', None, '\u0394 NTCP']]
        
    for i in range(max(x,y,z)):   # x,y and z are the lenghts of the seperate lists
        if i < 6:               # tacit assumption that there are six or more clinical goals or ROIs ---> the index i will be out of range otherwise.
            if i < x and i < y and i < z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], 
                None, None, clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None, None, clinical_goal_nominal2[i], None, delta_clinical_goal_nominal_string[i], None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_plan1[i], ntcp_plan2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i < x and i < y and i >= z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], 
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_plan1[i], ntcp_plan2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i < x and i >= y and i < z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], 
                None, None, clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None, None, clinical_goal_nominal2[i], None, delta_clinical_goal_nominal_string[i], None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_plan1[i], ntcp_plan2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i < x and i >= y and i >= z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], 
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_plan1[i], ntcp_plan2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i >= x and i < y and i < z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, None, None, None, None, None, None,  None, None, None, None, 
                None, None, clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None, None, clinical_goal_nominal2[i], None, None, None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_plan1[i], ntcp_plan2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i >= x and i < y and i >= z:     
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, None, None, None, None, None, None,  None, None, None, None, 
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_plan1[i], ntcp_plan2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i >= x and i >= y and i < z:
                all_data.append([None, None, None, None, None, None, None, None, None, None, None, None,  None, None, None, None, None, None, 
                clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None, None, clinical_goal_nominal2[i], None, None, None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_plan1[i], ntcp_plan2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
        else:
            if i < x and i < y and i < z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], 
                None, None, clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None, None, clinical_goal_nominal2[i], None, delta_clinical_goal_nominal_string[i], None])
            elif i < x and i < y and i >= z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], None])
            elif i < x and i >= y and i < z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], 
                None, None, clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None, None, clinical_goal_nominal2[i], None, delta_clinical_goal_nominal_string[i], None])
            elif i < x and i >= y and i >= z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_value_string1[i], None, clinical_goal_nominal1[i], None])
            elif i >= x and i < y and i < z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, None, None, None, None, None, None,  None, None, None, None, 
                None, None, clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None, None, clinical_goal_nominal2[i], None])
            elif i >= x and i < y and i >= z:     
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None])
            elif i >= x and i >= y and i < z:
                all_data.append([None, None, None, None, None, None, None, None, None, None, None, None,  None, None, None, None, None, None, 
                clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None, None, clinical_goal_nominal2[i], None])
    
    all_data.append([None])    
    all_data.append([None])    
    all_data.append([None])    
    all_data.append([None, None, None, plan_name1])    
    all_data.append(['Conformity index CTV_7000', None, None, conformity_index_7000])
    all_data.append(['Conformity index CTV_5425', None, None, conformity_index_5425])    
    
    dashboard_storage_file = str(dashboard_storage_path / patient.PatientID) + '_' + plan_name1 + '_' + plan_name2  
    # store_dashboard_data(all_data, dashboard_storage_file)
    
    # def store_dashboard_data(all_data, dashboard_storage_file)(all_data, dashboard_storage_file): 
        # # outputpath = '\\\\zkh\\appdata\\Raystation\\Research\\ML\\Erik and Roel\\erik\\scripts\\dashboard_Hielke\\dashboard-storage\\'
        # filename = patient.PatientID + '_' + plan_name1 + '_' + plan_name2  
        # with open(dashboard_storage_path + filename + '.csv', 'w', newline = '', encoding='utf-8-sig') as file:  # utf-8-sig enables greek letters to be written to the csv
                    # writer = csv.writer(file, delimiter = ';')                                       # without the colon delimiter all data would be put in one cell in Excel   
                    # writer.writerows(all_data)
                    # # writer.writerow([None])
                    # writer.writerow([None])
                    # writer.writerow([None, None, None, plan_name1])
                    # writer.writerow(['Conformity index CTV_7000', None, None, conformity_index_7000])
                    # writer.writerow(['Conformity index CTV_5425', None, None, conformity_index_5425])
        # return
                    
    '''Buttons'''
    
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = x + y + 27, column = 2)
    Button(window, text="Close", command = master.destroy).grid(row = x + y + 28, column = 2)        
    Button(window, text='save', command = store_dashboard_data(all_data, dashboard_storage_file)).grid(row = x + y + 28, column = 4)
    Button(window, text='save and close', command = lambda:[store_dashboard_data(all_data, dashboard_storage_file), master.destroy()]).grid(row = x + y + 28, column = 6)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = x + y + 29, column = 1)                     
                    
                
                
def create_new_window_photon_photon():                
    master.withdraw()
    root = Toplevel(master, background = '#2c2c2c')
    root.geometry('1400x1000')
    root.state('zoomed')
    
    def onFrameConfigure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    style = Style()
    style.configure('TFrame', background = '#2c2c2c')
    
    canvas = Canvas(root, background = '#2c2c2c')
    window = Frame(canvas, style = 'TFrame')
    scrollbar_ver = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar_hor = Scrollbar(root, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand = scrollbar_ver.set)
    canvas.configure(xscrollcommand = scrollbar_hor.set)
    scrollbar_ver.pack(side="right", fill="y")
    scrollbar_hor.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4,4), window=window, anchor="nw")

    window.bind("<Configure>", lambda event, canvas = canvas: onFrameConfigure(canvas))
    
    plan_name1 = variable.get()
    plan_name2 = variable1.get()
    photon_plan_name = variable5.get()
   
    plan1 = case.TreatmentPlans[plan_name1]
    plan2 = case.TreatmentPlans[plan_name2]
    photon_plan = case.TreatmentPlans[photon_plan_name]  
    
    nominal_plan1 = get_doses(plan1, ROI_NAMES)
    nominal_plan2 = get_doses(plan2, ROI_NAMES)
    y = len(nominal_plan1[0])

    
    clinical_goal_passed1, clinical_goal_ROI1, clinical_goal1, clinical_goal_value1, clinical_goal_nominal1, max_width_clinical_goal_ROI1, max_width_clinical_goal1 = clinical_goal_evaluations_photon(plan1)
    clinical_goal_passed2, clinical_goal_ROI2, clinical_goal2, clinical_goal_value2, clinical_goal_nominal2, max_width_clinical_goal_ROI2, max_width_clinical_goal2 = clinical_goal_evaluations_photon(plan2) 
    
    max_width_clinical_goal2 = max(len(x) for x in clinical_goal2)
    
    #Difference between plans
    delta_clinical_goal_nominal = [x - y for x,y in zip(clinical_goal_value1, clinical_goal_value2)]
    unused, delta_clinical_goal_nominal_string = clinical_goal_evaluations_to_string_nominal(plan1, delta_clinical_goal_nominal)   

    '''Text labels'''

    Label(window, text = 'Nominal plan (average dose in cGy)', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'center', width = nominal_plan1[2] + 30).grid(row = 1, column = 2, columnspan = 4)
    Label(window, text = 'ROI/POI', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'w').grid(row = 3, column = 2, sticky = 'ew')
    Label(window, text = plan_name1, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'w').grid(row = 3, column = 3, sticky = 'ew')
    Label(window, text = plan_name2, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'w').grid(row = 3, column = 4, sticky = 'ew')
    Label(window, text = '\u0394', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border  = 0.4, relief = 'solid', anchor = 'center', width = 12).grid(row = 3, column = 5, sticky = 'ew')
    Label(window, text = 'Clinical goal evaluation', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', anchor = 'center').grid(row = y + 6, column = 2, columnspan = 5, sticky = 'ew')
    Label(window, text = 'ROI/POI', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid').grid(row = y + 9, column = 2, sticky = 'ew')
    Label(window, text = 'Clinical goal', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', anchor = 'center').grid(row = y + 9, column = 3, columnspan = 3, sticky = 'ew')
    Label(window, text = plan_name1, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', anchor = 'center').grid(row = y + 8, column = 6, sticky = 'ew')
    Label(window, text = plan_name2, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', anchor = 'center').grid(row = y + 8, column = 8, sticky = 'ew')
    Label(window, text = 'Nominal result', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid').grid(row = y + 9, column = 6, sticky = 'ew')
    Label(window, text = 'Nominal result', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = 16).grid(row = y + 9, column = 8)
    Label(window, text = '\u0394 nominal result', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', border = 0.4, relief = 'solid', width = 16).grid(row = y + 9, column = 10)
    
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = 1, column = 1)       # These 'empty' labels add some empty space, otherwise everything is put right beside each other
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = 2, column = 2)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 4, column = 2)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 5, column = 2)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 5, column = 7, sticky = 'ew')
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 5, column = 9)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = y + 7, column = 11)            
                
    '''Dose values of ROI's'''

    delta_nominal_plan1_plan2 = [elem1 - elem2 for (elem1, elem2) in zip(nominal_plan1[1], nominal_plan2[1])]
    for i in range(y):
        Label(window, text = nominal_plan1[0][i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + 4, column = 2, sticky = 'ew')
        Label(window, text = str(nominal_plan1[1][i]), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = 12, border  = 0.4, relief = 'solid').grid(row = i + 4, column = 3, sticky = 'ew')
        Label(window, text = str(nominal_plan2[1][i]), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = 12, border  = 0.4, relief = 'solid').grid(row = i + 4, column = 4, sticky = 'ew')
        if delta_nominal_plan1_plan2[i] >= 0: 
            Label(window, text = str(delta_nominal_plan1_plan2[i]), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', width = 12, border  = 0.4, relief = 'solid').grid(row = i + 4, column = 5, sticky = 'ew')
        else:
            Label(window, text = str(delta_nominal_plan1_plan2[i]), background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', width = 12, border  = 0.4, relief = 'solid').grid(row = i + 4, column = 5, sticky = 'ew')            
                
    '''clinical goals and their values plan 1'''

    x = len(plan1.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
    for i in range(x):
        Label(window, text = clinical_goal_ROI1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 2, sticky = 'ew')
        Label(window, text = clinical_goal1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 3, columnspan = 3, sticky = 'ew')
        if clinical_goal_passed1[i] == True:
            Label(window, text = clinical_goal_nominal1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#62de87', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 6, sticky = 'ew')
        else:
            Label(window, text = clinical_goal_nominal1[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#f26a52', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 6, sticky = 'ew')
            
            
    '''clinical goals and their values plan 2'''

    z = len(plan2.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
    for i in range(x): 
        if clinical_goal_passed2[i] == True:
            Label(window, text = clinical_goal_nominal2[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#62de87', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 8, sticky = 'ew')
        else:
            Label(window, text = clinical_goal_nominal2[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#f26a52', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 8, sticky = 'ew')        
            
                   
    '''delta clinical goals'''

    for i in range(max(x,z)): 
        if i < x and i < z:
            if plan1.TreatmentCourse.EvaluationSetup.EvaluationFunctions[i].PlanningGoal.GoalCriteria == 'AtMost':
                if delta_clinical_goal_nominal[i] < 0:
                    Label(window, text = delta_clinical_goal_nominal_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 10, sticky = 'ew')
                else:
                    Label(window, text = delta_clinical_goal_nominal_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 10, sticky = 'ew')
            else:
                if delta_clinical_goal_nominal[i] > 0:
                    Label(window, text = delta_clinical_goal_nominal_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 10, sticky = 'ew')
                else:
                    Label(window, text = delta_clinical_goal_nominal_string[i], background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 10, sticky = 'ew')    
        else:
            Label(window, text = 'N/A', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border = 0.4, relief = 'solid').grid(row = i + y + 10, column = 10, sticky = 'ew')
                        
    '''NTCP'''
 
    chosen_tumorlocation = variable2.get()
    chosen_xerostomie = variable3.get()
    chosen_dysfagie = variable4.get()
    grade_2_dysphagia_plan1, grade_3_dysphagia_plan1 = calculate_ntcp_dys(plan1, chosen_tumorlocation, chosen_dysfagie)
    grade_2_dysphagia_plan2, grade_3_dysphagia_plan2 = calculate_ntcp_dys(plan2, chosen_tumorlocation, chosen_dysfagie)
    grade_2_dysphagia_photon, grade_3_dysphagia_photon = calculate_ntcp_dys(photon_plan, chosen_tumorlocation, chosen_dysfagie)
    grade_2_xerostomia_plan1, grade_3_xerostomia_plan1 = calculate_ntcp_xero(case, plan1, chosen_xerostomie)
    grade_2_xerostomia_plan2, grade_3_xerostomia_plan2 = calculate_ntcp_xero(case, plan2, chosen_xerostomie)
    grade_2_xerostomia_photon, grade_3_xerostomia_photon = calculate_ntcp_xero(case, photon_plan, chosen_xerostomie)
        
    delta_ntcp1 = delta_NTCP(grade_2_dysphagia_plan1, grade_3_dysphagia_plan1, grade_2_dysphagia_photon, grade_3_dysphagia_photon, grade_2_xerostomia_plan1, grade_3_xerostomia_plan1, grade_2_xerostomia_photon, grade_3_xerostomia_photon)  
    delta_ntcp2 = delta_NTCP(grade_2_dysphagia_plan2, grade_3_dysphagia_plan2, grade_2_dysphagia_photon, grade_3_dysphagia_photon, grade_2_xerostomia_plan2, grade_3_xerostomia_plan2, grade_2_xerostomia_photon, grade_3_xerostomia_photon)
    
    
    Label(window, text = 'NTCP', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'center', border  = 0.4, relief = 'solid').grid(row = x + y + 13, column = 2, columnspan = 6, sticky = 'ew')
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11), border  = 0.4, relief = 'solid').grid(row = x + y + 14, column = 2, sticky = 'ew')
    Label(window, text = 'Grade 2 Dysphagia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 15, column = 2, sticky = 'ew')
    Label(window, text = 'Grade 2 Xerostomia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 16, column = 2, sticky = 'ew')
    Label(window, text = 'Grade 3 Dysphagia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 17, column = 2, sticky = 'ew')
    Label(window, text = 'Grade 3 Xerostomia', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 18, column = 2, sticky = 'ew')
    Label(window, text = '\u03a3 graad 2', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 19, column = 2, sticky = 'ew')
    Label(window, text = '\u03a3 graad 3', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 20, column = 2, sticky = 'ew')
    Label(window, text = 'NTCP ' + photon_plan_name, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 14, column = 3, sticky = 'ew')
    Label(window, text = str(round(grade_2_dysphagia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 15, column = 3, sticky = 'ew')
    Label(window, text = str(round(grade_2_xerostomia_photon,1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 16, column = 3, sticky = 'ew')
    Label(window, text = str(round(grade_3_dysphagia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 17, column = 3, sticky = 'ew')
    Label(window, text = str(round(grade_3_xerostomia_photon, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 18, column = 3, sticky = 'ew')
    Label(window, text = 'NTCP ' + plan_name1, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 14, column = 4, sticky = 'ew')
    Label(window, text = str(round(grade_2_dysphagia_plan1, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 15, column = 4, sticky = 'ew')
    Label(window, text = str(round(grade_2_xerostomia_plan1, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 16, column = 4, sticky = 'ew')
    Label(window, text = str(round(grade_3_dysphagia_plan1, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 17, column = 4, sticky = 'ew')
    Label(window, text = str(round(grade_3_xerostomia_plan1, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 18, column = 4, sticky = 'ew')
    Label(window, text = 'NTCP ' + plan_name2, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 14, column = 5, sticky = 'ew')
    Label(window, text = str(round(grade_2_dysphagia_plan2, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 15, column = 5, sticky = 'ew')
    Label(window, text = str(round(grade_2_xerostomia_plan2, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 16, column = 5, sticky = 'ew')
    Label(window, text = str(round(grade_3_dysphagia_plan2, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 17, column = 5, sticky = 'ew')
    Label(window, text = str(round(grade_3_xerostomia_plan2, 1)) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 18, column = 5, sticky = 'ew')
    Label(window, text = photon_plan_name + ' - ' + plan_name1, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 14, column = 6, sticky = 'ew')
    Label(window, text = photon_plan_name + ' - ' + plan_name2, background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = x + y + 14, column = 7, sticky = 'ew')
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = x + y + 11, column = 2)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = x + y + 12, column = 2)
    
    
    for i in range(len(delta_ntcp1)):
        if np.isnan(delta_ntcp1[i]) == True:
            Label(window, text = 'N/A', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 15, column = 6, sticky = 'ew')
            Label(window, text = 'N/A', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 15, column = 7, sticky = 'ew')
        else:
            if delta_ntcp1[i] >= 0: 
                Label(window, text = str(delta_ntcp1[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 15, column = 6, sticky = 'ew')
            else:
                Label(window, text = str(delta_ntcp1[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 15, column = 6, sticky = 'ew')
            
            if delta_ntcp2[i] >= 0: 
                Label(window, text = str(delta_ntcp2[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = 'white', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 15, column = 7, sticky = 'ew')
            else:
                Label(window, text = str(delta_ntcp2[i]) + ' %', background = '#2c2c2c', font = ('TkDefaultFont', 11), foreground = '#ed7207', anchor = 'w', border  = 0.4, relief = 'solid').grid(row = i + x + y + 15, column = 7, sticky = 'ew')             
                
    '''Storing patient baseline'''
    store_patient_baseline([chosen_tumorlocation, chosen_xerostomie, chosen_dysfagie])              
            
    '''Store the data'''
    
    try:
        plan_mod_time1 = plan.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
    except:
        plan_mod_time1 = "Unknown"
    try:
        plan_mod_time2 = plan.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
    except:
        plan_mod_time2 = "Unknown"
    try:
        photon_plan_mod_time = photon_plan.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
    except:
        photon_plan_mod_time = photon_plan.TreatmentCourse.TotalDose.ModificationInfo.ModificationTime
               
    ntcp_labels = ['Grade 2 Dysphagia', 'Grade 2 Xerostomia', 'Grade 3 Dysphagia', 'Grade 3 Xerostomia', '\u03a3 grade 2', '\u03a3 grade 3']    
    ntcp_photon = [round(grade_2_dysphagia_photon, 1), round(grade_2_xerostomia_photon, 1), round(grade_3_dysphagia_photon, 1), round(grade_3_xerostomia_photon, 1), None, None]     
    ntcp_plan1 = [round(grade_2_dysphagia_plan1, 1), round(grade_2_xerostomia_plan1, 1), round(grade_3_dysphagia_plan1, 1), round(grade_3_xerostomia_plan1, 1), None, None]    
    ntcp_plan2 = [round(grade_2_dysphagia_plan2, 1), round(grade_2_xerostomia_plan2, 1), round(grade_3_dysphagia_plan1, 1), round(grade_3_xerostomia_plan2, 1), None, None]    
    
    all_data = [['Patient name:  ' + patient.Name, None, None, None, None, None, 'Patient ID:  ' + patient.PatientID],
                [None],
                [plan_name1 + ' last stored at:  ' + str(plan_mod_time1)],
                [plan_name2 + ' last stored at:  ' + str(plan_mod_time2)],
                [photon_plan_name + ' last stored at:  ' + str(photon_plan_mod_time)],
                [None],
                ['Nominal plan', None, None, None, None, None, 'Clinical goal evaluation', None, None, None, None, None, None, None, None, None, None, None, None, None, 'NTCP'],     
                [None],
                [None, None, plan_name1, plan_name2, None, None, None, None, None, None, None, None, None, plan_name1, None, plan_name2, None, None, None, None, None, None, photon_plan_name, plan_name1, plan_name2, 
                photon_plan_name + ' - ' + plan_name1, None, photon_plan_name + ' - ' + plan_name2, None, None],
                ['ROI/POI', None, 'Dose', 'Dose', '\u0394 Dose', None, 'ROI/POI', None, 'Clinical Goal', None, None, None, None, 'Nominal result', None, 'Nominal result', None, '\u0394 Nominal result',
                None, None, None, None, 'NTCP', 'NTCP', 'NTCP', '\u0394 NTCP', None, '\u0394 NTCP']]
        
    for i in range(max(x,y,z)):
        if i < 6:
            if i < x and i < y and i < z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_nominal1[i], 
                None, clinical_goal_nominal2[i], None, delta_clinical_goal_nominal_string[i], None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_plan1[i], ntcp_plan2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i < x and i < y and i >= z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_nominal1[i], 
                None, None, None, None, None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_plan1[i], ntcp_plan2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i < x and i >= y and i < z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_nominal1[i], 
                None, clinical_goal_nominal2[i], None, delta_clinical_goal_nominal_string[i], None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_plan1[i], ntcp_plan2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i < x and i >= y and i >= z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_nominal1[i], 
                None, None, None, None, None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_plan1[i], ntcp_plan2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i >= x and i < y and i < z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None,  None, None, 
                None, clinical_goal_nominal2[i], None, None, None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_plan1[i], ntcp_plan2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i >= x and i < y and i >= z:     
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, None, None, None, None, None, None,  None, None, 
                None, None, None, None, None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_plan1[i], ntcp_plan2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
            elif i >= x and i >= y and i < z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None,  None, None, 
                None, clinical_goal_nominal2[i], None, None, None, None, ntcp_labels[i], None, ntcp_photon[i], ntcp_plan1[i], ntcp_plan2[i], delta_ntcp1[i], None, delta_ntcp2[i]])
        else:
            if i < x and i < y and i < z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_nominal1[i], 
                None, clinical_goal_nominal2[i], None, delta_clinical_goal_nominal_string[i], None, None])
            elif i < x and i < y and i >= z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_nominal1[i], 
                None, None])
            elif i < x and i >= y and i < z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_nominal1[i], 
                None, clinical_goal_nominal2[i], None, delta_clinical_goal_nominal_string[i], None, None])
            elif i < x and i >= y and i >= z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI1[i], None, clinical_goal1[i], None, None, None,  None, clinical_goal_nominal1[i], None, None])
            elif i >= x and i < y and i < z:
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None,  None, None, 
                None, clinical_goal_nominal2[i], None, None])
            elif i >= x and i < y and i >= z:     
                all_data.append([nominal_plan1[0][i], None, nominal_plan1[1][i], nominal_plan2[1][i], delta_nominal_plan1_plan2[i], None, None])
            elif i >= x and i >= y and i < z:
                all_data.append([None, None, None, None, None, None, clinical_goal_ROI2[i], None, clinical_goal2[i], None, None, None,  None, None, None, clinical_goal_nominal2[i], None, None])
       
    dashboard_storage_file = str(dashboard_storage_path / patient.PatientID) + '_' + plan_name1 + '_' + plan_name2  
    # store_dashboard_data(all_data, dashboard_storage_file)
    
    # def store_dashboard_data(all_data, dashboard_storage_file): 
        # # outputpath = '\\\\zkh\\appdata\\Raystation\\Research\\ML\\Erik and Roel\\erik\\scripts\\dashboard_Hielke\\dashboard-storage\\'
        # filename = patient.PatientID + '_' + plan_name1 + '_' + plan_name2  
        # with open(dashboard_storage_path + filename + '.csv', 'w', newline = '', encoding='utf-8-sig') as file:  # utf-8-sig enables greek letters to be written to the csv
                    # writer = csv.writer(file, delimiter = ';')                                       # without the colon delimiter all data would be put in one cell in Excel   
                    # writer.writerows(all_data)
        # return
                    
    '''Buttons'''
    
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = x + y + 21, column = 2)
    Button(window, text="Close", command = master.destroy).grid(row = x + y + 22, column = 2)        
    Button(window, text='save', command = store_dashboard_data(all_data, dashboard_storage_file)).grid(row = x + y + 22, column = 4)
    Button(window, text='save and close', command = lambda:[store_dashboard_data(all_data, dashboard_storage_file), master.destroy()]).grid(row = x + y + 22, column = 6)
    Label(window, text = '\t', background = '#2c2c2c', font = ('TkDefaultFont', 11)).grid(row = x + y + 23, column = 1)                           
                
                
                
                
                
                
                
                
                
                
                
                
                
                
        