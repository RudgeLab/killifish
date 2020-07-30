import random
from CellModeller.Regulation.ModuleRegulator import ModuleRegulator
from CellModeller.Biophysics.GeneralModels.CLSPP import CLSPP
from CellModeller.GUI import Renderers
from CellModeller.Integration.CLEulerSigIntegrator import CLEulerSigIntegrator #add
from CellModeller.Signalling.GridDiffusion import GridDiffusion #add
import numpy as np
import math

n_cells = 800
side = 40
Ws = 1
Wc = 0
psi = 1

Fm = 0.5
gamma_s = 1
D = 0.5
fcil = 2 * D * psi
ftax = 1

#Specify parameter for solving diffusion dynamics #Add
s = 2
grid_size = (s, s, s) # grid size
grid_dim = (int(side*2/s), int(side*2/s), 12) # dimension of diffusion space, unit = number of grid
grid_orig = (-side + s/2, -side + s/2, -6) # where to place the diffusion space onto simulation space

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
            max_planes=6, 
            grid_spacing=2,
            cgs_tol=1e-2,
            max_substeps=1,
            spherical=False,
            compNeighbours=True)

    sig = GridDiffusion(sim, 1, grid_dim, grid_size, grid_orig, [1])
    integ = CLEulerSigIntegrator(sim, 1, 1, n_cells, sig, deg_rate=0, boundcond='constant')
    # use this file for reg too
    regul = ModuleRegulator(sim)
    # Only biophys and regulation
    sim.init(biophys, regul, sig, integ)

    # Specify the initial cell and its location in the simulation
    # Grid
    n_steps = np.sqrt(n_cells)
    step = side * 2 / n_steps
    for i in range(int(n_steps)):
        for j in range(int(n_steps)):
            p = (2 + i*step - side, 2 + j*step - side, 0) # np.random.uniform(-1,1)
            cell_dir = np.random.uniform(-1,1, size=(3,))
            cell_dir[2] = 0
            cell_dir /= np.sqrt(np.sum(cell_dir*cell_dir))
            sim.addCell(cellType=0, dir=tuple(cell_dir), pos=tuple(p))
    '''
    # Random
    for i in range(n_cells):
        p = np.random.uniform(-1,1, size=(3,)) * side
        p[2] = 0
        cell_dir = np.random.uniform(-1,1, size=(3,))
        cell_dir[2] = 0
        cell_dir /= np.sqrt(np.sum(cell_dir*cell_dir))
        sim.addCell(cellType=0, dir=tuple(cell_dir), pos=tuple(p))
    ''' 
    # Box
    biophys.addPlane((0,-side,0),(0,1,0), 20.)
    biophys.addPlane((0,side,0),(0,-1,0), 20.)
    biophys.addPlane((-side,0,0),(1,0,0), 20.)
    biophys.addPlane((side,0,0),(-1,0,0), 20.)

    # Add some objects to draw the models
    if sim.is_gui:
        # Add some objects to draw the models
        from CellModeller.GUI import Renderers
        therenderer = Renderers.GLSphereRenderer(sim, draw_axis=True, draw_nbr_dir=False, draw_gradient=True)
        sim.addRenderer(therenderer)
        sigrend = Renderers.GLGridRenderer(sig, integ, alpha=0.5) # Add
        sim.addRenderer(sigrend) #Add

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

   
def sigRateCL(): #Add
    return '''
    rates[0] = 0.f; // / (1.f + signals[0]); 
    '''

def update(cells):
    pass

def divide(parent, d1, d2):
    pass

