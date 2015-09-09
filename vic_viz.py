
import numpy
import sys

from mmdlab.datareader import readfile_tex_vic
from mmdlab.utils import make_mlab_scalar_field
from mmdlab.utils import show_scalar_planes
from mmdlab.utils import show_vector_planes
from mmdlab.utils import init_mlab_scene

from mmdlab.utils import showable
from mmdlab.utils import saveimg
from mmdlab.utils import offscreen

from mayavi import mlab
import time
import pylab
from numba import jit
from numba import float64, int8

def do_mlab():

	gas = readfile_tex_vic(sys.argv[1])

	size = int(1920), int(1080)
	fig = mlab.figure('Viz', size=size,bgcolor=(0,0,0))
	#fig.scene.anti_aliasing_frames = 0
	#print "Drawing metal"
	#metp = mlab.points3d(metal.x,metal.y,metal.z,metal.v,scale_mode="none",scale_factor=metal.d, colormap="copper")
#	print "Drawing gas"
	print gas.x
	scatter_g = mlab.pipeline.scalar_scatter(gas.x,gas.y,gas.z,gas.t, scale_mode="none",scale_factor=gas.d)
	
	gasp = mlab.points3d(gas.x, gas.y, gas.z, gas.t, scale_mode="none",scale_factor=gas.d)
	print gas.x.min()
	print gas.x.max()
	mlab.outline()
	mlab.colorbar(title='T', orientation='vertical', nb_labels=3)

		#print "saving to ./vid/{num:02d}.png".format(num=i)
		#mlab.savefig("./vid/{num:02d}.png".format(num=i))
		#mlab.clf()
	mlab.show_pipeline()
	mlab.show()






do_mlab()
