import numpy
import sys

from mmdlab.readers.backup_data_reader import BackupDataReader
from mmdlab.readers import transport
from mmdlab.filters import RegionFilter

from mmdlab.utils import init_mlab_scene
from mmdlab.utils import showable
from mmdlab.utils import saveimg

from mmdlab.utils import offscreen

from mayavi import mlab

elements_description = \
{ "Nickel" : { "id" : 0, "atom_mass" : 97.474, "atom_d" : 0.248}, 
  "Nitrogen" : { "id" : 1, "atom_mass" : 46.517, "atom_d" : 0.296} }


def read(f):

	reader = BackupDataReader(elements_description)

	elements = reader.read(transport.ssh_backup_dir(f,490000))

	m = elements["Nickel"]
	g = elements["Nitrogen"]

	f = RegionFilter([0,10,0,10,0,30])
	return f(m),f(g)

#@saveimg("lol.png")
#@offscreen()
@showable
def draw():
	
	
	m,g = read(sys.argv[1])
	init_mlab_scene((1024,768))
	print "Drawing Nickel" 
	mlab.points3d(m.x, m.y, m.z, m.t, mode="point", scale_mode="none",scale_factor=m.d, colormap="black-white")
	print "Drawing Nitrogenium"
	mlab.points3d(g.x, g.y, g.z, g.t, mode="point", scale_mode="none",scale_factor=g.d, colormap="cool") 
	mlab.outline()


draw()
