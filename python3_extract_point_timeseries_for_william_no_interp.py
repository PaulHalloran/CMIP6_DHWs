#Note there might be some relic code here from the version that quickly pulled out the results interpolated to a specific lat/lon which I've not had a chance to remove and retest.

import numpy as np
import iris
import pandas as pd
import glob
import iris.coord_categorisation
import netCDF4
import subprocess
import os
import os.path
import math

#function to approx. calculate the distance between two lat/lons used later to map out the nearest grid box to a (i.e. the grid box containing) specified lat/lon.
def dist_between_points(lat_lon1,lat_lon2):
    R = 6373.0
    lat1 = math.radians(lat_lon1[0])
    lon1 = math.radians(lat_lon1[1])
    lat2 = math.radians(lat_lon2[0])
    lon2 = math.radians(lat_lon2[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

#Function to get a list of model names from available files
def model_in_directory(directory,model,var):
    files = glob.glob(directory+'/processed_native_grid_global'+'/'+var+'*GBR.nc')
    tmp_model_list = [file.split('/')[-1].split('_')[2] for file in files]
    return model in tmp_model_list


#Dictionary containing all of the lat/lon pairs from Ben for each CMIP model.
my_dict = {}
my_dict["ACCESS-CM2"] = {}
my_dict["ACCESS-CM2"]["point_locations"] = [(-9.8338, 143.500000),(-10.1662, 143.500000),(-10.5014, 143.500000),(-10.8411, 143.500000),(-11.1908, 143.500000),(-19.3560, 152.500000),(-20.9920, 152.500000),(-21.8553, 152.500000),(-23.6600, 151.500000)]
# \nSea \(\d{1,2}, \d{1,2}\)
# \)\n \(----------------->) (
#\n \(----------------->\n[(
#\) \(----------------->),(
#\)$----------------->)]
my_dict["ACCESS-ESM1-5"] = {}
my_dict["ACCESS-ESM1-5"]["point_locations"] = [(-9.8338, 143.500000),(-10.1662, 143.500000),(-10.5014, 143.500000),(-10.8411, 143.500000),(-11.1908, 143.500000),(-19.3560, 152.500000),(-20.9920, 152.500000),(-21.8553, 152.500000),(-23.6600, 151.500000)]

my_dict["CanESM5"] = {}
my_dict["CanESM5"]["point_locations"] = [(-9.8494, 143.500000),(-10.5948, 143.500000),(-11.3851, 143.500000),(-18.6621, 152.500000),(-21.4785, 152.500000),(-22.4061, 152.500000),(-23.3275, 151.500000)]

my_dict["EC-Earth3"] = {}
my_dict["EC-Earth3"]["point_locations"] = [(-9.8494, 143.500000),(-10.5948, 143.500000),(-11.3851, 143.500000),(-18.6621, 152.500000),(-21.4785, 152.500000),(-22.4061, 152.500000),(-23.3275, 151.500000)]

my_dict["EC-Earth3-Veg"] = {}
my_dict["EC-Earth3-Veg"]["point_locations"] = [(-9.8494, 143.500000),(-10.5948, 143.500000),(-11.3851, 143.500000),(-18.6621, 152.500000),(-21.4785, 152.500000),(-22.4061, 152.500000),(-23.3275, 151.500000)]

my_dict["MIROC6"] = {}
my_dict["MIROC6"]["point_locations"] = [(-10.0432, 143.500000),(-10.9732, 143.500000),(-18.8639, 152.500000),(-21.7967, 152.500000),(-23.7292, 152.500000)]

my_dict["NorESM2-LM"] = {}
my_dict["NorESM2-LM"]["point_locations"] = [(-9.9350, 143.500000),(-10.2136, 143.500000),(-10.4956, 143.500000),(-11.0714, 143.500000),(-19.2882, 152.500000),(-21.1270, 152.500000),(-21.7999, 152.500000),(-23.2368, 151.500000)]

my_dict["NorESM2-MM"] = {}
my_dict["NorESM2-MM"]["point_locations"] = [(-9.9350, 143.500000),(-10.2136, 143.500000),(-10.4956, 143.500000),(-11.0714, 143.500000),(-19.2882, 152.500000),(-21.1270, 152.500000),(-21.7999, 152.500000),(-23.2368, 151.500000)]

my_dict["UKESM1-0-LL"] = {}
my_dict["UKESM1-0-LL"]["point_locations"] = [(-9.8494, 143.500000),(-10.5948, 143.500000),(-11.3851, 143.500000),(-18.6621, 152.500000),(-21.4785, 152.500000),(-22.4061, 152.500000),(-23.3275, 151.500000)]

my_dict["MPI-ESM1-2-LR"] = {}
my_dict["MPI-ESM1-2-LR"]["point_locations"] = [(-10.5468, 144.660606),(-10.4231, 143.071836),(-18.8996, 151.834381),(-20.3818, 151.672219),(-22.0003, 153.072654),(-23.2918, 151.342894)]

my_dict["MPI-ESM1-2-HR"] = {}
my_dict["MPI-ESM1-2-HR"]["point_locations"] = [(-10.9666, 143.153880),(-10.5751, 143.603880),(-10.1835, 143.603880),(-9.7919, 144.053880),(-19.1929, 152.153880),(-21.1510, 152.153880),(-21.5426, 152.153880),(-21.5427, 152.603880),(-22.3260, 152.603880),(-23.5005, 151.703880)]

base_dir = '/data/BatCaveNAS/ph290/CMIP6_william/'
tmp_dir = '/data/BatCaveNAS/ph290/CMIP6_william/tmp/'
hist_dir = base_dir+'tos_day_historical_r1i1p1f1_r1i1p1f2'
future_directories = {}
future_directories["ssp119"] = base_dir+'tos_day_ssp119_r1i1p1f1_r1i1p1f2'
future_directories["ssp126"] = base_dir+'tos_day_ssp126_r1i1p1f1_r1i1p1f2'
future_directories["ssp245"] = base_dir+'tos_day_ssp245_r1i1p1f1_r1i1p1f2'
future_directories["ssp460"] = base_dir+'tos_day_ssp460_r1i1p1f1_r1i1p1f2'
future_directories["ssp585"] = base_dir+'tos_day_ssp585_r1i1p1f1_r1i1p1f2'

#get a list of models with lats/lons specified by Ben
models = list(my_dict)
# models = ['EC-Earth3', 'MPI-ESM1-2-HR', 'UKESM1-0-LL', 'EC-Earth3-Veg', 'CanESM5', 'MIROC6', 'MPI-ESM1-2-LR', 'ACCESS-ESM1-5', 'NorESM2-LM', 'NorESM2-MM', 'ACCESS-CM2']

# loop through models one by one
for model in models:
# model = models[0]
    print(model)
    # loop through future scenarios (SPCs)
    for future_directory in list(future_directories):
    # future_directory = list(future_directories)[0]
        print(future_directory)
        # define variable of interest (included for future flexability)
        variable = 'tos'
        # tmp_file = tmp_dir+'ofile.txt'
        # tmp_file2 = tmp_dir+'ofile2.txt'

        # check if model has both historical (<= 2015) and future (> 2015) data for that scenario files avalable
        if model_in_directory(hist_dir,model,variable) and model_in_directory(future_directories[future_directory],model,variable):
            print('input files exist')
            #check if output file exists (and skip if it does)
            test = os.path.exists(base_dir+'timeseries_output_no_interp/'+model+'_'+future_directory+'_timeseries.csv')
            if not(test):
                print('output file does not exist')
                print('processing '+str(model)+' '+str(future_directory))
                #######
                # _historical_GBR
                #######

                #get file names
                file1 = glob.glob(hist_dir+'/processed_native_grid_global'+'/'+variable+'_Oday_'+model+'_historical_GBR.nc')
                file2 = glob.glob(future_directories[future_directory]+'/processed_native_grid_global'+'/'+variable+'_Oday_'+model+'_'+future_directory+'_GBR.nc')

                #load historial netcdf file metadata with scitools iris (https://scitools.org.uk/iris/docs/latest/)
                c = iris.load_cube(file1)
                #fill out date/time data
                datetime_object = netCDF4.num2date(c.coord('time').points,c.coord('time').units.name,c.coord('time').units.calendar)
                # relic of old code I think: initialise a pandas dataframe with the date data into which temperature data for each model can go.
                df1 = pd.DataFrame(data=datetime_object, columns=["date"])
                #take just the 1st day form the netcdf file from which we can quickly work out the x-y index matching teh lat/lon of interest.
                c2 = c[0]
                #relic code... hit memory problems, so had to find alternatives
                # try:
                #     c_data = c.data.data
                # except:
                #     c_data = c.data

                # as above but for the future model output
                c_ssp = iris.load_cube(file2)
                datetime_object_ssp = netCDF4.num2date(c_ssp.coord('time').points,c.coord('time').units.name,c.coord('time').units.calendar)
                c2_ssp = c_ssp[0]
                #relic code... hit memory problems, so had to find alternatives
                # try:
                #     c_data_ssp = c_ssp.data.data
                # except:
                #     c_data_ssp = c_ssp.data

                # combine the dates from the historical and future model output to initialise a pandas a rray into which the SST data fro each locatoin can be added
                datetime_object = np.concatenate((datetime_object, datetime_object_ssp))
                df = pd.DataFrame({'date':datetime_object})

                #pull the lat and lon m,etadata out of the netcdf file
                all_lats = c2.coord('latitude').points
                all_lons = c2.coord('longitude').points
                #make a 2D array to hold the distances of each grid point from the la/lon of interest, so we can identify the minimum distance and therefore correct grid cell. This seems like a strange way of doing things, but it wa sa practical way around the issues associated with irregular grid boxes (i.e. not paralleling lat/lon lines)
                distance_array = all_lats.data.copy()

                #Fill the distances array described above
                for lat_lon_target in my_dict[model]["point_locations"]:
                    print(my_dict[model]["point_locations"])
                    print(lat_lon_target)
                    distance_array[:] = np.nan
                    for i in range(np.shape(all_lats)[0]):
                        for j in range(np.shape(all_lats)[1]):
                            tmp_lat_lon = all_lats[i,j],all_lons[i,j]
                            distance_array[i,j] = dist_between_points(tmp_lat_lon,lat_lon_target)
                    closest_gridcell = np.where(distance_array == np.min(distance_array))
                    #relic code...
                    # closest_gridcell_linear =  np.where(np.reshape(distance_array,np.shape(distance_array)[1]*np.shape(distance_array)[0]) == np.min(distance_array))[0][0]
                    # timeseries_at_that_location = c[:,closest_gridcell[0],closest_gridcell[1]][:,0,0]
                    # timeseries_at_that_location = c_data[:,closest_gridcell[0],closest_gridcell[1]]
                    # timeseries_at_that_location_ssp = c_data_ssp[:,closest_gridcell[0],closest_gridcell[1]]
                    # timeseries_at_that_location_ssp = c_ssp[:,closest_gridcell[0],closest_gridcell[1]][:,0,0]
                    # the try is used here because some the data is read in from some of teh models as a masked array, and some as a non-masked array. We just want the data component, not the mask. This is got at in iris with .data.data if there is a mask, and .data is there is no mask.
                    print('reading in historical data')
                    try:
                        # pulls out the timeseries from the index identified as corresponding to thet lat and lon. NOTE THIS IS THE SLOW BIT. Iris uses dask to avoid having to read in the full data array from the netcdf file (https://scitools.org.uk/iris/docs/latest/userguide/real_and_lazy_data.html). This is great, but it is insanely slow. William, says xarray might do a better job?
                        timeseries_at_that_location = c[:,closest_gridcell[0],closest_gridcell[1]][:,0,0].data.data
                        #relic code...
                        # print "cdo --reduce_dim -selgridcell,"+str(closest_gridcell[1][0])+","+str(closest_gridcell[0][0])+" "+file1[0]+" output_001.nc"
                        # print "cdo --reduce_dim -selgridcell,"+str(closest_gridcell_linear)+" "+file1[0]+" output_001.nc"
                        # cdo -selgridcell,44235 /data/BatCaveNAS/ph290/CMIP6_william/tos_day_historical_r1i1p1f1_r1i1p1f2/processed_native_grid_global/tos_Oday_EC-Earth3_historical_GBR.nc output_002.nc
                        # cdo -outputtab,date,lon,lat,value output_001.nc > output_001.csv
                    except:
                        #as above but for where the data comes in without a mask
                        timeseries_at_that_location = c[:,closest_gridcell[0],closest_gridcell[1]][:,0,0].data
                    print('reading in ssp data')
                    try:
                        #as above within the try/except but for the future data not the historical
                        timeseries_at_that_location_ssp = c_ssp[:,closest_gridcell[0],closest_gridcell[1]][:,0,0].data.data
                    except:
                        timeseries_at_that_location_ssp = c_ssp[:,closest_gridcell[0],closest_gridcell[1]][:,0,0].data
                    print('concatenate the historical and future data')
                    timeseries_at_that_location = np.concatenate((timeseries_at_that_location, timeseries_at_that_location_ssp))
                    print('put the above data alongside its date data into a pandas dataframe')
                    df1_2 = pd.DataFrame({'date':datetime_object, str(lat_lon_target):np.reshape(timeseries_at_that_location,np.shape(timeseries_at_that_location)[0])})
                    print('slot the above data into the right dates in the dataframe which is holding the data for all of the diggreent geographical points (doing thsi way in case the date range of any of the futrure scenario netcdf files are different from each other)')
                    df = pd.merge(df, df1_2[['date',str(lat_lon_target)]], on="date")

                #write results out to file - note this is why I'm using pandas dataframes - it makes the writing to csv simple and flexible (in case you guys wanted it in a diffreent format!).
                df.to_csv(base_dir+'timeseries_output_no_interp/'+model+'_'+future_directory+'_timeseries.csv', index=False)

                # add results to dictionary to allow interactive interogation
                my_dict[model][future_directory] = df
