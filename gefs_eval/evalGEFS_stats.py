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
import mvalstats

outpdir="/scratch2/NCEPDEV/marine/Saeideh.Banihashemi/GlobalDev/GEFS/EP6-fix/summer-2018/EVAL/"


fdata_ep5,fmhs_ep5,fmwnd_ep5=wproc.orgensemblesat("list.txt",11)
print(fdata_ep5.shape)
print(fmhs_ep5.shape)
mean_hs_ep5=np.nanmean(fmhs_ep5,axis=1)
mean_wnd_ep5=np.nanmean(fmwnd_ep5,axis=1)

fctlt_ep5=np.array((fdata_ep5['time'].values[:]-fdata_ep5['cycle'].values[:])/(3600*24))
print(fctlt_ep5[:10])

frintervalsd_ep5=np.zeros((35,2),'f')*np.nan
frtagsd_ep5=np.arange(1,36,1).astype('int') 
for i in range(0,35):
	frintervalsd_ep5[i,0]=int(i)
	frintervalsd_ep5[i,1]=int(i+1)

frintervalsd_ep5=np.array(frintervalsd_ep5).astype('int')


# ASSESSMENTS ----------
print(" "); print(" ----- ASSESSMENTS ----- "); print(" ")
hdst="mean, variance, skewness, kurtosis, min, max, percentile80, percentile90, percentile95, percentile99, percentile99.9"
# 8 error metrics
nerrm=np.array(['bias','RMSE','NBias','NRMSE','SCrmse','SI','HH','CC'])
hdem="bias, RMSE, NBias, NRMSE, SCrmse, SI, HH, CC"

frtags=['day1','week1','week2','week3','week4','week5']
frintervals=np.array([[0,1],[1,7],[7,14],[14,21],[21,28],[28,35]])

# ---- GENERAL Deep Waters ---- (96 buoys)
print("GENERAL Deep Waters")
#indb=np.where((fdata_ep5['depth'].values>500)&(fdata_ep5['distcoast'].values>100))

# ---- GENERAL Deep Waters ---- (96 buoys)
print("GENERAL Deep Waters")
# summary statistics
hs_smrsts=np.zeros((frintervals.shape[0],3,11),'f')*np.nan
tm_smrsts=np.zeros((frintervals.shape[0],3,11),'f')*np.nan
tp_smrsts=np.zeros((frintervals.shape[0],3,11),'f')*np.nan
dm_smrsts=np.zeros((frintervals.shape[0],3,11),'f')*np.nan
wnd_smrsts=np.zeros((frintervals.shape[0],3,11),'f')*np.nan
# error metrics
hs_errm=np.zeros((frintervals.shape[0],2,8),'f')*np.nan
tm_errm=np.zeros((frintervals.shape[0],2,8),'f')*np.nan
tp_errm=np.zeros((frintervals.shape[0],2,8),'f')*np.nan
dm_errm=np.zeros((frintervals.shape[0],2,8),'f')*np.nan
wnd_errm=np.zeros((frintervals.shape[0],2,8),'f')*np.nan

for i in range(0,frintervals.shape[0]):

        #auxs=size(fohs[:,0,:,:][indb,:,frintervals[i][0]:frintervals[i][1]])

        # Hs
        index =[]
        index = np.where((fdata_ep5['depth'].values>500)&(fdata_ep5['distcoast'].values>100)& ((fctlt_ep5)>=frintervals[i][0]) & ((fctlt_ep5)<frintervals[i][1]) )
        obs=fdata_ep5['ohs'].values[index]
        modelctrl=fdata_ep5['mhs'].values[index]
        modelem=mean_hs_ep5[index]
        ind=np.where((obs>0.2)&(modelctrl>0.2)&(modelem>0.2)&(obs<15.)&(modelctrl<15.)&(modelem<15.))
        print(" - "+frtags[i]+", total amount of Hs data "+repr(size(ind)))
        # Summary Stats
        hs_smrsts[i,0,:]=np.array(mvalstats.smrstat(obs[ind],0.2,15))
        hs_smrsts[i,1,:]=np.array(mvalstats.smrstat(modelctrl[ind],0.2,15))
        hs_smrsts[i,2,:]=np.array(mvalstats.smrstat(modelem[ind],0.2,15))
        fname = outpdir+"Table_DW_SummaryStats_Hs_"+frtags[i]+".txt"
        ifile = open(fname,'w')
        ifile.write("# Summary Stats, total amount of data: "+repr(size(ind))+" \n")
        ifile.write('# '+hdst+' \n')
        ifile.write('# Obs, ControlMember, EnsembleMean \n')
        np.savetxt(ifile,np.atleast_2d(hs_smrsts[i,0,:]) ,fmt="%12.4f",delimiter='      ')
        np.savetxt(ifile,np.atleast_2d(hs_smrsts[i,1,:]) ,fmt="%12.4f",delimiter='      ')
        np.savetxt(ifile,np.atleast_2d(hs_smrsts[i,2,:]) ,fmt="%12.4f",delimiter='      ')
        ifile.close(); del ifile, fname
        # Error Metrics
        hs_errm[i,0,:]=np.array(mvalstats.metrics(modelctrl,obs,0.2,15,14))
        hs_errm[i,1,:]=np.array(mvalstats.metrics(modelem,obs,0.2,15,14))
        fname = outpdir+"Table_DW_ErrorMetrics_Hs_"+frtags[i]+".txt"
        ifile = open(fname,'w')
        ifile.write("# Error metrics, total amount of data: "+repr(size(ind))+" \n")
        ifile.write('# '+hdem+' \n')
        ifile.write('# ControlMember, EnsembleMean \n')
        np.savetxt(ifile,np.atleast_2d(hs_errm[i,0,:]) ,fmt="%12.4f",delimiter='        ')
        np.savetxt(ifile,np.atleast_2d(hs_errm[i,1,:]) ,fmt="%12.4f",delimiter='        ')
        ifile.close(); del ifile, fname
        # scatter plot, QQ-plot
        #pvalstats.scatterplot(np.c_[modelctrl[ind],modelem[ind]],obs[ind],outpdir+"ScatterPlot_"+frtags[i]+"_DW_Hs_",['Ctrl','EM'])
        #pvalstats.qqplot(np.c_[modelctrl[ind],modelem[ind]],obs[ind],outpdir+"QQplot_"+frtags[i]+"_DW_Hs_",['Ctrl','EM'])
        #pvalstats.taylordiagram(np.c_[modelctrl[ind],modelem[ind]],obs[ind],outpdir+"TaylorD_"+frtags[i]+"_DW_Hs_",['Ctrl','EM'])
#wind
        wndobs=fdata_ep5['ownd'].values[index]
        wndmodelctrl=fdata_ep5['mwnd'].values[index]
        wndmodelem=mean_wnd_ep5[index]
        ind=np.where((obs>0.2)&(modelctrl>0.2)&(modelem>0.2)&(obs<15.)&(modelctrl<15.)&(modelem<15.))
        print(" - "+frtags[i]+", total amount of Wind data "+repr(size(ind)))
        # Summary Stats
        wnd_smrsts[i,0,:]=np.array(mvalstats.smrstat(wndobs[ind],0.2,15))
        wnd_smrsts[i,1,:]=np.array(mvalstats.smrstat(wndmodelctrl[ind],0.2,15))
        wnd_smrsts[i,2,:]=np.array(mvalstats.smrstat(wndmodelem[ind],0.2,15))
        fname = outpdir+"Table_DW_SummaryStats_Wind_"+frtags[i]+".txt"
        ifile = open(fname,'w')
        ifile.write("# Summary Stats, total amount of data: "+repr(size(ind))+" \n")
        ifile.write('# '+hdst+' \n')
        ifile.write('# Obs, ControlMember, EnsembleMean \n')
        np.savetxt(ifile,np.atleast_2d(wnd_smrsts[i,0,:]) ,fmt="%12.4f",delimiter='      ')
        np.savetxt(ifile,np.atleast_2d(wnd_smrsts[i,1,:]) ,fmt="%12.4f",delimiter='      ')
        np.savetxt(ifile,np.atleast_2d(wnd_smrsts[i,2,:]) ,fmt="%12.4f",delimiter='      ')
        ifile.close(); del ifile, fname
        # Error Metrics
        wnd_errm[i,0,:]=np.array(mvalstats.metrics(wndmodelctrl,wndobs,0.2,15,14))
        wnd_errm[i,1,:]=np.array(mvalstats.metrics(wndmodelem,wndobs,0.2,15,14))
        fname = outpdir+"Table_DW_ErrorMetrics_Wind_"+frtags[i]+".txt"
        ifile = open(fname,'w')
        ifile.write("# Error metrics, total amount of data: "+repr(size(ind))+" \n")
        ifile.write('# '+hdem+' \n')
        ifile.write('# ControlMember, EnsembleMean \n')
        np.savetxt(ifile,np.atleast_2d(wnd_errm[i,0,:]) ,fmt="%12.4f",delimiter='        ')
        np.savetxt(ifile,np.atleast_2d(wnd_errm[i,1,:]) ,fmt="%12.4f",delimiter='        ')
        ifile.close(); del ifile, fname

