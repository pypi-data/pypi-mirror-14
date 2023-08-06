from .. import colsetup
from . import classifier, trainer
from wissen.cluster import termCluster

class Segments (colsetup.Segments):
	def __init__ (self, alias = ""):
		colsetup.Segments.__init__ (self, alias)
		self.N = 0
		self.pools = []		
		self.numpool = 0
		self.numvoca = 0
		self.features = {}
		self.parameters = {"build": (0, 0), "train": {}}
		

class Model (colsetup.CollectionSetup):
	exts = ["cfq", "cof", "coi", "fii", "fis", "cfi"]
	segment_class = Segments
	
	def __init__ (self, indexdir, mode = 'r', analyzer = None, logger = None, plock = None):
		colsetup.CollectionSetup.__init__ (self, indexdir, mode, analyzer, logger, plock)
		
	def get_learner (self, **karg):
		self.setopt (**karg)
		return trainer.Trainer (self)
	
	def get_classifier (self, **karg):
		self.setopt (**karg)
		return classifier.Classifier (self)
	
	def get_termcluster (self, **karg):
		self.setopt (**karg)
		return termCluster.TermCluster (self)
		
