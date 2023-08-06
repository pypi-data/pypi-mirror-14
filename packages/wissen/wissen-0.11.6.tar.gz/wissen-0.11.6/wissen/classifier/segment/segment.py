from ... import _wissen
from ...searcher.segment import segment
import os

class Segment (segment.Segment):
	def __init__ (self, home, seg = 0, mode = 'r'):
		self.home = home
		self.ident = "segments"
		self.seg = seg

		self.__opened = 0
		self.__cotermdb = 0
		self.log = None
		self.trace = None
		self.mode = mode		
	
	def get_base_path (self):
		return os.path.join (self.home, str (self.seg)  + ".")
		
	def open (self):
		bfn = self.get_base_path ()
		
		if self.mode in ("r", "m"):
			fopen_flag = os.O_RDONLY
		else:
			fopen_flag = os.O_WRONLY | os.O_CREAT
				
		if os.name == "nt":
			fopen_flag |= os.O_BINARY

		self.fs_tis = os.open (bfn + "fis", fopen_flag)
		self.fs_tii = os.open (bfn + "fii", fopen_flag)
		self.fs_tfq = os.open (bfn + "cfq", fopen_flag)
		
		bmode = self.mode.encode ("utf8")
		self.ti = _wissen.TermInfo (self.fs_tii, self.fs_tis, bmode)
		self.ti.initialize ()
		self.tf = _wissen.DBInt (self.fs_tfq, bmode)
		self.tf.initialize ()
		
		try:
			self.fs_cof = os.open (bfn + "cof", fopen_flag)
			self.fs_coi = os.open (bfn + "coi", fopen_flag)
		except OSError:
			pass			
		else:
			self.co = _wissen.DBInt (self.fs_cof, bmode)
			self.co.initialize ()
			self.ci = _wissen.DBInt (self.fs_coi, bmode)
			self.ci.initialize ()		
			self.__cotermdb = 1
		self.__opened = 1
		
	def close (self):
		if not self.__opened:
			raise segment.SegmentNotOpened

		if self.mode == "w":
			self.ti.commit ()
			self.tf.commit ()
		
		self.ti.close ()
		self.tf.close ()
		os.close (self.fs_tis)
		os.close (self.fs_tii)
		os.close (self.fs_tfq)
		
		if self.__cotermdb:
			self.co.close ()
			self.ci.close ()
			os.close (self.fs_cof)
			os.close (self.fs_coi)
		
		self.__opend = 0
