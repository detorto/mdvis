from particles_container import ParticlesContainer
import os 
import sys
import struct
import numpy

from numba import jit,float64,int8,autojit

def raw_particles(f,box_count,particles_count):

	n = numpy.zeros(particles_count, dtype='i')
	t = numpy.zeros(particles_count, dtype='i')		
	x = numpy.zeros(particles_count, dtype='d')
	y = numpy.zeros(particles_count, dtype='d')
	z = numpy.zeros(particles_count, dtype='d')
	vx = numpy.zeros(particles_count, dtype='d')
	vy = numpy.zeros(particles_count, dtype='d')
	vz = numpy.zeros(particles_count, dtype='d')
	
	
	particles_count = 0;
	for box in xrange(box_count):

		if box % 100000==0:
			print "Reading box", box, "of",box_count
	
		data = f.read(4*5)
		
		if not data:
			break;
		
		bxyz2, blay, breal, msize, csize  =  struct.unpack("iiiii", data);

		if csize <= 0:
			continue 
	
		data = f.read((4+4+8+8+8+8+8+8)*csize)
		
		ud = struct.unpack("%di%di%dd%dd%dd%dd%dd%dd"%(csize,csize,csize,csize,csize,csize,csize,csize),data)
		
		t[particles_count:particles_count+csize] = ud[0:csize]
		n[particles_count:particles_count+csize] = ud[csize:csize*2]
		x[particles_count:particles_count+csize] = ud[csize*2:csize*3]
		y[particles_count:particles_count+csize] = ud[csize*3:csize*4]
		z[particles_count:particles_count+csize] = ud[csize*4:csize*5]
		vx[particles_count:particles_count+csize] = ud[csize*5:csize*6]
		vy[particles_count:particles_count+csize] = ud[csize*6:csize*7]
		vz[particles_count:particles_count+csize] = ud[csize*7:csize*8]
		particles_count += csize;

	return n,t,x,y,z,vx,vy,vz,particles_count
class BinaryBoxReader:

	def __init__(self, elemets_description = None, chunk_size = 100000):
		self.elemets_description = elemets_description
		self.chunk_size = chunk_size

		if not self.elemets_description:
			return

		for elem in elemets_description:
			try:
				elemets_description[elem]["id"]
			except:
				raise "Elements description has to have \"id\" field"

		

	
	def read(self, filename, max_particles = 9000000):
		print ("Reading " + str(filename) + " as binary boxes")

		f = open(filename, "rb")
		data = f.read(4)
		box_count = struct.unpack("i",data)[0]
		print "Boxes count:",box_count
		
		containers = {}
		if self.elemets_description:
			for element in self.elemets_description:
				containers[element] = ParticlesContainer(element, self.elemets_description[element]["atom_d"], self.elemets_description[element]["atom_mass"])
		else:
			containers = ParticlesContainer("Unknown", 1, 1)
		
		if self.elemets_description:
			print ("Created {} containers".format(len(containers)))
		particles_count = max_particles;

		n,t,x,y,z,vx,vy,vz,particles_count  = raw_particles(f,box_count, max_particles)
		
		if self.elemets_description:
			for element in self.elemets_description:
				print "Filtering by type ", element
				t = t[0:particles_count]
				containers[element].addParticles(n[t == self.elemets_description[element]["id"]], 
												 x[t == self.elemets_description[element]["id"]],
												 y[t == self.elemets_description[element]["id"]],
												 z[t == self.elemets_description[element]["id"]], 
												 vx[t == self.elemets_description[element]["id"]],
												 vy[t == self.elemets_description[element]["id"]],
												 vz[t == self.elemets_description[element]["id"]])

				print "Finalizing ", element
				containers[element].finalize()
				print ("Readed [{}] {} particles".format(len(containers[element].n),element))
		else:
			print "Finalizing"
			containers.addParticles(n, x, y, z, vx, vy, vz)
			print "Finalizing2"
			containers.finalize()
			
		print "returning"
		return containers