#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Lucas Russell
Date: 18/01/2024
"""

import glob
import yaml
import pandas as pd


config = yaml.safe_load(open("config.yml"))
data_path = config['Setup']['grasp_path']
target_dir= config['Setup']['target_dir']

target_files = glob.glob(f"{target_dir}/*.y*") # .yaml or .yml

df = pd.read_csv(data_path)

def format_status(status):
    if status == 'done':
        return "$${\\color{green}\\textbf{DONE}}$$"
        # return '<span style="color:green">Done</span>'
    elif status == 'submitted':
        return "$${\\color{orange}\\textbf{SUBMITTED}}$$"
        # return '<span style="color:orange">Submitted</span>'
    elif status == 'new':
        return "$${\\color{orange}\\textbf{NEW}}$$"
        # return '<span style="color:orange">Submitted</span>'
    elif status == 'validation':
        return "$${\\color{blue}\\textbf{VALIDATION}}$$"
        # return '<span style="color:blue">Validation</span>'
    elif status == "N/A":
        return "$${\\color{red}\\textbf{MISSING}}$$"
        # return '<span style="color:red; font-weight:bold">MISSING</span>'
    else:
        return status
    
for yaml_file in target_files:
    
    out_df = pd.DataFrame()
    _names = []
    _datasets = []
    _23BPixwm_requests = []
    _23BPixwmstatus = []
    _23wm_requests = []
    _23wmstatus = []
    _multiple_requests = []
    
    
    print("************************************************************")
    print(f"\033[1mSearching for datasets in: {yaml_file}: \033[0m")
    
    n_datasets = 0 # track number of datasets in config
    n_datasets_found = 0 # track number that exist on GrASP
    
    with open(yaml_file, 'r') as file: # open the dataset list
        dataset_list = yaml.safe_load(file)
        
        # print(dataset_list)
        
        # raise RuntimeError("STOp")
        for name, dataset in dataset_list.items():
            if name=="config":
                continue
            else:
                dataset_name = dataset.split("/")[1]
                n_datasets += 1
                
                print("------------------------------------------------------------")
                print(f"Searching dataset name: \033[4m{dataset_name}\033[0m")
                
                # Search for this dataset
                search = df[df["Dataset"] == dataset_name]#["Root request status"]
                n_matches = len(search['Dataset'])
                if n_matches ==0:
                    print("\033[91m**WARNING!**\033[0m No Matches Found")
                    _names.append(name)
                    _datasets.append(dataset_name)  
                    _23BPixwm_requests.append("NONE")
                    _23BPixwmstatus.append("N/A")
                    _23wm_requests.append("NONE")
                    _23wmstatus.append("N/A")
                    # _multiple_requests.append(False)
                    
                elif n_matches >=1:
                    
                    _names.append(name)
                    _datasets.append(dataset_name)
                        
                    ## LOOK FOR BPIX AND NORMAL REQUESTS:
                    n_datasets_found += 1
                    print(f"\033[1m ** {n_matches} Matches ** \033[0m")
                    
                    found_BPix = 0
                    found_wm = 0
                    
                    for i in range(n_matches):
                        if ("23BPix" in search['Root request'].iloc[i] and not found_BPix):
                            print("DEBUG FOUND BPIX")
                            _23BPixwm_requests.append(search['Root request'].iloc[i])
                            _23BPixwmstatus.append(search['Root request status'].iloc[i])
                            found_BPix = True
                        elif ("23wm" in search['Root request'].iloc[i] and not found_wm):
                            print("DEBUG FOUND WM")
                            _23wm_requests.append(search['Root request'].iloc[i])
                            _23wmstatus.append(search['Root request status'].iloc[i])
                            found_wm = True
                            
                    if not found_BPix:
                        _23BPixwm_requests.append("NONE")
                        _23BPixwmstatus.append("N/A")
                    if not found_wm:
                        _23wm_requests.append("NONE")
                        _23wmstatus.append("N/A")
                        
                        
                        print(f"- ROOT request: {search['Root request'].iloc[i]}, Status : {search['Root request status'].iloc[i]}")
                        # _requests.append(search['Root request'].iloc[i])
                        # _status.append(search['Root request status'].iloc[i])
    
    out_df["Name"] = _names
    out_df["Dataset"] = _datasets
    
    print(_23wm_requests)
    
    
    out_df["23wm Request"] = _23wm_requests
    out_df["23wm Status"] = _23wmstatus
    out_df["23wm Status"] = out_df["23wm Status"].apply(format_status)
    
    
    out_df["23BPixwm Request"] =  _23BPixwm_requests
    out_df["23BPixwm Status"] = _23BPixwmstatus
    out_df["23BPixwm Status"] = out_df["23BPixwm Status"].apply(format_status)
    

    
    md = out_df.to_markdown(index = False)
    
    # Wrap the table in LaTeX commands to adjust font size
    latex_table = f"\\begin{{small}}\n{md}\n\\end{{small}}"

    with open(f"{config['Setup']['campaign']}/{yaml_file.split('/')[-1].split('.')[0]}.md", 'w') as f:
        f.write(latex_table)
    
    # out_df.to_csv(f"{config['Setup']['campaign']}/{yaml_file.split('/')[-1].split('.')[0]}.csv")
                        
                        
                        
    print("------------------------------------------------------------")
    print(f"\033[1;92mSUMMARY: {n_datasets_found} out of {n_datasets} located for {yaml_file.split('/')[-1]}\033[0m")
    print("************************************************************")
    print("")
    
    
