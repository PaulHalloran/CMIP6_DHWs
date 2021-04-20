import iris
import glob
import iris.coord_categorisation
import numpy as np
import datetime

#I think you shoudl be able to access this file, but I can copy it
f = '/home/shared/for_ben/testingdhw_Oday_CanESM5_hist_ssp119_GBR.nc'
cube = iris.load_cube(f)

#calculate simplified data related metadata
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

###
#print out the data of the first field using datetime
###

#1st print the units
print(cube.coord('time').units)
#result:
#days since 1850-01-01 0:0:0.0

#2nd print the time dimension values:
print(cube.coord('time').points)
#result:
#[36865.5 36866.5 36867.5 ... 91247.5 91248.5 91249.5]

#Now print out the datetime date associated with the 1st time value:
print(datetime.datetime(1850, 1, 1, 0, 0, 0) + datetime.timedelta(days=36865.5))
#result:
#1950-12-08 12:00:00

#The above is not what I would expect it to be. Now let's look at this a different way

###
#Print out the date as assigned by the iris.coord_categorisation function
###

print(cube[0].coord('year').points)
#result:
#[1951]

print(cube[0].coord('month_number').points)
#result:
#[1]

print(cube[0].coord('day_of_month').points)
#result:
#[1]

#This is what the date of that 1st field should be, but it is a bit of a mystery to me what in the netcdf file is recording this if it is not the standard time dimension.
#Digging in to the code behind the iris.coord_categorisation function (https://github.com/SciTools/iris/blob/83eead65363b85eb7c5adba312c97ab97bca8546/lib/iris/coord_categorisation.py)
#I see that it uses the iris function 'units.num2date' rather than datetime. If we use this, we get the answer:

print(cube[0].coord('time').units.num2date(0))
#result:
#1850-01-01 00:00:00
#which is what we would expect.

#It looks to me that num2date relies on the function cftime (https://pypi.org/project/cftime/) rather than datetime.
#I'm therefore confident that this is all working fine, but if you have any insights in to how cftime works differently to datetime, that would be great!
