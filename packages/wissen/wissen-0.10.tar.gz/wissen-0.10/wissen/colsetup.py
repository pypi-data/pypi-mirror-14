import wissen
from wissen import memory
import os
import shutil
import time
import pickle as pickle
from . import filesystem
from wissen.lib import logger as logs, flock, plock as _plock
import socket
from functools import reduce
if os.name == "nt":
	import win32process

class SwapError (Exception):
	pass

class Options:
	pass
	
class Segments:
	def __init__ (self, alias = ""):
		self.version = wissen.VERSION
		self.alias = alias
		self.N = 0
		self.segmentInfo = {}


class CollectionSetup:
	exts = []
	segment_class = Segments
	
	def __init__ (self, indexdir, mode = 'r', analyzer = None, logger = None, plock = None):
		self.indexdir = indexdir
		self.mode = mode
		self.analyzer = analyzer
		self.logger = logger
		self.fs = filesystem.FileSystem (self.indexdir)
		self.master = self.fs.getmaster ()		
		self.lock = flock.Lock (self.master)
		
		self.plock = plock # process lock at posix
		if self.plock is None and os.name == "posix":
			self.plock = _plock.Lock (os.path.join (self.master, ".plock"))
		
		self.rebuild = False
		if mode == "c":
			self.rebuild = True
			self.mode = "w"
		
		self.initial_newseg = 0
		self.options = Options ()

		if os.path.isfile (os.path.join (self.master, "segments")):
			self.read ()
			if self.rebuild:
				self.createSegments ()
		else:
			self.createSegments ()
		
		self._logger_created = False
		self._analyzer_created = False
		self._wissen_init = False		
		
		if not self.logger:
			self.logger = logs.screen_logger ()
			self.log ("logger is not provided, screen logger created", "warn")
			self._logger_created = True
		
		if self.mode == "r" and memory.memory is None: 
			self.log ("wissen not inited, forcely init for single thread", "warn")
			wissen.configure (1, self.logger)
			self._wissen_init = True
		
		if self.analyzer is None:
			self.analyzer = wissen.standard_analyzer (self.mode == wissen.READ and 32 or 3000)			
			if self.mode == wissen.READ:
				self.analyzer.setopt (ngram_no_space = 0)			
			self._analyzer_created = True
		
		if self.mode == wissen.READ: # for multi-thread
			self.analyzer = wissen.qualify_analyzer (self.analyzer)
		
	def __del__ (self):
		self.close ()
			
	def close (self):
		self.lock.unlock ("using-%s" % wissen.PID)
			
		if self._wissen_init:
			self.log ("shutdown wissen...", "info")
			wissen.shutdown ()
			self._wissen_init = False
						
		if self._analyzer_created:
			self.log ("close analyzer...", "info")
			self.analyzer.close ()	
			self._analyzer_created = False
			
		if self._logger_created:			
			self.log ("close logger...", "info")
			self.logger.close ()
			self._logger_created = False		
	
	def gtVersion (self):
		return self.segments.version
	
	def getMajorVersion (self):
		return int (self.segments.version.split (".") [0])
		
	def notify (self):
		ll = list(self.segments.segmentInfo.keys ())
		ll.sort ()
		self.log ("segments updated... %s" % ll)	
					
	def write (self, fn = "segments"):
		self.segments.N = reduce (lambda x, y: x + y, list(self.segments.segmentInfo.values ()))
		self.segments.alias = self.alias
		t = open (os.path.join (self.master, fn), "wb")
		pickle.dump (self.segments, t)
		t.close ()
		self.log ("total indexed docuemts are %d" % self.segments.N)
			
	def read (self, fn = "segments"):	
		t = open (os.path.join (self.master, fn), "rb")
		self.segments = pickle.load (t)
		t.close ()
		self.alias = self.segments.alias
		
		if self.mode == "r":
			self.setReadingSegments ()
		self.initial_newseg = max (self.segments.segmentInfo.keys ()) + 1			
		
	def flush (self, new = 1):
		if new:			
			segment = self.write ("segments.new")
		else:
			segment = self.write ()

		if new:
			self.log ("replace segments.new...")
			try:
				self.replaceFile ("segments")
			except:
				self.trace ()				
		
		self.notify ()		
		if self.mode == "w":
			self.removeDeletables ()

	def riaseSwapError (self, msg):
		raise SwapError("%s %s" % (self.alias, msg))

	def replaceFile (self, name):
		backup = os.path.join (self.master, name + ".bak")
		newone = os.path.join (self.master, name + ".new")
		replacement = os.path.join (self.master, name)

		try:
			try:
				os.remove (backup)
			except OSError as why:
				if why.errno != 2:
					self.riaseSwapError ("backup file cannot deleted")

			try:
				os.rename (replacement, backup)
			except OSError as why:
				if why.errno != 2:
					self.riaseSwapError ("backup failed")

			try:
				os.rename (newone, replacement)
			except:
				self.trace ()
				os.rename (backup, replacement)
				self.riaseSwapError ("replace failed. rollbacked")

			else:
				try: os.remove (backup)
				except: pass

		except:
			self.trace ()
			raise

		else:
			self.read ()
	
	def removeDeletables (self):
		all = self.fs.segments ()
		used = self.getReadingSegmentsAllProcesses () + self.getSegmentList ()
		for seg in all:
			if seg not in used:
				self.removeSegmentFile (seg)

	def removeSegment (self, seg):
		try:
			del self.segments.segmentInfo [int (seg)]
		except KeyError:
			pass
	
	def removeSegmentFile (self, seg):
		try:
			self.fs.remove (seg)
		except:
			self.log ("segment %s remove failed" % seg, "fail")
			return 0

		self.log ("segment %s removed" % seg)		
		return 1

	def getModfiedTime (self):
		try:
			return os.stat (os.path.join (self.master, "segments")).st_mtime
		except (IOError, OSError):
			return -1

	def createSegments (self):		
		alias = os.path.split (self.master) [-1]		
		self.segments = self.segment_class (alias)
		self.alias = self.segments.alias

	def log (self, msg, type = "info"):
		self.logger (msg, type, self.alias)

	def trace (self):
		return self.logger.trace (self.alias)

	def getSegmentList (self):
		return list(self.segments.segmentInfo.keys ())

	def getSegmentInfo (self):
		return self.segments.segmentInfo

	def getSegmentNumDoc (self, seg):
		try:
			return self.segments.segmentInfo [int (seg)]
		except KeyError:
			return 0

	def getNewSegment (self):
		if not self.segments.segmentInfo:
			return str (self.initial_newseg)
		return str (max (self.segments.segmentInfo.keys ()) + 1)

	def getSegmentList (self):
		return list(self.segments.segmentInfo.keys ())

	def getSegmentInfo (self):
		return self.segments.segmentInfo

	def addSegment (self, seg, numDoc = 0):
		self.segments.segmentInfo [int (seg)] = numDoc

	def setReadingSegments (self):
		segs = self.getSegmentList ()
		if not segs: return
		segs = [str (x) for x in segs]
		self.lock.lock ("using-%s" % wissen.PID, ",".join (segs))		
	
	def getReadingSegments (self):
		segs = self.lock.lockread ("using-%s" % wissen.PID)
		if not segs: return []
		return [int (x) for x in segs.split (",")]
	
	def getReadingSegmentsAllProcesses (self):
		locks, errmsg = self.lock.locks ("using")
		d = {}
		for lname, ltime in locks:
			pid = int (lname.split ("-")[-1])
			isWissenServer = flock.isCurrentProcess (pid, "python")

			if not isWissenServer:
				self.lock.unlock (lname)
				continue
					
			segs = self.lock.lockread (lname)
			if not segs: continue
			for seg in segs.split (","):
				d [int(seg)] = None
				
		return list(d.keys ())
		
	def isWissenServer (self, pid):
		proc = "/proc/%d/cmdline" % pid
		if os.path.isfile (proc):
			f = open (proc)
			exefilename = f.read ()
			f.close ()
			if exefilename.find ("python") != -1:
				return True
								
	def getN (self):
		return self.segments.N
		
	def getAlias (self):
		return self.alias
				
	def move (self, source, target, seg):
		for ext in self.exts:
			try:
				shutil.copyfile (os.path.join (source, str(seg) + "." + ext), os.path.join (target, str(seg) + "." + ext))
				os.remove (os.path.join (source, str(seg) + "." + ext))
			except IOError as why:
				if why [0] != 2:
					raise

	def getopt (self, name = None, default = None, **karg):
		if name:
			try: return getattr (self.options, name)
			except AttributeError: return default
		
		for k, v in list(karg.items ()):
			try: return getattr (self.options, k)
			except AttributeError: return v
						
	def setopt (self, name = "", value = "", **karg):	
		if name:
			setattr (self.options, name, value)
		for k, v in list(karg.items ()):
			setattr (self.options, k, v)
			
