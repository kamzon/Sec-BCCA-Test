#!/bin/bash

#same as -n
#SBATCH --ntasks=60
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=50000
#same as -t
#SBATCH --time 336:00:00

#same as -c
#SBATCH --cpus-per-task 8

#same as -j
#SBATCH --job-name Sec-BCCA_testData6
#SBATCH --partition=fuchs

#same as -o
#SBATCH --output Sec-BCCA_testData6.out


#same as -e
#SBATCH --error Sec-BCCA_testData6.err

#here the jobscript starts

#echo "hello $VARIABLE"

#SBATCH -n 1
#SBATCH -c 1
#SBATCH --exclusive
module purge
module load python                 # Load the Python module if required

OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_NUM_THREADS

srun python main.py
EXITCODE=$?
module purge
exit $EXITCODE


