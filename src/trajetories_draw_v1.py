import pp
import numpy as np
import mmdlab
from mmdlab import datareader, dataprocessor, utils

serv = pp.Server(ncpus = 4)

indexes = np.array([])

def get_indexes(f, region):
    c = mmdlab.datareader.fast_read(f)
    return mmdlab.dataprocessor.region_filter(c, region).indexes


datafiles = [("puzyrkov@imm6.keldysh.ru:/home/polyakov/mmd/metgas/cur3/calc4/_mpg_288x288x24_lam15_t273_t273_a0353140/_res/", i) for i in [10000,20000,30000,40000,50000]] 
region = [0, 10, 0, 10, 0, 30]

pp_imports = ("mmdlab","mmdlab.datareader","mmdlab.dataprocessor","mmdlab.utils")
jobs = [serv.submit(get_indexes,(f,region), (), pp_imports) for f in datafiles];

for job in jobs:	
	indexes = np.unique(np.append(indexes, job()))
	print "Job done"	

def get_container(f1, f2, indexes):
    c1 = mmdlab.dataprocessor.index_filter(mmdlab.datareader.fast_read(f1), indexes)
    c2 = mmdlab.dataprocessor.index_filter(mmdlab.datareader.fast_read(f2), indexes)
    return mmdlab.dataprocessor.merge(c1,c2)
	jobs=[]

for f in utils.pairs(datafiles):
    jobs.append(serv.submit(get_container,(f[0],f[1],indexes), (), pp_imports))

for job in jobs:		
	print c.x[0] #will print x coordinates of particles in first dataset
	print c.x[1] #will print x coordinates of particles in second dataset