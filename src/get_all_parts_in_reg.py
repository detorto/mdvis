# mencoder "mf://mpg_288x288x24_lam15_t273_a0353140_0000_rv.dat_%d.png" -mf fps=20 -o anim.avi -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=500
import numpy
import sys

from mmdlab.datareader import get_parts_in_region
import pp
	
file_c = len(sys.argv[0])

all_nth = [];

ppservers = ()
job_server = pp.Server(ncpus = 3,secret="password")

def get_parts(filename):
	return mmdlab.datareader.get_parts_in_region(filename, region= [36,40,35,40,9,20])

print "Starting pp with", job_server.get_ncpus(), "workers"
# The following submits 8 jobs and then retrieves the results

jobs = [ job_server.submit(get_parts,(f,), (), ("mmdlab","mmdlab.datareader")) for f in sys.argv[1:]];
print sys.argv[1:]
print jobs

for i,job in enumerate(jobs):		
	print "Getting result of job", i
	all_nth = numpy.append(all_nth, job())
	all_nth = numpy.unique(all_nth)
	print "Job",i,"done"

f = open("nth_35-40.dat","w")
for n in all_nth:
	f.write(str(n)+"\n")
f.close()



#mayavi.mlab.view(focalpoint=[5,5,15], distance=40)
#mayavi.mlab.show()
