import struct
import numpy

class BackupDataParser:
	def __init__(self, transport):
		self.transport = transport
		data = self.transport.read(4)
		self.box_count = struct.unpack("i",data)[0]	
		print "Box count: ",  self.box_count

	def raw_particles(self, particles_count):	
		n = numpy.zeros(particles_count, dtype='i')
		t = numpy.zeros(particles_count, dtype='i')		
		x = numpy.zeros(particles_count, dtype='d')
		y = numpy.zeros(particles_count, dtype='d')
		z = numpy.zeros(particles_count, dtype='d')
		ax = numpy.zeros(particles_count, dtype='d')
		ay = numpy.zeros(particles_count, dtype='d')
		az = numpy.zeros(particles_count, dtype='d')
		vx = numpy.zeros(particles_count, dtype='d')
		vy = numpy.zeros(particles_count, dtype='d')
		vz = numpy.zeros(particles_count, dtype='d')
		fx = numpy.zeros(particles_count, dtype='d')
		fy = numpy.zeros(particles_count, dtype='d')
		fz = numpy.zeros(particles_count, dtype='d')
		
		particles_count = 0;
		
		for box in xrange(self.box_count):

			if box % 5000==0:
				print "Reading box", box, "of",self.box_count
		
			data = self.transport.read(4*5)
			
			if not data:
				break;
			
			bxyz2, blay, breal, msize, csize  =  struct.unpack("iiiii", data);
		#	print bxyz2, blay, breal, msize, csize
			if csize <= 0:
				continue 
		
			data = self.transport.read((4+4+8+8+8+8+8+8+8+8+8+8+8+8)*csize)
			
			ud = struct.unpack("%di%di%dd%dd%dd%dd%dd%dd%dd%dd%dd%dd%dd%dd"%(csize,csize,csize,csize,csize,csize,csize,csize,csize,csize,csize,csize,csize,csize),data)
			
			t[particles_count:particles_count+csize] = ud[0:csize]
			n[particles_count:particles_count+csize] = ud[csize:csize*2]

			x[particles_count:particles_count+csize] = ud[csize*2:csize*3]
			y[particles_count:particles_count+csize] = ud[csize*3:csize*4]
			z[particles_count:particles_count+csize] = ud[csize*4:csize*5]

			ax[particles_count:particles_count+csize] = ud[csize*5:csize*6]
			ay[particles_count:particles_count+csize] = ud[csize*6:csize*7]
			az[particles_count:particles_count+csize] = ud[csize*7:csize*8]

			vx[particles_count:particles_count+csize] = ud[csize*8:csize*9]
			vy[particles_count:particles_count+csize] = ud[csize*9:csize*10]
			vz[particles_count:particles_count+csize] = ud[csize*10:csize*11]

			fx[particles_count:particles_count+csize] = ud[csize*11:csize*12]
			fy[particles_count:particles_count+csize] = ud[csize*12:csize*13]
			fz[particles_count:particles_count+csize] = ud[csize*13:csize*14]
			
			particles_count += csize;

		return {"n":n[:particles_count], 
				"t":t[:particles_count],
				"x":x[:particles_count],
				"y":y[:particles_count],
				"z":z[:particles_count],
				"ax":ax[:particles_count],
				"ay":ay[:particles_count],
				"az":az[:particles_count],
				"vx":vx[:particles_count],
				"vy":vy[:particles_count],
				"vz":vz[:particles_count],
				"fx":fx[:particles_count],
				"fy":fy[:particles_count],
				"fz":fz[:particles_count],
				"count":particles_count}



class ReconstructedDataParser:
	
	def __init__(self, transport):
		self.transport = transport
		data = self.transport.read(4)
		self.box_count = struct.unpack("i",data)[0]	
		print "Box count: ",  self.box_count


	def raw_particles(self,particles_count):

		n = numpy.zeros(particles_count, dtype='i')
		t = numpy.zeros(particles_count, dtype='i')		
		x = numpy.zeros(particles_count, dtype='d')
		y = numpy.zeros(particles_count, dtype='d')
		z = numpy.zeros(particles_count, dtype='d')
		vx = numpy.zeros(particles_count, dtype='d')
		vy = numpy.zeros(particles_count, dtype='d')
		vz = numpy.zeros(particles_count, dtype='d')
			
		particles_count = 0;

		for box in xrange(self.box_count):

			if box % 100000==0:
				print "Reading box", box, "of", self.box_count

			data = self.transport.read(4*5)
			
			if not data:
				break;
			
			bxyz2, blay, breal, msize, csize  =  struct.unpack("iiiii", data);
		
			if csize <= 0:
				continue 

			data = self.transport.read((4+4+8+8+8+8+8+8)*csize)
			
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

		return {"n":n[:particles_count], 
				"t":t[:particles_count],
				"x":x[:particles_count],
				"y":y[:particles_count],
				"z":z[:particles_count],
				"vx":vx[:particles_count],
				"vy":vy[:particles_count],
				"vz":vz[:particles_count],
				"count":particles_count}
