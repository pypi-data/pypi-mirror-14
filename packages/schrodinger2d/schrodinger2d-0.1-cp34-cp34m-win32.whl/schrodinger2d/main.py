import schrodinger2d.pyschrodinger2d as pyschrodinger2d
import numpy

TYPE_CARTESIAN = 10
COLORMAP_GRAY = 1
COLORMAP_TSV = 2
RENDERING_IMG = 1
RENDERING_SURFACE = 2

class Schrodinger2d:
    def __init__(self,px_min,py_min,levels,Lx,normalize=True,colormap=COLORMAP_GRAY,gamma=0.8):
        pyschrodinger2d.open(TYPE_CARTESIAN,px_min,py_min,levels,Lx,normalize,colormap,gamma)
        self.width = 2**(px_min+levels)
        self.height = 2**(py_min+levels)
        self.dx = Lx/(self.width-1)
        self.dy = self.dx
        self.Lx = Lx
        self.Ly = Lx*2**(py_min-px_min)
        
    def close(self):
        pyschrodinger2d.close()
    def time_step(self,dt):
        pyschrodinger2d.time_step(dt)
    def potential_rectangle(self,ci0,cj0,width,height,v):
        pyschrodinger2d.potential_rectangle(ci0,cj0,width,height,v)
    def potential_disk(self,ci0,cj0,radius,v):
        pyschrodinger2d.potential_disk(ci0,cj0,radius,v)
    def potential_function(self,V):
        def function(j,i):
            x = i*1.0/self.width*self.Lx
            y = j*1.0/self.height*self.Ly
            return V(x,y)
        array = numpy.fromfunction(function,shape=(self.height,self.width),dtype=numpy.float32)
        pyschrodinger2d.potential(array)
        return array
    def schrodinger(self,dt):
        pyschrodinger2d.time_step(dt)
        pyschrodinger2d.schrodinger()
        pyschrodinger2d.dirichlet_borders()
    def zero_line(self,i0,j0,length,direction):
        if direction=="u":
            d = 1
        elif direction=="d":
            d = 2
        elif direction=="l":
            d = 3
        elif direction=="r":
            d = 4
        else:
            return
        pyschrodinger2d.dirichlet_line(i0,j0,length,d)
    def zero_line_list(self,line_list):
        for line in line_list:
            self.zero_line(line[0],line[1],line[2],line[3])
    def init(self):
        pyschrodinger2d.init()
    def paquet(self,x0,y0,k0,sigma0):
        pyschrodinger2d.paquet(x0,y0,k0,sigma0)
    def iterations(self,ti,tf,threads=1):
        if threads==1:
            pyschrodinger2d.iterations(ti,tf)
        elif threads==2:
            pyschrodinger2d.iterations_2threads(ti,tf)
        elif threads==4:
            pyschrodinger2d.iterations_4threads(ti,tf)
        else:
            print("Nombre de threads : 1,2 ou 4")
            pyschrodinger2d.iterations_2threads(ti,tf)
    def get_psi(self):
        return pyschrodinger2d.get_psi()
    def get_proba(self):
        return pyschrodinger2d.get_proba()
    def get_proba_colors(self):
        return pyschrodinger2d.get_proba_colors()
    def get_contours(self):
        return pyschrodinger2d.get_contours()
    def opencl_platforms(self):
        pyschrodinger2d.opencl_platforms()
    def set_opencl_platform_device(self,platform,device):
        pyschrodinger2d.set_opencl_platform_device(platform,device)        
    def opencl_init(self):
        pyschrodinger2d.opencl_init()
    def opencl_create_memory(self):
        pyschrodinger2d.opencl_create_memory()
    def opencl_release_memory(self):
        pyschrodinger2d.opencl_release_memory()
    def opencl_iterations(self,ti,tf):
        pyschrodinger2d.opencl_iterations(ti,tf)
    def start_gl(self):
        pyschrodinger2d.start_gl()
    def start_rendering(self,ti,tf,opencl,width,height,rendering=RENDERING_IMG,surface_height=0.5,angle_x=30,angle_z=0):
        pyschrodinger2d.start_rendering(ti,tf,opencl,width,height,surface_height,rendering,angle_x,angle_z)
    def offscreen_rendering(self,ti,tf,opencl,width,height,surface_height=0.3,rendering=RENDERING_IMG,angle_x=30,angle_z=0):
        img = pyschrodinger2d.offscreen_rendering(ti,tf,opencl,width,height,surface_height,rendering,angle_x,angle_z)
        return numpy.flipud(img)
