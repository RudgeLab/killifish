import os
import sys
import subprocess
import string
import shutil
from pathlib import Path
from CellModeller.Simulator import Simulator
import numpy as np


def main():
    # Get module name to load
    if len(sys.argv)<2:
        print("Please template model (.py) file")
        exit(0)
    else:
        template = open(sys.argv[1], 'rt').read()

    N = 320
    sphere_rads = [25] #[100, 50, 25, 15]
    Ds = [1]
    chis = [10] #[10]
    ftaxs = [0] #[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    
    # change
    psis = [0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0] #[0,0.2...,2.0]
    forgs = [0, 0.01, 0.05, 0.1, 0.5, 1]
    wcs = [0,1] #[0,1]
    
    for sphere_rad in sphere_rads:
        for Wc in wcs: 
	        for psi in psis:
	            for D in Ds:
	                for ftax in ftaxs:
	                    for forg in forgs:
	                        for chi in chis:
	                            model = template%(N, sphere_rad, Wc, psi, D, ftax, forg, chi)
	                            outfn = 'Wc__%g__psi__%g__D__%g__ftax__%g__%d__cells_sphere__%d__forg__%g__chi__%g'%(Wc, psi, D, ftax, N, sphere_rad, forg, chi)
	                            outfn = outfn.replace('.', '_') + '.py'
	                            print('Creating model file %s'%outfn)
	                            outf = open(outfn, 'wt')
	                            outf.write(model)
	                            outf.close()
# Make sure we are running as a script
if __name__ == "__main__":
    main()
