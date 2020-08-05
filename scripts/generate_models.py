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
    sphere_rads = [100, 50, 25, 15]
    #iters = 10
    
    for sphere_rad in sphere_rads:
        for Wc in [1]: #np.linspace(0, 1, 10):
	        for psi in [0,1]: #np.linspace(0, 1, 10):
	            for D in [0.1,0.5,1]:
	                for ftax in [0]:
	                    model = template%(N, sphere_rad, Wc, psi, D, ftax)
	                    outfn = 'Wc__%g__psi__%g__D__%g__ftax__%g__%d_cells_sphere_%d'%(Wc, psi, D, ftax, N, sphere_rad)
	                    outfn = outfn.replace('.', '_') + '.py'
	                    print('Creating model file %s'%outfn)
	                    outf = open(outfn, 'wt')
	                    outf.write(model)
	                    outf.close()

# Make sure we are running as a script
if __name__ == "__main__": 
    main()
