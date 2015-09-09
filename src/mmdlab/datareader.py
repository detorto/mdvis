import numpy
from mmdlab.utils import absolute_speed, absolute_temp

import struct
from numba import jit,float64,int8

import os
import sys
class  ParticleContainer:

	def __init__(self, name, atom_d, atom_mass):

		self.x = []
		self.y = []
		self.z = []
		self.vx = []
		self.vy = []
		self.vz = []
		self.nx = []
		self.ny = []
		self.nz = []

		self.n = []
		self.d = atom_d
		self.atom_mass = atom_mass
		self.name = name
	
	#@jit(nogil=True)
	def add_particle(self, n, x, y, z, vx, vy, vz  ):
		self.x.append(x)
		self.y.append(y)
		self.z.append(z)
		self.vx.append(vx)
		self.vy.append(vy)
		self.vz.append(vz)
		self.n.append(n)

	def finalize(self):
		self.x = numpy.array(self.x)
		self.y = numpy.array(self.y)
		self.z = numpy.array(self.z)

		self.nx = numpy.array(self.nx)
		self.ny = numpy.array(self.ny)
		self.nz = numpy.array(self.nz)

		self.vx = numpy.array(self.vx)
		self.vy = numpy.array(self.vy)
		self.vz = numpy.array(self.vz)
		
		self.n = numpy.array(self.n)
		self.v = absolute_speed(self.vx,self.vy,self.vz)
		self.t = absolute_temp(self.vx, self.vy, self.vz, self.atom_mass)
		return self


@jit(int8(float64,float64,float64, float64,float64,float64,int8,int8),nopython=True,nogil=True)
def empty_part_filter(x,y,z,vx,vy,vz, t, n):
	return 1

@jit(int8(float64,float64,float64, float64[:]),nopython=True,nogil=True)
def in_region(x,y,z,region):
	if x >= region[0] and x <= region[1] and y >= region[2] and y <= region[3] and z >= region[4] and z <= region[5]:
		return 1
	else:
		return 0

@jit(nogil=True)
def readfile_metgas_bin( filename, region = None, pfilter = empty_part_filter, parts_at_once = 100000 ):

	particals_in_once = parts_at_once;

	print ("Reading " + str(filename) + " as metal-gas bin")
	nregion = numpy.array(region,dtype=numpy.float64)

	f = open(filename, "rb")
	
	partical_record_size = 56 #bytes
	filesize = os.path.getsize(filename)
	particles_count = filesize / partical_record_size;

	print ("Approximating particles count: [ %d ]" % (particles_count))
	#return (0,0)
	metal = ParticleContainer("Nickel", 0.248, 97.474)
	gas = ParticleContainer("Nitrogenium",0.296, 46.517)

	
	c = 0.0;
	pr = 0;
	prevpc = 0;
	#"""gc.disable()"""
	data = f.read(partical_record_size * particals_in_once);
	while data:		
		
		for i in xrange(len(data)/partical_record_size):
			n,t,x,y,z,vx,vy,vz = struct.unpack("iidddddd",data[i*partical_record_size:(i+1)*partical_record_size])
			
			if (not region or in_region(x, y, z, nregion)>0) and pfilter(x, y, z, vx, vy, vz, t, n) > 0:
				pr +=1
				if t == 0:
					metal.add_particle(n, x, y, z, vx, vy, vz)
				else:
					gas.add_particle(n, x, y, z, vx, vy, vz)

		percens = (c/filesize)*100.0
		if percens - prevpc > 1:
			sys.stdout.write("Readed [%d]prc " % (percens))
			sys.stdout.write("[%d] particles\r" % (pr))
			sys.stdout.flush()
			prevpc = percens;
		
		c += partical_record_size * particals_in_once;
		
		data = f.read(partical_record_size * particals_in_once);
	#"""gc.enable()"""
	
	print ("Readed [%d] gas particles" % (len(gas.n)))
	print ("Readed [%d] metal particles" % (len(metal.n)))
	return (metal.finalize(), gas.finalize())


@jit(nogil=True)
def readfile_metgas_bin_fast( filename,  parts_at_once = 100000 ):

	particals_in_once = parts_at_once;

	print ("Reading " + str(filename) + " as metal-gas bin")
	
	f = open(filename, "rb")
	
	partical_record_size = 56 #bytes
	filesize = os.path.getsize(filename)
	particles_count = filesize / partical_record_size;

	print ("Approximating particles count: [ %d ]" % (particles_count))
	#return (0,0)
	metal = ParticleContainer("Nickel", 0.248, 97.474)
	gas = ParticleContainer("Nitrogenium",0.296, 46.517)

	
	c = 0.0;
	pr = 0;
	prevpc = 0;
	#"""gc.disable()"""
	data = f.read(partical_record_size * particals_in_once);
	while data:		
		
		for i in xrange(len(data)/partical_record_size):
			n,t,x,y,z,vx,vy,vz = struct.unpack("iidddddd",data[i*partical_record_size:(i+1)*partical_record_size])
			
			if t == 0:
				metal.add_particle(n, x, y, z, vx, vy, vz)
			else:
				gas.add_particle(n, x, y, z, vx, vy, vz)

		percens = (c/filesize)*100.0
		if percens - prevpc > 1:
			sys.stdout.write("Readed [%d]prc " % (percens))
			sys.stdout.write("[%d] particles\r" % (pr))
			sys.stdout.flush()
			prevpc = percens;
		
		c += partical_record_size * particals_in_once;
		
		data = f.read(partical_record_size * particals_in_once);
	#"""gc.enable()"""
	
	print ("Readed [%d] gas particles" % (len(gas.n)))
	print ("Readed [%d] metal particles" % (len(metal.n)))
	return (metal.finalize(), gas.finalize())

#@jit(nogil=True)
def readfile_metgas_boxes( filename, region = None, pfilter = empty_part_filter):

	print ("Reading " + str(filename) + " as metal-gas boxes")
	nregion = numpy.array(region,dtype=numpy.float64)

	f = open(filename, "rb")
	
	data = f.read(4)
	box_count = struct.unpack("i",data)[0]
	print "Boxes count:",box_count,

	metal = ParticleContainer("Nickel", 0.248, 97.474)
	gas = ParticleContainer("Nitrogenium",0.296, 46.517)

	for box in xrange(box_count):
		if box % 100000==0:
			print "Reading box", box, "of",box_count
		
		data = f.read(4*5)
		if not data:
			break;
		bxyz2, blay, breal, msize, csize  =  struct.unpack("iiiii",data);
		#print "box size:",csize
		if csize <= 0:
		##	print "Box is empty, skipping"15
			continue 
		
		data = f.read((4+4+8+8+8+8+8+8)*csize)
		
		ud = struct.unpack("%di%di%dd%dd%dd%dd%dd%dd"%(csize,csize,csize,csize,csize,csize,csize,csize),data)
		matter = ud[0:csize]
		globid = ud[csize:csize*2]
		rx = ud[csize*2:csize*3]
		ry = ud[csize*3:csize*4]
		rz = ud[csize*4:csize*5]
		cvx = ud[csize*5:csize*6]
		cvy = ud[csize*6:csize*7]
		cvz = ud[csize*7:csize*8]
		for i,gid in enumerate(globid):
			x = rx[i]
			y = ry[i]
			z = rz[i]
			vx = cvx[i]
			vy = cvy[i]
			vz = cvz[i]
			t = matter[i]
			n = globid[i]

			if (not region or in_region(x, y, z, nregion)>0) and pfilter(x, y, z, vx, vy, vz, t, n) > 0:
				if t == 0:
					metal.add_particle(n, x, y, z, vx, vy, vz)
				else:
					gas.add_particle(n, x, y, z, vx, vy, vz)
			
	print ("Readed [%d] gas particles" % (len(gas.n)))
	print ("Readed [%d] metal particles" % (len(metal.n)))
	return (metal.finalize(), gas.finalize())


#@jit(nogil=True)
def readfile_metgas_boxes_nx( filename1, filename2, region):

	met1,gas1 = readfile_metgas_boxes(filename1, region = region)
	met2,gas2 = readfile_metgas_boxes(filename2, region = region)


	met_n  = numpy.append(met1.n,met2.n)
	gas_n  = numpy.append(gas1.n,gas2.n)

	met_n = numpy.unique(met_n)
	gas_n = numpy.unique(gas_n)
	print gas_n

	#@jit(int8(float64,float64,float64, float64,float64,float64,int8,int8),nopython=True,nogil=True)
	def my_part_filter(x,y,z,vx,vy,vz, t, n):
		if t == 0 and n >= met_n[0] and n <= met_n[-1]:
			if n in met_n:
				return 1
			else:
				return 0

		if t == 1 and n >= gas_n[0] and n <= gas_n[-1]:
			if n in gas_n: 
				return 1	
			else:
				return 0
		return 0


	print "Particle set size: ",len(met_n)+len(gas_n)

	met1,gas1 = readfile_metgas_boxes(filename1, pfilter=my_part_filter)
	met2,gas2 = readfile_metgas_boxes(filename2, pfilter=my_part_filter)

	print "resulting..."
	met1.nx = []
	met1.ny = []
	met1.nz = []
	gas1.nx = []
	gas1.ny = []
	gas1.nz = []
	for n in enumerate(met1.n):
		met1.nx.append(met2.x[numpy.where(met2.n == n)])
		met1.ny.append(met2.y[numpy.where(met2.n == n)])
		met1.nz.append(met2.z[numpy.where(met2.n == n)])
	for n in enumerate(gas1.n):
		met1.nx.append(gas2.x[numpy.where(gas2.n == n)])
		met1.ny.append(gas2.y[numpy.where(gas2.n == n)])
		met1.nz.append(gas2.z[numpy.where(gas2.n == n)])

	return (met1.finalize(), gas1.finalize())


	

#@jit(nogil=True)
def readfile_metgas_boxes_fast(filename):
	sys.stdout.write( ("Reading " + str(filename) + " fast as metal-gas boxes\n"))
	
	f = open(filename, "rb")
	data = f.read();
	sys.stdout.write( "Readed whole file, parsing\n")
	
	dpointer = 0
	box_count = struct.unpack("i",data[dpointer:4])[0]
	dpointer+=4
	sys.stdout.write( "Boxes count:" + str(box_count))

	metal = ParticleContainer("Nickel", 0.248, 97.474)
	gas = ParticleContainer("Nitrogenium",0.296, 46.517)

	for box in xrange(box_count):
		if box % 100:
			sys.stdout.write( "Parsing fast box " + str(box) + "  of"+ str(box_count) + "\r")
		
		box_params = data[dpointer : dpointer+4*5]
		dpointer += 4*5

		if not box_params:
			break

		bxyz2, blay, breal, msize, csize  =  struct.unpack("iiiii",box_params);

		if csize <= 0:
			continue 
		
		#print "Azaza"
		parts = data[dpointer:dpointer+(4+4+8+8+8+8+8+8)*csize]
		dpointer+=(4+4+8+8+8+8+8+8)*csize
		
		
		ud = struct.unpack("%di%di%dd%dd%dd%dd%dd%dd"%(csize,csize,csize,csize,csize,csize,csize,csize),parts)
		matter = ud[0:csize]
		globid = ud[csize:csize*2]
		rx = ud[csize*2:csize*3]
		ry = ud[csize*3:csize*4]
		rz = ud[csize*4:csize*5]
		cvx = ud[csize*5:csize*6]
		cvy = ud[csize*6:csize*7]
		cvz = ud[csize*7:csize*8]
		for i,gid in enumerate(globid):
			x = rx[i]
			y = ry[i]
			z = rz[i]
			vx = cvx[i]
			vy = cvy[i]
			vz = cvz[i]
			t = matter[i]
			n = globid[i]
			
			if t == 0:
				metal.add_particle(n, x, y, z, vx, vy, vz)
			else:
				gas.add_particle(n, x, y, z, vx, vy, vz)
			
	#print ("Readed [%d] gas particles" % (len(gas.n)))
	#print ("Readed [%d] metal particles" % (len(metal.n)))
	return (metal.finalize(), gas.finalize())

@jit(nogil=True)
def parts_in_region(cont, region):
	nth = []
	for i,g in enumerate(cont.n):
		if in_region(cont.x[i], cont.y[i], cont.z[i], region)>0:
			nth.append(g)
	return nth

#@jit(nogil = True)
def cut_patricles(cont, nth):
	indexes_to_delete = []
	print "Nth:",len(nth)
	
	for i,g in enumerate(cont.n):

		if g < nth[0] or g > nth[-1]:
			indexes_to_delete.append(i)
		elif numpy.any(nth == g):
			continue
		else:
			indexes_to_delete.append(i)

def cut_patricles_fast(cont, nth):
	print "Nth",len(nth)
	indeces = numpy.arange(cont.n.shape[0])[~numpy.in1d(cont.n,nth)]
#	print indeces

	cont.x = numpy.delete(cont.x, indeces)
	cont.y = numpy.delete(cont.y, indeces)
	cont.z = numpy.delete(cont.z, indeces)
	cont.vx = numpy.delete(cont.vx, indeces)
	cont.vy = numpy.delete(cont.vy, indeces)
	cont.vz = numpy.delete(cont.vz, indeces)
	cont.n = numpy.delete(cont.n, indeces)
	print "Becojme: ",len(cont.n)
	
	return cont


def readfile_track_fast( filename1, filename2, region):
	nregion = numpy.array(region,dtype=numpy.float64)
	print "---Reading files"

	met1,gas1 = readfile_metgas_boxes(filename1)
	met2,gas2 = readfile_metgas_boxes(filename2)
	
	met_n  = numpy.append(parts_in_region(met1, nregion), parts_in_region(met2, nregion))
	gas_n  = numpy.append(parts_in_region(gas1, nregion), parts_in_region(gas2, nregion))
	

	print "---Making diffs"
	met_n = numpy.unique(met_n)
	gas_n = numpy.unique(gas_n)
	
	#print "gn",gas1.n
	print "Whol parts g:", len(gas_n)
	print "Whol parts m:", len(met_n)
	
	print "---Applying diffs"
	met1 = cut_patricles_fast(met1, met_n);
	gas1 = cut_patricles_fast(gas1, gas_n);
	#return met1.finalize(),gas1.finalize()
	#return met1.finalize(), gas1.finalize()
	print "After cuts g: ", len(gas1.n)
	print "After cuts m: ", len(met1.n)
	
	print "---Making final"
	met1.nx = []
	met1.ny = []
	met1.nz = []
	met1.nt = []
	gas1.nx = []
	gas1.ny = []
	gas1.nz = []
	gas1.nt = []
	
	print len(met1.n)

	for n in met1.n:
		indx = numpy.where(met2.n == n)[0][0]
		met1.nx.append(met2.x[indx])
		met1.ny.append(met2.y[indx])
		met1.nz.append(met2.z[indx])
		met1.nt.append(met2.t[indx])
#	print "Nx", len(met1.nx)
	print len(gas1.n)
	for n in gas1.n:
#		print n
		indx= numpy.where(gas2.n == n)[0][0]
		gas1.nx.append(gas2.x[indx])
		gas1.ny.append(gas2.y[indx])
		gas1.nz.append(gas2.z[indx])
		gas1.nt.append(gas2.t[indx])
#	print "gNx", len(gas1.nx)

	#print gas1.x
	#print gas1.nx
	met1.nt = numpy.array(met1.nt)
	gas1.nt = numpy.array(gas1.nt)
	return (met1.finalize(), gas1.finalize())


def get_parts_in_region(file,region):
	nregion = numpy.array(region,dtype=numpy.float64)
	met,gas = readfile_metgas_boxes(file)
	
	met_n  = parts_in_region(met, nregion)
	gas_n  = parts_in_region(gas, nregion)

	return numpy.append(met_n,gas_n)
	


def readfile_track_parts_fast( filename1, filename2, parts):
	
	print "---Reading files"

	met1,gas1 = readfile_metgas_bin_fast(filename1)
	met2,gas2 = readfile_metgas_bin_fast(filename2)
	
	print "---Applying diffs"
	print "f1"
	met1 = cut_patricles_fast(met1, parts);
	gas1 = cut_patricles_fast(gas1, parts);
	print "f2"
	met2 = cut_patricles_fast(met2, parts);
	gas2 = cut_patricles_fast(gas2, parts);
	
	print "After cuts g: ", len(gas1.n)
	print "After cuts m: ", len(met1.n)
	
	print "---Making final"
	met1.nx = []
	met1.ny = []
	met1.nz = []
	gas1.nx = []
	gas1.ny = []
	gas1.nz = []
	
	print len(met1.n)

	for n in met1.n:
		indx = numpy.where(met2.n == n)[0][0]
		met1.nx.append(met2.x[indx])
		met1.ny.append(met2.y[indx])
		met1.nz.append(met2.z[indx])
#	print "Nx", len(met1.nx)
	print len(gas1.n)
	for n in gas1.n:
	#	print n
		indx= numpy.where(gas2.n == n)[0][0]
		gas1.nx.append(gas2.x[indx])
		gas1.ny.append(gas2.y[indx])
		gas1.nz.append(gas2.z[indx])
#	print "gNx", len(gas1.nx)

	#print gas1.x
	#print gas1.nx
		
	return (met1.finalize(), gas1.finalize())


def readfile_tex_vic( filename ):
	from utils import chunks
	import struct
	print ("Reading " + str(filename) + " as vic_txt")

	f = open(filename, "rb")
	
	gas = ParticleContainer("Nitrogenium",0.296, 46.517)

	p_count = 1000
	data = f.read().split();

	step = data[0]
	data = data[1:]

	x = [ struct.unpack("d",struct.pack("II",int(k[0]),int(k[1]))) for k in chunks(data[0:p_count*2],2)];
	y = [ struct.unpack("d",struct.pack("II",int(k[0]),int(k[1]))) for k in chunks(data[p_count*2:p_count*4],2)];
	z = [ struct.unpack("d",struct.pack("II",int(k[0]),int(k[1]))) for k in chunks(data[p_count*4:p_count*6],2)];
	vx = [ struct.unpack("d",struct.pack("II",int(k[0]),int(k[1]))) for k in chunks(data[p_count*6:p_count*8],2)];
	vy = [ struct.unpack("d",struct.pack("II",int(k[0]),int(k[1]))) for k in chunks(data[p_count*8:p_count*10],2)];
	vz = [ struct.unpack("d",struct.pack("II",int(k[0]),int(k[1]))) for k in chunks( data[p_count*10:p_count*12],2)];
	#y = [int(y) for y in data[p_count*2:p_count*4]]
	#z = [int(z) for z in data[p_count*4:p_count*6]]
	#vx = [int(vx) for vx in data[p_count*6:p_count*8]]
	#vy = [int(vy) for vy in data[p_count*8:p_count*10]]
	#vz = [int(vz) for vz in data[p_count*10:p_count*12]]

	

	for n,xx in enumerate(x):		
		#print xx
		gas.add_particle(n, (x[n]), (y[n]), (z[n]), (vx[n]), (vy[n]), (vz[n]))

	return gas.finalize()