import types
from .. import memory
from ..util import util

class Fetcher:
	DEBUG = 0
	def __init__ (self, segments, bucket, summarize, highlights, encoding = None):
		self.segments = segments
		self.bucket = bucket
		self.encoding = encoding
		
		if type (highlights) is bytes:
			self.highlights = highlights.split ("|")
		elif type (highlights) is dict:
			self.highlights = list(highlights.keys ())
		else:
			self.highlights = highlights

		self.summarize = summarize
		self.fetched_index = 0
		self.fetchmax = len (self.bucket)

	def close (self):
		pass

	def __fetch (self, seg, docid, extra, score):
		mem = memory.get (self.segments [seg]) #get mutex
		field, summary = self.segments [seg].getDocument (mem, docid, self.summarize, self.highlights)
		field = util.deserialize (field)
		
		row = [field]
		if self.summarize:
			if self.encoding:
				summary = summary.encode (self.encoding)
			row.append (summary)
		else:
			row.append ("")
		row.append (seg)
		row.append (docid)
		row.append (extra)
		row.append (score)
		return row

	def fetchmany (self, count):
		result = []
		for hit in self.bucket [self.fetched_index: self.fetched_index + count]:
			field = self.__fetch (*hit)
			result.append (field)

		self.fetched_index += count
		return result

	def fetchone (self):
		if self.fetched_index >= self.self.fetchmax:
			return None

		field = self.__fetch (self.bucket [self.fetched_index] *hit)
		self.fetched_index += 1
		return field

	def fetchall (self):
		return self.fetchmany (self.fetchmax)
