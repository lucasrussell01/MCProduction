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
                    
                elif n_matches >= 1:
                    n_datasets_found += 1
                    print(f"\033[1m ** {n_matches} Matches ** \033[0m")
                    campaign_matched = 0 # does the located request match campaign
                    # check if matches the campaign (eg 23BPix, 23, Winter24...)
                    for i in range(n_matches):
                        vetoed = any(v in search['Root request'].iloc[i] for v in veto)
                        if (campaign in search['Root request'].iloc[i] and not campaign_matched
                            and not vetoed):
                            campaign_matched = 1
                            out_dict["Request"].append(search['Root request'].iloc[i])         
                            out_dict["Status"].append(search['Root request status'].iloc[i])
                        print(f"- ROOT request: {search['Root request'].iloc[i]}, Status : {search['Root request status'].iloc[i]}")
                    if not campaign_matched:
                        out_dict["Request"].append("NONE")
                        out_dict["Status"].append("N/A")
    
    
    # Write out information to a markdown file...
    out_df = pd.DataFrame(out_dict)
    out_df.rename(columns={'Request': f'{campaign} Request'}, inplace=True)
    out_df["Status"] = out_df["Status"].apply(format_status)
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
    
