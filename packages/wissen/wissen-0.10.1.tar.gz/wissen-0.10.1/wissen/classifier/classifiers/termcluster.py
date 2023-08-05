from . import naivebayes
from . import tfidf
from . import featurevote
from . import metaclassifier
from wissen import _wissen

class Cluster:
	def __init__ (self, f1, f2="", mi=0.):		
		self.weight = {f1: mi}
		if f2:
			self.weight [f2] = mi
		
	def __cmp__ (x, y):
		return cmp (y.get_fitness (), x.get_fitness ())

	def get_weight (self, term):
		try:
			return self.weight [term]
		except KeyError:
			return 0.	

	def get_fitness (self):
		return sum (self.weight.values ()) / float (len (self.weight))

	def chain (self, f3, mis):
		t = []
		for f1 in self.weight:
			found = 0
			for index in range (len (mis)):
				if mis [index][0] in ((f1, f3), (f3,f1)):
					t.append ((f1, f3, mis [index] [1]))
					found = 1
					del mis [index]
					break		
			if not found:
				t.append (0.)

		summi = sum ([x[-1] for x in t])
		avgmi = summi / len (t)
		if avgmi < 1.0:
			return False
		
		self.weight [f3] = summi
		for f1, f3, mi in t:
			self.weight [f1] += mi
		
		return True

	def __repr__ (self):
		return "<Cluster (F %2.3f): %s>" % (self.get_fitness (), " ".join (list(self.weight.keys ())))


class Classifier (
	naivebayes.Classifier, 
	featurevote.Classifier, 
	tfidf.Classifier, 
	metaclassifier.Classifier
	):
	def match (self, name):
		return name in ("termcluster",)
	
	def createTermClusters (self, mem, terms):
		terms = [term for term in terms if term [0] in self.featset]
		if len (terms) <= 1:
			return [terms]
		
		featset = []
		for term, tf  in terms:
			findex = self.featset [term]
			df = self.reader.getDF (mem, term)
			featset.append ((term, findex, df))
		
		kd = 0
		mis = []
		for term1, x, m in featset:	
			kd += 1
			for term2, y, n in featset [kd:]:
				k = self.reader.getCoOccurrence (mem, x, y)
				if k is None:
					continue
				findex, co = k
				R = _wissen.IGmn (self.reader.si.getN (), m, n, co)				
				#print term1, term2, m,n, co, R
				mis.append (((term1, term2), R))
						
		if not mis:
			return [terms]
		
		misk.sort (key = lambda x: x [-1], reverse = True)
		(f1, f2), R = mis.pop (0)
		clusters = [Cluster (f1, f2, R)]
		
		for f3 in [feat [0] for feat in featset if feat [0] not in clusters [0].weight]:
			creates = {}
			for cluster in clusters[:]:
				if not cluster.chain (f3, mis) and f3 not in creates:
					clusters.append (Cluster (f3))
					creates [f3] = None
		
		terms = dict (terms)
		Nclusters = []
		clusters.sort ()
		for cluster in clusters:
			if len (cluster.weight) == 1: continue
			Nclusters.append ([(term, terms [term]) for term in cluster.weight])
		return Nclusters
		
	def guess (self, mem, qs):
		terms = self.getFeatures (mem, qs)
		clusters = self.createTermClusters (mem, terms)
				
		results = []
		for terms in clusters:
			result = featurevote.Classifier.guess (self, mem, terms)
			results.append (result)
			
		return metaclassifier.Classifier.merge_and_choice (self, results)
