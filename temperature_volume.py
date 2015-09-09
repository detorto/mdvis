
# coding: utf-8

import sys
sys.path.append("D:\\projects\\visual\\")
from mmdlab.datareader import readfile_metgas_boxes
from mmdlab.utils import init_mlab_scene
import glob
from mayavi import mlab
from tvtk.api import tvtk


init_mlab_scene((200,768))
fc = 1500
rot_per_frame = 20

files = glob.glob(sys.argv[1])
file_c = len(files)
def saved(str):
	return "Saved "+str


for f in files:
	(metal, gas) = readfile_metgas_boxes(f)
	gas.z = gas.z - 2.11884
	gscatt = mlab.pipeline.scalar_scatter(gas.x, gas.y, gas.z, gas.t)
	

	print "Temp gauss"
	mlab.title('Time [0{num:09d}]' .format(num=(750000+int(f[-13:-3])))).y_position=1
	#mlab.title('Time [0{num:09d}]' .format(num=(int(f[-13:-3])))).y_position=1
	filt = tvtk.GaussianSplatter()
	filt.radius=0.01
	filt.exponent_factor=-1.3
	filt.scale_factor=1.760

	tggauss_fog = mlab.pipeline.user_defined(gscatt, filter=filt)
	
	print "Done"
	tvol = mlab.pipeline.volume(tggauss_fog)
	
	tvol._volume_property.shade=False
	from tvtk.util.ctf import load_ctfs

	#ctf.add_hsv_point(0.975528258148,0.0521448216801, 1.0, 1.0)
	#ctfdic200 = {'alpha': [[0.0, 0.0], [2555.8166094521594, 0.019954483358229635]], 'range': (0.0, 62.545284288648858), 'rgb': [[0.0, 0.0, 0.0, 1.0], [62.545284288648858, 0.0, 0.31286893008046235, 1.0], [244.05876894980238, 0.0, 0.6180339887498951, 1.0], [526.77264942601448, 0.0, 0.9079809994790933, 1.0], [883.0129213128422, 0.0, 1.0, 0.7861513777574228], [1277.9083047260797, 0.0, 1.0, 0.0], [1672.8036881393173, 0.7861513777574234, 1.0, 0.0], [2029.043960026145, 1.0, 0.9079809994790935, 0.0], [2311.7578405023573, 1.0, 0.618033988749895, 0.0], [2493.2713251635109, 1.0, 0.31286893008046185, 0.0], [2555.8166094521594, 1.0, 0.0, 0.0]]}
	#ctfdic273 = {'alpha': [[0.0, 0.0], [1829.0109806669739, 0.027883922261309858]], 'range': (0.0, 44.759084564129651), 'rgb': [[0.0, 0.0, 0.0, 1.0], [44.759084564129651, 0.0, 0.31286893008046235, 1.0], [174.65500720450189, 0.0, 0.6180339887498951, 1.0], [376.97264997496654, 0.0, 0.9079809994790933, 1.0], [631.90775237124535, 0.0, 1.0, 0.7861513777574228], [914.50549033348693, 0.0, 1.0, 0.0], [1197.1032282957285, 0.7861513777574234, 1.0, 0.0], [1452.0383306920073, 1.0, 0.9079809994790935, 0.0], [1654.3559734624721, 1.0, 0.618033988749895, 0.0], [1784.2518961028445, 1.0, 0.31286893008046185, 0.0], [1829.0109806669739, 1.0, 0.0, 0.0]]}
	ctfdic346 = {'alpha': [[0.0, 0.0], [2412.1699408088612, 0.021142788962413825]], 'range': (0.0, 59.030000095649484), 'rgb': [[0.0, 0.0, 0.0, 1.0], [59.030000095649484, 0.0, 0.31286893008046235, 1.0], [230.34173268704083, 0.0, 0.6180339887498951, 1.0], [497.16601178910247, 0.0, 0.9079809994790933, 1.0], [833.38421788925609, 0.0, 1.0, 0.7861513777574228], [1206.0849704044306, 0.0, 1.0, 0.0], [1578.7857229196052, 0.7861513777574234, 1.0, 0.0], [1915.0039290197587, 1.0, 0.9079809994790935, 0.0], [2181.8282081218204, 1.0, 0.618033988749895, 0.0], [2353.1399407132121, 1.0, 0.31286893008046185, 0.0], [2412.1699408088612, 1.0, 0.0, 0.0]]}
	load_ctfs(ctfdic346,tvol._volume_property)
	#mlab.axes(nb_labels=15)
	#mlab.outline();
	for k in xrange(rot_per_frame):
		mlab.view(fc, 90, 3711, [50.1,50.1,774.5])
		mlab.savefig("./temper_distr/{num:09d}.png".format(num=fc))
		print saved("./temper_distr/{num:09d}.png".format(num=fc))
		fc+=1
	
	mlab.clf()




