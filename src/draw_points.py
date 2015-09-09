import numpy
import sys

from mmdlab.datareader import readfile_metgas_boxes

from mmdlab.utils import showable
from mmdlab.utils import saveimg
from mmdlab.utils import offscreen
from mmdlab.utils import init_mlab_scene

from mayavi import mlab
import time
import pylab
from numba import jit
from numba import float64, int8

print "Initing scene"

def rotate(deg):
	
	for rot in xrange(deg):
		mlab.view(azimuth=rot)	
		print "saving to ./advid/{num:03d}.png".format(num=rot)
		mlab.savefig("./advid/{num:03d}.png".format(num=rot))


print "Reading data"
fig = mlab.figure('Viz', size=(1366,768))
#for i,f in enumerate(sys.argv[1:]):
#	i=i+74
m,g = readfile_metgas_boxes(sys.argv[1])
print "Drawing metal"
mlab.points3d(m.x, m.y, m.z, mode="point", scale_mode="none",scale_factor=m.d, colormap="black-white" ,color=(1,1,1))
print "Drawing gas"
mlab.points3d(g.x, g.y, g.z, mode="point", scale_mode="none",scale_factor=g.d, colormap="cool",color=(0.,0.,1)) 
	
#mlab.show()
#rotate(360)
	#mlab.view(0.0, 90.0, 40.432823181152344, [ 20.02327204,  20.03512955,  14.38742304])
	#mlab.view(azimuth=0,elevation=90)
#	print mlab.view()
	#mlab.savefig("./advid/{num:05d}.png".format(num=i))
	#mlab.clf()
mlab.show()