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
        return "$${\\color{green}\\textbf{Done}}$$"
        # return '<span style="color:green">Done</span>'
    elif status == 'submitted':
        return "$${\\color{orange}\\textbf{Submitted}}$$"
        # return '<span style="color:orange">Submitted</span>'
    elif status == 'new':
        return "$${\\color{orange}\\textbf{New}}$$"
        # return '<span style="color:orange">Submitted</span>'
    elif status == 'validation':
        return "$${\\color{blue}\\textbf{Validation}}$$"
        # return '<span style="color:blue">Validation</span>'
    elif status is "N/A":
        return "$${\\color{red}\\textbf{MISSING}}$$"
        # return '<span style="color:red; font-weight:bold">MISSING</span>'
    else:
        return status
    
for yaml_file in target_files:
    
    out_df = pd.DataFrame()
    _datasets = []
    _requests = []
    _status = []
    
    
    print("************************************************************")
    print(f"\033[1mSearching for datasets in: {yaml_file}: \033[0m")
    
    n_datasets = 0 # track number of datasets in config
    n_datasets_found = 0 # track number that exist on GrASP
    
    with open(yaml_file, 'r') as file: # open the dataset list
        dataset_list = yaml.safe_load(file)
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
                    _datasets.append(dataset_name)
                    _requests.append("NONE")
                    _status.append("N/A")
                elif n_matches >=1:
                    n_datasets_found += 1
                    print(f"\033[1m ** {n_matches} Matches ** \033[0m")
                    for i in range(n_matches):
                        print(f"- ROOT request: {search['Root request'].iloc[i]}, Status : {search['Root request status'].iloc[i]}")
                        _datasets.append(dataset_name)
                        _requests.append(search['Root request'].iloc[i])
                        _status.append(search['Root request status'].iloc[i])
    
    out_df["Dataset"] = _datasets
    out_df["Request"] = _requests
    out_df["Status"] = _status
    
    out_df["Status"] = out_df["Status"].apply(format_status)

    print(f"{config['Setup']['campaign']}")
    
    md = out_df.to_markdown(index = False)
    with open(f"{config['Setup']['campaign']}/{yaml_file.split('/')[-1].split('.')[0]}.md", 'w') as f:
        f.write(md)
    
    # out_df.to_csv(f"{config['Setup']['campaign']}/{yaml_file.split('/')[-1].split('.')[0]}.csv")
                        
                        
                        
    print("------------------------------------------------------------")
    print(f"\033[1;92mSUMMARY: {n_datasets_found} out of {n_datasets} located for {yaml_file.split('/')[-1]}\033[0m")
    print("************************************************************")
    print("")
    
    
