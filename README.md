Downloading to **/data/BatCaveNAS/ph290/CMIP6_william/**

Useful summary of equivalent SSP RCPs https://www.researchgate.net/figure/SSP-RCP-scenario-matrix-illustrating-ScenarioMIP-simulations-Each-cell-in-the-matrix_fig1_301594661

# Model availability

## 0.25degree, tos, daily

### historical:
AWI-CM-1-1-MR, CNRM-CM6-1-HR, GFDL-CM4, HadGEM3-GC31-MM

### ssp585 (approx. RCP8.5):
AWI-CM-1-1-MR, CNRM-CM6-1-HR, GFDL-CM4 (1)

### No simulations from ssp119 which is the 1.5 degree focused scenario

## 1degree, tos, daily

### historical:
BCC-CSM2-MR, BCC-ESM1, CESM2, CESM2-FV2, CESM2-WACCM, CESM2-WACCM-FV2, CNRM-CM6-1, CNRM-CM6-1-HR, CNRM-ESM2-1, CanESM5, EC-Earth3, EC-Earth3-Veg, GFDL-CM4, HadGEM3-GC31-LL, IPSL-CM6A-LR, MIROC6 (10)
 MRI-ESM2-0, NESM3, NorESM2-LM, NorESM2-MM, SAM0-UNICON, UKESM1-0-LL

### ssp585 (approx. RCP8.5):
BCC-CSM2-MR,CESM2-WACCM,CNRM-CM6-1,CNRM-ESM2-1,CanESM5,EC-Earth3,EC-Earth3-Veg,GFDL-CM4,HadGEM3-GC31-LL,IPSL-CM6A-LR,MIROC6,MRI-ESM2-0,NESM3,NorESM2-LM,NorESM2-MM,UKESM1-0-LL

### ssp119 (1.5 degree focused)
CNRM-ESM2-1, CanESM5, EC-Earth3-Veg, IPSL-CM6A-LR, MIROC6, MRI-ESM2-0, UKESM1-0-LL

# Downloading for:

tos | day | historial | r1i1p1f1,r1i1p1f2

tos | day | ssp119 | r1i1p1f1,r1i1p1f2

tos | day | ssp585 | r1i1p1f1,r1i1p1f2

tos | day | ssp126 | r1i1p1f1,r1i1p1f2

tos | day | ssp245 | r1i1p1f1,r1i1p1f2

tos | day | ssp460 | r1i1p1f1,r1i1p1f2

NOTE I have had to exclude the NUIST model because it's download times were prohibitively slow.

regridding scrip here: /data/BatCaveNAS/ph290/CMIP6_william/concat_regrid_extract.py

Note - taking the gr (regridded data where available)


# DHW calculation

### MMM calculation
* average daily data to monthly averages
* take the 1985 to 2012 data inclusive of both start and end years 
* take the data falling within each calendar month (across all years) in turn and
  * perform a least squares linear regression through time for each latitiude/longitude box
  * calculate the value from that slope for the decimal year 1988.2857
  * assign this value to the lat/lon box for that regression
* For each lat/lon box take the maximum value from any month of the year to create a 2D array of lat and lon (i.e. it no longer has a time dimension)

### DHW calculation
* subtract the MMM climatology (as calculated above) from each daily field
* set all values less than 1 to zero
* starting with day 84 (i.e. 12 weeks times 7 days)
  * sum the anomalies from the MMM climatology (i.e. from step 'set all values less than 1 to zero') along the time axis from the 84 preceeding days (inclusive of the current day) and divide by 7
  * assign this field to that day (i.e. 1st time through loop, day 84)

# DHW code

```python
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
```
