import random
from CellModeller.Regulation.ModuleRegulator import ModuleRegulator
from CellModeller.Biophysics.GeneralModels.CLSPP import CLSPP
from CellModeller.GUI import Renderers
import numpy as np
import math

#Import Euler integrator for solving ODE system of chemical species inside the cells
from CellModeller.Integration.CLEulerIntegrator import CLEulerIntegrator

n_cells = 500
sphere_rad = 100

Wc = 0.5
psi = 0

gamma_s = 1
D = 1.
fcil = 2 * D * psi
Fm = 0.5

def setup(sim):
    sim.dt = 0.5
    # Set biophysics, signalling, and regulation models
    
    #max_sqr
    #biophys = CLBacterium(sim, max_cells=max_cells, jitter_z=False, max_sqs=256**2)
    biophys = CLSPP(sim, 
            max_cells=n_cells, 
            gamma_s=gamma_s, 
            Fm=Fm,
            Wc=Wc,
            fcil=fcil,
            ftax=0,
            D=D,
            max_spheres=2, 
            grid_spacing=2,
            max_substeps=1,
            cgs_tol=1e-4,
            spherical=True)

    # use this file for reg too
    regul = ModuleRegulator(sim)
    # Only biophys and regulation
    sim.init(biophys, regul, None, None)

    # Specify the initial cell and its location in the simulation
    for i in range(n_cells):
        p = np.random.uniform(-20,20, size=(3,))
        p = p * sphere_rad / np.sqrt(np.sum(p*p))
        cell_dir = np.random.uniform(-1,1, size=(3,))
        cell_dir /= np.sqrt(np.sum(cell_dir*cell_dir))
        sim.addCell(cellType=0, dir=tuple(cell_dir), pos=tuple(p))


    print('sphere_rad = ', sphere_rad)
    biophys.addSphere((0,0,0), sphere_rad, 50, 1.)
    biophys.addSphere((0,0,0), sphere_rad, 50, -1.)


    # Add some objects to draw the models
    therenderer = Renderers.GLSphereRenderer(sim, 
                                            draw_sphere=True, 
                                            sphere_radius=sphere_rad,
                                            sphere_color=[0,0,0,0.5],
                                            draw_axis=False,
                                            draw_gradient=False)
    sim.addRenderer(therenderer)

    sim.pickleSteps = 5

def init(cell):
    cell.color = [0.5,1,0.5]

def update(cells):
    pass

def divide(parent, d1, d2):
    pass

