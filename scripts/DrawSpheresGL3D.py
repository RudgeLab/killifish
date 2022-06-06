from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PIL import Image
from PIL import ImageOps

from CellModeller.GUI.Renderers import GLSphereRenderer

import sys
import pickle as pickle

fname = '/Users/guillermo/Code/killifish/pickles/'#/data/SPPTest_diffusion-20-07-25-22-41/step-00000.pickle'
width, height = 1024, 1024

class DummySim:
    def __init__(self, cellStates, stepNum):
        self.cellStates = cellStates
        self.stepNum = stepNum

class GLRenderer():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.modelview_matrix_  = []
        self.translate_vector_  = [0.0, 0.0, 0.0]
        self.viewport_matrix_   = []
        self.projection_matrix_ = []
        self.near_   = 0.1
        self.far_    = 400.0
        self.fovy_   = 45.0

        self.set_radius(32)

        glClearColor(1.0, 1.0, 1.0, 1.0)

        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        gluPerspective( self.fovy_, float(width) / float(height), self.near_, self.far_ ) 

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.modelview_matrix_ = glGetDoublev( GL_MODELVIEW_MATRIX )
        glLoadMatrixd(self.modelview_matrix_)

    def set_projection(self, _near, _far, _fovy):
        self.near_ = _near
        self.far_ = _far
        self.fovy_ = _fovy
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        gluPerspective( self.fovy_, float(width) / float(height), self.near_, self.far_ )

    def set_center(self, _cog):
        self.center_ = _cog
        self.view_all()

    def set_radius(self, _radius):
        self.radius_ = _radius
        self.set_projection(_radius / 100.0, _radius * 100.0, self.fovy_)
        self.reset_view()
        self.translate([0, 0, -_radius * 2.0])
        self.view_all()

    def reset_view(self):
        # scene pos and size
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity();
        self.modelview_matrix_ = glGetDoublev( GL_MODELVIEW_MATRIX )
        self.set_center([0.0, 0.0, 0.0])

    def translate(self, _trans):
        # Translate the object by _trans
        # Update modelview_matrix_
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(_trans[0], _trans[1], _trans[2])
        glMultMatrixd(self.modelview_matrix_)
        self.modelview_matrix_ = glGetDoublev(GL_MODELVIEW_MATRIX)
        self.translate_vector_[0] = self.modelview_matrix_[3][0]
        self.translate_vector_[1] = self.modelview_matrix_[3][1]
        self.translate_vector_[2] = self.modelview_matrix_[3][2]

    def view_all(self):
        self.translate( [ -( self.modelview_matrix_[0][0] * self.center_[0] +
                             self.modelview_matrix_[0][1] * self.center_[1] +
                             self.modelview_matrix_[0][2] * self.center_[2] +
                             self.modelview_matrix_[0][3]),
                           -( self.modelview_matrix_[1][0] * self.center_[0] +
                              self.modelview_matrix_[1][1] * self.center_[1] +
                              self.modelview_matrix_[1][2] * self.center_[2] +
                              self.modelview_matrix_[1][3]),
                           -( self.modelview_matrix_[2][0] * self.center_[0] +
                              self.modelview_matrix_[2][1] * self.center_[1] +
                              self.modelview_matrix_[2][2] * self.center_[2] +
                              self.modelview_matrix_[2][3] +
                              self.radius_ / 2.0 )])

    def rotate(self, _axis, _angle):
        t = [self.modelview_matrix_[0][0] * self.center_[0] +
             self.modelview_matrix_[1][0] * self.center_[1] +
             self.modelview_matrix_[2][0] * self.center_[2] +
             self.modelview_matrix_[3][0],
             self.modelview_matrix_[0][1] * self.center_[0] +
             self.modelview_matrix_[1][1] * self.center_[1] +
             self.modelview_matrix_[2][1] * self.center_[2] +
             self.modelview_matrix_[3][1],
             self.modelview_matrix_[0][2] * self.center_[0] +
             self.modelview_matrix_[1][2] * self.center_[1] +
             self.modelview_matrix_[2][2] * self.center_[2] +
             self.modelview_matrix_[3][2]]

        glLoadIdentity()
        glTranslatef(t[0], t[1], t[2])
        glRotated(_angle, _axis[0], _axis[1], _axis[2])
        glTranslatef(-t[0], -t[1], -t[2])
        glMultMatrixd(self.modelview_matrix_)
        self.modelview_matrix_ = glGetDoublev(GL_MODELVIEW_MATRIX)

def render_scene(dummy_sim, renderer, outfn):
    scene_renderer = GLRenderer(width, height)
    # change this for zoom
    scene_renderer.translate([0,0,-75])
    scene_renderer.rotate([0,0,1], -65)
    scene_renderer.rotate([1,0,0], -60.)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()

    
    # Draw a grid in xy plane
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glColor3f(0.5, 0.5, 0.5)
    glEnable(GL_LINE_SMOOTH)
    glLineWidth(1.0)
    
    """
    glBegin(GL_LINES)
    for i in range(25):
        glVertex(-120, (i-12)*10, 0)
        glVertex(120, (i-12)*10, 0)
        glVertex((i-12)*10, -120, 0)
        glVertex((i-12)*10, 120, 0)
    glEnd()
    """
    
    """
    """ 
    # Draw x,y,z axes
    glBegin(GL_LINES)
    glColor3f(1.0,0.0,0.0)
    glVertex(0,0,0)
    glVertex(25,0,0)
    glColor3f(0.0,1.0,0.0)
    glVertex(0,0,0)
    glVertex(0,25,0)
    glColor3f(0.0,0.0,1.0)
    glVertex(0,0,0)
    glVertex(0,0,25)
    glEnd()
    glPopMatrix()
    

    # Draw model
    renderer.render_gl()

    glDisable(GL_DEPTH_TEST)
    glFlush()
    
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGBA", (width, height), data)
    image = ImageOps.flip(image) # in my case image is flipped top-bottom for some reason
    image.save(outfn, 'PNG')


def main():
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"OpenGL Offscreen")
    #glutHideWindow()

    angle = 0

    # For now just assume a list of files
    #infns = sys.argv[1:]
    
    # massive files in this directory
    path = os.getcwd()+"/pickles"
    folders = os.listdir(path)
    print(folders)
    folders.sort()
    folders = folders[1:]
    for folder in folders:
        print(folder)
        #folder='Wc__1__psi__2__D__1__ftax__0__500__cells_sphere__15__forg__0-20-10-22-21-24'
        infns = os.listdir(os.path.join(path,folder))
        infns.sort()
        infns = infns[1:]
        os.mkdir(os.path.join('figs',folder))
        print(infns)   
        
        for infn in infns:
            print(infn)
            # File names
            if infn[-7:]!='.pickle':
                print(('Ignoring file %s, because its not a pickle...'%(infn)))
                continue

            #########################
            # Just some pickles
            #pics = ['00000','00080','00500','00800']
            #if any(pic in infn for pic in pics):
            #########################
            outfn = infn.replace('.pickle', '.png')
            outfn = os.path.basename(os.path.join(folder,outfn)) # Put output in this dir
            print(('Processing %s to generate %s'%(infn,outfn)))
            
            # Import data
            print(path+folder+"/"+infn)
            data = pickle.load(open(os.path.join(path,folder,infn), 'rb'))
            if not data:
                print("Problem importing data!")
                return
            
            cs = data['cellStates']
            
            for cell in cs.keys():
                cs[cell].color=[1,47/203,57/203]
            #dummy_sim = DummySim(data['cellStates'], 0)
            dummy_sim = DummySim(cs, 0)
            renderer = GLSphereRenderer(dummy_sim, 
                                        draw_axis=False, 
                                        draw_nbr_dir=False, 
                                        draw_gradient=False,
                                        draw_sphere=True,
                                        #sphere_color=[0,0,0,0.5],
                                        sphere_color=[0,0,0,0.2],
                                        sphere_radius=25)
            render_scene(dummy_sim, renderer, os.path.join(os.getcwd(),"figs",folder,outfn))
            #else:
             #   continue
        #break
main()
