#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Lucas Russell
Date: 18/01/2024
"""

import glob
import yaml
import pandas as pd
from utils import format_status
import os
import numpy as np

# Config specifying paths and campaign
config = yaml.safe_load(open("config.yml"))
base_path = config['Setup']['base_dir']
data_path = f"{base_path}/{config['Setup']['grasp_file']}"
target_dir= f"{base_path}/{config['Setup']['target_dir']}"
campaign = config['Setup']['campaign']
veto = config['Setup']['veto'] # list of campaigns to veto

# Find target files (yaml file lists)
target_files = glob.glob(f"{target_dir}/*.y*") # .yaml or .yml

# Dataframe storing request statuses on GrASP
GrASP_info = pd.read_csv(data_path)


filter_v15_only = True # only look for nanov15
if filter_v15_only:
    print('WARNING: Filtering Nanov15 outputs')
    print(f'N entries before: {len(GrASP_info)}')
    if filter_v15_only:
        GrASP_info['NanoAOD output'] = GrASP_info['NanoAOD output'].fillna("NONE")
        GrASP_info = GrASP_info[GrASP_info['NanoAOD output'].str.contains("NanoAODv15", na=False)]
    print(f'N entries after: {len(GrASP_info)}')

for yaml_file in target_files:
    
    # Dictionary to store each dataset request info
    out_dict = {"Name": [], "Dataset": [], "Request": [], "Status": []}
    
    print("************************************************************")
    print(f"\033[1mSearching GrASP for datasets in: {yaml_file}: \033[0m")
    
    n_datasets = 0 # track number of datasets in config
    n_datasets_found = 0 # track number that have existing request on GrASP
    
    with open(yaml_file, 'r') as file: 
        
        dataset_list = yaml.safe_load(file) # open the dataset list
        
        for name, dataset in dataset_list.items():
            if name=="config":
                continue
            elif 'ext' in name:
                continue
            else:
                dataset_name = dataset.split("/")[1]
                n_datasets += 1
                
                print("------------------------------------------------------------")
                print(f"Searching dataset name: \033[4m{dataset_name}\033[0m")
                
                # Check if request exists
                search = GrASP_info[GrASP_info["Dataset"] == dataset_name]
                n_matches = len(search['Dataset'])
                
                out_dict["Name"].append(name)
                out_dict["Dataset"].append(dataset_name)

                if n_matches == 0:
                    print("\033[91m**WARNING!**\033[0m No Matches Found")
                    out_dict["Request"].append("NONE")
                    out_dict["Status"].append("N/A")
                    
                elif n_matches == 1:
                    n_datasets_found += 1
                    print(f"\033[1m ** Found 1 Match ** \033[0m")
                    out_dict["Request"].append(search['Root request'].iloc[0])
                    out_dict["Status"].append(search['Root request status'].iloc[0])
                    print(f"- ROOT request: {search['Root request'].iloc[0]}, Status : {search['Root request status'].iloc[0]}")

                elif n_matches > 1:
                    # find most advanced request
                    status_order = ['new', 'validation', 'defined', 'submitted', 'done']
                    most_advanced_status = max(np.array(search['Root request status']), key=lambda x: status_order.index(x))
                    most_advanced_index = np.argmax([status_order.index(s) for s in np.array(search['Root request status'])])

                    out_dict["Request"].append(search['Root request'].iloc[most_advanced_index])
                    out_dict["Status"].append(search['Root request status'].iloc[most_advanced_index])
                    print(f"Most advanced status: {most_advanced_status}, Request: {search['Root request'].iloc[most_advanced_index]}")

                else:
                    out_dict["Request"].append("NONE")
                    out_dict["Status"].append("N/A")

    
    # Write out information to a markdown file...
    out_df = pd.DataFrame(out_dict)
    out_df.rename(columns={'Request': f'{campaign} Request'}, inplace=True)
    out_df["Status"] = out_df["Status"].apply(format_status)
    # for d in out_df['Dataset']:
    #     print(d)
    out_md = out_df.to_markdown(index = False)
    out_path = f"{base_path}/{campaign}"
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    with open(f"{out_path}/{yaml_file.split('/')[-1].split('.')[0]}.md", 'w') as f:
        f.write(out_md)
    
    # Print summary                 
    print("------------------------------------------------------------")
    print(f"\033[1;92mSUMMARY: {n_datasets_found} out of {n_datasets} located for {yaml_file.split('/')[-1]}\033[0m")
    print("************************************************************")
    print("")
    
