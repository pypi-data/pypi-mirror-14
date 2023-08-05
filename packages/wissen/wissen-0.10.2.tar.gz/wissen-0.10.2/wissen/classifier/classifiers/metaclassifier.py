import math
import wissen
from wissen import _wissen
from . import naivebayes

class Classifier (naivebayes.Classifier):
	def __init__ (self, clfs, logger = None):
		self.clfs = clfs
		self.logger = logger
			
	def match (self, name):
		return name == "meta"
	
	def merge_and_choice (self, res):
		nres = []
		for r in res:
			if not r: continue
			nres.append ([x[0] for x in r [:2]])
		res = nres		
		if not res: return []
		d = {}
		for each in res:
			try: d [each [0]] += 1
			except KeyError: d [each [0]] = 1

		if len (d) < len (res):
			k = list(d.items ())
			k.sort (key = lambda x: x [1], reverse = True)
			return [(x[0], 1.0) for x in k]

		for each in res:
			if len (each) == 1: continue
			try: d [each [1]] += 1
			except KeyError: pass

		k = list(d.items ())
		k.sort (key = lambda x: x [1], reverse = True)

		maxt = k [0][1]
		r = []
		for c, f in k:
			if f == maxt:
				r.append (c)
			else:
				break
				
		return [(each, 1.0) for each in r]
	
	def guess (self, mem, qs):
		result = []
		for name, classifier in list(self.clfs.items ()):
			try:
				subresult = classifier.guess (mem, qs)
				if not subresult:
					continue
				elif type (subresult [0]) == type ([]):
					result.extend (subresult)
				else:	
					result.append (subresult)
			except:
				self.logger.trace ("engine")	
		
		return self.merge_and_choice (result)
		