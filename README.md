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
  * assign this field to that day in the output array (i.e. 1st time through loop, day 84)

# DHW code

In script DHW_cmip6.py
