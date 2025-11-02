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



# Function to plot RMSE map
def plot_rmse_map( latitudes, longitudes, rmse_values):
    plt.figure(figsize=(12, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Add map features
    ax.set_global()
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=0.3)
    ax.gridlines(draw_labels=True, linestyle="--", alpha=0.5)

    # Scatter plot of RMSE
    rmse_plot = ax.pcolormesh(Lon, Lat, rmse_grid, cmap="coolwarm", shading='auto', transform=ccrs.PlateCarree(),vmin=0, vmax=2)

    #sc = plt.scatter(longitudes, latitudes, c=rmse_values, cmap="coolwarm", s=5, alpha=0.7, transform=ccrs.PlateCarree())
    plt.colorbar(rmse_plot, label="RMSE (m)")

    plt.title(f"Global RMSE of Significant Wave Height (Hs) - {category}")

    # Save the figure
    output_file = f"rmse_global_d1.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Figure saved as {output_file}")

    plt.show() 

# Generate RMSE maps for each forecast category
#for category, data in rmse_data.items():
#    if data["lat"]:  # Only plot if there is data for the category
plot_rmse_map(Lon, Lat, np.array(rmse_grid))

