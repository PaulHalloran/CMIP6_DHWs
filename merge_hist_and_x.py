import os
import os.path
import subprocess

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


models = ['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','BCC-ESM1','CanESM5','CESM2-FV2','CESM2','CESM2-WACCM-FV2','CNRM-CM6-1','CNRM-CM6-1-HR','CNRM-ESM2-1','EC-Earth3','EC-Earth3-Veg','GFDL-CM4','IPSL-CM6A-LR','MIROC6','MPI-ESM-1-2-HAM','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NorESM2-LM','NorESM2-MM','SAM0-UNICON','UKESM1-0-LL']

directories = ['tos_day_ssp119_r1i1p1f1_r1i1p1f2','tos_day_ssp126_r1i1p1f1_r1i1p1f2','tos_day_ssp245_r1i1p1f1_r1i1p1f2','tos_day_ssp460_r1i1p1f1_r1i1p1f2','tos_day_ssp585_r1i1p1f1_r1i1p1f2']

basedir = '/data/BatCaveNAS/ph290/CMIP6_william/'
lock_file = basedir+'lock_merge_hist_and_x'
touch(lock_file)

for directorie in directories:
        for model in models:
                    if not(os.path.exists(basedir+'tos_day_'+directorie.split('_')[2]+'_r1i1p1f1_r1i1p1f2/processed/tos_Oday_'+model+'_hist_'+directorie.split('_')[2]+'_GBR.nc')):
                                    subprocess.call('cdo mergetime '+basedir+'tos_day_'+directorie.split('_')[2]+'_r1i1p1f1_r1i1p1f2/processed/tos_Oday_'+model+'_'+directorie.split('_')[2]+'_GBR.nc '+basedir+'tos_day_historical_r1i1p1f1_r1i1p1f2/processed/tos_Oday_'+model+'_historical_GBR.nc '+basedir+'tos_day_'+directorie.split('_')[2]+'_r1i1p1f1_r1i1p1f2/processed/tos_Oday_'+model+'_hist_'+directorie.split('_')[2]+'_GBR.nc', shell=True)

for directorie in directories:
    for model in models:
        if not(os.path.exists(basedir+'tos_day_'+directorie.split('_')[2]+'_r1i1p1f1_r1i1p1f2/processed/tos_Oday_'+model+'_hist_'+directorie.split('_')[2]+'.nc')):
            subprocess.call('cdo mergetime '+basedir+'tos_day_'+directorie.split('_')[2]+'_r1i1p1f1_r1i1p1f2/processed/tos_Oday_'+model+'_'+directorie.split('_')[2]+'.nc '+basedir+'tos_day_historical_r1i1p1f1_r1i1p1f2/processed/tos_Oday_'+model+'_historical.nc '+basedir+'tos_day_'+directorie.split('_')[2]+'_r1i1p1f1_r1i1p1f2/processed/tos_Oday_'+model+'_hist_'+directorie.split('_')[2]+'.nc', shell=True)

os.remove(lock_file)


