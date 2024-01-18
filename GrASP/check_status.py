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
    print(f"Searching for datasets in: {yaml_file}: ")
    
    with open(target_files[0], 'r') as file: # open the dataset list
        dataset_list = yaml.safe_load(file)
        
        for name, dataset in dataset_list.items():
            if name=="config":
                continue
            else:
                dataset_name = dataset.split("/")[1]
                
                print("------------------------------------------------------------")
                print(f"Searching dataset name: {dataset_name}")
                
                # Search for this dataset
                search = df[df["Dataset"] == dataset_name]#["Root request status"]
                n_matches = len(search['Dataset'])
                if n_matches ==0:
                    print("**WARNING!** No Matches Found")
                elif n_matches == 1:
                    print(f"Located Request: Status = {search['Root request status'].iloc[0]}, ROOT request: {search['Root request'].iloc[0]}")
                else:
                    print("**WARNING!** Multiple Matches, please check:")
                    for i in range(n_matches):
                        print(f"Located Request: Status = {search['Root request status'].iloc[i]}, ROOT request: {search['Root request'].iloc[i]}")
    
    print("************************************************************")
    
    