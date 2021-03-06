import iris
import iris.coord_categorisation
import matplotlib.pyplot as plt
import numpy as np
import iris.quickplot as qplt
import netCDF4
import datetime
import scipy
import scipy.signal
import glob
import cartopy.feature as cfeature
from scipy.stats import t
import pickle
import os
import glob
from mpl_toolkits.axes_grid1 import AxesGrid
from cartopy.mpl.geoaxes import GeoAxes
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import os
import os.path
    import time
    from datetime import datetime

    basedir = '/data/BatCaveNAS/ph290/CMIP6_william/'
    lock_file = basedir+'lock_merge_hist_and_x'

    while os.path.exists(lock_file):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        print 'waiting '
        time.sleep(30.0)

def linregress_3D(y_array):
    # y_array is a 3-D array formatted like (time,lon,lat)
    # The purpose of this function is to do linear regression using time series of data over each (lon,lat) grid box with consideration of ignoring np.nan
    # Construct x_array indicating time indexes of y_array, namely the independent variable.
    x_array=np.empty(y_array.shape)
    for i in range(y_array.shape[0]): x_array[i,:,:]=i+1 # This would be fine if time series is not too long. Or we can use i+yr (e.g. 2019).
    x_array[np.isnan(y_array)]=np.nan
    # Compute the number of non-nan over each (lon,lat) grid box.
    n=np.sum(~np.isnan(x_array),axis=0)
    # Compute mean and standard deviation of time series of x_array and y_array over each (lon,lat) grid box.
    x_mean=np.nanmean(x_array,axis=0)
    y_mean=np.nanmean(y_array,axis=0)
    x_std=np.nanstd(x_array,axis=0)
    y_std=np.nanstd(y_array,axis=0)
    # Compute co-variance between time series of x_array and y_array over each (lon,lat) grid box.
    cov=np.nansum((x_array-x_mean)*(y_array-y_mean),axis=0)/n
    # Compute correlation coefficients between time series of x_array and y_array over each (lon,lat) grid box.
    cor=cov/(x_std*y_std)
    # Compute slope between time series of x_array and y_array over each (lon,lat) grid box.
    slope=cov/(x_std**2)
    # Compute intercept between time series of x_array and y_array over each (lon,lat) grid box.
    intercept=y_mean-x_mean*slope
    # Compute tstats, stderr, and p_val between time series of x_array and y_array over each (lon,lat) grid box.
    tstats=cor*np.sqrt(n-2)/np.sqrt(1-cor**2)
    stderr=slope/tstats
    p_val=t.sf(tstats,n-2)*2
    # Compute r_square and rmse between time series of x_array and y_array over each (lon,lat) grid box.
    # r_square also equals to cor**2 in 1-variable lineare regression analysis, which can be used for checking.
    r_square=np.nansum((slope*x_array+intercept-y_mean)**2,axis=0)/np.nansum((y_array-y_mean)**2,axis=0)
    rmse=np.sqrt(np.nansum((y_array-slope*x_array-intercept)**2,axis=0)/n)
    # Do further filteration if needed (e.g. We stipulate at least 3 data records are needed to do regression analysis) and return values
    n=n*1.0 # convert n from integer to float to enable later use of np.nan
    n[n<3]=np.nan
    slope[np.isnan(n)]=np.nan
    intercept[np.isnan(n)]=np.nan
    p_val[np.isnan(n)]=np.nan
    r_square[np.isnan(n)]=np.nan
    rmse[np.isnan(n)]=np.nan
#     return n,slope,intercept,p_val,r_square,rmse
    return slope,intercept


def mmm_skirving(cube):
    cube = cube.aggregated_by(['year','month'], iris.analysis.MEAN)
    print 'calculating NOAA Skirving MMM for month:'
#     missing_data_value_greater_than = -32768.0
#     missing_data_equals = -32768.0
    missing_data_equals = cube.data.fill_value
    years_for_mmm_climatology = [1985,2012]
    standardisation_date = 1988.2857
    mm_cube = cube[0:12].copy()
    mm_cube_data = mm_cube.data.copy()
    cube_years = cube.coord('year').points
    #subset the data into the bit you want to use to calculate the MMM climatology and the bit you want to calculate DHW on
    clim_cube = cube[np.where((cube_years >= years_for_mmm_climatology[0]) & (cube_years <= years_for_mmm_climatology[1]))]
    clim_cube_detrended = clim_cube.copy()
    clim_cube_detrended_data = clim_cube_detrended.data
    print np.shape(clim_cube_detrended)
    for i,month in enumerate(np.unique(cube.coord('month_number').points)):
        print i+1
        loc = np.where(clim_cube.coord('month_number').points == month)
        tmp = clim_cube_detrended_data[loc,:,:][0]
        tmp[np.where(tmp == missing_data_equals )] = np.nan
        slope,intercept = linregress_3D(tmp)
        x = standardisation_date - years_for_mmm_climatology[0]
        y = (slope * x ) + intercept
        mm_cube_data[i,:,:] = y
    mm_cube.data = mm_cube_data
    mmm_climatology = mm_cube.collapsed('time',iris.analysis.MAX)
    return mmm_climatology


def dhw(cube,mmm_climatology,years_over_which_to_calculate_dhw):
    cube_years = cube.coord('year').points
    #note this is to be uef with daily data...
    main_cube = cube[np.where((cube_years > years_over_which_to_calculate_dhw[0]) & (cube_years < years_over_which_to_calculate_dhw[1]))]
    #subtract the monthly mean climatology from the rest of the data
    try:
        main_cube.remove_coord('month_number')
        main_cube.remove_coord('month')
        main_cube.remove_coord('year')
    except:
        pass
    main_cube -= mmm_climatology
    #set all values less than 1 to zero
    main_cube.data[np.where(main_cube.data < 1.0)] = 0.0
    #make a cube to hold the output data
    output_cube = main_cube[83::].copy()
    output_cube.data[:] = np.nan
    output_cube_data = output_cube.data.copy()
    #loop through from day 84 to the end of the dataset
    for i in range(output_cube.shape[0]):
#         print i,' of ',output_cube.shape[0]
        #sum the temperatures in that 84 day window and divide result by 7 to get in DHWeeks rather than DHdays
        tmp_data = main_cube[i:i+84].collapsed('time',iris.analysis.SUM)/7.0
        output_cube_data[i,:,:] = tmp_data.data
    #save the output
    output_cube.data = output_cube_data
    return output_cube


models = ['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','BCC-ESM1','CanESM5','CESM2-FV2','CESM2','CESM2-WACCM-FV2','CNRM-CM6-1','CNRM-CM6-1-HR','CNRM-ESM2-1','EC-Earth3','EC-Earth3-Veg','GFDL-CM4','IPSL-CM6A-LR','MIROC6','MPI-ESM-1-2-HAM','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NorESM2-LM','NorESM2-MM','SAM0-UNICON','UKESM1-0-LL']
directories = ['tos_day_ssp119_r1i1p1f1_r1i1p1f2','tos_day_ssp126_r1i1p1f1_r1i1p1f2','tos_day_ssp245_r1i1p1f1_r1i1p1f2','tos_day_ssp460_r1i1p1f1_r1i1p1f2','tos_day_ssp585_r1i1p1f1_r1i1p1f2']
base_directory = '/data/BatCaveNAS/ph290/CMIP6_william/'
years_over_which_to_calculate_dhw = [1950,2100]

for directorie in directories:
    print directorie
    models = ['MRI-ESM2-0']
    for model in models:
        print model
        file = base_directory+'tos_day_'+directorie.split('_')[2]+'_r1i1p1f1_r1i1p1f2/processed/tos_Oday_'+model+'_hist_'+directorie.split('_')[2]+'_GBR.nc'
        print file
        if os.path.exists(file):
            output_filename = base_directory+'tos_day_'+directorie.split('_')[2]+'_r1i1p1f1_r1i1p1f2/processed/dhw_Oday_'+model+'_hist_'+directorie.split('_')[2]+'_GBR.nc'
            output_filename2 = base_directory+'tos_day_'+directorie.split('_')[2]+'_r1i1p1f1_r1i1p1f2/processed/dhw_Oday_'+model+'_hist_'+directorie.split('_')[2]+'_GBR_ann_max.nc'
            mmm_file = base_directory+'tos_day_historical_r1i1p1f1_r1i1p1f2/processed/'+model+'_mmm.nc'
            test1 = os.path.exists(output_filename)
            test2 = os.path.exists(output_filename2)
            if not(test1) and not(test2):
                print 'reading in file'
                cube = iris.load_cube(file)
                try:
                    iris.coord_categorisation.add_year(cube, 'time', name='year')
                except:
                    pass
                try:
                    iris.coord_categorisation.add_month(cube, 'time', name='month')
                except:
                    pass
                try:
                    iris.coord_categorisation.add_month_number(cube, 'time', name='month_number')
                except:
                    pass
                if not(os.path.exists(mmm_file)):
                    print 'calculating mmm_climatology'
                    mmm_climatology = mmm_skirving(cube)
                    iris.fileformats.netcdf.save(mmm_climatology, mmm_file)
                else:
                    print 'reading in mmm_climatology'
                    mmm_climatology = iris.load_cube(mmm_file)
                print 'calculating DHW'
                dhw_cube = dhw(cube,mmm_climatology,years_over_which_to_calculate_dhw)
                cube = iris.load_cube(file)
                try:
                    iris.coord_categorisation.add_year(dhw_cube, 'time', name='year')
                except:
                    pass
                dhw_cube_max = dhw_cube.aggregated_by('year',iris.analysis.MAX)
                print 'saving file'
                iris.fileformats.netcdf.save(dhw_cube, output_filename)
                iris.fileformats.netcdf.save(dhw_cube_max, output_filename2)
            else:
                print 'output already exists'
        else:
            print 'file does not exist'
