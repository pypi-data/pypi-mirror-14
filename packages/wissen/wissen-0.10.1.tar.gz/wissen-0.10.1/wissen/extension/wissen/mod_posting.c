#include "Python.h"
#include "core.h"
#include "structmember.h"
#include "index/index.h"
#include <stdio.h>

/****************************************************************
Module Memeber Definition
****************************************************************/

typedef struct {
	int lastFrqPointer;	
	int lastPrxPointer;
	int lastDocId;
	BFILE* bfile;
} SKIP;

typedef struct {
	PyObject_HEAD
	int frq;
	int prx;
	char mode;		
	SMIS* smis;
	SKIP *skipBuffer;
	BFILE* bfrq;
	BFILE* bprx;
} Posting;


/****************************************************************
Shared Functions
****************************************************************/


/****************************************************************
Contructor / Destructor
****************************************************************/
static PyObject *
Posting_new (PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	Posting *self;
	self = (Posting*)type -> tp_alloc(type, 0);	
	return (PyObject*) self;
}

static void
Posting_destroy (Posting *self) {
	if (self->bfrq) bclose (self->bfrq);
	if (self->bprx) bclose (self->bprx);
	if (self->skipBuffer) {
		if (self->skipBuffer->bfile) bclose (self->skipBuffer->bfile);
		free (self->skipBuffer);
	}	
}
	
	
static int
Posting_init (Posting *self, PyObject *args)
{
	if (!PyArg_ParseTuple(args, "ii|c", &self->frq, &self->prx, &self->mode)) return -1;
	
	self->bfrq = NULL;
	self->bprx = NULL;
	self->skipBuffer = NULL;
	
	if (self->mode == 'w') {
		if (!(self->bfrq = bopen (self->frq, 'w', FILEBUFFER_LENGTH, 0))) goto fail;
		if (!(self->bprx = bopen (self->prx, 'w', FILEBUFFER_LENGTH, 0))) goto fail;
		if (!(self->skipBuffer = malloc (sizeof (SKIP)))) goto fail;
		
		self->skipBuffer->bfile = NULL;
		if (!(self->skipBuffer->bfile = bopen (-1, 'w', FILEBUFFER_LENGTH, 1))) goto fail;
		self->skipBuffer->lastFrqPointer = 0;
		self->skipBuffer->lastPrxPointer = 0;
		self->skipBuffer->lastDocId = 0;
	}
	
	return 0;
	
fail:
	Posting_destroy (self);
	PyErr_NoMemory (); 
	return -1;		
}

static void
Posting_dealloc (Posting* self)
{
	Py_TYPE(self)->tp_free ((PyObject*) self);
}


/****************************************************************
Module Methods
****************************************************************/

static PyObject*
Posting_initialize (Posting* self)
{
	Py_INCREF (Py_None);
	return Py_None;
}


static PyObject*
Posting_commit (Posting* self)
{
	if (bcommit (self->skipBuffer->bfile, self->bfrq) == -1) {
		if (self->skipBuffer->bfile->errcode == 1 || self->bfrq->errcode == 1) {return PyErr_NoMemory ();}
		else if (self->skipBuffer->bfile->errcode == 2 || self->bfrq->errcode == 2) {return PyErr_SetFromErrno (PyExc_IOError);}		
	}
	
	self->skipBuffer->lastFrqPointer = btell (self->bfrq);
	self->skipBuffer->lastPrxPointer = btell (self->bprx);
	self->skipBuffer->lastDocId = 0;
		
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
Posting_tell (Posting* self)
{
	return Py_BuildValue ("ll", btell (self->bfrq), btell (self->bprx));
}

static PyObject*
Posting_close (Posting* self)
{
	Posting_destroy (self);
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
Posting_writeSkip (Posting *self, int docid)
{
	unsigned int _uint;
	//printf ("docid: %d docdelta:%d\n",  docid, docid - self->skipBuffer->lastDocId);
	bwriteVInt (self->skipBuffer->bfile, docid - self->skipBuffer->lastDocId);
	bwriteVInt (self->skipBuffer->bfile, btell (self->bfrq) - self->skipBuffer->lastFrqPointer);
	bwriteVInt (self->skipBuffer->bfile, btell (self->bprx) - self->skipBuffer->lastPrxPointer);
	
	self->skipBuffer->lastDocId = docid;
	self->skipBuffer->lastFrqPointer = btell (self->bfrq);
	self->skipBuffer->lastPrxPointer = btell (self->bprx);
	
	Py_INCREF (Py_None);
	return Py_None;

memoryerror:
	PyErr_NoMemory ();
	return NULL;
	
iowriteerror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;		
}

static PyObject*
Posting_write (Posting *self, PyObject *args)
{
	unsigned int _uint;
	
	/* for PyList */
	int i;
	int docid, freq;	
	
	/* for PyCObject */
	recType* rec;
	
	int docdelta, df = 0;
	PyObject *pyposting;
	int last_docid = 0;
	int last_prox = 0;
	
	short int *prox;
	
	/* for skip delta */	
	if (!PyArg_ParseTuple(args, "O", &pyposting)) return NULL;
	
	rec = (recType*) PyCObject_AsVoidPtr (pyposting);
	while (rec) {
		docid = rec->docid; 
		freq = rec->tf;
		prox = rec->prox;
		
		docdelta = docid - last_docid; //delta
		last_docid = docid;
		
		docdelta <<= 1; /* docdelta x 2 */
		if (freq == 1) {
			docdelta |= 1; /* docdelta + 1 */
			bwriteVInt(self->bfrq, docdelta);
		}
		else {
			bwriteVInt(self->bfrq, docdelta);
			bwriteVInt(self->bfrq, freq);
		}
		
		if (prox) {
			last_prox = 0;
			for (i = 0; i < freq; i++) {								
				if (i == 0) {
					bwriteVInt (self->bprx, prox [i]);
				}	
				else {
					/* -1 compression taking d-gaps document number gaps */
					bwriteVInt (self->bprx, prox [i] - last_prox - 1);
				}	
				last_prox = prox [i];
			}			
		}
		
		rec = rec->next;
		
		df ++;
		if (df % SKIP_INTERVAL == 0) {
			Posting_writeSkip (self, docid);
		}	
	}
	
	return Py_BuildValue ("ill", df, btell (self->bfrq), btell (self->bprx));

iowriteerror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

memoryerror:
	PyErr_NoMemory ();
	return NULL;
		
}

static PyObject*
Posting_setsmis (Posting *self, PyObject *args)
{
	PyObject* smis;
	if (!PyArg_ParseTuple(args, "O", &smis)) return NULL;	
	self->smis = (SMIS*) PyCObject_AsVoidPtr (smis);
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
Posting_merge (Posting *self, PyObject *args)
{
	unsigned char _uchar;	
	unsigned int _uint;	
	int _shift;
	
	/* args */
	int seg;
	long doff, poff;
	int df, tdf = 0, plen;
	
	/* for reader */
	int rd_last_docid = 0;
	
	/* for writer */
	int prox, docdelta, docid, freq, deleted, last_docid = 0;
	
	/* buffred reading */
	int j = 0, k = 0;
	SMI* segment;
	
	if (!PyArg_ParseTuple(args, "iillii|i", &seg, &df, &doff, &poff, &plen, &tdf, &last_docid)) return NULL;
	/* pointer for current segment */
	segment = self->smis->smi[seg];
	/* set to offset */
	bseek (segment->bfrq, doff);
	if (plen && poff > -1) bseek (segment->bprx, poff);		
	
	for (k = 0; k < df; k++) {		
		breadVInt (segment->bfrq, docdelta);
		/* get freq: if docdelta is odd number then freq is `1` */
		if (docdelta & 1) {
			freq = 1;
		} else {
			//printf ("DF: %d, reading freq, why?\n", df);
			breadVInt (segment->bfrq, freq);		
		}
		
		docdelta >>= 1; /* real docdelta: / 2 */		
		docid = docdelta + rd_last_docid;
		/* save reader's last docid */
		rd_last_docid = docid;
		
		/* check deleted and rebuild docid */
		if (segment->docmap) {
			deleted = segment->docmap [docid];
			if (deleted == -1) {
				/* drop rpox info */
				 if (plen) {
					/* skip read deleted doc's position */
					for (j = 0; j < freq; j++) {
						breadVInt (segment->bprx, prox);
					}
				}
				continue;
			}
			/* else, re-numbering docId */
			docid += self->smis->smi [seg]->base - deleted;						
		}
		
		else {
			docid += self->smis->smi [seg]->base;						
		}
		
		docdelta = docid - last_docid; //delta
		last_docid = docid;
		
		docdelta <<= 1; /* x2 */
		if (freq == 1) {
			docdelta |= 1; /* +1 */
			bwriteVInt (self->bfrq, docdelta);
		}						
		else {
			bwriteVInt (self->bfrq, docdelta);
			bwriteVInt (self->bfrq, freq);
		}			
		
		if (plen) {
			for (j = 0; j < freq; j++) {					
				breadVInt (segment->bprx, prox);
				bwriteVInt (self->bprx, prox);
			}
		}
		
		tdf ++; /* increase df value */		
		if (tdf % SKIP_INTERVAL == 0) {
			Posting_writeSkip (self, docid);
		}
	}
	
	return Py_BuildValue ("illi", tdf, btell (self->bfrq), btell (self->bprx), last_docid);

iowriteerror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

ioreaderror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

memoryerror:
	PyErr_NoMemory ();
	return NULL;
}


static PyObject*
Posting_read (Posting *self, PyObject *args)
{
	int df;
	int skip, plen, getprox = 0, zoff = -1, zlen = -1;
	long doff, poff;
	long odoff, opoff;
	int roff, coff, xoff, i, ic;
	int docdelta, proxdelta;
	int freq;
	int freqPointerDelta, proxPointerDelta;
	int readprox = 0;
	int readToFreq, readToProx;
	unsigned char _uchar;
	int _shift;
	
	PyObject* pymem;
	Memory* mem;
	MPOSTING* mpt;
	
	if (!PyArg_ParseTuple(args, "Oillii|iii",
		&pymem, &df, &doff, &poff, &skip, &plen, &zoff, &zlen, &getprox
	)) return NULL;
	mem = (Memory*) PyCObject_AsVoidPtr (pymem);
	odoff = doff;
	opoff = poff;
	readToFreq = doff;
	readToProx = poff;
	
	mpt = mem->mpt;
	mpt->df = df;
	mpt->dc = 0;
	mpt->lastdocid = 0;
	mpt->hasprox = 0;
	mpt->hasextra = 0;
	
	/* overflow, return immediately */
	if (zoff > df) goto end;
	
	if (getprox && plen) {
		readprox = 1;		
		mpt->hasprox = 1;
	}
	
	/* generalize */
	if (zoff == -1) zoff = 0;
	if (zlen == -1) zlen = df;
	if ((zoff + zlen) > df) zlen = df - zoff;
	
	/* reversing offset */
	roff = df - zoff - zlen;
	mpt->dc = zlen;
	
	coff = 0;
	xoff = 0;	
	
	if (zlen == df) { /* entire reading */
		xoff = df;
		readToFreq = odoff + skip;
		readToProx = opoff + plen;
	}
	
	/* big jump to roff step SKIP_INTERVAL (= 16) */	
	else if ((int) (df / SKIP_INTERVAL)) {
		readToFreq = doff;
		readToProx = poff;		
		
		if (blink (mpt->freq, self->frq, mem->mutex, doff + skip, (int) (df / SKIP_INTERVAL) * 12) == -1) {
			if (mpt->freq->errcode == 1) {
				goto memoryerror;
			} else if (mpt->freq->errcode == 2) {
				goto ioreaderror;
			}			
		}
							
		for (i = (int) (df / SKIP_INTERVAL); i-- ;) {			
			breadVInt (mpt->freq, docdelta);
			breadVInt (mpt->freq, freqPointerDelta);
			breadVInt (mpt->freq, proxPointerDelta);
			
			readToFreq += freqPointerDelta;
			readToProx += proxPointerDelta;
			xoff += SKIP_INTERVAL;
				
			if (xoff < roff) {
				mpt->lastdocid += docdelta;
				coff = xoff;
				doff = readToFreq;
				if (readprox) poff = readToProx;
			}
			if (xoff > roff + zlen) break; /* satified all data */
		}		
	}
	
	/* read to last */
	if (!xoff || xoff <= roff + zlen) {
		readToFreq = odoff + skip;
		readToProx = opoff + plen;
	}
	
	/* small jump skip docid step 1 */
	if (coff < roff) {
		if (blink (mpt->freq, self->frq, mem->mutex, doff, MIN_IOBUFFER) == -1) {
			if (mpt->freq->errcode == 1) {
				goto memoryerror;
			} else if (mpt->freq->errcode == 2) {			
				goto ioreaderror;
			}			
		}
		if (readprox) {
			if (blink (mpt->prox, self->prx, mem->mutex, poff, MIN_IOBUFFER) == -1) {
				if (mpt->prox->errcode == 1) {
					goto memoryerror;
				} else if (mpt->prox->errcode == 2) {			
					goto ioreaderror;
				}				
			}
		}	
				
		/* skip until roff */
		for (ic = roff-coff; ic--;) {
			//printf ("skipping: coff=%d roff=%d\n", coff, roff);
			breadVInt (mpt->freq, docdelta);
			if (docdelta & 1) freq = 1;
			else {
				breadVInt (mpt->freq, freq);
			}
			docdelta >>= 1;
			mpt->lastdocid += docdelta;		
			if (readprox) {
				/* skip prox data */
				for (i = 0; i < freq; i++) {
					breadVInt (mpt->prox, proxdelta);
				}
			}
		}
		
		doff = btell (mpt->freq);
		
		if (readprox) {
			poff = btell (mpt->prox);
		}		
	}
	
	/* set skip information */
	if ((int) (df / SKIP_INTERVAL)) {
		if (blink (mpt->skip->skip, self->frq, mem->mutex, odoff + skip, (int) (df / SKIP_INTERVAL) * 12) == -1) {
			if (mpt->skip->skip->errcode == 1) {
				goto memoryerror;
			} else if (mpt->skip->skip->errcode == 2) {			
				goto ioreaderror;		
			}
		}
		mpt->skip->needle = 0;
		mpt->skip->docid = 0;
		mpt->skip->freqposition = odoff;
		mpt->skip->proxposition = opoff;
		
		breadVInt (mpt->skip->skip, docdelta);
		breadVInt (mpt->skip->skip, freqPointerDelta);
		breadVInt (mpt->skip->skip, proxPointerDelta);
		
		mpt->skip->nextdocid = docdelta;
		mpt->skip->nextfreqposition = freqPointerDelta + odoff;
		mpt->skip->nextproxposition = proxPointerDelta + opoff;
		mpt->skip->skipnum = df / SKIP_INTERVAL - 1;		
	}
	
	else {
		mpt->skip->skipnum = 0;
	}	
	
	if (blink (mpt->freq, self->frq, mem->mutex, doff, readToFreq - doff) == -1) {
		if (mpt->freq->errcode == 1) {
			goto memoryerror;
		} else if (mpt->freq->errcode == 2) {			
			goto ioreaderror;
		}
	}
			
	if (readprox) {
		if (blink (mpt->prox, self->prx, mem->mutex, poff, readToProx - poff) == -1) {
			if (mpt->prox->errcode == 1) {
				goto memoryerror;
			} else if (mpt->prox->errcode == 2) {
				goto ioreaderror;
			}			
		}	
	}	

end:
	return Py_BuildValue ("i", mpt->dc); /* confidecial posting document count */		

ioreaderror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

memoryerror:
	PyErr_NoMemory ();
	return NULL;
}



/****************************************************************
Module Definition
****************************************************************/

static PyMemberDef Posting_members[] = {
	//{"mode", T_CHAR, offsetof(Posting, mode), 0, ""},
	{NULL}
};

static PyMethodDef Posting_methods[] = {
	{"close", (PyCFunction) Posting_close, METH_VARARGS, ""},	
	{"tell", (PyCFunction) Posting_tell, METH_VARARGS, ""},	
	{"write", (PyCFunction) Posting_write, METH_VARARGS, ""},			
	{"read", (PyCFunction) Posting_read, METH_VARARGS, ""},	
	{"merge", (PyCFunction) Posting_merge, METH_VARARGS, ""},		
	{"commit", (PyCFunction) Posting_commit, METH_VARARGS, ""},		
	{"setsmis", (PyCFunction) Posting_setsmis, METH_VARARGS, ""},
	{"initialize", (PyCFunction) Posting_initialize, METH_VARARGS, ""},
	{NULL}
};

PyTypeObject PostingType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"core.Posting",			 /*tp_name*/
	sizeof (Posting),			 /*tp_basicsize*/
	0,						 /*tp_itemsize*/
	(destructor) Posting_dealloc, /*tp_dealloc*/
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
	0, //(iternextfunc) Posting_iternext,	   /* tp_iternext */
	Posting_methods,			 /* tp_methods */
	Posting_members,			 /* tp_members */
	0,						 /* tp_getset */
	0,						 /* tp_base */
	0,						 /* tp_dict */
	0,						 /* tp_descr_get */
	0,						 /* tp_descr_set */
	0,						 /* tp_dictoffset */
	(initproc) Posting_init,	  /* tp_init */
	0,						 /* tp_alloc */
	Posting_new,				 			/* tp_new */
};


