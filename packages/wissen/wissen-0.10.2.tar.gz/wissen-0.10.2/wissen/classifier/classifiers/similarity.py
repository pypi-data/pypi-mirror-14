from . import tfidf
import math

class Classifier (tfidf.Classifier):
	def match (self, name):
		return name in ("similarity", "sim")
	
	def guess (self, mem, qs):
		surfix, terms = self.getFeatures (mem, qs)
		if not terms: return []
		searcher = self.reader.searcher
		
		K = 2
		A = 0.0
		d = []
		result = []
		comp = {}
		tfc = {}
		TF = 0
		
		for term, tf in terms:
			TF += math.pow (tf, 2.0)
		TF = math.sqrt (TF)

		for term, tf in terms:
			try: 
				tfv = tfc [tf]
			except KeyError:
				tfv = float (tf) / TF
				tfc [tf] = tfv
			df = self.reader.getDF (mem, term)
			comp [term] = tfv * self.reader.getIDF (df)
			A += math.pow (comp [term], 2.0)
		A = math.sqrt (A)
		
		res = searcher.do_query ("(%s) %s" % (" or ".join ([x [0] for x in terms]), surfix), 0, self.fetchcount, sort="tfidf", analyze = 0)
		if res ["total"] == 0:
			return []
		
		for row in res ["result"]:
			cla, stream = row [0][:2]
			B = C = 0.0
			TF = 0
			tfc = {}			
			stream = [x for x in stream if x [0] in self.featset]
				
			for term, tf in stream:
				TF += math.pow (tf, 2.0)
			if not TF:continue
			TF = math.sqrt (TF)
			
			for term, tf in stream:				
				try: 
					tfv = tfc [tf]
				except KeyError:
					tfv = float (tf) / TF
					tfc [tf] = tfv
				df = self.reader.getDF (mem, term)
				tfidf = tfv * self.reader.getIDF (df)
				B += math.pow (tfidf, 2.0)
				if term in comp:
					C += comp [term] * tfidf

			if B:
				result.append ((cla, C / (A * math.sqrt (B))))

		result.sort (key = lambda x: x [1], reverse = True)
		return result
