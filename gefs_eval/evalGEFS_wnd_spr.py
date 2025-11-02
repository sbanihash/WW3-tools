import matplotlib
# matplotlib.use('Agg')
import time
import os
from time import strptime
from calendar import timegm
import xarray as xr
import netCDF4 as nc
import numpy as np
from numpy import size
import properscoring as ps
# from pylab import *
# import matplotlib.pyplot as plt
import sys
import pandas as pd
from matplotlib import ticker
from pylab import *
import cartopy
from datetime import datetime
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
from matplotlib import ticker

import sys
import warnings; warnings.filterwarnings("ignore")

import wproc
import pvalstats      

outpdir="/scratch2/NCEPDEV/marine/Saeideh.Banihashemi/GlobalDev/GEFS/EP6-fix/summer-2018/EVAL"


fdata_ep5,fmhs_ep5,fmwnd_ep5=wproc.orgensemblesat("list.txt",11)
print(fdata_ep5.shape)
print(fmhs_ep5.shape)
mean_wnd_ep5=np.nanmean(np.c_[fdata_ep5['mwnd'].values,fmwnd_ep5],axis=1)
#print(mean_hs_ep5[:10])

squared_diff_ep5 = np.square(fmwnd_ep5 - mean_wnd_ep5[:, np.newaxis])
#print(squared_diff_ep5[:10])
ensemble_variance_ep5 = np.nanmean(squared_diff_ep5,axis=1)
#print(ensemble_variance_ep5[:10])
ensemble_spread_ep5 = sqrt(ensemble_variance_ep5)

minus_ensemble_spread_ep5 = mean_wnd_ep5 - ensemble_spread_ep5
plus_ensemble_spread_ep5 = mean_wnd_ep5 + ensemble_spread_ep5

fctlt_ep5=np.array((fdata_ep5['time'].values[:]-fdata_ep5['cycle'].values[:])/(3600*24))
print(fctlt_ep5[:10])


frtags=['day1','week1','week2','week3','week4','week5']
frintervalsd_ep5=np.array([[0,1],[1,7],[7,14],[14,21],[21,28],[28,35]])

#frintervalsd_ep5=np.zeros((35,2),'f')*np.nan
#frtagsd_ep5=np.arange(1,36,1).astype('int') 
#for i in range(0,35):
#	frintervalsd_ep5[i,0]=int(i)
#	frintervalsd_ep5[i,1]=int(i+1)
#
#frintervalsd_ep5=np.array(frintervalsd_ep5).astype('int')

fcst_mwnd_ep5={}
fcst_ctrl_ep5={}
fcst_obs_wnd_ep5={}
fcst_minus_spread_wnd_ep5={}
fcst_plus_spread_wnd_ep5 ={}
key_1 = None
key_2 = None
key_3 = None
key_4 = None
key_5 = None

for k in range(0,frintervalsd_ep5.shape[0]):
	index =[]
	index = np.where( ((fctlt_ep5)>=frintervalsd_ep5[k][0]) & ((fctlt_ep5)<=frintervalsd_ep5[k][1]) ) 
	key = "key_{}".format(k)
	fcst_mwnd_ep5 ['key'] = mean_wnd_ep5[index]
	fcst_ctrl_ep5['key']=fdata_ep5['mwnd'].values[index]
	fcst_minus_spread_wnd_ep5 ['key'] = minus_ensemble_spread_ep5[index]
	fcst_plus_spread_wnd_ep5 ['key'] = plus_ensemble_spread_ep5[index]
	fcst_obs_wnd_ep5 ['key'] = fdata_ep5['ownd'].values[index]
	pvalstats.qqplot(np.c_[fcst_mwnd_ep5 ['key'],fcst_minus_spread_wnd_ep5 ['key'],fcst_plus_spread_wnd_ep5 ['key']],fcst_obs_wnd_ep5['key'],outpdir+'/plots_summer/ep6-fix_wnd_fcst_week_'"{}".format(k),['ensemble mean','ensemble spread','ensemble spread'])

	pvalstats.taylordiagram(np.c_[fcst_ctrl_ep5['key'],fcst_mwnd_ep5['key']],fcst_obs_wnd_ep5['key'],outpdir+'/plots_summer/ep6-fix_wnd_taylor_fcst_week'f"{k}",['CTRL', 'EM'])
