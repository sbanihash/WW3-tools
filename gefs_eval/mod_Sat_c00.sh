#!/bin/sh --login

#SBATCH -n 1
#SBATCH --ntasks-per-node=1
#SBATCH -q batch
#SBATCH --nodes=1                    # Number of nodes
#SBATCH --ntasks-per-node=1  
#SBATCH -t 08:00:00
#SBATCH -A coastal
#SBATCH -J ModSat_vv
#SBATCH -o Mod_sat_c00.out

set -x

module use /scratch1/NCEPDEV/climate/Jessica.Meixner/general/modulefiles-rocky16
module load ww3tools

#source activate myenv

export DEV=/scratch2/NCEPDEV/marine/Saeideh.Banihashemi/GlobalDev/GEFS/EP6-fix/summer-2018/EVAL
#prod

#define cycle
cd ${DEV}

DATES="20180802 20180809 20180816 20180823 20180830 20180906 20180913 20180920"

MEM="mem000"
for DATE in $DATES
  do 
sed -e "s/TIME/$DATE/g" \
      -e "s/mem/$MEM/g" \
                               ww3list.tmpl > ww3list_${DATE}_${MEM}.txt

python3 /scratch2/NCEPDEV/marine/Saeideh.Banihashemi/Share/Ghazal/TestPR68/WW3-tools/ww3tools/modelSat_collocation.py ww3list_${DATE}_${MEM}.txt satlist.txt gridInfo_GEFS.nc CycloneMap_2018.nc 1    

done
