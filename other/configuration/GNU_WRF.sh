#!/bin/bash
#WRF Variables
export DIR=/home/sun/Build_WRF/LIBRARIES
export CC=gcc
export CXX=g++
export FC=gfortran
export FCFLAGS=-m64
export F77=gfortran
export FFLAGS=-m64
export NETCDF=/usr
export HDF5=/usr/lib/x86_64-linux-gnu/hdf5/serial
export LDFLAGS="-L/usr/lib/x86_64-linux-gnu/hdf5/serial/ -L/usr/lib"
export CPPFLAGS="-I/usr/include/hdf5/serial/ -I/usr/include"
export LD_LIBRARY_PATH=/usr/lib
export JASPERLIB=/home/sun/Build_WRF/LIBRARIES/grib2/lib
export JASPERINC=/home/sun/Build_WRF/LIBRARIES/grib2/include