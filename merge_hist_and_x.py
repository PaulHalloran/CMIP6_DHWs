import subprocess

models = ['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','BCC-ESM1','CanESM5','CESM2-FV2','CESM2','CESM2-WACCM-FV2','CNRM-CM6-1','CNRM-CM6-1-HR','CNRM-ESM2-1','EC-Earth3','EC-Earth3-Veg','GFDL-CM4','IPSL-CM6A-LR','MIROC6','MPI-ESM-1-2-HAM','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NorESM2-LM','NorESM2-MM','SAM0-UNICON','UKESM1-0-LL']

directories = ['tos_day_ssp119_r1i1p1f1_r1i1p1f2','tos_day_ssp126_r1i1p1f1_r1i1p1f2','tos_day_ssp245_r1i1p1f1_r1i1p1f2','tos_day_ssp460_r1i1p1f1_r1i1p1f2','tos_day_ssp585_r1i1p1f1_r1i1p1f2']

for directorie in directories:
    for model in models:
        subprocess.call('cdo mergetime tos_day_'+directorie.split('_')[2]+'_r1i1p1f1_r1i1p1f2/processed/tos_Oday_'+model+'_'+directorie.split('_')[2]+'_GBR.nc tos_day_historical_r1i1p1f1_r1i1p1f2/processed/tos_Oday_'+model+'_historical_GBR.nc tos_day_'+directorie.split('_')[2]+'_r1i1p1f1_r1i1p1f2/processed/tos_Oday_'+model+'_hist_'+directorie.split('_')[2]+'_GBR.nc', shell=True)
