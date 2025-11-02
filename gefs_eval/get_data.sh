#!/bin/sh --login

#SBATCH -n 1
#SBATCH --ntasks-per-node=1
#SBATCH -q batch
#SBATCH --nodes=1                    # Number of nodes
#SBATCH --ntasks-per-node=1  
#SBATCH -t 08:00:00
#SBATCH -A marine-cpu
#SBATCH -J GEFS_vv
#SBATCH -o GEFS_2019_04.out

module purge
module use /scratch2/NCEPDEV/nwprod/hpc-stack/libs/hpc-stack/modulefiles/stack
module load hpc/1.1.0
module load hpc-intel/18.0.5.274
module load hpc-impi/2018.0.4
module load netcdf/4.7.4
module load jasper/2.0.25
module load zlib/1.2.11
module load png/1.6.35
module load hdf5/1.10.6
module load bacio/2.4.1
module load g2/3.4.1
module load w3nco/2.4.1
module load esmf/8_1_1
module load wgrib2/2.0.8
export WWATCH3_NETCDF=NC4
export METIS_PATH=/scratch2/COASTAL/coastal/save/Ali.Abdolali/hpc-stack/parmetis-4.0.3
export JASPER_LIB=$JASPER_ROOT/lib64/libjasper.a
export PNG_LIB=$PNG_ROOT/lib64/libpng.a
export Z_LIB=$ZLIB_ROOT/lib/libz.a
export ESMFMKFILE=$ESMF_LIB/esmf.mk
export WW3_PARCOMPN=4
export WGRIB2=/scratch2/NCEPDEV/nwprod/hpc-stack/libs/hpc-stack/intel-18.0.5.274/impi-2018.0.4/wgrib2/2.0.8/bin/wgrib2

export DEV=/scratch2/NCEPDEV/marine/Saeideh.Banihashemi/GlobalDev/GEFS/EP4_f_Validation
#prod
export DATA=/scratch2/NCEPDEV/marine/Saeideh.Banihashemi/GlobalDev/GEFS/Data/EP4_f
#Obs

set -x

##load modules


#define cycle


#DATES="20180404 20180411 20180418 20180425 20180502 20180509 20180516 20180523 20180530" 
#20180606 20180613 20180620 20180627"
#DATES="20180704 20180711 20180718 20180725 20180801 20180808 20180815 20180822 20180829 20180905 20180912 20180919 20180926"
#DATES="20181003 20181010 20181017 20181024 20181031 20181107 20181114 20181121 20181128 20181205 20181212 20181219 20181226"
#DATES="20190102 20190109 20190116 20190123 20190130 20190206 20190213 20190220 20190227 20190306 20190313 20190320 20190327"
#DATES="20190403 20190410 20190417 20190424 20190501 20190508 20190515 20190522 20190529 20190605 20190612 20190619 20190626"
#DATES="20190703 20190710 20190717 20190724 20190731 20190807 20190814 20190821 20190828 20190904 20190911 20190918 20190925"
#DATES="20201007 20201014 20201021 20201028 20201104 20201111 20201118 20201125 20201202 20201209 20201216 20201223 20201230"
#DATES="20210106 20210113 20210120 20210127 20210203 20210210 20210217 20210224 20210303 20210310 20210317 20210324 20210331"
#DATES="20210407 20210414 20210421 20210428 20210505 20210512 20210519 20210526 20210602 20210609 20210616 20210623 20210630"
DATES="20210707 20210714 20210721 20210728 20210804 20210811 20210818 20210825 20210901 20210908 20210915 20210922 20210929"
for DATE in $DATES
do
 MEMS="c00 p01 p02 p03 p04 p05 p06 p07 p08 p09 p10"
 start=$(date -d $DATE +%s)
 d="$start"
 for MEM in $MEMS
   do
   echo "start date: $(date -d @$start '+%Y-%m-%d %2H')"

   #date -d @$d '+%Y-%m-%d %2H'
   #YY=$(date -d @$d '+%Y')
   #MM=$(date -d @$d '+%m')
   #DD=$(date -d @$d '+%d')
   #HH=$(date -d @$d '+%2H')
   #MONTHNAME=`date -d ${YY}-${MM}-${DD} '+%b'`
    
   export DIR=${DATA}/${DATE}/wav/${MEM}/gridded
   cd ${DIR}
   cat gfswave.t00z.global.0p25.f* > gefswave.t00z.global.0p25.${DATE}.${MEM}.grib2
#  $WGRIB2 gefswave.t00z.global.0p25.${YY}${MM}${DD}.${MEM}.grib2 -netcdf gefswave.t00z.global.0p25.${YY}${MM}${DD}.${MEM}.nc
   cd ${DEV}
   ln -s ${DIR}/gefswave.t00z.global.0p25.${DATE}.${MEM}.grib2 .
  done
    
done
