import os 
import sys
import struct
import numpy
from time import time
from particles_container import ParticlesContainer

import multiprocessing as mp
import threading

from data_parsers import BackupDataParser

#from numba import jit,float64,int8,autojit

def rd(f, t, max_particles):
	while True:
		try:
			print "Reading ",f
			trsp = t.transport_for_file(f)
			return BackupDataParser(trsp).raw_particles(max_particles)
		except:
			print "Bad thing while reading, trying once more"
	
class BackupDataReader:

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

	
	def read(self, transport, max_particles = 100000, np=50):

		print ( "Reading backup directory " + transport.address )

		files = transport.list()
		
		containers = {}

		if self.elemets_description:
			for element in self.elemets_description:
				containers[element] = ParticlesContainer(element, self.elemets_description[element]["atom_d"], self.elemets_description[element]["atom_mass"])
		else:
			containers = ParticlesContainer("Unknown", 1, 1)
		
		if self.elemets_description:
			print ("Created {} containers".format(len(containers)))
		particles_count = max_particles;

		pool = mp.Pool(processes=np)
	
		results = [pool.apply_async(rd, args=(f, transport, max_particles)) for f in files]
		print "Created ",np," readers"

		ts = time();
		for raw_particles in results:
			raw_particles = raw_particles.get()
			n = raw_particles["n"]
			t = raw_particles["t"]
			x = raw_particles["x"]
			y = raw_particles["y"]
			z = raw_particles["z"]
			vx = raw_particles["vx"]
			vy = raw_particles["vy"]
			vz = raw_particles["vz"]
			particles_count = raw_particles["count"]
			tts = time()
			if self.elemets_description:
				
				for element in self.elemets_description:
			#		print "Filtering by type ", element
		
					containers[element].add_particles(n[t == self.elemets_description[element]["id"]], 
													 x[t == self.elemets_description[element]["id"]],
													 y[t == self.elemets_description[element]["id"]],
													 z[t == self.elemets_description[element]["id"]], 
													 vx[t == self.elemets_description[element]["id"]],
													 vy[t == self.elemets_description[element]["id"]],
													 vz[t == self.elemets_description[element]["id"]])

		
			else:
			#	print "Finalizing"
				containers.add_particles(n, x, y, z, vx, vy, vz)
				
		if self.elemets_description:
			for element in self.elemets_description:	
				print "Finalizing ", element
				containers[element].finalize()
				print ("Readed [{}] {} particles".format(len(containers[element].n),element))
		else:
			print "Finalizing "
			containers.finalize()
			print ("Readed [{}] particles".format(len(containers.n)))


		print "Readed directory, total read time:", time()-ts
		
		return containers
