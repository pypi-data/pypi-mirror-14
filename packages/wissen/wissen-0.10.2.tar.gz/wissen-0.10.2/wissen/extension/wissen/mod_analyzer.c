#include "analyzer/analyzer.h"
#include "Python.h"
#include "core.h"
#include "stdlib.h"
#include "stdio.h"
#include "structmember.h"
#include "stoplist.h"
#include <stdio.h>


/****************************************************************
Module Memeber Definition
****************************************************************/

typedef struct {
	PyObject_HEAD
	int wcount;
	POSTOKENS tokens;
	char* temp;
	size_t tempsize;
	int stem_level;
	NGRAMOPTIONS ngram;	
	WORDLIST stopword;
	WORDLIST endword;
} Analyzer;


/****************************************************************
Shared Functions
****************************************************************/

static PyObject*
__makedict (PyObject *pydict, POSTOKENS tokens)
{
	PyObject *l, *p;
	int i, newone;
	
	for (i = 0; i < tokens->tsnum; i++) {
		newone = 0;
		l = PyDict_GetItemString (pydict, tokens->ts [i]->token);
		if (!l) {
			l = PyList_New (0);
			newone = 1;
		} else if (PyList_Size (l) >= MAXPROX) {
			/* ignore data what is over MAXPROX */
			continue;
		}

		p = PyLong_FromLong (tokens->ts [i]->position);
		PyList_Append (l, p);
		Py_DECREF (p);
		PyDict_SetItemString (pydict, tokens->ts [i]->token, l);
		if (newone) Py_DECREF (l);
 	}

 	return pydict;
}

/****************************************************************
Contructor / Destructor
****************************************************************/
static PyObject *
Analyzer_new (PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	Analyzer *self;
	self = (Analyzer*)type -> tp_alloc(type, 0);
	return (PyObject*) self;
}

static int
Analyzer_init (Analyzer *self, PyObject *args)
{
	int i;
	self->wcount = 3000;
	self->tokens = NULL;
	self->temp = NULL;
	self->stem_level = 1; // 0: no stem, 1: weak stem, 2: full stem
	self->ngram.n = 0;
	self->ngram.ignore_space = 0;
	
	self->stopword.wordlist = NULL;
	self->stopword.numword = 0;
	self->stopword.iscreated = 0;
	self->stopword.case_sensitive = 1;
	
	self->endword.wordlist = NULL;
	self->endword.numword = 0;
	self->endword.iscreated = 0;
	self->stopword.case_sensitive = 1;
	
	if (!PyArg_ParseTuple(args, "|iiii", &self->wcount, &self->stem_level, &self->ngram.n, &self->ngram.ignore_space)) return -1;
	self->tokens = (POSTOKENS) malloc ((sizeof(int) * 3) + (sizeof (WORD*) * self->wcount));
	if (!self->tokens) {
		PyErr_NoMemory ();
		return -1;
	}
	
	self->tokens->tsize = self->wcount;
	for (i = 0; i < self->wcount; i++) {
		self->tokens->ts [i] = (WORD*) malloc (sizeof (WORD));		 		
	}	
	self->temp = (char*) malloc (4096);
	self->tempsize = 4096;
	return 0;
}

static void
Analyzer_dealloc (Analyzer* self)
{
	Py_TYPE(self)->tp_free ((PyObject*) self);
}


/****************************************************************
Module Methods
****************************************************************/


PyObject *
Analyzer_close (Analyzer *self, PyObject *args)
{
	int i;
	if (self->tokens) {
		for (i = 0; i < self->wcount; i++) {
			free (self->tokens->ts [i]);		
		}	
		free (self->tokens);
		self->tokens = NULL;
	}
	
	if (self->temp) {
		free (self->temp);
		self->temp = NULL;
	}
	
	if (self->stopword.iscreated) {
		for (i=0; i<self->stopword.numword;i++) free (self->stopword.wordlist[i]);
		free (self->stopword.wordlist);
		self->stopword.numword = 0;
	}
	
	if (self->endword.iscreated) {
		for (i=0; i<self->endword.numword;i++) free (self->endword.wordlist[i]);
		free (self->endword.wordlist);
		self->endword.numword = 0;
	}
	
	Py_INCREF (Py_None);
	return Py_None;
}

PyObject *
Analyzer_isstopword (Analyzer *self, PyObject *args) {
	char *py_str;
	if (!PyArg_ParseTuple(args, "s", &py_str)) return NULL;
	return PyLong_FromLong (isstopword (py_str, &self->stopword));
}

PyObject *
Analyzer_formalize (Analyzer *self, PyObject *args)
{
	size_t size;
	PyObject *result, *pytext;
	char *document;

	if (!PyArg_ParseTuple(args, "O", &pytext)) return NULL;
		
#if PY_MAJOR_VERSION >= 3
	document = PyUnicode_AsUTF8 (pytext);
#else
	document = PyString_AsString (pytext);
#endif
	
	size = strlen (document);
	
	if (self->tempsize < size + 1) {
		self->temp = realloc (self->temp, size + 1);
		self->tempsize = size + 1;
	}
	
	self->temp = formalize (self->temp, document, (int) size);

#if PY_MAJOR_VERSION >= 3
	result = PyUnicode_FromString (self->temp);
#else	
	result = PyString_FromString (self->temp);
#endif	
	
	if (self->tempsize > 65536)	 {
		self->temp = realloc (self->temp, 4096);
		self->tempsize = 4096;
	}	
	return result;
}

PyObject *
Analyzer_stem (Analyzer *self, PyObject *args)
{
	char* document;
	char* lang;
	char **stoplist;
	int stoplist_len;
	int i;
	PyObject *result, *pystr;

	if (!PyArg_ParseTuple(args, "Os", &pystr, &lang)) return NULL;

#if PY_MAJOR_VERSION >= 3
	document = PyUnicode_AsUTF8 (pystr);
#else
	document = PyString_AsString (pystr);
#endif
	
	if (!strlen (document)) {
		return PyList_New (0);
	}	
	if (!self->stopword.iscreated) {
		SELECT_STOPLIST;	
		self->stopword.wordlist = stoplist;
		self->stopword.numword = stoplist_len / sizeof (stoplist[0]);		
	}	
	
	analyze (self->tokens, document, lang, self->stem_level, &self->ngram, &self->stopword, &self->endword);
	if (!self->tokens->tsnum) {
		return PyList_New (0);
	}
	result = PyList_New (self->tokens->tsnum);
	for (i=0; i<self->tokens->tsnum; i++) {		

#if PY_MAJOR_VERSION >= 3
		PyList_SetItem (result, i, PyUnicode_FromString (self->tokens->ts[i]->token));
#else		
		PyList_SetItem (result, i, PyString_FromString (self->tokens->ts[i]->token));		
#endif	

	}
	return result;
}

PyObject *
Analyzer_analyze (Analyzer *self, PyObject *args)
{
	char *document;	
	char* lang;
	char **stoplist;
	int stoplist_len;
	PyObject *result, *pystr;
	
	if (!PyArg_ParseTuple(args, "Os", &pystr, &lang)) return NULL;

#if PY_MAJOR_VERSION >= 3
	document = PyUnicode_AsUTF8 (pystr);
#else
	document = PyString_AsString (pystr);
#endif

	result = PyDict_New ();
	if (!strlen (document)) {		
		return result;
	}	
	if (!self->stopword.iscreated) {
		SELECT_STOPLIST;
		self->stopword.wordlist = stoplist;
		self->stopword.numword = stoplist_len / sizeof (stoplist[0]);		
	}	
	
	analyze (self->tokens, document, lang, self->stem_level, &self->ngram, &self->stopword, &self->endword);
	if (!self->tokens->tsnum) {
		return result;
	}
	__makedict (result, self->tokens);	
	return result;
}

PyObject *
Analyzer_count_stopwords (Analyzer *self, PyObject *args)
{
	char *document;	
	char* lang;
	char **stoplist;
	int stoplist_len;
	PyObject *pystr;
	NGRAMOPTIONS ngram;
	
	if (!PyArg_ParseTuple(args, "Os", &pystr, &lang)) return NULL;

#if PY_MAJOR_VERSION >= 3
	document = PyUnicode_AsUTF8 (pystr);
#else
	document = PyString_AsString (pystr);
#endif

	if (!strlen (document)) {
		return PyLong_FromLong (0);
	}	
	if (!self->stopword.iscreated) {
		SELECT_STOPLIST;
		self->stopword.wordlist = stoplist;
		self->stopword.numword = stoplist_len / sizeof (stoplist[0]);		
	}
	ngram.ignore_space = 0;
	ngram.n = 0;
	analyze (self->tokens, document, lang, 0, &ngram, &self->stopword, &self->endword);
	// (stop-words, total-words)
	return Py_BuildValue ("ii", self->tokens->stopwords, self->tokens->stopwords + self->tokens->tsnum);
}

PyObject *
Analyzer_set_stem_level (Analyzer *self, PyObject *args) {
	if (!PyArg_ParseTuple(args, "i", &self->stem_level)) return NULL;
	return PyLong_FromLong (self->stem_level);
}

PyObject *
Analyzer_set_ngram (Analyzer *self, PyObject *args) {
	if (!PyArg_ParseTuple(args, "i", &self->ngram.n)) return NULL;
	return PyLong_FromLong (self->ngram.n);
}

PyObject *
Analyzer_set_ngram_ignore_space (Analyzer *self, PyObject *args) {
	if (!PyArg_ParseTuple(args, "i", &self->ngram.ignore_space)) return NULL;
	return PyLong_FromLong (self->ngram.ignore_space);
}

PyObject *
Analyzer_get_ngram_ignore_space (Analyzer *self, PyObject *args) {
	return PyLong_FromLong (self->ngram.ignore_space);
}

PyObject *
Analyzer_get_stem_level (Analyzer *self, PyObject *args) {
	return PyLong_FromLong (self->stem_level);
}

PyObject *
Analyzer_get_ngram (Analyzer *self, PyObject *args) {
	return PyLong_FromLong (self->ngram.n);
}

PyObject *
Analyzer_set_stopwords_case_sensitive (Analyzer *self, PyObject *args) {
	if (!PyArg_ParseTuple(args, "i", &self->stopword.case_sensitive)) return NULL;	
	Py_INCREF (Py_None);
	return Py_None;
}

PyObject *
Analyzer_set_endwords_case_sensitive (Analyzer *self, PyObject *args) {
	if (!PyArg_ParseTuple(args, "i", &self->endword.case_sensitive)) return NULL;	
	Py_INCREF (Py_None);
	return Py_None;
}

PyObject *
Analyzer_set_stopwords (Analyzer *self, PyObject *args) {
	int i;
	char *word;
	char *temp;
	size_t wlen;
	PyObject *pystoplist = NULL;
	if (!PyArg_ParseTuple(args, "|Oi", &pystoplist, &self->stopword.case_sensitive)) return NULL;
	if (!pystoplist) {
		self->stopword.wordlist = stoplist_en;
		self->stopword.numword = sizeof (stoplist_en) / sizeof (stoplist_en[0]);
		self->stopword.iscreated = 0;		
	}
	
	else {
		self->stopword.numword = (int) PyList_Size (pystoplist);
		self->stopword.wordlist = malloc (sizeof (char*) * self->stopword.numword);
		for (i = 0; i < self->stopword.numword; i++) {

#if PY_MAJOR_VERSION >= 3
			word = PyUnicode_AsUTF8 (PyList_GetItem (pystoplist, i));
#else			
			word = PyString_AsString (PyList_GetItem (pystoplist, i));
#endif	
		
			wlen = strlen(word);
			temp = (char*) malloc (wlen+1);
			strncpy (temp, word, wlen + 1);
			self->stopword.wordlist [i] = temp;
		}
		self->stopword.iscreated = 1;
	}
	qsort (self->stopword.wordlist, self->stopword.numword, sizeof (char*), cmp_str);
	Py_INCREF (Py_None);
	return Py_None;
}

PyObject *
Analyzer_set_endwords (Analyzer *self, PyObject *args) {
	int i;
	char *word;
	char *temp;
	size_t wlen;
	PyObject *pyendlist;
	if (!PyArg_ParseTuple(args, "O|i", &pyendlist, &self->endword.case_sensitive)) return NULL;
	self->endword.numword = (int) PyList_Size (pyendlist);
	self->endword.wordlist = malloc (sizeof (char*) * self->endword.numword);	
	for (i = 0; i < self->endword.numword; i++) {

#if PY_MAJOR_VERSION >= 3
		word = PyUnicode_AsUTF8 (PyList_GetItem (pyendlist, i));
#else			
		word = PyString_AsString (PyList_GetItem (pyendlist, i));
#endif

		wlen = strlen(word);
		temp = (char*) malloc (wlen+1);
		strncpy (temp, word, wlen + 1);
		self->endword.wordlist [i] = temp;
	}
	qsort (self->endword.wordlist, self->endword.numword, sizeof (char*), cmp_str);
	self->endword.iscreated = 1;
	Py_INCREF (Py_None);
	return Py_None;
}

/****************************************************************
Module Definition
****************************************************************/

static PyMemberDef Analyzer_members[] = {
	//{"mode", T_CHAR, offsetof(Analyzer, mode), 0, ""},
	{NULL}
};

static PyMethodDef Analyzer_methods[] = {
	{"analyze", (PyCFunction) Analyzer_analyze, METH_VARARGS, ""},	
	{"formalize", (PyCFunction) Analyzer_formalize, METH_VARARGS, ""},	
	{"stem", (PyCFunction) Analyzer_stem, METH_VARARGS, ""},	
	{"isstopword", (PyCFunction) Analyzer_isstopword, METH_VARARGS, ""},	
	{"is_stopword", (PyCFunction) Analyzer_isstopword, METH_VARARGS, ""},	
	{"count_stopwords", (PyCFunction) Analyzer_count_stopwords, METH_VARARGS, ""},	
	{"close", (PyCFunction) Analyzer_close, METH_VARARGS, ""},	
	{"set_stopwords", (PyCFunction) Analyzer_set_stopwords, METH_VARARGS, ""},	
	{"set_stopwords_case_sensitive", (PyCFunction) Analyzer_set_stopwords_case_sensitive, METH_VARARGS, ""},	
	{"set_endwords", (PyCFunction) Analyzer_set_endwords, METH_VARARGS, ""},	
	{"set_endwords_case_sensitive", (PyCFunction) Analyzer_set_endwords_case_sensitive, METH_VARARGS, ""},	
	{"set_stem_level", (PyCFunction) Analyzer_set_stem_level, METH_VARARGS, ""},	
	{"set_ngram", (PyCFunction) Analyzer_set_ngram, METH_VARARGS, ""},	
	{"set_ngram_ignore_space", (PyCFunction) Analyzer_set_ngram_ignore_space, METH_VARARGS, ""},		
	{"get_ngram_ignore_space", (PyCFunction) Analyzer_get_ngram_ignore_space, METH_VARARGS, ""},		
	{"get_stem_level", (PyCFunction) Analyzer_get_stem_level, METH_VARARGS, ""},	
	{"get_ngram", (PyCFunction) Analyzer_get_ngram, METH_VARARGS, ""},		
	{NULL}
};

PyTypeObject AnalyzerType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"core.Analyzer",			 /*tp_name*/
	sizeof (Analyzer),			 /*tp_basicsize*/
	0,						 /*tp_itemsize*/
	(destructor) Analyzer_dealloc, /*tp_dealloc*/
	0,						 /*tp_print*/
	0,						 /*tp_getattr*/
	0,						 /*tp_setattr*/
	0,						 /*tp_compare*/
	0,						 /*tp_repr*/
	0,						 /*tp_as_number*/
	0,						 /*tp_as_sequence*/
	0,						 /*tp_as_mapping*/
	0,						 /*tp_hash */
	0,						 /*tp_call*/
	0,						 /*tp_str*/
	0,						 /*tp_getattro*/
	0,						 /*tp_setattro*/
	0,						 /*tp_as_buffer*/
	Py_TPFLAGS_DEFAULT, /*tp_flags*/
	"DocMap objects",		   /* tp_doc */
	0,					   /* tp_traverse */
	0,					   /* tp_clear */
	0,					   /* tp_richcompare */
	0,					   /* tp_weaklistoffset */
	0, //PyObject_SelfIter,					   /* tp_iter */
	0, //(iternextfunc) Analyzer_iternext,	   /* tp_iternext */
	Analyzer_methods,			 /* tp_methods */
	Analyzer_members,			 /* tp_members */
	0,						 /* tp_getset */
	0,						 /* tp_base */
	0,						 /* tp_dict */
	0,						 /* tp_descr_get */
	0,						 /* tp_descr_set */
	0,						 /* tp_dictoffset */
	(initproc) Analyzer_init,	  /* tp_init */
	0,						 /* tp_alloc */
	Analyzer_new,				 			/* tp_new */
};
