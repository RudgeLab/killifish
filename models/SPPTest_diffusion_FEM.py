import random
from CellModeller.Regulation.ModuleRegulator import ModuleRegulator
from CellModeller.Biophysics.GeneralModels.CLSPP import CLSPP
from CellModeller.GUI import Renderers
from CellModeller.Integration.CLEulerFEMIntegrator import CLEulerFEMIntegrator #add
from CellModeller.Signalling.FEMDiffusion import FEMDiffusion #add
import numpy as np
import math

n_cells = 1000
sphere_rad = 40
Ws = 1
Wc = 0
psi = 0

Fm = 0.5
gamma_s = 1
D = 1
fcil = 2 * D * psi
ftax = 100

# Parameters for FEM solver
mesh_file = '/home/timrudge/cellmodeller/killifish/notebooks/shell.xml'
pvd_file = None #'sphere_diffusion_FEM.pvd'
diffusion_rate = 1000

def setup(sim):
    sim.dt = 0.5
    # Set biophysics, signalling, and regulation models
    
    #max_sqr
    #biophys = CLBacterium(sim, max_cells=max_cells, jitter_z=False, max_sqs=256**2)
    biophys = CLSPP(sim, 
            max_cells=n_cells, 
            gamma_s=gamma_s, 
            Fm=Fm,
            Ws=Ws,
            Wc=Wc,
            fcil=fcil,
            ftax=ftax,
            D=D,
            max_spheres=2, 
            grid_spacing=2,
            cgs_tol=1e-4,
            max_substeps=1,
            spherical=True,
            compNeighbours=True)

    sig = FEMDiffusion(sim, mesh_file, pvd_file, 1, diffusion_rate, sim.dt)
    integ = CLEulerFEMIntegrator(sim, 1, 1, n_cells, sig)
    # use this file for reg too
    regul = ModuleRegulator(sim)
    # Only biophys and regulation
    sim.init(biophys, regul, sig, integ)

    # Specify the initial cell and its location in the simulation
    for i in range(n_cells):
        p = np.random.uniform(-20,20, size=(3,))
        p = p * sphere_rad / np.sqrt(np.sum(p*p))
        cell_dir = np.random.uniform(-1,1, size=(3,))
        cell_dir /= np.sqrt(np.sum(cell_dir*cell_dir))
        sim.addCell(cellType=0, dir=tuple(cell_dir), pos=tuple(p))


    print('sphere_rad = ', sphere_rad)
    biophys.addSphere((0,0,0), sphere_rad, 1, 1.)
    biophys.addSphere((0,0,0), sphere_rad, 1, -1.)


    # Add some objects to draw the models
    therenderer = Renderers.GLSphereRenderer(sim, 
                                            draw_sphere=True, 
                                            sphere_radius=sphere_rad,
                                            sphere_color=[0,0,0,0.5],
                                            draw_axis=True,
                                            draw_gradient=True)
    sim.addRenderer(therenderer)

    sim.pickleSteps = 1

def init(cell):
    # Specify initial concentration of chemical species
    cell.species[:] = [0]
    # Specify initial concentration of signaling molecules 
    cell.signals[:] = [0]
    cell.color = [0.5, 1, 0.5]
    cell.t = 0

def specRateCL(): # Add
    return '''
    rates[0] = 0.f;
    '''

    # D1 = diffusion rate of x0 
    # k1 = production rate of x0
   
def sigRateCL(): #Add
    return '''
    rates[0] = 1.f; // / (1.f + signals[0]); 
    '''

def update(cells):
    pass

def divide(parent, d1, d2):
    pass

