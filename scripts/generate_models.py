import os
import sys
import subprocess
import string
import shutil
from pathlib import Path
from CellModeller.Simulator import Simulator

n_steps = 400

def main():
    # Get module name to load
    if len(sys.argv)<2:
        print("Please template model (.py) file")
        exit(0)
    else:
        template = open(sys.argv[1], 'rt').read()

    N = 1000
    for Wc in [0, 0.5]:
        for psi in [0, 1]:
            for ftax in [0, 1]:
                model = template%(N, Wc, psi, ftax)
                outfn = 'Wc__%g__psi__%g__ftax__%g__%d_cells'%(Wc, psi, ftax, N)
                outfn = outfn.replace('.', '_') + '.py'
                print('Creating model file %s'%outfn)
                outf = open(outfn, 'wt')
                outf.write(model)
                outf.close()

# Make sure we are running as a script
if __name__ == "__main__": 
    main()
