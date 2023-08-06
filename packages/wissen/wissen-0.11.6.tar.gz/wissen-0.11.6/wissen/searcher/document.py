import types
from wissen.lib import unistr

class Document:
	def __init__ (self, content = None):
		self.fields = {}
		self.data = None
		self.stored = []
		self.summary = None		
		if content:
			self.set_content (content)
	
	def set_content (self, content):
		# any encoding even allowed python objects
		if self.stored: raise ValueError("Already got content(s)")
		self.data = content
	
	def add_content (self, content, option = []):
		# any encoding even allowed python objects
		if self.data: 
			self.stored.append (self.data)
			self.data = None
		self.stored.append ((content, option))
			
	def add_field (self, name, value, ftype = "Text", lang = "un", encoding = None, option = {}):
		self.fields [name] = (unistr.makes (value, encoding), ftype, lang, option)
	
	def set_auto_snippet (self, text, option = {}, encoding = None):
		self.summary = (unistr.makes (text, encoding), option)

