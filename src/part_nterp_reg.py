# mencoder "mf://mpg_288x288x24_lam15_t273_a0353140_0000_rv.dat_%d.png" -mf fps=20 -o anim.avi -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=500
import numpy
import sys

from mmdlab.datareader import readfile_track_fast
from mmdlab.utils import make_mlab_scalar_field
from mmdlab.utils import show_scalar_planes
from mmdlab.utils import show_vector_planes
from mmdlab.utils import init_mlab_scene

from mmdlab.utils import showable
from mmdlab.utils import saveimg
from mmdlab.utils import offscreen
import mmdlab

from mayavi import mlab
import mayavi
import time
import pylab
from numba import jit
from numba import float64, int8
#import pp

import threading
from multiprocessing.dummy import Pool as ThreadPool
import glob
	
files = glob.glob(sys.argv[1])
file_c = len(files)

frame_count = 50.0
fc  = 0
init_mlab_scene((800,600))

def saved(str):
	return "Saved "+str
def simg(fc):

	mlab.view(45.0, 54.735610317245346, 15.002953389457407, [ 37.98949814,  37.52174377,  13.84111261])
	mlab.savefig("./advid/close_{num:09d}.png".format(num=fc))
	print saved("./advid/close_{num:09d}.png".format(num=fc))
	
	mlab.view(0, 85.735610317245346, 15.002953389457407, [ 37.98949814,  37.52174377,  13.84111261])
	mlab.savefig("./advid/close_proj_{num:09d}.png".format(num=fc))
	print saved("./advid/close_proj_{num:09d}.png".format(num=fc))
	
	mlab.view(45.0, 54.735610317245346, 23.002953389457407, [ 37.98949814,  37.52174377,  13.84111261])
	mlab.savefig("./advid/far_{num:09d}.png".format(num=fc))
	print saved("./advid/far_{num:09d}.png".format(num=fc))
	
	mlab.view(45, 85.735610317245346, 23.002953389457407, [ 37.98949814,  37.52174377,  13.84111261])
	mlab.savefig("./advid/far_proj_{num:09d}.png".format(num=fc))
	print saved("./advid/far_proj_{num:09d}.png".format(num=fc))

	mlab.view(0, 85.735610317245346, 23.002953389457407, [ 37.98949814,  37.52174377,  13.84111261])
	mlab.savefig("./advid/far_proj2_{num:09d}.png".format(num=fc))
	print saved("./advid/far_proj2_{num:09d}.png".format(num=fc))

	mlab.view(0, 0, 15.002953389457407, [ 37.98949814,  37.52174377,  13.84111261])
	mlab.savefig("./advid/up_{num:09d}.png".format(num=fc))
	print saved("./advid/up_{num:09d}.png".format(num=fc))

#parts = load_parts("./nth_35-40.dat")

#print "Loaded parts", len(parts)
print files
print file_c
for i in xrange(len(sys.argv[1:])):
	print sys.argv[i+1], sys.argv[i+2]
	m,g = readfile_track_fast(sys.argv[i+1], sys.argv[i+2], region= [36,40,35,40,8,20])


	print "Drawing metal"
	mp = mayavi.mlab.points3d(m.x, m.y, m.z,m.t, scale_mode="none",scale_factor=m.d,  colormap="black-white")
	print mlab.view()
	print "Drawing gas"
	gp = mayavi.mlab.points3d(g.x, g.y, g.z,g.t, scale_mode="none",scale_factor=g.d, colormap="cool", )	
	#mlab.outline()
	mlab.title('Time [0{num:09d}]' .format(num=(int(files[i][-13:-3]))))
	simg(fc)
	fc +=1
	gvx = numpy.array(g.x)
	gvy = numpy.array(g.y)
	gvz = numpy.array(g.z)
	gvt = numpy.array(g.t)

	mvx = numpy.array(m.x)
	mvy = numpy.array(m.y)
	mvz = numpy.array(m.z)
	mvt = numpy.array(m.t)
	
	for ii,gg in enumerate(g.n):
		#print ii
		gvx[ii] = (g.nx[ii] - g.x[ii])/frame_count
		#g.x[ii] += vec
		gvy[ii] = (g.ny[ii] - g.y[ii])/frame_count
		#g.y[ii] += vec
		gvz[ii] = (g.nz[ii] - g.z[ii])/frame_count

		gvt[ii] = (g.nt[ii] - g.t[ii])/frame_count
		#g.z[ii] += vec


	for ii,gg in enumerate(m.n):
		mvx[ii] = (m.nx[ii] - m.x[ii])/frame_count
		#m.x[ii] += vec
		mvy[ii] = (m.ny[ii] - m.y[ii])/frame_count
		#m.y[ii] += vec
		mvz[ii] = (m.nz[ii] - m.z[ii])/frame_count
		mvt[ii] = (m.nt[ii] - m.t[ii])/frame_count
		#m.z[ii] += vec

	for f in xrange(int(frame_count)):
		
		g.x = g.x+gvx
		g.y = g.y+gvy
		g.z = g.z+gvz
		g.t = g.t + gvt

		m.x = m.x+mvx
		m.y = m.y+mvy
		m.z = m.z+mvz
		m.t = m.t+mvt

		gp.mlab_source.reset(x=g.x, y=g.y, z=g.z,scalars=g.t)
		mp.mlab_source.reset(x=m.x, y=m.y, z=m.z,scalars=m.t)
		#mlab.outline()
		
		simg(fc)
		fc += 1
	mlab.clf()


#mayavi.mlab.view(focalpoint=[5,5,15], distance=40)
#mayavi.mlab.show()