#!/bin/sh --login
  
#SBATCH -n 1
#SBATCH -q batch
#SBATCH -t 08:00:00
#SBATCH -A coastal
#SBATCH -J ww3grid
#SBATCH -o log.out
#SBATCH --exclusive
#SBATCH --mem-per-cpu=8G



  module purge
  module use /scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.6.0/envs/unified-env-rocky8/install/modulefiles/Core
  module load stack-intel/2021.5.0
  module load stack-intel-oneapi-mpi/2021.5.1
  module load cmake/3.23.1
  module load libpng/1.6.37
  module load zlib/1.2.13
  module load jasper/2.0.32
  module load hdf5/1.14.0
  module load netcdf-c/4.9.2
  module load netcdf-fortran/4.6.1
  module load bacio/2.4.1
  module load g2/3.4.5
  module load w3emc/2.10.0
  module load esmf/8.5.0
  module load scotch/7.0.4

  export WWATCH3_NETCDF=NC4
  export NETCDF_CONFIG=$NETCDF_ROOT/bin/nc-config
  
  
  workDir="$1"
  WW3Dir_new="$2"
  restart_time="$3"
  restart_file="$4"
  grid1="$5"
  grid2="$6"

 ${WW3Dir_new}/exec/ww3_grid > ww3_grid.out
 #Here the old and new have similar grids, so it's enough to just copy the mod_def for both
 cp mod_def.ww3 mod_def.$grid1
 cp mod_def.ww3 mod_def.$grid2

 cp ${restart_file} restart.${grid1} 
 time="`echo $restart_time | cut -c1-8` `echo $restart_time | cut -c9-10`0000"

 sed -e "s/TIME/$time/g" \
     -e "s/GR1/$grid1/g" \
     -e "s/GR2/$grid2/g" ww3_gint.inp.tmpl > ww3_gint.inp

 ${WW3Dir_new}/exec/ww3_gint > ww3_gint.out





