from . import segment
from . import segmentreader
from ... import _wissen
import time

class SegmentMerger (segment.Segment):	
	def __init__ (self, si):	
		self.si = si
		newseg = self.si.getNewSegment ()		
		segment.Segment.__init__ (self, si.fs.new (newseg), newseg, 'w')
		self.mergeinfo = _wissen.MergeInfo ()
		self.smis = self.mergeinfo.get ()
		self.segments = []		
	
	def close (self):
		if self.mergeinfo:
			self.mergeinfo.close ()
			self.mergeinfo = None
					
		segment.Segment.close (self)
			
	def addSegment (self, seg):
		reader = segmentreader.SegmentBulkReader (self.si, seg)
		self.segments.append (reader)
		
	def merge (self):
		self.segments.sort (key = lambda x: int (x.seg))
		
		for segment in self.segments:
			self.mergeinfo.add (*segment.getMergeInfo ())
			
		self.tf.setsmis (self.smis)	
		self.fd.setsmis (self.smis)
		self.sm.setsmis (self.smis)
		
		self.mergeDocument ()
		self.mergeSortMap ()		
		self.mergeTermInfo ()
		self.flush ()
		
	def flush (self):
		for reader in self.segments:			
			seg = reader.seg
			reader.close ()
			self.si.removeSegment (seg)
						
		self.si.addSegment (self.seg, self.numDoc)
		self.close ()
		self.si.flush ()
		
	def mergeTermInfo (self):
		slots = [None] * len (self.segments)
		i = 0
		for segment in self.segments:
			slots [i] = segment.advanceTermInfo ()
			i += 1
		
		#slots = slots [:1]
		termnum = 0
		while 1:
			termnum += 1
			
			fslots = [_f for _f in slots if _f]
			if not fslots: break
			#slots = slots [:1]
			
			miti = min (fslots)			
			
			_term, _fdno = miti.term, miti.fdno
			
			i = 0
			last_docid = 0
			tdf = 0
			
			frqposition, prxposition = self.tf.tell ()			
			for ti in slots:
				if ti and miti == ti:
					tdf, skip, pskip, last_docid = self.tf.merge (i, ti.df, ti.frqPosition, ti.prxPosition, ti.prxLength, tdf, last_docid)
					try: 
						slots [i] = self.segments [i].advanceTermInfo ()					
					except IndexError: 
						slots [i] = None
						
				i += 1
			
			#if miti.term == "servic":
			#	print "writing2:", pskip, pskip - prxposition
			
			self.ti.add (_term, _fdno, tdf, frqposition, prxposition, skip - frqposition, pskip - prxposition) #skipdelta: skip - position
			self.tf.commit ()		
			
	def mergeDocument (self):
		for seg in range (len (self.segments)):
			for docid in range (self.segments [seg].numDoc):
				self.numDoc += self.fd.merge (seg, docid)
			
	def mergeSortMap (self):
		for fdno, _size in self.si.getSortMapFields ():
			for seg in range (len (self.segments)):
				pointer, size = self.segments [seg].getSortMapPointer (fdno)			
				self.sm.merge (seg, fdno, pointer, size)			
			
							