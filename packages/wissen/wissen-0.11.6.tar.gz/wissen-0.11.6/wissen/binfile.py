from wissen import _wissen
import os

class BinFile:
	def __init__ (self, path, mode = "r"):
		self.path = path
		self.mode = mode		
		
		if mode == "r":
			flag = os.O_RDONLY
		else:
			flag = os.O_WRONLY | os.O_CREAT			
		if os.name == "nt":
			flag |= os.O_BINARY
			
		self.fdno = os.open (self.path, flag)
		self.bf = _wissen.BinFile (self.fdno, self.mode)
		
	def __getattr__ (self, attr):
		return getattr (self.bf, attr)
		
	def close (self):
		self.bf.close ()
		os.close (self.fdno)


def open (path, mode = "r"):
	return BinFile (path, mode)
	