#include "Python.h"
#include "core.h"
#include "structmember.h"
#include "index/index.h"
#include "pthread.h"
#include <stdio.h>


/****************************************************************
Module Memeber Definition
****************************************************************/

typedef struct TermInfo {
	PyObject_HEAD		
	Term lastTerm;
	Term lastIndexTerm;
	MemTerm** termindex;
	int numterm;
	int numindexterm;
	char mode;	
	int index;
	unsigned char *fdmap;
	BFILE* btii;
	BFILE* btis;
	int tii;
	int tis;	
} TermInfo;


/****************************************************************
Shared Functions
****************************************************************/
static 
int compare (const void *p1, const void *p2) {
	if ( (* (Term * const)p1).fdno == (* (Term * const)p2).fdno ) {
		return strcmp ( (char *) ((* (Term * const)p1).term), (char *) ((* (Term * const)p2).term) );
	}
	else {
		 if ( (* (Term * const)p1).fdno > (* (Term * const)p2).fdno ) return 1;
		 if ( (* (Term * const)p1).fdno < (* (Term * const)p2).fdno )  return -1;
		 return 0;
	}
}

static 
int ncompare (const void *p1, const void *p2, int len) {
	if ( (* (Term * const)p1).fdno == (* (Term * const)p2).fdno ) {
		return strncmp ( (char *) ((* (Term * const)p1).term), (char *) ((* (Term * const)p2).term), len );
	}
	else {
		 if ( (* (Term * const)p1).fdno > (* (Term * const)p2).fdno ) return 1;
		 if ( (* (Term * const)p1).fdno < (* (Term * const)p2).fdno )  return -1;
		 return 0;
	}
}

static 
int compare_with_index (const void *p1, const void *p2) {
	if ( (*(Term * const)p1).fdno == (* (MemTerm * const)p2).fdno ) {
		//printf ("COMP [%s-%s // %i]\n", (char *) (*(Term * const)p1).term, (char *) ((* (MemTerm * const)p2).term), strcmp ( (char *) (*(Term * const)p1).term, (char *) ((* (MemTerm * const)p2).term) ));
		return strcmp ( (char *) (*(Term * const)p1).term, (char *) ((* (MemTerm * const)p2).term) );
	}
	else {
		 if ( (*(Term * const)p1).fdno > (* (MemTerm * const)p2).fdno ) return 1;
		 if ( (*(Term * const)p1).fdno < (* (MemTerm * const)p2).fdno )  return -1;
		 return 0;
	}
}


/****************************************************************
Contructor / Destructor
****************************************************************/
static PyObject *
TermInfo_new (PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	TermInfo *self;
	self = (TermInfo*) type -> tp_alloc(type, 0);
	return (PyObject*) self;
}

static void
TermInfo_destroy (TermInfo *self) {
	int i;
	if (self->btis) bclose (self->btis);
	if (self->btii) bclose (self->btii);
					
	if (self->termindex) {
		for (i = 0; i < self->numindexterm; i++) {
			free (self->termindex [i]->term);
			free (self->termindex [i]);
		}
		free (self->termindex);
	}
	
	if (self->fdmap) free (self->fdmap);	
}

static int
TermInfo_init (TermInfo *self, PyObject *args)
{
	char mode = 'r';
	int _shift;
	unsigned char _uchar;
	
	if (!PyArg_ParseTuple(args, "ii|c", &self->tii, &self->tis, &mode)) return -1;
	
	self->index = 0;
	self->numterm = 0;
	self->numindexterm = 0;
	self->mode = mode;
	self->termindex = NULL;
	self->fdmap = NULL;
	
	self->btii = NULL;
	self->btis = NULL;
	
	if (mode == 'w') {		
		if (!(self->btii = bopen (self->tii, 'w', 4096, 0))) goto fail;
		if (!(self->btis = bopen (self->tis, 'w', 4096, 0))) goto fail;
	}
	
	else if (mode == 'm') {
		if (!(self->btii = bopen (self->tii, 'r', 4, 0))) goto fail;
		if (!(self->btis = bopen (self->tis, 'r', 4096, 0))) goto fail;		
		breadInt (self->btii, self->numindexterm, 4);
		breadInt (self->btis, self->numterm, 4);
		bclose (self->btii);
		self->btii = NULL;
	}
	
	else {
		/* get index numterm */
		if (!(self->btii = bopen (self->tii, 'r', 4, 0))) goto fail;
		if (!(self->btis = bopen (self->tis, 'r', 4, 0))) goto fail;		
		breadInt (self->btii, self->numindexterm, 4);
		breadInt (self->btis, self->numterm, 4);		
		bclose (self->btis);
		self->btis = NULL;
	}
	
	/* setup lastterm */
	self->lastTerm.term [0] = '\0';	
	self->lastTerm.frqPointer = 0;	
	self->lastTerm.prxPointer = 0;	
	
	self->lastIndexTerm.term [0] = '\0';
	self->lastIndexTerm.frqPointer = 0;
	self->lastIndexTerm.prxPointer = 0;
	self->lastIndexTerm.indexPointer = 0;
	
	return 0;

fail:
	TermInfo_destroy (self);
	PyErr_NoMemory ();
	return -1;

ioreaderror:
	TermInfo_destroy (self);
	PyErr_SetFromErrno (PyExc_IOError);
	return -1;
}

static void
TermInfo_dealloc (TermInfo* self)
{
	Py_TYPE(self)->tp_free ((PyObject*) self);
}


/****************************************************************
Module Methods
****************************************************************/

static PyObject*
TermInfo_initialize (TermInfo *self, PyObject *args)
{
	int _shift;
	unsigned int _uint;
	
	if (self->mode == 'w') {
		bwriteInt (self->btis, 0, 4);
		bwriteInt (self->btii, 0, 4);
	}	
	Py_INCREF (Py_None);
	return Py_None;

iowriteerror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

memoryerror:
	PyErr_NoMemory ();
	return NULL;	
}

static PyObject*
TermInfo_set_fieldinfo (TermInfo* self, PyObject *args)
{
	PyObject *pydict;
	PyObject *key, *value;
	Py_ssize_t pos = 0;
	
	/* finally flush buffer to file */
	if (!PyArg_ParseTuple(args, "O", &pydict)) return NULL;	
	
	if (!(self->fdmap = (unsigned char*) malloc (256))) return PyErr_NoMemory ();
	for (pos = 0; pos < 256; pos ++) {
		self->fdmap [pos] = 'f';
	}
	
	pos = 0;
	while (PyDict_Next(pydict, &pos, &key, &value)) {		
	    self->fdmap [(int) PyLong_AsLong (key)] = (unsigned char) (PyBytes_AsString (value) [0]);
	}

	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject* 
TermInfo_commit (TermInfo *self, PyObject *args) 
{
	unsigned int _uint;
	int _shift;
	
	/* write numterm */	
	bseek (self->btis, 0);
	bwriteInt (self->btis, self->numterm, 4);				
	
	/* write index numterm */	
	bseek (self->btii, 0);
	bwriteInt (self->btii, self->numindexterm, 4);		
	
	Py_INCREF (Py_None);
	return Py_None;

iowriteerror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

memoryerror:
	PyErr_NoMemory ();
	return NULL;
}

static PyObject*
TermInfo_close (TermInfo* self)
{
	TermInfo_destroy (self);	
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject* 
TermInfo_write (TermInfo *self, Term* term, Term* lastTerm, int isi)	
{
	unsigned int _uint;	
	int i, _shift;
	char *a, *tdelta;
	int delta;
	long indexPointer = 0;
	BFILE* bfile;
	
	if (isi) 	bfile = self->btii;
	else 		bfile = self->btis;
	
	a = lastTerm->term;	
	tdelta = term->term;
	//printf ("[%s-%s, %i]\n", a, tdelta, isi);
	
	for (i = 0; i < 100; i++) {
		if (*a++ != *tdelta++) {
			tdelta--;
			break;
		}
	}
	//if (isi) printf ("[%s-%s, %i, %i]\n", lastTerm->term, term->term, i, strlen (tdelta));
	
	bwriteVInt (bfile, i); /* prefix len */
	bwriteVInt (bfile, strlen (tdelta)); /* suffix len */
	bwriteString (bfile, tdelta, strlen (tdelta)); /* suffix */
	bwriteVInt (bfile, term->fdno);	/* field num */
	bwriteVInt (bfile, term->df);/* df */
	delta = (int) (term->frqPointer - lastTerm->frqPointer);
	
	bwriteVInt (bfile, delta); /* freq delta */
	delta = (int)(term->prxPointer - lastTerm->prxPointer);
	
	bwriteVInt (bfile, delta); /* prox delta */
	bwriteVInt (bfile, (int)term->skipDelta); /* skip delta */		 
	bwriteVInt (bfile, (int)term->proxLength); /* skip delta */
	
	if (isi) {
		indexPointer = btell (self->btis);
		delta = (int) (indexPointer - lastTerm->indexPointer);
		bwriteVInt (bfile, delta); /* index delta */
		lastTerm->indexPointer = indexPointer;		
	}
	
	strcpy (lastTerm->term, term->term);	
	lastTerm->frqPointer = term->frqPointer;
	lastTerm->prxPointer = term->prxPointer;
	lastTerm->fdno = term->fdno;
	lastTerm->df = term->df;
	lastTerm->skipDelta = term->skipDelta;	
	lastTerm->proxLength = term->proxLength;
	
	Py_INCREF (Py_None);
	return Py_None;

iowriteerror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

memoryerror:
	PyErr_NoMemory ();
	return NULL;			
}


PyObject *
TermInfo_add (TermInfo *self, PyObject *args) {
	Term term;
	char *str;	
	
	if (!PyArg_ParseTuple(args, "siillii", 
		&str, &term.fdno, &term.df, &term.frqPointer, &term.prxPointer, &term.skipDelta, &term.proxLength)) return NULL;
	
	strcpy (term.term, str);
	
	if (self->numterm == 0) {
		TermInfo_write (self, &term, &self->lastIndexTerm, 1);
		self->numindexterm ++;
	} else if (self->numterm % INDEX_INTERVAL == 0) {
		TermInfo_write (self, &self->lastTerm, &self->lastIndexTerm, 1);
		self->numindexterm ++;
	}
	
	TermInfo_write (self, &term, &self->lastTerm, 0);
	self->numterm++;
	
	Py_INCREF (Py_None);
	return Py_None;
}

int
TermInfo_read (TermInfo *self, Memory* mem, Term* term, Term* lastTerm, int isi) {	
	unsigned char _uchar;
	int _shift;
	
	int surfixlen;
	int prefixlen;
	int delta;	
	char *p;
	BFILE* fs;
	
	if (isi) 	fs = self->btii;
	else 		{
		if (self->mode == 'r') {
			fs = mem->mfi->btis;
		}
		else {
			fs = self->btis;
		}	
	}
	p = term->term;
	breadVInt (fs, prefixlen); /*prefix len */	
	breadVInt (fs, surfixlen); /*suffix len */
		
	strncpy (p, lastTerm->term, prefixlen); /*copy prefix */
	p += prefixlen;
	breadString (fs, p, surfixlen);
	term->term [prefixlen + surfixlen] = '\0'; /* join suffix */
	//printf ("[%s]\n", term->term);
	breadVInt (fs, term->fdno);
	breadVInt (fs, term->df);
	
	breadVInt (fs, delta); /* freq delta */
	term->frqPointer = (long) delta + lastTerm->frqPointer;
	
	breadVInt (fs, delta); /* prox delta */	
	term->prxPointer = (long) delta + lastTerm->prxPointer;	
	
	breadVInt (fs, term->skipDelta); /* skip delta */
	breadVInt (fs, term->proxLength); /* skip delta */
	
	if (isi) {
		breadVInt (fs, delta);	/* index delta */
		term->indexPointer = (long) delta + lastTerm->indexPointer;		
		lastTerm->indexPointer = term->indexPointer;
	}
	
	strcpy (lastTerm->term, term->term);
	lastTerm->frqPointer = term->frqPointer;
	lastTerm->prxPointer = term->prxPointer;
	lastTerm->fdno = term->fdno;
	lastTerm->df = term->df;
	lastTerm->skipDelta = term->skipDelta;	
	lastTerm->proxLength = term->proxLength;
	
	return 0;

ioreaderror:
	PyErr_SetFromErrno (PyExc_IOError);
	return -1;
} 

PyObject *
TermInfo_load (TermInfo *self) {
	Term term;
	Term lastTerm;
	int i = 0;	
	
	bseek (self->btii, 4);
	
	self->termindex = NULL;	
	if (!(self->termindex = (MemTerm**) malloc (sizeof (MemTerm) * self->numindexterm))) goto memoryerror;
	/* init */
	lastTerm.term [0] = '\0';
	lastTerm.frqPointer = 0;
	lastTerm.prxPointer = 0;
	lastTerm.indexPointer = 0;
	
	while (i < self->numindexterm) {
		if (TermInfo_read (self, NULL, &term, &lastTerm, 1) == -1) goto ignore_ioerror;
		self->termindex [i] = NULL;		
		if (!(self->termindex [i] = (MemTerm*) malloc (sizeof (MemTerm)))) goto memoryerror;
		self->termindex [i]->term = NULL;
		if (!(self->termindex [i]->term = (char*) malloc (strlen (term.term) + 1))) goto memoryerror;
		strcpy (self->termindex [i]->term, term.term);
		self->termindex [i]->fdno = term.fdno;
		self->termindex [i]->df = term.df;
		self->termindex [i]->frqPointer = term.frqPointer;
		self->termindex [i]->prxPointer = term.prxPointer;
		self->termindex [i]->skipDelta = term.skipDelta;		
		self->termindex [i]->proxLength = term.proxLength;
		self->termindex [i]->indexPointer = term.indexPointer;		
		i++;
	}
	
	bclose (self->btii);
	self->btii = NULL;
	
	Py_INCREF (Py_None);
	return Py_None;	

ignore_ioerror:
	self->numindexterm = i; // resize numindexterm	
	bclose (self->btii);
	self->btii = NULL;		
	PyErr_Clear ();
	Py_INCREF (Py_None);
	return Py_None;	

memoryerror:
	if (self->termindex) {
		for (; i; i--) {
			if (self->termindex [i])	{
				if (self->termindex [i]->term) {
					free (self->termindex [i]->term);
				}
				free (self->termindex [i]);
			}
		}
		free (self->termindex);
	}
	PyErr_NoMemory ();
	return NULL;	
}

long
TermInfo_search (TermInfo *self, Term* term, Term* lastTerm)
{
	int low = 0;
	int high;
	int mid;
	int r;
	int match = 0;	
	
	high = self->numindexterm - 1;
	
	while(low <= high){
		mid = (low + high) / 2;
		r = compare_with_index ((const void*) term, (const void*) self->termindex [mid]);
		if (r == 0) {
			match = 1;
			break;
		}	
		else if(r < 0) high = mid -1;
		else low = mid + 1;
	}
	//if (low >= self->numindexterm - 1) {
	//	low --;
	//}
	//printf ("low high: %i %i %i %i\n", low, high, mid, match);
	
	/* matched, set term directly from index */
	if (match) {		
		term->df = self->termindex [mid]->df;
		term->frqPointer = self->termindex [mid]->frqPointer;
		term->prxPointer = self->termindex [mid]->prxPointer;
		term->skipDelta = self->termindex [mid]->skipDelta;
		term->proxLength = self->termindex [mid]->proxLength;
		return (long) (-1 * self->termindex [mid]->indexPointer);
	}
	
	/* not matched, but possibly this term within offset INDEX_INTERVALset */
	/* return frqPointer */
	else {
		if (low) low --;		
		strcpy (lastTerm->term, self->termindex [low]->term);
		lastTerm->fdno = self->termindex [low]->fdno;
		lastTerm->df = self->termindex [low]->df;
		lastTerm->frqPointer = self->termindex [low]->frqPointer;
		lastTerm->prxPointer = self->termindex [low]->prxPointer;
		lastTerm->skipDelta = self->termindex [low]->skipDelta;		
		lastTerm->proxLength = self->termindex [low]->proxLength;		
		return (long) self->termindex [low]->indexPointer;
	}
}

static PyObject* 
TermInfo_get (TermInfo *self, PyObject *args) 
{
	char* str;
	Term term;
	Term key;
	Term lastTerm;
	long indexPointer = -1;
	int scan = 0;
	int notmatch = -1;
	PyObject* pymem;
	Memory* mem;
	
	if (self->mode == 'w') return NULL;
	if (!self->termindex) {
		TermInfo_load (self);
	}
	
	if (!PyArg_ParseTuple(args, "Osi", &pymem, &str, &term.fdno)) return NULL;
	mem = (Memory*) PyCObject_AsVoidPtr (pymem);
	strcpy (term.term, str);
	
	indexPointer = TermInfo_search (self, &term, &lastTerm);
	//printf ("indexPointer: %i %s\n", indexPointer, term);
	if (indexPointer < 0) {		
		return Py_BuildValue ("illii", term.df, term.frqPointer, term.prxPointer, term.skipDelta, term.proxLength);
	}	
	blink (mem->mfi->btis, self->tis, mem->mutex, indexPointer, 0);	
	while (notmatch && scan < INDEX_INTERVAL) {
		if (TermInfo_read (self, mem, &key, &lastTerm, 0) == -1) goto fail;
		//printf ("--%s-%s %d\n", key.term, str, key.fdno);
		notmatch = compare (&term, &key);
		scan ++;
	}
		
	if (notmatch == 0) {
		return Py_BuildValue ("illii", key.df, key.frqPointer, key.prxPointer, key.skipDelta, key.proxLength);
	}
	
	Py_INCREF (Py_None);
	return Py_None;

fail:
	PyErr_Clear ();
	Py_INCREF (Py_None);
	return Py_None;	
}

static PyObject* 
TermInfo_getwildcard (TermInfo *self, PyObject *args) 
{
	char* str;
	int len;
	Term term;
	Term key;
	Term lastTerm;
	long indexPointer = -1;
	int scan = 0;
	int notmatch = -1;
	PyObject* infos = NULL, *o;
	PyObject* pymem;
	Memory* mem;
	
	if (self->mode == 'w') return NULL;
	if (!self->termindex) TermInfo_load (self);
	
	if (!PyArg_ParseTuple(args, "Os#i", &pymem, &str, &len, &term.fdno)) return NULL;
	mem = (Memory*) PyCObject_AsVoidPtr (pymem);
	infos = PyList_New (0);
	
	if (len < 3) return infos;
	strcpy (term.term, str);
	
	indexPointer = TermInfo_search (self, &term, &lastTerm);	
	if (indexPointer < 0) {
		indexPointer *= (long) -1;
	}		
	blink (mem->mfi->btis, self->tis, mem->mutex, indexPointer, 0);	
	while (notmatch && scan < INDEX_INTERVAL) {
		if (TermInfo_read (self, mem, &key, &lastTerm, 0) == -1) goto fail;
		//printf ("--%s\n", key.term);
		if (ncompare (&term, &key, len) == 0) {			
			o = Py_BuildValue ("illii", key.df, key.frqPointer, key.prxPointer, key.skipDelta, key.proxLength);
			PyList_Append (infos, o);
			Py_DECREF (o);
		}		
		scan ++;
	}
	return infos;
	
fail:
	PyErr_Clear ();
	return infos;
}


static PyObject* 
TermInfo_advance (TermInfo *self) 
{
	Term term;
	if (self->index == 0)
		bseek (self->btis, 4);
	
	if (self->index == self->numterm)
		return PyErr_SetFromErrno(PyExc_IndexError);
	
	if (TermInfo_read (self, NULL, &term, &self->lastTerm, 0) == -1) return NULL;
	
	self->index++;	
	return Py_BuildValue ("siillii", term.term, term.fdno, term.df, term.frqPointer, term.prxPointer, term.skipDelta, term.proxLength);	
}

static PyObject* 
TermInfo_reset (TermInfo *self) 
{
	self->index = 0;
	bseek (self->btis, 4);
	
	Py_INCREF (Py_None);
	return Py_None;
}


/****************************************************************
Module Definition
****************************************************************/
static PyMemberDef TermInfo_members[] = {
    {"numterm", T_INT, offsetof(TermInfo, numterm), 0, ""},
    {NULL}
};

static PyMethodDef TermInfo_methods[] = {
	{"add", (PyCFunction) TermInfo_add, METH_VARARGS, ""},
	{"initialize", (PyCFunction) TermInfo_initialize, METH_VARARGS, ""},	
	{"advance", (PyCFunction) TermInfo_advance, METH_VARARGS, ""},
	{"load", (PyCFunction) TermInfo_load, METH_VARARGS, ""},	
	{"get", (PyCFunction) TermInfo_get, METH_VARARGS, ""},	
	{"getwildcard", (PyCFunction) TermInfo_getwildcard, METH_VARARGS, ""},		
	{"close", (PyCFunction) TermInfo_close, METH_VARARGS, ""},	
	{"set_fieldinfo", (PyCFunction) TermInfo_set_fieldinfo, METH_VARARGS, ""},		
	{"commit", (PyCFunction) TermInfo_commit, METH_VARARGS, ""},	
	{"reset", (PyCFunction) TermInfo_reset, METH_VARARGS, ""},	
	{NULL}
};

PyTypeObject TermInfoType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"core.TermInfo",			 /*tp_name*/
	sizeof (TermInfo),			 /*tp_basicsize*/
	0,						 /*tp_itemsize*/
	(destructor) TermInfo_dealloc, /*tp_dealloc*/
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
	0, //(iternextfunc) TermInfo_iternext,	   /* tp_iternext */
	TermInfo_methods,			 /* tp_methods */
	TermInfo_members,			 /* tp_members */
	0,						 /* tp_getset */
	0,						 /* tp_base */
	0,						 /* tp_dict */
	0,						 /* tp_descr_get */
	0,						 /* tp_descr_set */
	0,						 /* tp_dictoffset */
	(initproc) TermInfo_init,	  /* tp_init */
	0,						 /* tp_alloc */
	TermInfo_new,			/* tp_new */
};




