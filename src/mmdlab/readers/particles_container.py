from ..utils import absolute_speed
from ..utils import absolute_temp
import numpy
class  ParticlesContainer:

	def __init__(self, name, atom_d, atom_mass):
		self.d = atom_d
		self.atom_mass = atom_mass
		self.name = name
		a = numpy.array([])
		self.set_particles(a,a,a,a,a,a,a)

	def set_particles(self, n, x, y, z, vx, vy, vz  ):
		self.n = n
		self.x = x
		self.y = y
		self.z = z
		self.vx = vx
		self.vy = vy
		self.vz = vz
		self.data = {"n": n, "x" : x, "y" : y, "z" : z, "vx" : vx, "vy" : vy, "vz" : vz}

	def add_particles(self, n, x, y, z, vx, vy, vz  ):
		self.n = numpy.append(self.n, n)
		self.x = numpy.append(self.x, x)
		self.y = numpy.append(self.y, y)
		self.z = numpy.append(self.z, z)
		self.vx = numpy.append(self.vx, vx)
		self.vy = numpy.append(self.vy, vy)
		self.vz = numpy.append(self.vz, vz)
		self.data = {"n": n, "x" : x, "y" : y, "z" : z, "vx" : vx, "vy" : vy, "vz" : vz}
	
	def finalize(self):
		self.data["v"] = absolute_speed(self.vx,self.vy,self.vz)
		self.data["t"] = absolute_temp(self.vx, self.vy, self.vz, self.atom_mass)
		self.v = self.data["v"]
		self.t = self.data["t"]

		print 
		return self

	#def __getattr__(self, key):
		#try:
		#	return self.get(key)
		#except:
	#	return self.data[key]
