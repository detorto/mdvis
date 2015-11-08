class localfile:
	def __init__(self, filename):
		self.address = filename
		self.file = open(filename,"rb")

	def read(self, sz):
		return self.file.read(sz)


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
		sftp = paramiko.SFTPClient.from_transport(t)
		print "Opening file", filename
		self.remote_file = sftp.file(filename,"r",bufsize=1024*1024*10)
		self.st = 0

	def read(self,size):
		print 'Dataread ',size, self.st/1024, 746564356/1024
	
		self.st += size
		#print  self.remote_file.stat()
		return self.remote_file.read(size)

