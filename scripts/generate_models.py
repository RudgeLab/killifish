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

    N = 500
    sphere_rads = [15, 25]#[100, 50, 25, 15]
    #iters = 10
    wcs = [0.375,0.5,0.625]#[0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]
    #wcs.reverse()
    psis = [1,1.25,1.5]#[0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
    #psis.reverse()
    Ds = [1]#[0.1,0.5,1]
    #Ds.reverse()
    
    for sphere_rad in sphere_rads:
        for Wc in wcs: #np.linspace(0, 1, 10):
	        for psi in psis: #np.linspace(0, 1, 10):
	            for D in Ds:
	                for ftax in [0]:
	                    for forg in [0]:
	                        model = template%(N, sphere_rad, Wc, psi, D, ftax, forg)
	                        outfn = 'Wc__%g__psi__%g__D__%g__ftax__%g__%d__cells_sphere__%d__forg__%g'%(Wc, psi, D, ftax, N, sphere_rad, forg)
	                        outfn = outfn.replace('.', '_') + '.py'
	                        print('Creating model file %s'%outfn)
	                        outf = open(outfn, 'wt')
	                        outf.write(model)
	                        outf.close()

# Make sure we are running as a script
if __name__ == "__main__": 
    main()
