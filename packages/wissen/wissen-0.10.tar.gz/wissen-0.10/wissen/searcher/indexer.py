import sys
import os
import re
import glob
import zlib
import types
try: 
	import xmlrpc.client
	xmlrpcclient = xmlrpc.client.Server
except ImportError:
	import xmlrpclib
	xmlrpcclient = xmlrpclib.Server
	
from datetime import datetime
import time
import wissen
from .. import _wissen
from .segment import indexwriter
from .segment import segmentwriter
from .segment import segmentreader
from .segment import segmentmerger
from wissen.lib import flock

class ExitNow (Exception):
	pass


class Indexer:
	def __init__ (self, si):
		self.si = si
		self.setMergeFactor (self.si.getopt ("merge_factor", 10))
		self._force_merge = self.si.getopt ("force_merge", False)
		self._max_memory = self.si.getopt ("max_memory", 10000000)	# 10M	
		self._optimize = self.si.getopt ("optimize", True)	# 10M	
		self._indexed = 0
		self._initialized = False
		self.writer = None
	
	def setMergeFactor (self, factor):
		self._merge_factor = factor
		self._merge_factor_onindex = factor * 3
			
	def init (self, newsegment = 1):
		self.si.log ("initializing indexer...", "info")
		if not self.isIndexable ():
			raise ExitNow("`%s' not Indexable" % self.si.getAlias ())
		self.isDuplicating ()
		self.maybeMerge (self._merge_factor_onindex)
		self.si.lock.lock ("index", str (os.getpid ()))
		if newsegment:
			self.writer = indexwriter.IndexWriter (self.si, self.si.analyzer)
		self._initialized = True
	
	def maybeAbort (self):
		if self.si.lock.islocked ("abort"):
			self.si.lock.unlock ("abort")
			raise ExitNow("`%s' was aborted indexing" % self.si.getAlias ())
		
	def isDuplicating (self):
		while self.si.lock.isplocked ("duplicate"):
			self.si.log ("index is under duplicating, wait 10 sec.", "info")
			time.sleep (10)			
			self.maybeAbort ()

	def isIndexable (self, force = 0):
		if self.si.lock.islocked ("index"):
			if not force and flock.isCurrentProcess (int (self.si.lock.lockread ("index"))):
				self.si.log ("already under indexing, terminated", "info")				
				return 0							
		self.si.lock.unlock ("index")
		self.si.lock.unlock ("panic")
		self.si.lock.unlock ("merge")			
		return 1
		
	def merge (self):
		self.si.log ("merging all segments...", "info")
		all_segments = list(self.si.getSegmentInfo ().keys ())
		filesizeinfo = {}
		for seg in all_segments:
			if self.merge_and_check (filesizeinfo, seg):
				self.si.log ("file size reaches limit, merging failed", "fail")
				return		
		self.mergeSegment (all_segments)

	def mergeSegment (self, segs):
		t = self.si.getSegmentInfo ()
		t = list(t.items ())
		t.sort (key = lambda x: x[0], reverse = True)

		if len (segs) == 1: return
		self.si.log ("merging segments %s" % str (segs))

		self.si.lock.lock ("merge")
		merger = segmentmerger.SegmentMerger (self.si)

		try:
			for seg in segs:
				merger.addSegment (seg)

			merger.merge ()

		finally:
			merger.close ()
			self.si.lock.unlock ("merge")
	
	def merge_and_check (self, base, target_segment):
		for k, v in list(self.si.fs.getsegmentsize (target_segment).items ()):
			try: base [k] += v
			except KeyError: base [k] = v
		
		maxsize = max (base.values ())
		if maxsize > wissen.LIMIT_SEGMENTSIZE:
			self.si.log ("found LIMIT FILESIZE (%d Bytes), breaking" % maxsize)
			return True
		return False
		
	def maybeMerge (self, merge_factor, force = 0):
		SegmentInfo = self.si.getSegmentInfo ()
		if len (SegmentInfo) <= 2: return
					
		SegmentInfoItems = list(SegmentInfo.items ())
		SegmentInfoItems.sort (key = lambda x: x[0], reverse = True)
		
		seg0 = SegmentInfoItems [0][0]
		seg1 = SegmentInfoItems [1][0]
		if max (self.si.fs.getsegmentsize (seg0).values ()) > wissen.LIMIT_FILESIZE: return
		if max (self.si.fs.getsegmentsize (seg1).values ()) > wissen.LIMIT_FILESIZE: return
		
		if self.si.lock.islocked ("write"): # deleting documents
			self.si.log ("index writing by another process, wait for 60 sec.")
			for i in range (60): time.sleep (1)
		
		filesizeinfo = self.si.fs.getsegmentsize (seg0)
		self.merge_and_check (filesizeinfo, seg1)
		targetSegments = [seg0, seg1]
		segmentIndex = 2
		isOver = False
		while segmentIndex < len (SegmentInfoItems):
			seg, numDoc = SegmentInfoItems [segmentIndex]
			if max (self.si.fs.getsegmentsize (seg).values ()) > wissen.LIMIT_FILESIZE: 
				self.si.log ("found BIG FILESIZE (%d Bytes), breaking" % max (self.si.fs.getsegmentsize (seg).values ()))
				break
			targetSegments.append (seg)
			if self.merge_and_check (filesizeinfo, seg):
				isOver = True
				break			
			segmentIndex += 1
			
		if isOver:
			self.si.log ("start merging segments because reaching size limit...")
			return self.mergeSegment (targetSegments)			
			
		if not force and len (SegmentInfo) <= merge_factor:
			return
		
		filesizeinfo = self.si.fs.getsegmentsize (seg0)
		self.merge_and_check (filesizeinfo, seg1)
		targetSegments = [seg0, seg1]
		segmentIndex = 2
		mergeDocCount = SegmentInfoItems [0][1] + SegmentInfoItems [1][1]
		while segmentIndex < len (SegmentInfoItems):
			seg, numDoc = SegmentInfoItems [segmentIndex]
			if max (self.si.fs.getsegmentsize (seg).values ()) > wissen.LIMIT_FILESIZE: 
				self.si.log ("found BIG FILESIZE (%d Bytes), breaking" % max (self.si.fs.getsegmentsize (seg).values ()))
				break
			if self.merge_and_check (filesizeinfo, seg):
				targetSegments.append (seg)
				self.si.log ("start merging segments because reaching size limit while optimizing...")
				return self.mergeSegment (targetSegments)			
			if numDoc > mergeDocCount <= merge_factor: break
			targetSegments.append (seg)
			mergeDocCount += numDoc			
			segmentIndex += 1
			
		self.si.log ("start merging segments because optimizing...")
		self.mergeSegment (targetSegments)
			
	def optimize (self):
		if not self._optimize: 
			return
		
		if self._force_merge:
			self.si.log ("optimizing segments forcely...")
			self.merge ()

		else:
			self.si.log ("optimizing segments...")
			self.maybeMerge (self._merge_factor)			

	def commit (self, final = 0):
		self.si.log ("commit segment...")
		if self.writer:
			self.writer.flush (final)
		# replace new writer
		if not final:
			self.maybeMerge (self._merge_factor_onindex)

	def close (self, err = 0):
		self.si.log ("closing indexer...")
		self.commit (1)
		self.optimize ()
		
		if self.writer:
			self.writer.close ()
			
		self.si.lock.unlock ("index")
		self.si.log ("indexer closed")
		self.si.close ()
		self.si = None
	
	def add_document (self, document):
		if not self._initialized: 			
			self.init ()
		self.maybeAbort ()
		
		wdoc = self.writer.newWDocument ()
		for name, (val, ftype, lang, option) in list(document.fields.items ()):
			wdoc.addField (ftype, name, val, lang, option)
		
		if document.data:
			wdoc.setData (document.data)
		else:
			for each in document.stored:
				wdoc.addStored (*each)
		
		if document.summary:
			wdoc.addSummary (*document.summary)
		self.writer.addWDocument (wdoc)
		
		self._indexed += 1
		
		if self._indexed % 100 == 0:
			self.si.log ("indexed %d documents, %d terms" % (self._indexed, self.writer.segment.termTable.numterm))
		if self._indexed % 1000 == 0:
			self.si.log ("estimated %3.2f MB data allocated" % (self.writer.getMemUsage () / 1048576.0,))

			if self.writer.getMemUsage () >= self._max_memory:
				self.commit ()

	def delete_documents_by_query (self, qs):
		if not qs: return		
		s = xmlrpcclient.Server ("http://" + self.si.index_server)
		s.wissen.util.delete (self.si.getAlias (), qs)
		s.wissen.util.commit (self.si.getAlias ())

