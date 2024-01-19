# Search through GrASP for status of Dataset production


Login to GrASP and select an era, eg:
```
https://cms-pdmv-prod.web.cern.ch/grasp/samples?campaign=Run3Summer23*GS
```

Click `Download Table: CSV` (located towards the top of the page).

Add the path to the Downloaded Table to the `grasp_path` line in the `config.yml` file. 

Create a directory and fill with yaml files that include dataset names for all the different samples. Add the path to `target_dir` in `config.yaml`.

Run `check_status.py` to check the status of every dataset in the downloaded GrASP information.
