import glob
import os
import time
import numpy as np
import iris
import iris.coord_categorisation
import iris.analysis
import subprocess
import uuid
import os.path
import time
import datetime
from datetime import datetime

def model_names(directory):
    files = glob.glob(directory+'/*.nc')
    models_tmp = []
    for file in files:
        statinfo = os.stat(file)
        if statinfo.st_size >= 1:
            models_tmp.append(file.split('/')[-1].split('_')[2])
            models = np.unique(models_tmp)
    return models

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)



temporary_file_space = '/disk2/ph290/tmp/'
base_dir = '/data/BatCaveNAS/ph290/CMIP6_william/'
directs = ['tos_day_ssp119_r1i1p1f1_r1i1p1f2','tos_day_ssp460_r1i1p1f1_r1i1p1f2','tos_day_ssp585_r1i1p1f1_r1i1p1f2','tos_day_ssp245_r1i1p1f1_r1i1p1f2','tos_day_ssp126_r1i1p1f1_r1i1p1f2','tos_day_historical_r1i1p1f1_r1i1p1f2']
subdir = 'processed_native_grid'
var = 'tos'
# lonlat_box = '141.0,153.0,-25.0,-8.0'
lonlat_box = '140.0,154.0,-26.0,-7.0' # widening Ben's box by 1 degree to account for any funny thhings happening at the edges
 # e.g. -68.4,-69.1,-17.5,-18.5 == lat -17.5 -18.5 S long: -68.4 -69.1 W
# lats/lons from William: North West lat -9.475 lon 152.875, south east corner: lat -24.175 lon 141.875

daterange='1950-01-01T00:00:00,2099-12-31T00:00:00'

lock_file = base_dir+'lock_concat_extract'
touch(lock_file)

temp_file1 = str(uuid.uuid4())+'.nc'
temp_file2 = str(uuid.uuid4())+'.nc'



for direct in directs:
    print '#################################'
    print '#################################'
    print direct
    print '#################################'
    print '#################################'
    in_directory = base_dir + direct +'/'
    out_directory = base_dir + direct +'/'+subdir+'/'
    try:
        os.mkdir(out_directory)
    except:
        print 'outdir already exists'
    models = model_names(in_directory)
    for model in models:
        print model
        file_name = glob.glob(in_directory+'*_'+model+'_*')[0]
        output_filename = '_'.join(file_name.split('/')[-1].split('_')[0:4])+'_GBR.nc'
        tmp = glob.glob(out_directory+output_filename)
        if np.size(tmp) == 0:
            print 'reading in: '+model
            file_starter = '_'.join(file_name.split('/')[-1].split('_')[0:6])
            files = glob.glob(in_directory+'/'+file_starter+'*.nc')
            sizing = np.size(files)
            if not sizing == 0:
                if sizing > 1:
                    files = ' '.join(files)
                    print 'merging files'
                    subprocess.call(['cdo -P 15 mergetime '+files+' '+temporary_file_space+temp_file1], shell=True)
                if sizing == 1:
                    subprocess.call(['cp '+files[0]+' '+temporary_file_space+temp_file1], shell=True)
                print 'extracting area and range'
                subprocess.call(['cdo -P 15 -f nc4c -z zip_2 -selvar,'+var+' -seldate,'+daterange+' -sellonlatbox,'+lonlat_box+' '+temporary_file_space+temp_file1+' '+out_directory+output_filename], shell=True)
                subprocess.call('rm '+temporary_file_space+temp_file1, shell=True)
        else:
            print model,' output exists'


os.remove(lock_file)
