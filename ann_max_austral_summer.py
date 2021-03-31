import iris
import glob
import iris.coord_categorisation
import numpy as np

directories = glob.glob('/data/BatCaveNAS/ph290/CMIP6_william/tos_day_ssp???_r1i1p1f1_r1i1p1f2/processed_native_grid_global')

for d in directories:
    # d = directories[0]
    files = glob.glob(d+'/dhw_*GBR.nc')

    for f in files:
        # f = files[0]
        cube = iris.load_cube(f)

        try:
            iris.coord_categorisation.add_year(cube, 'time', name='year')
        except:
            pass

        try:
            iris.coord_categorisation.add_year(cube, 'time', name='year2')
        except:
            pass

        try:
            iris.coord_categorisation.add_month_number(cube, 'time', name='month_number')
        except:
            pass

        try:
            iris.coord_categorisation.add_day_of_month(cube, 'time', name='day_of_month')
        except:
            pass

        cube_years = cube.coord('year').points
        cube_months = cube.coord('month_number').points
        cube_days = cube.coord('day_of_month').points

        # print cube.coord('year2').points

        #change the year value from calendar years to the same 'year' used in William's relentless march paper (2019) (i.e. August 1-July 31) to encompass the complete austral summer.
        #This is important so that one bleaching season (which crosses 1st Jan) does not get picked up as two bleaching years.
        #Skirving 2019: 'for example, 1998 refers to (1) August 1, 1997–July 31, 1998 for the Southern Hemisphere'
        coral_stress_year = np.zeros(len(cube_years))
        coral_stress_year[:] = np.nan
        tmp_year = np.min(cube_years)
        for i in range(len(cube_years)):
            if (cube_months[i] == 8) & (cube_days[i] == 1):
                tmp_year += 1
            coral_stress_year[i] = tmp_year


        cube.coord('year2').points = coral_stress_year.astype(int)

        # note the [1:-1] is because the first and last year will have only aggregated half a year of data because of the above
        dhw_austral_ann_max = cube.aggregated_by('year2', iris.analysis.MAX)[1:-1]

        iris.fileformats.netcdf.save(dhw_austral_ann_max, f.split('.nc')[0]+'_austral_summer_ann_max.nc')
