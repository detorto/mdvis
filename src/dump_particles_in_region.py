import numpy
import sys

from mmdlab.readers.binary_box_reader import BinaryBoxReader
from mmdlab.filters import RegionFilter;

import pp

files_count = len(sys.argv[2:])
parts_in_reg = [];

ppservers = ()
job_server = pp.Server(ncpus = 5,secret="password")

def get_parts(filename):
	f = mmdlab.filters.RegionFilter([36,40,35,40,9,20])
	reader = mmdlab.readers.binary_box_reader.BinaryBoxReader()
	return f(reader.read(filename))


#get_parts(sys.argv[1])
print "Starting pp with", job_server.get_ncpus(), "workers"
# The following submits 8 jobs and then retrieves the results

jobs = [ job_server.submit(get_parts,(f,), (), ("mmdlab","mmdlab.readers.binary_box_reader","mmdlab.filters","mmdlab.filters.RegionFilter")) for f in sys.argv[2:]];
#print sys.argv[1:]
print jobs

for i,job in enumerate(jobs):		
	print "Getting result of job", i
	parts_in_reg = numpy.append(parts_in_reg, job())
	parts_in_reg = numpy.unique(parts_in_reg)
	print "Job",i,"done"

f = open(sys.argv[1],"w")
for n in parts_in_reg:
	f.write(str(n)+"\n")
f.close()



#mayavi.mlab.view(focalpoint=[5,5,15], distance=40)
#mayavi.mlab.show()
