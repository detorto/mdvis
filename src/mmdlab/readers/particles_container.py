from ..utils import absolute_speed
from ..utils import absolute_temp

class  ParticlesContainer:

	def __init__(self, name, atom_d, atom_mass):
		self.d = atom_d
		self.atom_mass = atom_mass
		self.name = name

	def addParticles(self, n, x, y, z, vx, vy, vz  ):
		self.n = n
		self.x = x
		self.y = y
		self.z = z
		self.vx = vx
		self.vy = vy
		self.vz = vz
		self.data = {"n": n, "x" : x, "y" : y, "z" : z, "vx" : vx, "vy" : vy, "vz" : vz}
	
	def finalize(self):
		self.data["v"] = absolute_speed(self.vx,self.vy,self.vz)
		self.data["t"] = absolute_temp(self.vx, self.vy, self.vz, self.atom_mass)
		self.v = self.data["v"]
		self.t = self.data["t"]
		return self

	#def __getattr__(self, key):
		#try:
		#	return self.get(key)
		#except:
	#	return self.data[key]
