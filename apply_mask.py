import iris
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import numpy as np

basedir = '/data/BatCaveNAS/ph290/CMIP6_william/'
mask_file = 'reef_mask.nc3.nc'

#load in the reef data and put into cube
# North West
# lat -9.475
# lon 152.875
# south east corner:
# lat -24.175
# lon 141.875
latitude = iris.coords.DimCoord(np.arange(-24.175,  -9.475, 0.05),
standard_name='latitude', units='degrees')
longitude = iris.coords.DimCoord(np.arange(141.875, 152.875, 0.05),
standard_name='longitude', units='degrees')
new_mask_cube = iris.cube.Cube(np.zeros((len(np.arange(-24.175,  -9.475, 0.05)), len(np.arange(141.875, 152.875, 0.05))),
np.float32),standard_name='sea_surface_temperature',
long_name='Sea Surface Temperature', var_name='tos',
units='K',dim_coords_and_dims=[(latitude, 0), (longitude, 1)])
new_mask_cube.data = np.flipud(mask_cube.data)
new_mask_cube_copy = new_mask_cube.copy()

#resam ple 5km reef mack to cmip grid
file = 'tos_day_ssp119_r1i1p1f1_r1i1p1f2/processed/dhw_Oday_MRI-ESM2-0_hist_ssp119_GBR_ann_max.nc'

mask_cube = iris.load_cube(basedir+mask_file)

cube = iris.load_cube(basedir+file)
outmask = cube[0].copy()
outmask.data[:] = np.nan
outmask.data.mask[:] = False

xx, yy = np.meshgrid(new_mask_cube.coord('longitude').points, new_mask_cube.coord('latitude').points)
loc = np.isfinite(new_mask_cube.data.data)
ref_lons = xx[loc]
ref_lats = yy[loc]

lat = cube.coord('latitude')
lon = cube.coord('longitude')
for i,dummy in enumerate(ref_lons):
    print i
    lat_coord1 = lat.nearest_neighbour_index(ref_lats[i])
    lon_coord1 = lon.nearest_neighbour_index(ref_lons[i])
    outmask.data.data[lat_coord1,lon_coord1] = 1.0


#apply to all models
models = ['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','BCC-ESM1','CanESM5','CESM2-FV2','CESM2','CESM2-WACCM-FV2','CNRM-CM6-1','CNRM-CM6-1-HR','CNRM-ESM2-1','EC-Earth3','EC-Earth3-Veg','GFDL-CM4','IPSL-CM6A-LR','MIROC6','MPI-ESM-1-2-HAM','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NorESM2-LM','NorESM2-MM','SAM0-UNICON','UKESM1-0-LL']
directories = ['tos_day_ssp119_r1i1p1f1_r1i1p1f2','tos_day_ssp126_r1i1p1f1_r1i1p1f2','tos_day_ssp245_r1i1p1f1_r1i1p1f2','tos_day_ssp460_r1i1p1f1_r1i1p1f2','tos_day_ssp585_r1i1p1f1_r1i1p1f2']

for directorie in directories:
    print directorie
    for model in models:
        print model
        file = base_directory+'tos_day_'+directorie.split('_')[2]+'_r1i1p1f1_r1i1p1f2/processed/dhw_Oday_'+model+'_hist_'+directorie.split('_')[2]+'_GBR_ann_max.nc'
        file2 = base_directory+'tos_day_'+directorie.split('_')[2]+'_r1i1p1f1_r1i1p1f2/processed/dhw_Oday_'+model+'_hist_'+directorie.split('_')[2]+'_GBR_ann_masked.nc'
        print file
        cube = iris.load_cube(basedir+file)
        cube.data.data[:,np.logical_not(np.isfinite(outmask.data.data))] = np.nan
        iris.fileformats.netcdf.save(cube, file2)
