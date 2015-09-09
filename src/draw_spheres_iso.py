#!/usr/bin/python
# mencoder "mf://mpg_288x288x24_lam15_t273_a0353140_0000_rv.dat_%d.png" -mf fps=20 -o anim.avi -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=500
import numpy
import sys

from mmdlab.datareader import readfile_metgas_bin, save_region
from mmdlab.utils import make_mlab_scalar_field
from mmdlab.utils import show_scalar_planes
from mmdlab.utils import show_vector_planes
from mmdlab.utils import init_mlab_scene

from utils import offscreen
from utils import saveimg

from mayavi import mlab
import time
import pylab


@decoratorFunctionWithArguments("1","2","3")
def do_mlab():

	figure = init_mlab_scene((1920,1080))	
	figure.scene.anti_aliasing_frames = 0
	
	(metal, gas) = readfile_metgas_bin(sys.argv[2],[50,70,50,70, 5,12])

	scatter_g = mlab.pipeline.scalar_scatter(gas.x,gas.y,gas.z,gas.v)
	scatter_m = mlab.pipeline.scalar_scatter(metal.x,metal.y,metal.z,metal.v)

	metp = mlab.points3d(metal.x,metal.y,metal.z,scale_mode="none",scale_factor=metal.d,colormap="black-white" ,color=(1,1,1),resolution=6)
	gasp = mlab.points3d(gas.x,gas.y,gas.z,scale_mode="none",scale_factor=gas.d,colormap="cool",color=(0.5,0.5,1),resolution=6)
	
	print "gauss"
	
	gsm = mlab.pipeline.gaussian_splatter(scatter_m)
	gsg = mlab.pipeline.gaussian_splatter(scatter_g)
	
	print "surf"
	mlab.pipeline.iso_surface(gsm,contours=5,opacity=0.5,colormap="copper",transparent=True)
	mlab.pipeline.iso_surface(gsg,contours=5,opacity=0.5,colormap="cool",transparent=True)


#	mlab.show()
	

do_mlab()
