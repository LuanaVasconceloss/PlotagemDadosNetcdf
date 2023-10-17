import xarray as xr
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
import geopandas as gpd


# Abra o arquivo NetCDF
ds = xr.open_dataset('era5.nc')
#shapefile
shapefile = gpd.read_file("AL_UF_2022.shp")

# Selecione o tempo, expver, latitude e longitude desejados
time_index = 0  # Selecione o primeiro índice de tempo (altere conforme necessário)
expver_index = 0  # Selecione o primeiro índice de expver (altere conforme necessário)
variable_name = 't2m'  # Nome da variável de temperatura do ar
d1 = ds[variable_name].mean(dim="time")
print(d1)

# Selecione os dados de temperatura do ar para o tempo e expver desejados, e a conversão da temperatura de K para C
data = (d1.isel(expver=expver_index))-273.15

# Crie uma figura
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())

# Criando matrizes de longitude e latitude
lon, lat = np.meshgrid(data.longitude, data.latitude)

# Plote os dados de temperatura do ar
im = ax.contourf(lon, lat, data,
                 levels=np.arange(data.min(), data.max(), 0.1), cmap='turbo',
                 transform=ccrs.PlateCarree())

cbar = plt.colorbar(im, ax=ax, pad=0.06, fraction=0.023)
cbar.set_label(label='ºC', size=20)
cbar.ax.tick_params(labelsize=12)

# Adicione o contorno dos continentes
ax.add_feature(cfeature.COASTLINE)
shapefile.plot(facecolor='none',alpha=0.3,edgecolor= 'black', lw =1, ax=ax)

states = cfeature.NaturalEarthFeature(category='cultural',
                                      name='admin_1_states_provinces_shp',
                                      scale='50m',
                                      facecolor='none')

# Adicione o título da figura
ax.set_title('Temperatura do Ar (ERA5)', fontsize=20)

# Adicione as linhas de grade
g1 = ax.gridlines(crs=ccrs.PlateCarree(), linestyle='--', color='gray', draw_labels=True)

# Remova os rótulos do topo e da direita
g1.right_labels = False
g1.top_labels = False

# Formate os rótulos como latitude e longitude
g1.yformatter = LATITUDE_FORMATTER
g1.xformatter = LONGITUDE_FORMATTER


plt.show()
