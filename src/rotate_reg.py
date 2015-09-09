# mencoder "mf://mpg_288x288x24_lam15_t273_a0353140_0000_rv.dat_%d.png" -mf fps=20 -o anim.avi -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=500
import numpy
import sys

from mmdlab.datareader import readfile_metgas_boxes
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
import pp

import threading
from multiprocessing.dummy import Pool as ThreadPool

def rotate(deg, v, i):

	mayavi.mlab.view(*v)
	mayavi.mlab.view(azimuth=i*deg)	
	for rot in xrange(deg):
		mayavi.mlab.view(azimuth=i*deg+rot)	
		print "saving to ./advid/{num:05d}.png".format(num=i*deg+rot)
		mayavi.mlab.savefig("./advid/{num:05d}.png".format(num=i*deg+rot))
	mayavi.mlab.close()

#@offscreen
def draw_rot(data,i,v):
	f = open("./jobs/%d.log"%i,"w")
	f.write("Job do")

	size = int(800), int(600)
	mayavi.mlab.options.offscreen = True 

	fig = mayavi.mlab.figure('Viz', size=size,bgcolor=(0,0,0))
	
	print "Reading data"

	m,g = mmdlab.datareader.readfile_metgas_boxes(data,region=[0,20,0,20,9,20])
	f.write("readed")
	if i > 74:
		m.z -=2.1184
		g.z -=2.1184
	
	f.write("fig")
	fig.scene.anti_aliasing_frames = 0
	
	print "Drawing metal"
	mayavi.mlab.points3d(m.x, m.y, m.z, scale_mode="none",scale_factor=m.d,  color=(0.5,0.5,0.5))
	print "Drawing gas"
	mayavi.mlab.points3d(g.x, g.y, g.z, scale_mode="none",scale_factor=g.d, color=(0.5,1,0.5), )	
	if v == None:
		v = mayavi.mlab.view()

	rotate(20, v, i)
	f.write("rotated")
	f.write("Job done")
	return v

def do_mlab():
	global view
	f = open(sys.argv[1]+"/index.list","r")
	lines = f.readlines()

	tasks = []
	lc = len(lines)

	for i,line in enumerate(lines):
		tasks.append( (sys.argv[1]+line[:-1],i))

	f = open(sys.argv[2]+"/index.list","r")
	lines = f.readlines()

	for i,line in enumerate(lines):
		tasks.append((sys.argv[2]+line[:-1],i+lc))

	view = draw_rot(tasks[0][0], 0, None)

	job_server = pp.Server(ncpus = 5)
	jobs = [ job_server.submit(draw_rot,(data,i,view,), (rotate,), ("mmdlab","mmdlab.datareader","mayavi","mayavi.mlab",)) for data,i in tasks[1:]];
	import time
	job_server.print_stats()
	time.sleep(5)
	job_server.print_stats()
	time.sleep(5)
	job_server.print_stats()
	for i,job in enumerate(jobs):
		print "Job ", i
		print job()
		print "Job ", i," done"



	
do_mlab()

