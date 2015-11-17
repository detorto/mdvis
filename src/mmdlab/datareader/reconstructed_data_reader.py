import os 
import sys
import struct
import numpy

from particles_container import ParticlesContainer

from data_parsers import ReconstructedDataParser

from numba import jit,float64,int8,autojit

class ReconstructedDataReader:

	def __init__(self, elemets_description = None, data_parser = ReconstructedDataParser, chunk_size = 100000):
		self.elemets_description = elemets_description
		self.chunk_size = chunk_size
		self.data_parser = data_parser
		if not self.elemets_description:
			return

		for elem in elemets_description:
			try:
				elemets_description[elem]["id"]
			except:
				raise "Elements description has to have \"id\" field"

	
	def read(self, transport, max_particles = 9000000, ):

		print ( "Reading binary boxes from " + transport.address )
		
		containers = {}
		if self.elemets_description:
			for element in self.elemets_description:
				containers[element] = ParticlesContainer(element, self.elemets_description[element]["atom_d"], self.elemets_description[element]["atom_mass"])
		else:
			containers = ParticlesContainer("Unknown", 1, 1)
		
		if self.elemets_description:
			print ("Created {} containers".format(len(containers)))
		particles_count = max_particles;
		
		raw_particles  = self.data_parser(transport).raw_particles(max_particles)
		
		n = raw_particles["n"]
		t = raw_particles["t"]
		x = raw_particles["x"]
		y = raw_particles["y"]
		z = raw_particles["z"]
		vx = raw_particles["vx"]
		vy = raw_particles["vy"]
		vz = raw_particles["vz"]
		particles_count = raw_particles["count"]

		if self.elemets_description:
			for element in self.elemets_description:
				print "Filtering by type ", element
				containers[element].set_particles(n[t == self.elemets_description[element]["id"]], 
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
			containers.set_particles(n, x, y, z, vx, vy, vz)
			containers.finalize()
			print ("Readed [{}] particles".format(len(containers.n)))
			
		print "returning"
		return containers