# mencoder "mf://mpg_288x288x24_lam15_t273_a0353140_0000_rv.dat_%d.png" -mf fps=20 -o anim.avi -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=500
import numpy
import sys

from mmdlab.datareader import readfile_metgas_bin
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
import pp



#@jit(int8(float64,float64,float64, float64,float64,float64,int8,int8),nogil=True)
def mfilter(x,y,z,vx,vy,vz,t,n):
	ns =[8144152, 8142982, 8137175, 8142432, 8132058, 8130816, 8139516, 8137854, 8139295,
 8154596, 8129084, 8134502, 8149714, 8134528, 8145199, 8131842, 8155706, 8129805,
 8139771, 8146148, 8135555, 8134526, 8144085, 8130692, 8148841, 8142874, 8134494,
 8129329, 8154557, 8128711, 8150156, 8150207, 8142836, 8154068, 8134148, 8129157,
 8143673, 8144130, 8148536, 8128829, 8155106, 8137542, 8150948, 8135426, 8151492,
 8155319, 8140672, 8144383, 8152104, 8145686, 8140149, 8155759, 8140222, 8151178,
 8135977, 8149256, 8147517, 8148704, 8133363, 8155726, 8154429, 8139576, 8152290,
 8151215, 8130536, 8139455, 8155697, 8147242, 8145822, 8137803, 8134794, 8149551,
 8129039, 8149311, 8131412, 8130617, 8130340, 8133518, 8153647, 8144446, 8147725,
 8141710, 8128719, 8137067, 8155636, 8138744, 8149002, 8131983, 8156214, 8139178,
 8148133, 8135299, 8142516, 8129059, 8148007, 8129397, 8139214, 8135681, 8155840,
 8151616, 8147665, 8146178, 8136830, 8150754, 8128688, 8154616, 8141421, 8145621,
 8153072, 8142961, 8139978, 8144150, 8134973, 8130922, 8150702, 8145994, 8138922,
 8135463, 8150372, 8155600, 8151275, 8146091, 8131391, 8146084, 8131485, 8136487,
 8147690, 8145297, 8142450, 8144011, 8146063, 8152593, 8140472, 8141862, 8147634,
 8153645, 8138217, 8131751, 8132770, 8138279, 8131678, 8149772, 8141578, 8143689,
 8137524, 8129998, 8148840, 8136955, 8152885, 8137300, 8150211, 8138343, 8140685,
 8150252, 8151006, 8151222, 8134343, 8136585, 8152699, 8152629, 8156585, 8147751,
 8154660, 8134584, 8142159, 8150187, 8154913, 8148868, 8135148, 8150579, 8138668,
 8154089, 8156221, 8131715, 8146196, 8134778, 8141532, 8132951, 8145946, 8133361,
 8129611, 8137788, 8140157, 8146085, 8149448, 8142679, 8148455, 8144180, 8135738,
 8143517, 8140707, 8145667, 8153296, 8151223, 8144199, 8146648, 8129640, 8133488,
 8132506, 8149683, 8145992, 8133813, 8139051, 8155016, 8132819, 8130806, 8138958,
 8149266, 8129537, 8150855, 8133341, 8155787, 8156076, 8132352, 8150047, 8133205,
 8154433, 8139094, 8138391, 8149463, 8146049, 8154772, 8139710, 8133987, 8144938,
 8156507, 8145558, 8132492, 8154418, 8148501, 8133796, 8140191, 8137956, 8133245,
 8152886, 8129477, 8132385, 8142977, 8154559, 8141061, 8149822, 8148963, 8149369,
 8134210, 8146548, 8130786, 8133663, 8139704, 8140119, 8146637, 8142395, 8142729,
 8135689, 8150938, 8144609, 8130139, 8135347, 8147166, 8149730, 8146620, 8134913,
 8134598, 8141882, 8143001, 8129198, 8144080, 8139374, 8139692, 8135254, 8133328,
 8142561, 8137775, 8140855, 8134791, 8150071, 8151090, 8129054, 8149964, 8132777,
 8132536, 8132268, 8136593, 8149078, 8154799, 8129224, 8139046, 8137099, 8152772,
 8153219, 8135262, 8150266, 8136507, 8132670, 8153935, 8155594, 8137538,]
	#global ns	
	if t == 0 and z > 9:
		return 1
	else:
		if n in ns:
			return 1
		else:
			return 0
	return 0

#@showable
#@saveimg("test.png")

import threading
from multiprocessing.dummy import Pool as ThreadPool


def readdata(datafile):
	print datafile
	return mmdlab.datareader.readfile_metgas_bin(datafile,pfilter=mfilter, parts_at_once=10000)

@jit(nogil = True)
def get_traj(gas_steps):
	parts = {}
	for n in gas_steps[0].n:
		print "Making traj for ", n
		
		parts[n] = {"x":[],"y":[],"z":[],"t":[]}

		for step in gas_steps:
			parts[n]["x"].append(step.x[numpy.where(step.n==n)])
			parts[n]["y"].append(step.y[numpy.where(step.n==n)])
			parts[n]["z"].append(step.z[numpy.where(step.n==n)])
			parts[n]["t"].append(step.t[numpy.where(step.n==n)])

	return parts

def do_mlab():

	f = open(sys.argv[1]+"/index.list","r")
	lines = f.readlines()


	calls = []
	lc = None
	for i,line in enumerate(lines):
		calls.append( (i, sys.argv[1]+line[:-1])) #,region=[0,10000,0,30,8,13])
		lc = sys.argv[1]+line[:-1]		
	print calls

	ppservers = ()
	job_server = pp.Server(ppservers=ppservers, ncpus = 10)

	print "Starting pp with", job_server.get_ncpus(), "workers"
	# The following submits 8 jobs and then retrieves the results
	jobs = [ job_server.submit(readdata,(data[1],), (mfilter,), ("mmdlab","mmdlab.datareader")) for data in calls];

	size = int(1920), int(1080)
	fig = mlab.figure('Viz', size=size,bgcolor=(0,0,0))
	fig.scene.anti_aliasing_frames = 0

	import time
	gas  = []
	for i,job in enumerate(jobs):
		(metal,g)  =  job()
		gas.append(g)
		print "Job",i,"done"

	traj = get_traj(gas)

	parts_no = [8144152,8156221, 8131715, 8146196, 8134778, 8141532, 8132951, 8145946, 8133361,
 8129611, 8137788, 8140157, 8146085,]
	lm,lg = readfile_metgas_bin(lc, pfilter=mfilter, parts_at_once=10000)
	for p in parts_no:
		val = traj[p]
		ppl = mlab.plot3d(val["x"], val["y"], val["z"], val["t"], tube_radius=0.025, colormap='cool');
		mlab.colorbar(ppl)
		#for g in gas:
		#	mlab.points3d(g.x[numpy.where(g.n == p)],g.y[numpy.where(g.n == p)],g.z[numpy.where(g.n == p)],scale_factor=lm.d, colormap='cool')
		#	mlab.text(color=(1,0,0),width=0.06,x = g.x[numpy.where(g.n == p)][0],y= g.y[numpy.where(g.n == p)][0],z = g.z[numpy.where(g.n == p)][0],text = str(g.t[numpy.where(g.n == p)][0]))
	#mlab.points3d(lg.x, lg.y, lg.z, lg.t, scale_mode="none",scale_factor=lg.d, colormap="cool")
	
	mscat = mlab.pipeline.scalar_scatter(lm.x, lm.y, lm.z)
	mgauss = mlab.pipeline.gaussian_splatter(mscat)

	mlab.pipeline.iso_surface(mgauss,colormap="black-white",contours=[0.9999,],opacity = 1)
	#mlab.points3d(lm.x, lm.y, lm.z, lm.t, scale_mode="none",scale_factor=lm.d, colormap="copper")
	#for val in traj.values():
	#	
		#print "Drawing metal"
		#metp = mlab.points3d(metal.x,metal.y,metal.z,metal.v,scale_mode="none",scale_factor=metal.d, colormap="copper",mode = "point",mask_points = 100)
		#print "Drawing gas"
		#gasp = mlab.points3d(gas.x,gas.y,gas.z,gas.v,scale_mode="none",scale_factor=gas.d,colormap="cool")
		#print "saving to ./vid/{num:02d}.png".format(num=i)
		#mlab.savefig("./vid/{num:02d}.png".format(num=i))
		#mlab.clf()
	mlab.show()





do_mlab()
