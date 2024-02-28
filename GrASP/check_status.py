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

for yaml_file in target_files:
    
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
                elif n_matches >=1:
                    n_datasets_found += 1
                    print(f"\033[1m ** {n_matches} Matches ** \033[0m")
                    for i in range(n_matches):
                        print(f"- ROOT request: {search['Root request'].iloc[i]}, Status : {search['Root request status'].iloc[i]}")
                        
    print("------------------------------------------------------------")
    print(f"\033[1;92mSUMMARY: {n_datasets_found} out of {n_datasets} located for {yaml_file.split('/')[-1]}\033[0m")
    print("************************************************************")
    print("")
    
    
