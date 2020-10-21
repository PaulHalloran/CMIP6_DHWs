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

def model_in_directory(directory,model,var):
    files = glob.glob(directory+'/processed_native_grid_global'+'/'+var+'*GBR.nc')
    tmp_model_list = [file.split('/')[-1].split('_')[2] for file in files]
    return model in tmp_model_list


# def extract_ts_lat_lon(cube,site_lat_lon):
#     lat = cube.coord('latitude')
#     lon = cube.coord('longitude')
#     lat_coord1 = lat.nearest_neighbour_index(site_lat_lon[0])
#     lon_coord1 = lon.nearest_neighbour_index(site_lat_lon[1])
#     site_timeseries = cube.data[:,lat_coord1,lon_coord1].data
#     return site_timeseries

def extract_cube_dates(cube):
    iris.coord_categorisation.add_year(cube, 'time', name='year')
    iris.coord_categorisation.add_day_of_year(cube, 'time', name='year_day')



my_dict = {}
my_dict["ACCESS-CM2"] = {}
my_dict["ACCESS-CM2"]["point_locations"] = [(-13.6591, 143.500000),(-13.1882, 143.500000),(-12.7453, 143.500000),(-12.3262, 143.500000),(-11.9301, 143.500000),(-11.5520, 143.500000),(-11.1908, 143.500000),(-10.8411, 143.500000),(-10.5014, 143.500000),(-10.1662, 143.500000),(-9.8338, 143.500000),(-23.6600, 152.500000),(-19.3560, 152.500000),(-20.9920, 152.500000),(-21.8553, 152.500000),(-22.7449, 152.500000)]
# \nSea \(\d{1,2}, \d{1,2}\)

my_dict["ACCESS-ESM1-5"] = {}
my_dict["ACCESS-ESM1-5"]["point_locations"] = [(-13.6591, 143.500000),(-13.1882, 143.500000),(-12.7453, 143.500000),(-12.3262, 143.500000),(-11.9301, 143.500000),(-11.5520, 143.500000),(-11.1908, 143.500000),(-10.8411, 143.500000),(-10.5014, 143.500000),(-10.1662, 143.500000),(-9.8338, 143.500000),(-23.6600, 152.500000),(-22.7449, 152.500000),(-21.8553, 152.500000),(-20.9920, 152.500000),(-19.3560, 152.500000)]

my_dict["EC-Earth3"] = {}
my_dict["EC-Earth3"]["point_locations"] = [(-13.0790, 143.500000),(-12.2149, 143.500000),(-11.3851, 143.500000),(-10.5948, 143.500000),(-9.8494, 143.500000),(-22.4061, 152.500000),(-21.4785, 152.500000),(-19.6058, 152.500000),(-18.6621, 152.500000),(-23.3275, 152.500000)]

my_dict["EC-Earth3-Veg"] = {}
my_dict["EC-Earth3-Veg"]["point_locations"] = [(-13.0790, 143.500000),(-12.2149, 143.500000),(-11.3851, 143.500000),(-10.5948, 143.500000),(-9.8494, 143.500000),(-22.4061, 152.500000),(-21.4785, 152.500000),(-19.6058, 152.500000),(-18.6621, 152.500000),(-23.3275, 152.500000)]

my_dict["MIROC6"] = {}
my_dict["MIROC6"]["point_locations"] = [(-11.9333, 143.500000),(-10.9732, 143.500000),(-10.0432, 143.500000),(-22.7653, 152.500000),(-21.7967, 152.500000),(-20.8235, 152.500000),(-18.8639, 152.500000),(-23.7292, 152.500000)]

my_dict["NorESM2-LM"] = {}
my_dict["NorESM2-LM"]["point_locations"] = [(-12.9236, 143.500000),(-12.5989, 143.500000),(-12.2815, 143.500000),(-11.9705, 143.500000),(-11.6655, 143.500000),(-11.3660, 143.500000),(-11.0714, 143.500000),(-10.7815, 143.500000),(-10.4956, 143.500000),(-10.2136, 143.500000),(-9.9350, 143.500000),(-9.6596, 143.500000),(-22.5034, 152.500000),(-21.7999, 152.500000),(-21.1270, 152.500000),(-19.2882, 152.500000),(-18.7317, 152.500000),(-23.2368, 152.500000)]

my_dict["NorESM2-MM"] = {}
my_dict["NorESM2-MM"]["point_locations"] = [(-12.9236, 143.500000),(-12.5989, 143.500000),(-12.2815, 143.500000),(-11.9705, 143.500000),(-11.6655, 143.500000),(-11.3660, 143.500000),(-11.0714, 143.500000),(-10.7815, 143.500000),(-10.4956, 143.500000),(-10.2136, 143.500000),(-9.9350, 143.500000),(-9.6596, 143.500000),(-22.5034, 152.500000),(-21.7999, 152.500000),(-21.1270, 152.500000),(-19.2882, 152.500000),(-18.7317, 152.500000),(-23.2368, 152.500000)]

my_dict["UKESM1-0-LL"] = {}
my_dict["UKESM1-0-LL"]["point_locations"] = [(-13.0790, 143.500000),(-12.2149, 143.500000),(-11.3851, 143.500000),(-10.5948, 143.500000),(-9.8494, 143.500000),(-22.4061, 152.500000),(-21.4785, 152.500000),(-19.6058, 152.500000),(-18.6621, 152.500000),(-23.3275, 152.500000)]

my_dict["MPI-ESM1-2-LR"] = {}
my_dict["MPI-ESM1-2-LR"]["point_locations"] = [(-13.6502, 144.399748),(-12.1055, 144.531024),(-10.5468, 144.660606),(-22.0003, 153.072654),(-20.5361, 153.240649),(-18.8996, 151.834381),(-23.2918, 151.342894)]

my_dict["MPI-ESM1-2-HR"] = {}
my_dict["MPI-ESM1-2-HR"]["point_locations"] = [(-12.5332, 143.603880),(-12.1416, 143.603880),(-11.7499, 143.603880),(-11.3583, 143.603880),(-10.9667, 143.603880),(-10.5751, 143.603880),(-10.1835, 143.603880),(-9.7918, 143.603880),(-22.3260, 152.603880),(-21.9343, 152.603880),(-21.5427, 152.603880),(-21.1511, 152.603880),(-19.1929, 152.153880),(-18.8013, 152.153880),(-23.5005, 151.703880)]

base_dir = '/data/BatCaveNAS/ph290/CMIP6_william/'
tmp_dir = '/data/BatCaveNAS/ph290/CMIP6_william/tmp/'
hist_dir = base_dir+'tos_day_historical_r1i1p1f1_r1i1p1f2'
future_directories = {}
future_directories["ssp119"] = base_dir+'tos_day_ssp119_r1i1p1f1_r1i1p1f2'
future_directories["ssp126"] = base_dir+'tos_day_ssp126_r1i1p1f1_r1i1p1f2'
future_directories["ssp245"] = base_dir+'tos_day_ssp245_r1i1p1f1_r1i1p1f2'
future_directories["ssp460"] = base_dir+'tos_day_ssp460_r1i1p1f1_r1i1p1f2'
future_directories["ssp585"] = base_dir+'tos_day_ssp585_r1i1p1f1_r1i1p1f2'


models = list(my_dict)

for model in models:
# model = models[0]
    for future_directory in list(future_directories):
    # future_directory = list(future_directories)[0]
        variable = 'tos'
        # tmp_file = tmp_dir+'ofile.txt'
        # tmp_file2 = tmp_dir+'ofile2.txt'

        if model_in_directory(hist_dir,model,variable) and model_in_directory(future_directories[future_directory],model,variable):

            #######
            # _historical_GBR
            #######

            file1 = glob.glob(hist_dir+'/processed_native_grid_global'+'/'+variable+'_Oday_'+model+'_historical_GBR.nc')
            file2 = glob.glob(future_directories[future_directory]+'/processed_native_grid_global'+'/'+variable+'_Oday_'+model+'_'+future_directory+'_GBR.nc')

            c = iris.load_cube(file1)
            datetime_object = netCDF4.num2date(c.coord('time').points,c.coord('time').units.name,c.coord('time').units.calendar)
            df1 = pd.DataFrame(data=datetime_object, columns=["date"])
            c2 = c[0]
            try:
                c_data = c.data.data
            except:
                c_data = c.data

            c_ssp = iris.load_cube(file2)
            datetime_object_ssp = netCDF4.num2date(c_ssp.coord('time').points,c.coord('time').units.name,c.coord('time').units.calendar)
            datetime_object = np.concatenate((datetime_object, datetime_object_ssp))
            c2_ssp = c_ssp[0]
            try:
                c_data_ssp = c_ssp.data.data
            except:
                c_data_ssp = c_ssp.data

            df = pd.DataFrame({'date':datetime_object})

            all_lats = c2.coord('latitude').points
            all_lons = c2.coord('longitude').points
            distance_array = all_lats.data.copy()


            for lat_lon_target in my_dict[model]["point_locations"]:
                distance_array[:] = np.nan
                for i in range(np.shape(all_lats)[0]):
                    for j in range(np.shape(all_lats)[1]):
                        tmp_lat_lon = all_lats[i,j],all_lons[i,j]
                        distance_array[i,j] = dist_between_points(tmp_lat_lon,lat_lon_target)

                closest_gridcell = np.where(distance_array == np.min(distance_array))
                timeseries_at_that_location = c_data[:,closest_gridcell[0],closest_gridcell[1]]
                timeseries_at_that_location_ssp = c_data_ssp[:,closest_gridcell[0],closest_gridcell[1]]
                timeseries_at_that_location = np.concatenate((timeseries_at_that_location, timeseries_at_that_location_ssp))
                df1_2 = pd.DataFrame({'date':datetime_object, str(lat_lon_target):timeseries_at_that_location})
                df = pd.merge(df, df1_2[['date',str(site_lat_lon)]], on="date")


            df.to_csv(base_dir+'timeseries_output_no_interp/'+model+'_'+future_directory+'_timeseries.csv', index=False)

            my_dict[model][future_directory] = df
