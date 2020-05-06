import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import iris
import iris.quickplot as qplt
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

file = 'test_mygrid.nc'
c = iris.load_cube(file)[0]
file2 = 'test_mygrid2.nc'
c2 = iris.load_cube(file2)[0]
file0 = 'test.nc'
c0 = iris.load_cube(file0)[0]

ax = plt.axes(projection=ccrs.Mercator())
ax.coastlines()

qplt.pcolormesh(c2)
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='gray', alpha=0.5, linestyle='--')
gl.xlabels_top = False
gl.ylabels_left = False
gl.xlines = True
gl.xlocator = mticker.FixedLocator([-180, -45, 0, 45, 180])
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'size': 15, 'color': 'gray'}
gl.xlabel_style = {'color': 'red', 'weight': 'bold'}

plt.show()
