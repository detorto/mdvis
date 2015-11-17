import numpy

from numba import jit,float64,int8,autojit

class RegionFilter:

	def __init__(self, region):
		self.region = region
	def __call__(self, particles_container):
		print "RegionFilter"
		print "making mask"
		indexes = []
		indexes.append(  particles_container.x > self.region[0] )
		indexes.append(  particles_container.x < self.region[1] )
		indexes.append(  particles_container.y > self.region[2] )
		indexes.append(  particles_container.y < self.region[3] )
		indexes.append(  particles_container.z > self.region[4] )
		indexes.append(  particles_container.z < self.region[5] )
		print "xoring"
		i = indexes[0] & indexes[1] & indexes[2] & indexes[3] & indexes[4] & indexes[5]
		print "filtering"
		particles_container.x = particles_container.x[i]
		particles_container.y = particles_container.y[i]
		particles_container.z = particles_container.z[i]
		particles_container.vx = particles_container.vx[i]
		particles_container.vy = particles_container.vy[i]
		particles_container.vz = particles_container.vz[i]
		return particles_container.finalize()