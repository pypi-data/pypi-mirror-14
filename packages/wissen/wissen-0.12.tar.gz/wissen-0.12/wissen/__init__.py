# 2014. 12. 9 by Hans Roh hansroh@gmail.com

VERSION = "0.12"
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

ALL = "default"
NAIVEBAYES = "naivebayes"
FEATUREVOTE = "featurevote"
TFIDF = "tfidf"
SIMILARITY = "similarity"
ROCCHIO = "rocchino"
ROCCHINO = "rocchino"
MULTIPATH = "multipath"
META = "metaclassifier"

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

R = "r"

SUM = "sum"
MAX = "max"
AVG = "avg"
MIN = "min"

WRITE = "w"
APPEND = "w"
MODIFY = "w"
READ = "r"
CREATE = "c"

osbit, __x = platform.architecture()
if osbit == "64bit":
	LIMIT_SEGMENTSIZE = 10000000000	# 2**39, 10GB but max 500GB is possible
else:
	LIMIT_SEGMENTSIZE = 1900000000 # 2**31, 2GB
LIMIT_FILESIZE = int (LIMIT_SEGMENTSIZE * 0.7)

logger = None
	
class Task:
	def __init__ (self, logger):
		self.logger = logger
		self._d_ = {}
		
	def cleanup (self):
		for tname, reactor in self._d_.items ():
			self.logger ("... wissen closing %s" % tname, "info")
			reactor.close ()		
			
	def __contains__ (self, tname):
		return (tname in self._d_)
	
	def __getattr__ (self, tname):
		return self._d_ [tname]
	
	def __delattr__ (self, tname):
		self.rempove (tname)

	def __dir__ (self):
		return list (self._d_.keys ())
	
	def __len__ (self):
		return len (self._d_)
		
	def assign (self, tname, obj):
		obj.si.set_ident (tname)
		self._d_ [tname] = obj
	
	def resign (self, tname):
		del self._d_ [tname]
		
	def get (self, tname):
		return self._d_ [tname]
	
	def status (self):
		d = {}
		for tname, reactor in self._d_.items ():
			d [tname] = reactor.status ()
		return d
		

class NoTask:
	def __getattr__ (self, name):
		raise AssertionError ("wissen not configured, configure first")

task = NoTask ()

def configure (numthread, logger_t, io_buf_size = 4096, mem_limit = 128, max_segment_size = 0):
	global logger, task
	
	if isinstance (task, Task):
		return
		
	logger = logger_t
	if max_segment_size:
		set_max_segment_size (max_segment_size)
		
	if not memory.isInitialized ():
		memory.initialize (numthread, io_buf_size, mem_limit, "segment", logger_t)
		analyzers.buildFactory (numthread, logger_t)
	
	task = Task (logger)
	return task
	
def shutdown ():
	global task
	
	if isinstance (task, Task):
		task.cleanup ()
		
	if memory.isInitialized ():
		analyzers.close ()
		memory.destroy ()

# For Skitai
cleanup = shutdown

def set_max_segment_size (mbytes):
	global LIMIT_SEGMENTSIZE, LIMIT_FILESIZE
	LIMIT_SEGMENTSIZE = int (mbytes * 1000000)
	LIMIT_FILESIZE = int (LIMIT_SEGMENTSIZE * 0.7)

def qualify_analyzer (analyzer):
	if memory.isInitialized ():
		return analyzers.checkIn (analyzer) 
	return analyzer	


#=========================================
# query and guess by task alias
#=========================================

#-----------------------------------------
# common jobs
#-----------------------------------------

def assign (tname, obj):
	global task
	task.assign (tname, obj)
	
def resign (tname):
	global task
	task.resign (tname, obj)
		
def close (tname, *args, **karg):
	global task	
	reactor = task.get (tname)
	if not reactor.closed:
		reactor.close (*args, **karg)
	task.remove (tname)

def get (tname):
	global task	
	return task.get (tname)

def status (tname = "", *args, **karg):
	global task
	if tname == "":
		return task.status ()
	return task.get (tname).status (*args, **karg)

def refresh (tname, *args, **karg):
	global task
	return task.get (tname).refresh (*args, **karg)	

#-----------------------------------------
# searcher only jobs	
#-----------------------------------------
def query (tname, *args, **karg):
	global task
	return task.get (tname).query (*args, **karg)

def delete (tname, *args, **karg):
	global task
	return task.get (tname).delete (*args, **karg)		

def remove (tname, *args, **karg):
	global task
	return task.get (tname).remove (*args, **karg)
	
def fetch (tname, *args, **karg):
	global task
	return task.get (tname).fetch (*args, **karg)	

#-----------------------------------------
# classifier only jobs	
#-----------------------------------------
def guess (tname, *args, **karg):
	global task
	return task.get (tname).guess (*args, **karg)	

	
	