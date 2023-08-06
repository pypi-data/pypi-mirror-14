#include "Python.h"
#include "core.h"
#include "structmember.h"
#include "index/index.h"
#include "pthread.h"
#include "analyzer/analyzer.h"
#include <stdio.h>


/****************************************************************
Module Memeber Definition
****************************************************************/

typedef struct {
	PyObject_HEAD
	int numdoc;
	int index;
	BFILE *bfdi;
	BFILE *bfda;
	BFILE *bdoc;
	BFILE *bpos;
	BFILE *bzfld;
	BFILE *bzdoc;
	int fdi;
	int fda;
	SMIS* smis;
	char mode;
} Document;

typedef struct {
	int length;
	int found;
	char term [100];
} TermMeta;

typedef struct {
	char* buffer;
	int length;	
} Summary;

/****************************************************************
Shared Functions
****************************************************************/


/****************************************************************
Contructor / Destructor
****************************************************************/
static PyObject *
Document_new (PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	Document *self;
	self = (Document*)type -> tp_alloc(type, 0);
	return (PyObject*) self;
}

static void
Document_destroy (Document *self)
{
	if (self->bfdi) bclose (self->bfdi);
	if (self->bfda) bclose (self->bfda);
	if (self->bdoc) bclose (self->bdoc);
	if (self->bpos) bclose (self->bpos);
	if (self->bzfld) bclose (self->bzfld);
	if (self->bzdoc) bclose (self->bzdoc);
}

static int
Document_init (Document *self, PyObject *args)
{
	int _shift;
	unsigned char _uchar;

	if (!PyArg_ParseTuple(args, "iic", &self->fdi, &self->fda, &self->mode)) return -1;

	self->index = 0;
	self->numdoc = 0;

	self->bfdi = NULL;
	self->bfda = NULL;
	self->bdoc = NULL;
	self->bpos = NULL;
	self->bzfld = NULL;
	self->bzdoc = NULL;

	if (self->mode == 'w') {
		if (!(self->bfdi = bopen (self->fdi, 'w', FILEBUFFER_LENGTH, 0))) goto fail;
		if (!(self->bfda = bopen (self->fda, 'w', FILEBUFFER_LENGTH, 0))) goto fail;
		if (!(self->bdoc = bopen (-1, 'w', FILEBUFFER_LENGTH, 1))) goto fail;
		if (!(self->bpos = bopen (-1, 'w', FILEBUFFER_LENGTH, 1))) goto fail;
		if (!(self->bzfld = bopen (-1, 'w', FILEBUFFER_LENGTH, 1))) goto fail;
		if (!(self->bzdoc = bopen (-1, 'w', FILEBUFFER_LENGTH, 1))) goto fail;
	}

	else {
		if (!(self->bfdi = bopen (self->fdi, 'r', MIN_IOBUFFER, 0))) goto fail;
		breadInt (self->bfdi, self->numdoc, 4);
		bclose (self->bfdi);
		self->bfdi = NULL;
	}

	return 0;

fail:
	Document_destroy (self);
	PyErr_NoMemory ();
	return -1;

ioreaderror:
	Document_destroy (self);
	PyErr_SetFromErrno (PyExc_IOError);
	return -1;
}

static void
Document_dealloc (Document* self)
{
	Py_TYPE(self)->tp_free ((PyObject*) self);
}


/****************************************************************
Module Methods
****************************************************************/
static PyObject*
Document_initialize (Document *self, PyObject *args)
{
	int _shift;
	unsigned int _uint;

	if (self->mode == 'w') {
		bwriteInt (self->bfdi, 0, 4);
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
Document_setsmis (Document *self, PyObject *args)
{
	PyObject* smis;
	if (!PyArg_ParseTuple(args, "O", &smis)) return NULL;
	self->smis = (SMIS*) PyCObject_AsVoidPtr (smis);
	Py_INCREF (Py_None);
	return Py_None;
}


static PyObject*
Document_write (Document *self, PyObject *args)
{
	int _shift;
	unsigned int _uint;
	unsigned long long _ulong;
	char lch='a', ch; /* do not write position 0 */
	int* position;
	int positionindex = 0;
	int i, lastposition = 0;

	int len, dlen = 0;
	char* field, *document = NULL;

	if (!PyArg_ParseTuple(args, "s#|s#", &field, &len, &document, &dlen)) return NULL;

	if (!zcompress (field, len, self->bzfld, 6)) return PyErr_NoMemory ();
	bwriteLong (self->bfdi, btell (self->bfda), 5);

	bwriteVInt (self->bfda, btell (self->bzfld));
	if (dlen) {
		/* prepare document buffer */
		bseek (self->bdoc, 0);
		bseek (self->bpos, 0);

		if (!(position = (int*) malloc (dlen * 2))) return PyErr_NoMemory ();

		/* word index */
		for (i=0; i< dlen; i++) {
			ch = document [i];
			if (!isunialnum (lch) && isunialnum (ch) && isunialnum (document [i+1])) {
				position [positionindex++] = i;
			}
			lch = ch;
		}
		/* last position */
		position [positionindex++] = dlen;

		/* position delta */
		for (i = 0; i < positionindex; i++) {
			bwriteVInt (self->bpos, position [i] - lastposition);
			lastposition = position [i];
		}
		free (position);

		/* position length */
		bwriteVInt (self->bdoc, positionindex);

		/* position skip */
		bwriteVInt (self->bdoc, btell (self->bpos));

		/* write position */
		if (bcommit (self->bpos, self->bdoc) == -1) {
			if (self->bpos->errcode == 1 || self->bdoc->errcode == 1) {goto memoryerror;}
			else if (self->bpos->errcode == 2 || self->bdoc->errcode == 2) {goto iowriteerror;}			
		}

		/* document */
		bwriteString (self->bdoc, document, dlen);
		if (!zcompress (self->bdoc->buffer, self->bdoc->position, self->bzdoc, 9)) return PyErr_NoMemory ();
		bwriteVInt (self->bfda, btell (self->bzdoc));
	}

	else {
		bwriteVInt (self->bfda, 0); /* postion length */
	}

	/* write fields */
	if (bcommit (self->bzfld, self->bfda) == -1) {
		if (self->bpos->errcode == 1 || self->bfda->errcode == 1) {goto memoryerror;}
		else if (self->bpos->errcode == 2 || self->bfda->errcode == 2) {goto iowriteerror;}		
	}


	/* write document */
	if (dlen) {
		if (bcommit (self->bzdoc, self->bfda) == -1) {
			if (self->bzdoc->errcode == 1 || self->bfda->errcode == 1) {goto memoryerror;}
			else if (self->bzdoc->errcode == 2 || self->bfda->errcode == 2) {goto iowriteerror;}			
		}
	}

	self->numdoc++;
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
Document_usage (Document *self, PyObject *args) {
	return PyLong_FromLong ((bsize (self->bdoc) + bsize (self->bpos) + bsize (self->bzfld) + bsize (self->bzdoc)));
}

static PyObject*
Document_merge (Document *self, PyObject *args)
{
	int _shift;
	unsigned int _uint;
	unsigned long long _ulong;
	unsigned char _uchar;
	int docid, seg;
	SMI* segment;
	int offset, flen, dlen;

	if (!PyArg_ParseTuple(args, "ii", &seg, &docid)) return NULL;

	segment = self->smis->smi [seg];

	/* skip deleted doc */
	if (segment->bits && segment->bits [docid >> 3] & (1 << (docid & 7))) {
		return PyLong_FromLong (0);
	}

	bwriteLong (self->bfdi, btell (self->bfda), 5);

	/* find offset from doc index */
	bseek (segment->bfdi, docid * 5 + 4);
	breadLong (segment->bfdi, offset, 5);
	/* seek offset */
	bseek (segment->bfda, (long) offset);

	/* string length */
	breadVInt (segment->bfda, flen);
	bwriteVInt (self->bfda, flen);
	breadVInt (segment->bfda, dlen);
	bwriteVInt (self->bfda, dlen);

	/* copy string data */
	if (bncopy (segment->bfda, self->bfda, flen) == -1) {
		if (segment->bfda->errcode == 1 || self->bfda->errcode == 1) {goto memoryerror;}
		else if (segment->bfda->errcode == 2 || self->bfda->errcode == 2) {goto ioreaderror;}		
	}

	if (dlen) {
		if (bncopy (segment->bfda, self->bfda, dlen) == -1) {
			if (segment->bfda->errcode == 1 || self->bfda->errcode == 1) {goto memoryerror;}
			else if (segment->bfda->errcode == 2 || self->bfda->errcode == 2) {goto ioreaderror;}			
		}
	}

	self->numdoc++;

	return PyLong_FromLong (1);

ioreaderror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

iowriteerror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

memoryerror:
	PyErr_NoMemory ();
	return NULL;
}

static PyObject*
Document_close (Document *self, PyObject *args)
{
	Document_destroy (self);
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
Document_commit (Document *self, PyObject *args)
{
	int _shift;
	unsigned int _uint;

	bseek (self->bfdi, 0);
	bwriteInt (self->bfdi, self->numdoc, 4);
	Py_INCREF (Py_None);
	return Py_None;

iowriteerror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

memoryerror:
	PyErr_NoMemory ();
	return NULL;
}


static int
Document_read_document (Memory* mem, int fdi, int fda, int docid)
{
	int _shift;
	unsigned char _uchar;
	long long offset;
	int flen, dlen;
	MSTORED* mfd;
	MTEMP* tmp;
	
	//mfd = mem->mfd;
	mfd = mem->mfd;
	tmp = mem->tmp;
	
	/* find offset from doc index */
	blink (mfd->bfdi, fdi, mem->mutex, docid * 5 + 4, 5);
	breadLong (mfd->bfdi, offset, 5);
	
	/* read data length */
	blink (mfd->bfda, fda, mem->mutex, (long) offset, 0);	
	breadVInt (mfd->bfda, flen);
	breadVInt (mfd->bfda, dlen);
	
	bseek (tmp->bxx2, 0);
	if (bextend (tmp->bxx2, flen) == -1) {
		goto memoryerror;
	}
	if (bncopy (mfd->bfda, tmp->bxx2, flen) == -1) {
		goto ioreaderror;
	}
	// bxx0 -> field
	if (!zdecompress (tmp->bxx2->buffer, tmp->bxx2->position, tmp->bxx0)) {
		goto memoryerror;
	}
	// bxx1 -> document
	bseek (tmp->bxx2, 0);	
	if (dlen) {		
		if (bextend (tmp->bxx2, dlen) == -1) {
			goto memoryerror;
		}
		if (bncopy (mfd->bfda, tmp->bxx2, dlen) == -1) {
			goto ioreaderror;
		}
		if (!zdecompress (tmp->bxx2->buffer, tmp->bxx2->position, tmp->bxx1)) {
			goto memoryerror;
		}		
	}
	return 0;

ioreaderror:
	return -1;
memoryerror:
	return -2;	
}


static int
Document_make_summary (Summary* suminfo, BFILE *dbuffer, BFILE*sbuffer, BFILE* pbuffer, int summary, TermMeta* terms, int termsize)
{
	int _shift;
	unsigned char _uchar;
	int tc, i, j, delta, match = 0;
	int *positions;
	int lastposition = 0, poscount, skip, metalen, start=0, end=0, next = 0;
	char* bpointer, *p, *t;
	int fblen, tlen;
	int numterm = 0, neof;
	int maxfound = 2;
	
	breadVInt (dbuffer, poscount);
	if (poscount == 0) {
		suminfo->buffer = NULL;
		suminfo->length = 0;			
		return 0;
	}
	
	breadVInt (dbuffer, skip);
	metalen = btell (dbuffer);
	bpointer = dbuffer->buffer + skip + metalen; /* starting document */

	bseek (sbuffer, 0);

	if (termsize) {
		/* build term array */
		if (termsize == 1) maxfound = 3;
		else if (termsize == 2) maxfound = 2;
		else maxfound = 1;
		
		fblen = (int) ((float) summary / (float) termsize / 2.0);
	
		if (fblen < 3) fblen = 5;
		
		/* positions */
		bseek (pbuffer, 0);
		if (bextend (pbuffer, poscount * 4 + 4) == -1) {
			return -1;
		}
				
		positions = (int*) pbuffer->buffer; /* for first position 0 */
		positions [0] = 0;
		for (i = 1; i <= poscount; i ++) {
			breadVInt (dbuffer, delta);
			positions [i] = lastposition + delta;
			lastposition = 	positions [i];
		}
	
		/* build summary */
		if (bextend (sbuffer, lastposition) == -1) {
			return -1;
		}
				
		for (i=0; i < poscount; i++) {
			neof = (poscount - 1) - i;
			for (tc = 0; tc < termsize; tc++) {
				p = bpointer + positions [i];
				t = terms [tc].term;
				tlen = terms [tc].length;
	
				for (j=0; j<tlen; j++) {
					match = 1;
					if (tolower (*p++) !=  *t++) {
						match = 0;
						break;
					}
				}
	
				/* exceptions: roof => roofs */
				if (match && neof && isunialnum (*p)) {
					match = 0;
				}
	
				if (match) {
					if (terms [tc].found >= maxfound && next < fblen) {
						next = 0;
						break;
					}
										
					terms [tc].found ++; /* set found */					
	
					if (next ==0) {
						start = i - fblen;
						if (start < 0) { start = 0; }
						else {bwriteString (sbuffer, "...", 3);}
	
						p = bpointer + positions [start];
						bwriteString (sbuffer, p, positions [i] - positions [start]);
						numterm += i -start;
					}
	
					p = bpointer + positions [i];
					bwriteString (sbuffer, "<b>", 3);
					bwriteString (sbuffer, p, tlen);
					bwriteString (sbuffer, "</b>", 4);
					p = bpointer + positions [i] + terms [tc].length;
					bwriteString (sbuffer, p, positions [i+1] - (positions [i] + tlen));
					numterm ++;
					next = fblen + 1;
					break;
				}
			}
	
			if (!match && next > 0 && i < poscount) {
				p = bpointer + positions [i];
				bwriteString (sbuffer, p, positions [i+1] - positions [i]);
				numterm ++;
			}
	
			if (next) next -= 1;
	
			/* early termination */
			if (numterm > summary) break;			
		}
	}
	
	if (!btell (sbuffer)) {
		lastposition = 0;
		bseek (dbuffer, metalen);
		bpointer = dbuffer->buffer + skip + metalen; /* starting document */

		for (i = 0; i < poscount; i ++) {
			breadVInt (dbuffer, delta);
			end = lastposition + delta;
			lastposition = 	end;
			if (i > summary) break;
		}
		
		if (poscount == i) {
			suminfo->buffer = bpointer;
			suminfo->length = end; // full doc
			return 0;
		}
		else {
			suminfo->buffer = bpointer;
			suminfo->length = end-1; // remove space or special char
			return 0;
		}
	}
	
	suminfo->buffer = sbuffer->buffer;
	suminfo->length = sbuffer->position;
	return 0;

iowriteerror:
	return -1;

ioreaderror:
	return -1;

memoryerror:
	return -2;
}

static PyObject*
Document_read (Document *self, PyObject *args)
{
	int docid;
	int summary = 0;
	PyObject* pyfield, *pydocument, *pyterms = NULL, *result, *pymem;
	Memory* mem;
	MTEMP* tmp;
	int res = 0;
	Summary suminfo;
	PyObject* o;
	TermMeta terms [100];
	int tc, termsize = 0, i = 0;
	char* s;
	
	if (!PyArg_ParseTuple(args, "Oi|iO", &pymem, &docid, &summary, &pyterms)) return NULL;
	mem = (Memory*) PyCObject_AsVoidPtr (pymem);
	tmp = mem->tmp;
	
	Py_BEGIN_ALLOW_THREADS
	// bxx0 -> field, bxx1 -> document
	res = Document_read_document (mem, self->fdi, self->fda, docid);
	Py_END_ALLOW_THREADS
	if (res < 0) goto error;
	pyfield = PyBytes_FromStringAndSize (tmp->bxx0->buffer, tmp->bxx0->position);

	if (summary && tmp->bxx2->position) { // if has zipdata
		if (pyterms) {
			termsize = (int) PyList_Size (pyterms);
			if (termsize > 100) termsize = 100;
			for (tc = 0; tc <termsize; tc++) {
				o = PyList_GetItem (pyterms, tc);

#if PY_MAJOR_VERSION >= 3
				s = PyUnicode_AsUTF8 (o);
				terms [tc].length = strlen (s);
#else	
				s = PyString_AsString (o);
				terms [tc].length = (int) PyString_Size (o);
#endif	
				terms [tc].found = 0;
				for (i=0; i < terms [tc].length; i++) {
					terms [tc].term [i] = tolower (*s++);
				}
			}
		}
		
		Py_BEGIN_ALLOW_THREADS
		// bxx1 -> document, bxx0, bxx2 -> temp buffer
		bseek (tmp->bxx1, 0);
		res = Document_make_summary (&suminfo, tmp->bxx1, tmp->bxx0, tmp->bxx2, summary, terms, termsize);
		Py_END_ALLOW_THREADS
		
		if (res < 0) {
			Py_DECREF (pyfield);
			goto error;
		}

		if (!suminfo.buffer)
			pydocument = PyUnicode_FromString ("");
		else {			
			pydocument = PyUnicode_FromStringAndSize (suminfo.buffer, suminfo.length);			
		}	
	}
			
	else {
		pydocument = PyUnicode_FromString ("");
	}

	result = Py_BuildValue ("OO", pyfield, pydocument);
	Py_DECREF (pyfield);
	Py_DECREF (pydocument);

	return result;

error:
	if (res == -1) {
		return PyErr_SetFromErrno (PyExc_IOError);
	}	
	return PyErr_NoMemory ();	
}



/****************************************************************
Module Definition
****************************************************************/

static PyMemberDef Document_members[] = {
    {"numdoc", T_INT, offsetof(Document, numdoc), 0, ""},
    {"index", T_INT, offsetof(Document, index), 0, ""},
    {NULL}
};

static PyMethodDef Document_methods[] = {
	{"read", (PyCFunction) Document_read, METH_VARARGS, ""},
	{"initialize", (PyCFunction) Document_initialize, METH_VARARGS, ""},
	{"write", (PyCFunction) Document_write, METH_VARARGS, ""},
	{"merge", (PyCFunction) Document_merge, METH_VARARGS, ""},
	{"close", (PyCFunction) Document_close, METH_VARARGS, ""},
	{"commit", (PyCFunction) Document_commit, METH_VARARGS, ""},
	{"setsmis", (PyCFunction) Document_setsmis, METH_VARARGS, ""},
	{"usage", (PyCFunction) Document_usage, METH_VARARGS, ""},
	{NULL}
};

PyTypeObject DocumentType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"core.Document",			 /*tp_name*/
	sizeof (Document),			 /*tp_basicsize*/
	0,						 /*tp_itemsize*/
	(destructor) Document_dealloc, /*tp_dealloc*/
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
	0, //(iternextfunc) Document_iternext,	   /* tp_iternext */
	Document_methods,			 /* tp_methods */
	Document_members,			 /* tp_members */
	0,						 /* tp_getset */
	0,						 /* tp_base */
	0,						 /* tp_dict */
	0,						 /* tp_descr_get */
	0,						 /* tp_descr_set */
	0,						 /* tp_dictoffset */
	(initproc) Document_init,	  /* tp_init */
	0,						 /* tp_alloc */
	Document_new,				 			/* tp_new */
};
