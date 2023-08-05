from wissen import _wissen
from .util import htmlstrip
from . import abstractAnalyzer
	
class Analyzer (abstractAnalyzer.Analyzer):
	def __init__ (self, max_term = 8, numthread = 1, **karg):
		self.hstriper = htmlstrip.build_parser ()
		self.strip_html = False # for fast detect
		self.options = {
			"ngram": 1,
			"stem_level": 1,
			"stopwords": None,	
			"endwords": None,
			"stopwords_case_sensitive": 1,
			"ngram_no_space": 0,	
			"strip_html": False
		}
		abstractAnalyzer.Analyzer.__init__ (self, max_term, numthread)
		self.setopt (**karg)
	
	def createTSAnalyzers (self, num):
		for i in range (num):
			# stem-level=weak, ngram=bi, default stopwords list			
			f = _wissen.Analyzer (self.max_term, self.getopt (stem_level = 1), self.getopt (ngram = 2))
			f.set_stopwords ()
			self.ats.append (f)
	
	#------------------------------------------------
	# set options 
	#------------------------------------------------
	def getopt (self, **karg):
		for k, v in list(karg.items ()):	
			return self.options.get (k, v)
						
	def setopt (self, **karg):	
		for k, v in list(karg.items ()):
			self.apply_option (k, v)
			
	def apply_option (self, name, value):
		self.options [name] = value
		
		if name == "stopwords":
			self._setStopwords (value)
			
		elif name == "endwords":	
			self._setEndwords (value)
			
		elif name == "stopwords_case_sensitive":		
			self._setStopwordsCaseSensitive (value)
			
		elif name == "ngram":			
			self._setNgram (value)
			
		elif name == "ngram_no_space":
			self._setNgramIgnoreSpace (value)
					
		elif name == "stem_level":	
			self._setStemLevel (value)
		
		elif name == "strip_html":
			self._enableHtmlStrip (value)
		
		else:
			raise NameError("Unknown Option `%s`" % name)
			
	#------------------------------------------------
	# exported methods
	#------------------------------------------------			
	def htmlStrip (self, document):
		return self.hstriper.parse (document)
	
	def formalize (self, document):
		return self.ats [self.get_tid ()].formalize (document)
	
	def index	(self, document, lang = "en"):
		if self.strip_html:
			document = self.htmlStrip (document)
		#for k, v in self.ats [self.get_tid ()].analyze (document).items():
		#	print k.decode("utf8").encode("euckr"), v
		return self.ats [self.get_tid ()].analyze (document, lang)

	def term (self, document, lang = "en"):		
		k = self.index (document, lang)
		if k:
			return [(x [0], len (x [1])) for x in list(k.items ())]
	
	def query (self, document, lang = "en"):
		return self.ats [self.get_tid ()].stem (document, lang)
	
	#------------------------------------------------
	# handle options 
	#------------------------------------------------	
	def _enableHtmlStrip (self, flag):
		self.strip_html = flag
						
	def _setStopwords (self, wordlist):
		for an in self.ats:
			an.set_stopwords (wordlist)
			
	def _setEndwords (self, wordlist):
		for an in self.ats:
			an.set_endwords (wordlist)		
	
	def _setStemLevel (self, stem_level):
		self.stem_level = stem_level
		for an in self.ats:
			an.set_stem_level (stem_level)
		
	def _setNgramIgnoreSpace (self, flag):
		self.ngram_ignore_space = flag		
		for an in self.ats:
			an.set_ngram_ignore_space (flag)	
	
	def _setStopwordsCaseSensitive (self, flag):
		self.stopwords_case_sensitive = flag		
		for an in self.ats:
			an.set_stopwords_case_sensitive (flag)	
				
	def _setNgram (self, ngram):
		self.ngram = ngram
		for an in self.ats:
			an.set_ngram (ngram)	
	
	
					
	
