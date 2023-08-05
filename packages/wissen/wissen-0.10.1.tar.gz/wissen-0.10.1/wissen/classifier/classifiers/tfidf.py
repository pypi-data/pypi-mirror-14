from . import naivebayes
import math

class Classifier (naivebayes.Classifier):
	fetchcount = 10		
	def setopt (self, **opts):		
		if opts:
			self.fetchcount = int (opts.get ("fetch", 10))
			
	def match (self, name):
		return name in ("tfidf",)
	
	def getFeatures (self, mem, qs):
		try: 
			surfix, qs = qs.split ("|", 1)
		except ValueError:
			surfix, qs = "", qs			
		return surfix, naivebayes.Classifier.getFeatures (self, mem, qs)	
			
	def guess (self, mem, qs):
		searcher = self.reader.searcher
		surfix, terms = self.getFeatures (mem, qs)
		if not terms: return []
					
		res = searcher.do_query ("(%s) %s" % (" or ".join ([x [0] for x in terms]), surfix), 0, self.fetchcount, sort="tfidf", analyze = 0)
		if res ["total"] == 0:
			return []
				
		result = []
		for row  in res ["result"]:
			cla, score = row [0][0], row [-1]
			result.append ((cla, score))		
		return result
