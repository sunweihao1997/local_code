#!/bin/bash
# Intel ICX IFX complier environment

source /home/sun/intel/oneapi_latest/setvars.sh

export CC=icx
export FC=ifx
export F90=ifx
export CXX=icx

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/sun/app/intel_new/lib