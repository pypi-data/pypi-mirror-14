import math
from wissen import _wissen

class Classifier:
	def __init__ (self, reader, analyzer, featset, use_top_features, logger = None):
		self.reader = reader
		self.analyzer = analyzer
		self.featset = featset
		self.logger = logger
		self.numfeat = len (self.featset)
		self.use_top_features = use_top_features
		
	def setopt (self, **opts):
		pass
			
	def match (self, name):
		return name in ("nb", "bayes", "naivebayes")
	
	def close (self):
		pass
	
	def getFeatures (self, mem, qs):
		terms = self.analyzer.term (qs)
		if not terms: return []
		return self.reader.getFeatures (
			mem, 
			[term for term in terms if term [0] in self.featset], 
			self.numfeat, 
			self.use_top_features
			)
			
	def guess (self, mem, qs):
		terms = self.getFeatures (mem, qs)
		if not terms: return []
		
		classifier = _wissen.Classifier (mem, self.reader.corpus, self.numfeat, self.reader.getN ())
		for term, tf  in terms:
			if self.reader.readTermInfo (mem, term):
				classifier.load ()
				classifier.bayes (tf)

		result = classifier.get (0, self.reader.numpools)
		classifier.close ()
		return self.reader.translate (result)
	
	