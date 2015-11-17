import reconstructed_data_reader
import backup_data_reader
import transport

def fast_read(address, elements = None):
	reader = backup_data_reader.BackupDataReader(elements)
	elements = reader.read(transport.ssh_backup_dir(address[0], address[1], passwd = "P)o9@>!1"))
	return elements


	