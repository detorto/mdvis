import numpy
import sys


from mayavi import mlab
import time
import pylab


from numba import jit
@jit
def absolute_speed(vx,vy,vz,multiplier=100, kb=1.38065):
	return	numpy.sqrt(((vx*vx) + (vy*vy) + (vz*vz)))*multiplier;

@jit
def absolute_temp(vx,vy,vz,m,multiplier=100, kb=1.38065):
	return multiplier*m*((vx*vx) + (vy*vy) + (vz*vz)) / (3.0*kb)


def offscreen(draw_func):
	def wrapper():
		mlab.options.offscreen = True
		draw_func()
	return wrapper

def saveimg(filename):
	def wrap(draw_func):
		def wrapped_f(*args):
			draw_func(*args)
			mlab.savefig(filename)
		return wrapped_f
	return wrap


def showable(draw_func):
	def wrapper():
		draw_func()
		mlab.show()
	return wrapper

def show_scalar_planes(f):
	planey = mlab.pipeline.image_plane_widget(f, plane_orientation='y_axes')
	planex = mlab.pipeline.image_plane_widget(f, plane_orientation='x_axes')
	planez = mlab.pipeline.image_plane_widget(f, plane_orientation='z_axes')
	return (planex, planey, planez)

def show_vector_planes(f,vx,vy,vz):
	src = mlab.pipeline.vector_scatter(x,y,z,vx,vy,vz)
	planex = mlab.pipeline.vector_cut_plane(src, plane_orientation='x_axes')
	planey = mlab.pipeline.vector_cut_plane(src, plane_orientation='y_axes')
	planez = mlab.pipeline.vector_cut_plane(src, plane_orientation='z_axes')
	return(planex, planey, planez, src)

def make_mlab_scalar_field(x,y,z,v,pts=100j):
	from scipy.interpolate import griddata
	X, Y, Z = numpy.mgrid[x.min():x.max():pts,y.min():y.max():pts,z.min():z.max():pts]
	R = numpy.dstack([x,y,z])
	R = R.reshape((len(x),3))
	F = griddata(R,v,(X,Y,Z))
	fi = mlab.pipeline.scalar_field(F)
	return fi

def init_mlab_scene(size):
	fig = mlab.figure('Viz', size=size, bgcolor=(0,0,0))
	fig.scene.set_size(size)
	fig.scene.anti_aliasing_frames = 0

	mlab.clf()
	return fig


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def pairs(l):
    """Yield successive n-sized chunks from l."""
    for i in xrange(1, len(l)):
        yield (l[i-1],l[i]])