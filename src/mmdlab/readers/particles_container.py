from ..utils import absolute_speed
from ..utils import absolute_temp
from  time import time
import numpy
import numpy as np
class  ParticlesContainer:

	def __init__(self, name, atom_d, atom_mass):
		self.d = atom_d
		self.atom_mass = atom_mass
		self.name = name

		self.n = []
		self.x = []
		self.y = []
		self.z = []
		self.vx = []
		self.vy = []
		self.vz = []

	def set_particles(self, n, x, y, z, vx, vy, vz  ):
#		pass
		self.n = n
		self.x = x
		self.y = y
		self.z = z
		self.vx = vx
		self.vy = vy
		self.vz = vz
		self.data = {"n": n, "x" : x, "y" : y, "z" : z, "vx" : vx, "vy" : vy, "vz" : vz}

	def add_particles(self, n, x, y, z, vx, vy, vz  ):
		self.n.append(n)
		self.x.append(x)
		self.y.append(y)
		self.z.append(z)
		self.vx.append(vx)
		self.vy.append(vy)
		self.vz.append(vz)
	
	def finalize(self):
		try:	
			self.n = np.concatenate(self.n)
	                self.x = np.concatenate(self.x)
	                self.y = np.concatenate(self.y)
        	        self.z = np.concatenate(self.z)
                	self.vx = np.concatenate(self.vx)
	                self.vy = np.concatenate(self.vy)
        	        self.vz = np.concatenate(self.vz)
		except:
			pass

		self.data = {"n": self.n, "x" : self.x, "y" : self.y, "z" : self.z, "vx" :self.vx, "vy" : self.vy, "vz" : self.vz}

		self.data["v"] = absolute_speed(self.vx,self.vy,self.vz)
		self.data["t"] = absolute_temp(self.vx, self.vy, self.vz, self.atom_mass)
		self.v = self.data["v"]
		self.t = self.data["t"]

		print 
		return self
