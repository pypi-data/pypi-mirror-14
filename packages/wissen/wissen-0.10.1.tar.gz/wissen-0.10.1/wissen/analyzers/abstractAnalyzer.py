import wissen
from wissen import _wissen
import threading

class Analyzer:
	def __init__ (self, max_term = 8, numthread = 1):
		self.max_term = max_term
		self.numthread = numthread
		self.ats = []
		self.createTSAnalyzers (numthread)
		self.closed = False
		
	def __len__ (self):
		return len (self.ats)
		
	def get_tid (self):
		try: return threading.currentThread ().getId ()
		except AttributeError: return -1
	
	def createTSAnalyzers (self, num):
		pass
	
	def close (self):
		if self.closed: return
		for each in self.ats:
			each.close ()
		self.closed = True
		self.ats = []

	def generalize (self, t):
		return t.replace ("\x00", "")
	
	def transform (self, document):
		return document

	def analyze (self, document, lang, fdtype):		
		if fdtype == wissen.TEXT:
			return self.index (document, lang)
		elif fdtype == wissen.TERM:
			return self.term (document, lang)
		else:
			return self.query (document, lang)

	def index	(self, document, lang = "en"):
		raise NotImplementedError

	def term (self, document, lang = "en"):
		raise NotImplementedError

	def query (self, document, lang = "en"):
		raise NotImplementedError
