from .segment import segment
from wissen.searcher import searcher, cache
import time
import threading
import math
from .classifiers import metaclassifier
from .segment import composedsegmentreader
import sys
import re
import wissen
import copy
from wissen.lib import unistr

class TermInfo:
	def __init__ (self):
		pass
	
	def __repr__ (self):
		r = []
		for name, attr in list(self.__dict__.items ()):
			r.append ("%s:%s" % (name, attr))
		return "<%s>" % " ".join (r)
		
	
class Classifier (searcher.Searcher):
	def __init__ (self, si, do_init = True):
		self.si = si
		
		self.reader = composedsegmentreader.ComposedSegmentReader (self.si)			
		self.clfs = {}
		
		self.top_features = self.numQueryCache = self.si.getopt (use_features_top = 0) # use all features
		
		self.numquery = 0
		self.references = 0
		self.shutdown_level = 0
		self.maintern_time = -1
		self.closed = 1
		self.clean = 0
		self.cond = threading.Condition ()
		self.mutex = threading.Lock ()
		self.mod_time = self.si.getModfiedTime ()	
		self.has_deletable = False
		self.numQueryCache = 200
		self.classifer_opts = []
		self.cache = cache.Cache (self.numQueryCache)	
		
		self._initiallized = False		
		
		if do_init: 
			self.init ()
	
	def maintern (self):
		if time.time () - self.maintern_time > self.MAINTERN_INTERVAL and self.ismainternable ():
			self.maintern_time = time.time ()
			if self.need_refresh ():				
				self.do_refresh ()
				
	def addClassifier (self, classifier):
		self.reader.si.log ("text-classifier [%s] initializing..." % classifier)
		featureset = self.getFeatureSet (classifier == "tfidf" and "similarity" or classifier) or self.default_featureset
		if not featureset:
			self.reader.si.log ("text-classifier [%s] has no features" % classifier, "fail")
			return
			
		modulename = "wissen.classifier.classifiers.%s" % classifier
		__import__ (modulename)
		clf = sys.modules [modulename].Classifier (self.reader, self.si.analyzer, featureset, self.top_features, self.si.logger)
		self.clfs [classifier] = clf
	
	def getFeatureSet (self, classifier):
		return self.reader.si.segments.features.get (classifier, None)
	
	def setopt (self, cl, **option):
		self.classifer_opts.append ((cl, option))
		if type (cl) is str:
			cl = [cl]
		for each in cl:
			self.__setopt (each, **option)
	
	def getopt (self, cl, option):
		return self.get_classifier (cl).getopt (name)
			
	def __setopt (self, cl, **option):
		self.get_classifier (cl).setopt (**option)
		
	def get_classifier (self, name):
		return self.clfs [name]
		
	def do_close (self):
		if self.closed: return 1
		if self.reader:			
			self.reader.close ()			
			self.reader = None
		self.si.close ()
		self.si = None
		self.closed = 1

	def do_refresh (self, *arg, **karg):
		self.clean = 1
		if self.si.getModfiedTime () == -1:
			self.clean = 0
			return 
						
		try:
			self.reader.load ()
		except:
			# if failed, loading next time
			self.si.trace ()
			self.clean = 0
			return 0
		
		self.default_featureset = self.getFeatureSet ("default")
		
		self.clfs = {}
		self.addClassifier (wissen.NAIVEBAYES)
		self.addClassifier (wissen.FEATUREVOTE)	
		self.addClassifier (wissen.ROCCHINO)
		self.addClassifier (wissen.TFIDF)
		self.addClassifier (wissen.SIMILARITY)		
		
		#	finally, add meta		
		meta = dict ([(cl, obj) for cl, obj in self.clfs.items () if cl in (wissen.NAIVEBAYES, wissen.FEATUREVOTE, wissen.ROCCHINO)])
		self.clfs [wissen.META] = metaclassifier.Classifier (meta, logger = self.si.logger)
		
		for classifier, option in self.classifer_opts [:]:
			self.__setopt (classifier, **option)
		
		self.cache.clear ()
		self.closed = 0
		self.mod_time = self.si.getModfiedTime ()			
		return 1

	def do_status (self, *arg, **karg):
		if self.reader:
			segmentinfos = [(self.reader.reader.seg, 0, 0, self.reader.reader.ti.numterm)]		
		else:
			segmentinfos = []
			
		locks, note = self.si.lock.locks ()
		if self.mod_time == -1:
			mod_time = "N/A"
		else:
			mod_time = time.asctime (time.localtime (self.mod_time))

		return {
			"modtime": mod_time,
			"numquery": self.numquery,
			"N": self.si.getN (),
			"segment": segmentinfos,			
			"locks": locks,
			"note": note,
			"files": self.si.fs.dirinfo ()
		}
	
	def guess (self, *arg, **karg):
		default = {"code": 500, "err": "Default Error", "total": 0, "result": []}
		return self.multi_job (self.do_quess, default, *arg, **karg)
	
	def do_delete (self, qs):
		self.reader.delete (qs)		
		
	RX_SPACE = re.compile ("\s+")
	def do_quess (self, qs, lang = 'un', cl = "meta", top = 0, cond = "", *arg, **karg):
		try:
			top = int (top)
			qs = unistr.makes (qs)
			if cond:
				cond = unistr.makes (cond)
			
		except:
			return {"code": 501, "err": "Arguments Error", "total": 0, "result": []}
		
		if not qs:
			return {"code": 502, "err": "No Keyword", "total": 0, "result": []}
		
		if not self.reader:
			return {"code": 503, "err": "No Reader", "total": 0, "result": []}
		
		s = time.time ()
		mem = self.reader.get_memory ()				
		
		classifier = self.get_classifier (cl)
		if not classifier:
			return {"code": 504, "err": "No Classifier", "total": 0, "result": []}
			#return [501, 0, 0, 0]
			
		decision = classifier.guess (mem, qs, lang, cond)
		if top == 0:
			top_decision = []
			current_score = None
			for label, score in decision:
				if top_decision and (score < top_decision [-1][-1] or label == top_decision [-1][0]):
					break
				top_decision.append ((label, score))				
			decision = top_decision			
		else:
			decision = decision [0:top]
			
		result = {
			"code": 200,
			"time": int ((time.time () - s) * 1000),
			"total": len (decision),	
			"result": decision
		}		
		return result

		
def main ():
	from wissen import indexinfo
	from wissen.lib import confparse
	import odbc

	memory.create (1, 32768, 100, "segment")
	inf = indexinfo.IndexInfo (confparse.ConfParse (r"d:\bladepub\proto\etc\col\unspsc.family.class"))
	f = Classifier (inf)
	f.initialize ()

	dbc = odbc.odbc ("pepsi/ibizweb/*0=`db]")
	c = dbc.cursor ()
	c.execute ("""
		select top 1300 left (egcc, 4) unspsc, 
		isnull (title, '') + ' ' + isnull (seg, '') + ' ' + isnull (fam, '') + ' '+ isnull (cla, '') + ' ' + isnull (com, '') as description
		from iisd.dbo.trainset_unspsc
		where lang = 0 and substring (egcc, 3, 2) <> '00'		
	""")

	matched = 0
	processed = 0
	unclassified = 0
	agreed = 0
	c1 = 0
	c2 = 0
	c3 = 0

	items = c.fetchall ()
	for item in items [1000:]:	
		processed += 1
		unspsc, title = item
		res = f.query (title, engine = "nb")
		#res = f.guess (title)
		res = res [4:]
		
		if res:
			print(unspsc, res [:2])
			if type (res [0]) == type (()):
				if res [0][0] == unspsc:
					matched += 1
			else:	
				if res [0] == unspsc:
					matched += 1
		else:
			unclassified += 1
	f.close ()
	
	print("_" * 79)
	print((
		"Processed: %d\n"
		"Unclassified: %d\n"
		"Matched: %d\n"
		"Agree: %d\n"
		"1 Class: %d\n"
		"2 Classes: %d\n"
		"3 Classes: %d\n"

		"Accuracy: %2.3f%%\n" % (processed, unclassified, matched, agreed, c1, c2, c3, float (matched) / (processed - unclassified) * 100)
	))

	c.close ()
	dbc.close ()
	

if __name__ == "__main__":
	main ()
