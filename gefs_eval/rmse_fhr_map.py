import time
import os
import glob
import netCDF4 as nci
import properscoring as ps
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime
from cartopy.util import add_cyclic_point
from matplotlib import ticker

import sys
import warnings; warnings.filterwarnings("ignore")

import wproc
import pvalstats

from matplotlib.cm import get_cmap

cmap = get_cmap("YlOrRd")
cmap = cmap.with_extremes(bad="white")  # Forces NaN or low values to be white



palette = plt.cm.jet


# Directory containing NetCDF files
data_dir = "/scratch2/NCEPDEV/marine/Saeideh.Banihashemi/GlobalDev/GEFS/EP6/fall_2017/EVAL/"  # Change this to your directory
file_pattern = os.path.join(data_dir, "WW3.*mem000*.nc")


fdata,fmhs,fmwnd=wproc.orgensemblesat("list.txt",11)
mean_hs=np.nanmean(np.c_[fdata['mhs'].values,fmhs],axis=1)
#print(mean_hs_ep5[:10])

# Forecast hour categories
forecast_categories = {
    "Day 1 (0-24h)": (0, 24),
#    "Week 1 (24-168h)": (24, 168),
#    "Week 2 (168-336h)": (168, 336),
#    "Beyond Week 2 (>336h)": (336, np.inf),
}

# Initialize dictionary to store RMSE values per category
rmse_data = {key: {"lat": [], "lon": [], "rmse": []} for key in forecast_categories}

    # Extract variables
lat = fdata["lat"].values
lon = fdata["lon"].values
model_hs = fdata["mhs"].values
obs_hs = fdata["ohs"].values
time = fdata["time"].values  # Time in seconds since 1970
print(f"time shape: {time.shape}")
# Compute forecast hour
fctlt=np.array((fdata['time'].values[:]-fdata['cycle'].values[:])/(3600))

    # Loop through forecast categories
for category, (min_h, max_h) in forecast_categories.items():
    mask = (fctlt >= min_h) & (fctlt < max_h)
    print(f"Mask for {category}: {np.sum(mask)} values selected")
    unique_lat = np.unique(lat)
    unique_lon = np.unique(lon)

# Create an empty RMSE grid
    rmse_grid = np.full((len(unique_lat), len(unique_lon)), np.nan)  # Initialize with NaNs

# Compute RMSE for each (lat, lon) pair
    for i, lat_val in enumerate(unique_lat):
        for j, lon_val in enumerate(unique_lon):
            # Find matching indices in the dataset
            loc_mask = (lat == lat_val) & (lon == lon_val) & mask

            if np.any(loc_mask):  # Ensure at least one valid observation exists
                rmse_grid[i, j] = np.sqrt(np.nanmean((mean_hs[loc_mask] - obs_hs[loc_mask]) ** 2))
                print(rmse_grid.shape)
                print(unique_lat.shape)
                print(unique_lon.shape)
    
    Lon, Lat = np.meshgrid(unique_lon, unique_lat)



  #  if np.any(mask):  # Only process if there are valid time steps
  #      rmse = np.sqrt(np.nanmean((mean_hs[mask] - obs_hs[mask]) ** 2))
  #      print(rmse)
  #      rmse_data[category]["lat"].extend(lat[mask])
  #      rmse_data[category]["lon"].extend(lon[mask])

# Function to plot RMSE map
def plot_rmse_map( latitudes, longitudes, rmse_values):
    plt.figure(figsize=(12, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Add map features
    ax.set_global()
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=0.3)
    ax.gridlines(draw_labels=True, linestyle="--", alpha=0.5)
    #levels = np.linspace(np.nanmin(rmse_values),np.nanpercentile(rmse_values,99.995),101)
    # Scatter plot of RMSE
    #rmse_plot = ax.pcolormesh(Lon, Lat, rmse_grid, cmap="coolwarm", shading='auto', transform=ccrs.PlateCarree())
    
    #rmse_plot = ax.contourf(
    #Lon, Lat, rmse_grid, levels=20, cmap='coolwarm', vmin=0, vmax=2, extend="both")
    rmse_plot = ax.contourf(Lon, Lat, rmse_grid, levels=20, cmap=cmap, vmin=0, vmax=2, extend="both")


# Add colorbar with improved positioning
    cbar = plt.colorbar(rmse_plot, ax=ax, orientation="vertical", shrink=0.8, pad=0.02)

    #cbar = plt.colorbar(rmse_plot, ax=ax, orientation="vertical", fraction=0.04, pad=0.02)
    cbar.set_label("RMSE (m)", fontsize=12)
    cbar.ax.tick_params(labelsize=10)

# Title
    ax.set_title("Global RMSE of Significant Wave Height (Hs) - Day 1 (0-24h)", fontsize=14)

# Save the figure
    plt.savefig("rmse_global_improved.png", dpi=300, bbox_inches="tight")
    plt.show()
    

# Generate RMSE maps for each forecast category
#for category, data in rmse_data.items():
#    if data["lat"]:  # Only plot if there is data for the category
plot_rmse_map(Lon, Lat, np.array(rmse_grid))

