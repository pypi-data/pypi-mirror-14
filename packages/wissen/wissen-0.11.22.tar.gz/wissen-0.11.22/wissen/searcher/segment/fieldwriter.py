import re
from . import typeinfo
import wissen

class FieldWriter:
	def __init__ (self, segment, analyzer = None):
		self.segment = segment
		self.analyzer = analyzer
		self.tcache = {}

	#---------------------------------------------------------------------------
	# add posting
	#---------------------------------------------------------------------------
	def indexText (self, type, docid, num, name, value, lang, option):
		if self.analyzer:
			if "removehtml"in option:
				temp = value
				value = self.analyzer.htmlStrip (temp)
			if "formalize" in option:
				value = self.analyzer.formalize (value)					
			if "transform" in option:
				value = self.analyzer.transform (value)
			term = value	
			value = self.analyzer.analyze (value, lang, type)
		
		if not value:
			self.segment.writeNorm (num, 0)
			return
		
		numTerm = 0
		if not value:
			self.segment.writeNorm (num, 0)
			return
		
		if type == wissen.TEXT:
			for term in value:				
				self.segment.writePosting (docid, num, term, len (value [term]), value [term])
				numTerm += len (value [term])

		elif type == wissen.TERM:
			for term, tf in value:
				self.segment.writePosting (docid, num, term, tf)
				numTerm += tf

		self.segment.writeNorm (num, numTerm)

	def indexField (self, type, docid, num, name, value, lang, option):
		if not value: return
		self.segment.writePosting (docid, num, value, 1)

	def indexList (self, ftype, docid, num, name, value, lang, option):
		if not value: return
		if type (value)	is type (""):			
			delim = ","
			if "delim" in option:
				ii = option.index ("delim")
				try:
					delim = option [ii + 1]
				except IndexError:
					pass
			value = value.split (delim)
		
		d = {}
		for each in [_f for _f in [x.strip () for x in value] if _f]:
			d [each] = None
		
		for each in d:
			self.indexField (ftype, docid, num, name, each, lang, option)

	def indexInt (self, type, docid, num, name, value, lang, option):
		try: val = int (value)
		except: val = 0
		self.segment.writeSortKey (num, val, typeinfo.typemap.getsize (type))

	def indexBit (self, type, docid, num, name, value, lang, option):
		try: val = int (value, 2)
		except: val = 0
		self.segment.writeSortKey (num, val, typeinfo.typemap.getsize (type))

	def indexStringSort (self, type, docid, num, name, value, option):
		self.segment.writeStringSortKey (num, value, typeinfo.typemap.getsize (type))

	def indexCoord (self, type, docid, num, name, value, lang, option):
		tsize = typeinfo.typemap.getsize (type)
		precision = 10 ** (tsize-2)
		try:
			val = [int ((round (float (x), tsize) + 180.0) * precision) for x in value.split ("/", 2)]
			assert (len (val) == 2)
			if [x for x in val if x > (360 * precision)]:
				raise ValueError
		except:
			val = [0, 0]
		self.segment.writeSortKey (num, val, tsize)

	def __call__ (self, type, docid, num, name, value, lang, option):
		method = getattr (self, "index" + typeinfo.typemap.getmethod (type))
		method (type, docid, num, name, value, lang, option)
