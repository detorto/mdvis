import select 
import paramiko
import getpass
import logging
logging.basicConfig()

class localfile:
	def __init__(self, filename):
		self.address = filename
		self.file = open(filename,"rb")

	def read(self, sz):
		return self.file.read(sz)

class local_backup_dir:
	def __init__(self, path, timestep = 0):
		self.address = path
		self.timestep = timestep

	def read(self, sz):
		raise BaseException("Can't read from directory, it is not a file!")
	def transport_for_file(self, f):
		return open(f,"rb")
	def list(self):
		import glob
		a = glob.glob(self.address+"/"+"*st0{num:09d}*.w2".format(num=self.timestep))
		return a


class sshfile:
	def __init__(self, address, passwd = None):
		import paramiko
		import getpass

		self.address = address
		
		login,address = address.split("@")
		address,filename = address.split(":")
		
		if not passwd:
			passwd = getpass.getpass()

		print "Connecting to ", address
		t = paramiko.Transport((address, 22))  
		t.connect(username=login, password=passwd)  
		t.window_size = 2147483647
		t.packetizer.REKEY_BYTES = pow(2, 40) # 1TB max, this is a security degradation
		t.packetizer.REKEY_PACKETS = pow(2, 40) # 1TB max, this is a security degradation
		
		sftp = paramiko.SFTPClient.from_transport(t)
		print "Opening file", filename
		self.remote_file = sftp.file(filename,"r",bufsize=1024*1024)
		self.st = 0

	def read(self,size):
		print 'Dataread ',size, self.st/1024, 746564356/1024
	
		self.st += size
		#print  self.remote_file.stat()
		return self.remote_file.read(size)

class ssh_backup_dir:
	
	def __init__(self, address, timestep = 0,passwd=None):
		
		self.timestep = timestep
		self.address = address
		self.passwd = passwd
		
		login,address = address.split("@")
		self.login = login

		address,filename = address.split(":")
		self.server = address
		
		if not passwd:
			passwd = getpass.getpass()
			self.passwd = passwd

		print "Connecting to ", address
		
		#list dir for nessesary files
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(address,username=login, password=passwd)
		stdin, stdout, stderr = client.exec_command("ls "+filename+"/"+"*st0{num:09d}*.w2".format(num=self.timestep))
		self.files = [f.strip() for f in  stdout.readlines()]	

	def read(self, sz):
		raise BaseException("Can't read from directory, it is not a file!")
	
	def transport_for_file(self, f):
		t = paramiko.Transport((self.server, 22))  
		t.connect(username=self.login, password=self.passwd)  
		t.window_size = 2147483647
		t.packetizer.REKEY_BYTES = pow(2, 40) # 1TB max, this is a security degradation
		t.packetizer.REKEY_PACKETS = pow(2, 40) # 1TB max, this is a security degradation
		sftp = paramiko.SFTPClient.from_transport(t)		
		tr = sftp.file(f,"r",bufsize=1024*1024)
		return tr
		

	def list(self):
		return self.files
		#tr = [self.sftp.file(f,"r",bufsize=1024*1024) for f in self.files]
		#for i,t in enumerate(tr):
		#	t.address = self.files[i]
		#return tr

#		print "Opening file", filename
#		self.remote_file = sftp.file(filename,"r",bufsize=1024*1024)
#		self.st = 0
#		print self.sftp.listdir(self.filename)
		#import glob
		#a = glob.glob(self.address+"/"+"*st0{num:09d}*.w2".format(num=self.timestep))
		#return [localfile(f) for f in a]