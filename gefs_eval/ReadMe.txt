1-Run get_data.sh
2-Get CycloneMap, GridInfo, and AltimeterGridded_JASON3_*.nc
3-Add the CyclonMap, Grid Info and AltimererGridded info in a script called mod_Sat_c00.sh that will run modelSat_Collocation
4-Make a ww3list.tmpl that has this data for example:
/scratch2/NCEPDEV/marine/Saeideh.Banihashemi/GlobalDev/GEFS-PHYS-OPT/BMax/EVAL/gefswave.t00z.global.0p25.TIME.grib2
Where Time is being set in the mod_Sat bash script
5-Run mod_Sat_c00.sh, these files will be created:
WW3.Altimeter_20180103_2018010300to2018011900.nc
You have to create same run scripts for p00-p10 for other members and edit the mod_sat_c00.sh job accordingly
6-Now we run evalGEFS_spr.py/evalGEFS_wnd_spr.py/evalGEFS_stats.py 

