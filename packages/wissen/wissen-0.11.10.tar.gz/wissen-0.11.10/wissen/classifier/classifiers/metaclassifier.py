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
			current_score = None
			for label, score in r:	
				if current_score is not None and score < current_score:
					break
				nres.append (label)
				current_score = score
		#print (nres)
		if not nres: return []
		score = 1 / len (nres)
		d = {}		
		for label in nres:
			try: d [label] += score
			except KeyError: d [label] = score

		k = list(d.items ())
		k.sort (key = lambda x: x [1], reverse = True)
		return k			
	
	def guess (self, mem, qs, lang = "un", cond = ""):
		result = []
		for name, classifier in list(self.clfs.items ()):
			try:
				subresult = classifier.guess (mem, qs, lang, cond)
				if not subresult:
					continue					
				
				#print (name, subresult)
				if type (subresult [0]) == type ([]):
					result.extend (subresult)
				else:	
					result.append (subresult)
			except:
				self.logger.trace ("engine")	
		
		return self.merge_and_choice (result)
		