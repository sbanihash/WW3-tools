#!/bin/sh --login
  
#SBATCH -n 1
#SBATCH -q batch
#SBATCH -t 08:00:00
#SBATCH -A coastal
#SBATCH -J ww3grid
#SBATCH -o log.out
#SBATCH --exclusive
#SBATCH --mem-per-cpu=8G


# you would also need to have a  grid.inp for the grid you are using in the rundir
# $1: where we are running (rundir)
# $2: Target WW3 code
# $3: YYYYMMDDHH for restart dile
# $4: path to restart file
# $5: old grid ID
# $6: new grid ID


./convert.sh  /scratch2/NCEPDEV/marine/Saeideh.Banihashemi/GlobalDev/FIX_RSTRT/code /scratch2/NCEPDEV/marine/Saeideh.Banihashemi/GlobalDev/FIX_RSTRT/work/WW3_new 2018121303 /scratch2/NCEPDEV/marine/Saeideh.Banihashemi/GlobalDev/FIX_RSTRT/work/20181213.000000.restart.glo_025 "old" "new"  
