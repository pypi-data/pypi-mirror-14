import os
import sys
import types
from wissen import _wissen
from wissen.searcher import indexer, document
from ..util import util
from .segment import composedsegmentwriter
import math
import wissen

class ExitNow (Exception): 
	pass
	
class PoolInfo:
	def __init__ (self, name, df):
		self.name = name
		self.df = df
		self.tf = 0

	def __lt__ (a, b):
		return a.name < b.name

	def __repr__ (self):
		return self.name


class Corpus:
	N = 0
	pools = []
	numpools = 0
	poolno = {}
	terms = {}
	scores = []
	features = {}
		
			
class Trainer (indexer.Indexer):
	def __init__ (self, si):
		self.si = si
	
		self.corpus = Corpus ()	
		self.indexer = None
		self.writer = None
		self._initialized = False
	
	def init (self):
		self.si.log ("initializing trainer...", "info")
		if not self.isIndexable ():
			raise ExitNow("`%s' not Indexable" % self.si.getAlias ())
		self.writer = composedsegmentwriter.ComposedSegmentWriter (self.si)
		self.corpus.N = self.writer.getIndexedNumDoc ()
	
	def indexFeatureSet (self, bog):
		# shrink term demension but almost useless, I think...
		class FilterAnalyzer:
			def __init__ (self, bog):
				self.bog = bog
			
			def index (self, document):
				res = {}
				for term, tf in document:
					if term not in self.bog: continue
					res [term] = [1] *tf				
				return res
				
		analyzer = FilterAnalyzer (bog)
		col = wissen.collection (os.path.join (self.si.indexdir, "FS"), self.si.rebuild and wissen.CREATE or wissen.WRITE, analyzer, self.si.logger)
		indexer = col.get_indexer ()
		breader = self.writer.getSegmentBulkReader ()
		
		t = breader.getNumDoc ()
		i = 0
		mem = _wissen.MemoryPool (threads, 1024, 10)
		while i < t:
			field, summary = breader.getDocument (mem, i)
			label, terms = util.deserialize (field)						
						
			doc = indexer.Document ()
			doc.add_field ("label", label, wissen.STRING)
			doc.add_field ("default", terms, wissen.TEXT, lang = self.lang)
			doc.set_content ([label, terms])
			indexer.add_document (doc)
			i += 1
		
		indexer.commit (1)
		indexer.merge ()
		indexer.close ()
		
	def add_document (self, labeledDocument):
		# labeleddocument
		if self.indexer is None:
			col = wissen.collection (os.path.join (self.si.indexdir, "TS"), self.si.rebuild and wissen.CREATE or wissen.WRITE, self.si.analyzer, self.si.logger)
			self.indexer = col.get_indexer ()
		
		terms = self.si.analyzer.term (labeledDocument.text)
		if not terms: return
		
		doc = document.Document ()
		doc.add_field ("label", labeledDocument.label, wissen.STRING)
		doc.add_field ("default", labeledDocument.text, wissen.TEXT, lang = labeledDocument.lang )
		for name, (val, ftype, lang, option) in list(labeledDocument.fields.items ()):
			doc.add_field (name, val, ftype, option, lang = lang)
		doc.set_content ([labeledDocument.label, terms])
		self.indexer.add_document (doc)
		
	def close (self):
		if self.indexer: self.indexer.close ()
		if self.writer: 
			self.writer.flush ()
			self.writer.close ()
		self.si.lock.unlock ("index")
		self.si.close ()
		self.si = None
	
	def train (self, classifier = None, **options):
		#if classifier == wissen.CL_TFIDF:
		#	raise ValueError, "can't train CL_TFIDF directly, use CL_SIMILARITY"
		if classifier is None:
			classifier = "default"
			
		selector = options.get ("selector", None)
		if not selector and classifier == "default":
			raise ValueError("No default selector, be specify")
				
		if selector:
			select_way = options.get ("select_way", wissen.SUM)
			select = float (options.get ("select", 1.0))
			prune_df_min = options.get ("prune_df_min", 0)
			prune_df_max = options.get ("prune_df_max", 10)
			
			if prune_df_min <= 1: prune_df_min = int (prune_df_min * len (self.corpus.terms))
			if prune_df_max <= 1: prune_df_max = int (prune_df_max * len (self.corpus.terms))
			
			self.selectFeatures (classifier, select, selector, select_way, prune_df_min, prune_df_max)
					
	def build (self, min_df = 0):
		if self.indexer is not None:
			self.indexer.commit (1)
			self.indexer.merge ()
			self.indexer.close ()
			self.indexer = None
			
		if not self._initialized:
			self.init ()
		
		self.si.log ("building corpus data")
		self.writer.dirty = 1
		breader = self.writer.getSegmentBulkReader ()
		# get self.corpus pools and DF
		tindex = 0
		pruned = 0
		total = -1
		stat = {}
		while 1:
			try:
				ti = breader.advanceTermInfo ()
				if ti.fdno == self.writer.fdnoclass:
					self.corpus.pools.append (PoolInfo (ti.term, ti.df))
				elif ti.fdno == self.writer.fdnoterm:
					total += 1
					if min_df and ti.df < min_df:
						pruned += 1
					else:	
						self.corpus.terms [ti.term] = tindex
						stat [ti.term] = ti.df
						tindex += 1					
			except IndexError:
				break
		
		breader.close ()
		self.si.log ("%d (%d%%) terms pruned term dimension was shrinked: %d->%d" % (pruned, 1.*pruned/total*100, total, total-pruned))
		temp = list(stat.items ())
		temp.sort (key = lambda x: x[1], reverse = True)		
		for term, df in temp [:20]:
			self.si.log ("top DF term: %s %d" % (term, df))
		del stat
		del temp
			
		self.corpus.pools.sort ()
		
		# caching related with pools
		self.corpus.numpools = len (self.corpus.pools)
		pindex = 0
		poolno = {}
		for pool in self.corpus.pools:
			poolno [pool.name] = pindex
			pindex += 1
		self.corpus.poolno = poolno
		# caching related with pools--
		
		c = 0
		t = len (self.corpus.terms)
		for term in self.corpus.terms:
			if c % 1000 == 0:				
				self.si.log ("build corpus %d/%d" % (c, t))
			tdf, fi = self.writer.featureClassInfo (term, self.corpus)
			i = 0
			for df, tf in fi:
				self.corpus.pools [i].tf += tf
				i += 1
			c +=1
		
		self.writer.commit (self.corpus)		
		
	def scoringFeaures (self, selector, select_way, prune_df_min, prune_df_max):
		terms = self.corpus.terms		
		sl = _wissen.Selector (len (self.corpus.pools), self.corpus.N, len (terms))
		
		if select_way == wissen.SUM:		method = 0
		elif select_way == wissen.MAX:	method = 1
		elif select_way == wissen.AVG:	method = 2
		
		selector = getattr (sl, selector)		
		self.si.log ("setting corpus")
		fi = []
		for pool in self.corpus.pools:
			fi.append ((pool.df, pool.tf))
		sl.addCorpus (fi)

		self.si.log ("calculating feature's score...")
		scores = []
		t = len (terms)
		c = 0
		p = 0
		for term in terms:
			c += 1
			if c % 1000 == 0:
				self.si.log ("calculating feature %d/%d (%d pruned)" % (c, t, p))
				
			tdf, fi = self.writer.featureClassInfo (term, self.corpus)
			if not tdf: continue
			if prune_df_min > 0 and tdf <= prune_df_min:
				p += 1
				continue
			if prune_df_max > 0 and tdf >= prune_df_max:
				p += 1
				continue			
			sl.add (fi)
			score = selector (method)
			scores.append ((term, score))			
		
		self.si.log ("sorting by score")
		scores.sort (key = lambda x: x [1], reverse = True)
		self.si.log ("feature selection, done.")
		sl.close ()
		return scores
	
	def selectFeatures (self, name, select, selector, select_way, prune_df_min = 0, prune_df_max = 0):
		self.si.log ("selecting [%s] using [%s:%s] for [%s]" % (select, selector, select_way, name))
		
		scores = self.scoringFeaures (selector, select_way, prune_df_min, prune_df_max)
		if not select:
			select = 1.0
		if select <= 1.0:
			select = int (len (scores) * select)
		else:
			select = int (select)
		if len (scores) < select:
			select = len (scores)
		
		c = 0
		for term, score in scores:
			c += 1
			self.si.log ("feature (score): %d. %s (%2.1f)" % (c,term, score))
				
		self.si.log ("selecting within %d th features" % (select,))
		terms = scores [:select]
		terms = [x [0] for x in terms]
		
		fmap = dict ([(term, self.corpus.terms [term]) for term in terms])
		if name == "all":
			self.writer.si.segments.features = fmap
		else:	
			self.writer.si.segments.features [name] = fmap
	
	def getFeatureSet (self, name):
		return self.writer.si.segments.features	[name]	
			
	
def usage ():
	print("""
Usage:
	%s [long option list...]
	--config=configuration file path
	--force
	--index
		sub option: --[bulk | append]	
	""" % sys.argv [0])
	sys.exit ()
	
	
def main (path, index = 0, rebuild = 0, force = 0):
	util.check_config (path)
	f = Trainer (path)
	if f.indexable (force):
		f.main (index, rebuild, force)


if __name__ == "__main__":
	import sys, getopt
	import profile

	try: argopt = getopt.getopt(sys.argv[1:], "", \
		["config=", "index", "bulk", "append", "force"])
	except:
		usage ()

	_config = None
	_rebuild = None
	_force = 0
	_index = 0

	for k, v in argopt[0]:
		if k == "--config":
			_config = v
		elif k == "--index":
			_index = 1
		elif k == "--bulk":
			_rebuild = 1
		elif k == "--append":
			_rebuild = 0
		elif k == "--force":
			_force = 1

	if not _config: usage ()
	if _index and _rebuild is None: usage ()

	main (_config, _index, _rebuild, _force)	
