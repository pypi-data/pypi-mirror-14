# 2014. 12. 9 by Hans Roh hansroh@gmail.com

VERSION = "0.10"
version_info = tuple (map (lambda x: not x.isdigit () and x or int (x),  VERSION.split (".")))

from .analyzers import standardAnalyzer
from .searcher import collection
from .classifier import model
from . import memory
from . import analyzers
import platform
import os
from .searcher import indexer, document
from .classifier import trainer, labeld_document

PID = os.getpid ()

standard_analyzer = standardAnalyzer.Analyzer

collection = collection.Collection
model = model.Model

document = document.Document
labeled_document = labeld_document.LabeledDocument

TEXT = "Text"
TERM = "Term"
STRING = "String"
LIST = "List"
COORD = "Coord4" 
COORD4 = "Coord4" # 4 decimals, 10 M precision
COORD6 = "Coord6" # 6 decimals, 10 CM precision
COORD8 = "Coord8" # 8 decimals, 1 MM precision
BIT8  = "Bit8"
BIT16 = "Bit16"
BIT24 = "Bit24"
BIT32 = "Bit32"
BIT40 = "Bit40"
BIT48 = "Bit48"
BIT56 = "Bit56"
BIT64 = "Bit64"
INT8  = "Int8"
INT16 = "Int16"
INT24 = "Int24"
INT32 = "Int32"
INT40 = "Int40"
INT48 = "Int48"
INT56 = "Int56"
INT64 = "Int64"

NAIVEBAYES = "naivebayes"
FEATUREVOTE = "featurevote"
TFIDF = "tfidf"
SIMILARITY = "similarity"
#TERMCLUSTER = "termcluster"
META = "meta"
ALL = None

CHI2 = "chi"
GSS = "gss"
DF = "df"
NGL = "ngl"
MI = "mi"
TFIDF = "tfidf"
IG = "ig"
OR = "or"
OR4P = "or4p"
RS = "rs"
LOR = "lor"
COS = "cos"
PPHI = "pphi"
YULE = "yule"
RMI = "rmi"

SUM = "sum"
MAX = "max"
AVG = "avg"

WRITE = "w"
APPEND = "w"
READ = "r"
CREATE = "c"

osbit, __x = platform.architecture()
if osbit == "64bit":
	LIMIT_SEGMENTSIZE = 10000000000	# 2**39, 10GB but max 500GB is possible
else:
	LIMIT_SEGMENTSIZE = 1900000000 # 2**31, 2GB
LIMIT_FILESIZE = int (LIMIT_SEGMENTSIZE * 0.7)

def configure (numthread, logger, io_buf_size = 8192, mem_limit = 256, max_segment_size = 0):
	if max_segment_size:
		set_max_segment_size (max_segment_size)
		
	if not memory.isInitialized ():
		memory.initialize (numthread, io_buf_size, mem_limit, "segment", logger)
		analyzers.buildFactory (numthread, logger)

def shutdown ():
	if memory.isInitialized ():
		analyzers.close ()
		memory.destroy ()

def set_max_segment_size (mbytes):
	global LIMIT_SEGMENTSIZE, LIMIT_FILESIZE
	LIMIT_SEGMENTSIZE = int (mbytes * 1000000)
	LIMIT_FILESIZE = int (LIMIT_SEGMENTSIZE * 0.7)

def qualify_analyzer (analyzer):
	if memory.isInitialized ():
		return analyzers.checkIn (analyzer) 
	return analyzer	


class WissenCloud:
	def __init__ (self, numthread, logger, io_buf_size = 8192, mem_limit = 256):
		self.numthread = numthread		
		self.logger = logger
		self.logger ("[info] ... `wissen cloud` is initializing with %d threads, %dKb IO buffer and %dMb mem option" % (numthread, io_buf_size, mem_limit))
		self.d = {}
		init (numthread, logger, io_buf_size, mem_limit)
		
	def cleanup (self):
		self.logger ("[info] ... `wissen cloud` will be entering shutdown process...")
		for idn, searcher in list(self.d.items ()):
			searcher.close ()		
		shutdown ()
		self.logger ("[info] ... `wissen cloud` shutdown complete")
	
	def get (self, idn):
		return self.d [idn] 
	
	def add (self, idn, searcher):
		self.d [idn] = searcher		
	
	def remove (self, idn):
		searcher = self.d [idn]
		searcher.close ()
		del self.d [idn]
	
	def has_key (self, idn):
		return idn in self.d
			
	def __getitem__ (self, idn):
		return self.d [idn]
	
	def __setitem__ (self, idn, searcher):
		self.add (idn, searcher)
		
	def __delitem__ (self, idn):
		self.remove (idn)
			
	
		
	