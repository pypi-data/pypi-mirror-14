#include "Python.h"
#include "core.h"
#include "structmember.h"
#include "index/index.h"
#include <stdio.h>
#include <math.h>


/****************************************************************
Module Memeber Definition
****************************************************************/

typedef struct {
	PyObject_HEAD
	int numdoc;
	int numfield;
	int fdno;
	int smp;
	BFILE *bsmp;
	BFILE *sorters [255];
	SMIS* smis;
	char mode;
} SortMap;


/****************************************************************
Shared Functions
****************************************************************/


/****************************************************************
Contructor / Destructor
****************************************************************/
static PyObject *
SortMap_new (PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	SortMap *self;
	self = (SortMap*)type -> tp_alloc(type, 0);	
	return (PyObject*) self;
}

static int
SortMap_init (SortMap *self, PyObject *args)
{
	int _shift;
	unsigned char _uchar;	
	int i;
	if (!PyArg_ParseTuple(args, "ic", &self->smp, &self->mode)) return -1;		
	
	self->numdoc = 0;
	self->numfield = 0;
	self->fdno = -1;
	self->bsmp = NULL;
	
	if (self->mode == 'w') {
		if (!(self->bsmp = bopen (self->smp, 'w', FILEBUFFER_LENGTH, 0))) {PyErr_NoMemory (); return -1;}
		//if (!(self->sorters [0] = (BFILE*) malloc (sizeof (BFILE*) * 255))) {PyErr_NoMemory (); return -1;}
		for (i = 0; i < 255; i++) {
			self->sorters [i] = NULL;
		}
	}
	
	else {
		if (!(self->bsmp = bopen (self->smp, 'r', FILEBUFFER_LENGTH, 0))) {PyErr_NoMemory (); return -1;}
		breadInt (self->bsmp, self->numdoc, 4);
		bclose (self->bsmp);
		self->bsmp = NULL;
	}
			
	return 0;

ioreaderror:
	PyErr_SetFromErrno (PyExc_IOError);
	return -1;
}

static void
SortMap_dealloc (SortMap* self)
{
	Py_TYPE(self)->tp_free ((PyObject*) self);
}


/****************************************************************
Module Methods
****************************************************************/

static PyObject*
SortMap_initialize (SortMap *self, PyObject *args)
{
	int _shift;
	unsigned int _uint;
	
	if (self->mode == 'w') {
		bwriteInt (self->bsmp, 0, 4);
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
SortMap_setsmis (SortMap *self, PyObject *args)
{
	PyObject* smis;
	if (!PyArg_ParseTuple(args, "O", &smis)) return NULL;	
	self->smis = (SMIS*) PyCObject_AsVoidPtr (smis);
	Py_INCREF (Py_None);
	return Py_None;
}


static PyObject* 
SortMap_close (SortMap *self, PyObject *args) 
{
	if (self->bsmp) bclose (self->bsmp);
	Py_INCREF (Py_None);
	return Py_None;
}

static int
SortMap_check (SortMap *self, int fdno) 
{	
	if (self->fdno == -1) {
		self->fdno = fdno;
		self->numdoc  = 1;
	} else if (fdno == self->fdno) {
		self->numdoc ++;
	}
		
	if (self->sorters [fdno] == NULL) {
		if (!(self->sorters [fdno] = bopen (-1, 'w', FILEBUFFER_LENGTH, 1))) return -1;
		self->numfield++;
		return 1;
	}
	
	return 0;
}
	
static PyObject*
SortMap_addInt (SortMap *self, PyObject *args) 
{
	int _shift;
	unsigned int _uint;	
	unsigned long long _ulong;	
	int fdno;	
	int value;
	int isnew;
	int size = 4;
	
	if (!PyArg_ParseTuple(args, "iii", &fdno, &value, &size)) return NULL;
	
	isnew = SortMap_check (self, fdno);	
	if (isnew == -1) return PyErr_NoMemory ();
	if (size <= 4) {
		bwriteInt (self->sorters [fdno], value, size);
	}	
	else {
		bwriteLong (self->sorters [fdno], value, size);
	}
	return PyLong_FromLong (isnew); /* mem size */

iowriteerror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

memoryerror:
	PyErr_NoMemory ();
	return NULL;
}

static PyObject*
SortMap_addIntList (SortMap *self, PyObject *args) 
{
	int _shift;
	unsigned int _uint;	
	unsigned long long _ulong;	
	int fdno;	
	PyObject* value;
	int isnew;
	int size = 4;
	Py_ssize_t eachsize;
	int i;
	
	if (!PyArg_ParseTuple(args, "iOi", &fdno, &value, &size)) return NULL;
	
	isnew = SortMap_check (self, fdno);	
	if (isnew == -1) return PyErr_NoMemory ();
	
	eachsize = size / PyList_Size (value);
	for (i = 0; i < PyList_Size (value); i++) {
		if (eachsize <= 4) {
			bwriteInt (self->sorters [fdno], (unsigned int) PyLong_AsLong (PyList_GetItem (value, i)), eachsize);
		} else {
			bwriteLong (self->sorters [fdno], (unsigned long long) PyLong_AsLongLong (PyList_GetItem (value, i)), eachsize);
		}
	}	
	return PyLong_FromLong (isnew); /* mem size */

iowriteerror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

memoryerror:
	PyErr_NoMemory ();
	return NULL;
}

static PyObject* 
SortMap_addNorm (SortMap *self, PyObject *args) 
{
	int _shift;
	int fdno;	
	int value;
	int isnew;
	char normfactor [1];
	
	if (!PyArg_ParseTuple(args, "ii", &fdno, &value)) return NULL;
	
	isnew = SortMap_check (self, fdno);	
	if (isnew == -1) return PyErr_NoMemory ();
		
	if (!value) 	normfactor [0] = 0;
	/* else			normfactor [0] = (char) ceil(255.0 / sqrt( (double)value)); */
	else {
		if (value<100) value = 100; /* Doug-fix 5/24/2014*/
		normfactor [0] = (char) ceil(2550.0 / sqrt( (double)value)); /* max val = 255 */
	}
	
	bwriteString (self->sorters [fdno], normfactor, 1);
	return PyLong_FromLong (isnew); /* mem size */

iowriteerror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

memoryerror:
	PyErr_NoMemory ();
	return NULL;
}

static PyObject* 
SortMap_addShortString (SortMap *self, PyObject *args)
{
	int _shift;
	int fdno;	
	PyObject* value;
	int size, i;
	Py_ssize_t len;
	char* str;
	char c;
	int isnew;
	long long sortkey;
	int readmax;
	unsigned int _uint;	
	unsigned long long _ulong;	
	
	if (!PyArg_ParseTuple(args, "iOi", &fdno, &value, &size)) return NULL;
	len = PyBytes_Size (value);
	str = PyBytes_AsString (value);
	isnew = SortMap_check (self, fdno);	
	if (isnew == -1) return PyErr_NoMemory ();
	
	if (size <= 2) readmax = size;
	else if (size <= 5) readmax = size + 1;
	else readmax = size + 2;	
	if (readmax > 9) readmax = 9;
	
	sortkey = 0;
	for (i = 0; i < (int) len; i++) {
		c = *str++;
		if (isalpha (c))
			sortkey += 46 - (c - 76);
		else if (isdigit (c))
			sortkey += 37 - (c - 47);
		else 
			continue;	
						
		sortkey <<= 6;		
		readmax--;
		if (readmax == 0) break;
	}
	
	for (i = 0; i < readmax; i++) {
		sortkey <<= 6;
	}	

	if (size <= 4) {
		bwriteInt (self->sorters [fdno], (int) sortkey, size);
	}	
	else {
		bwriteLong (self->sorters [fdno], sortkey, size);
	}
		
	return PyLong_FromLong (isnew); /* mem size */

iowriteerror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

memoryerror:
	PyErr_NoMemory ();
	return NULL;
}

static PyObject* 
SortMap_commit (SortMap *self) 
{
	int i;
	int _shift;	
	unsigned int _uint;
	
	for (i = 0; i < 255; i++) {
		if (self->sorters [i]) {		
			if (bcommit (self->sorters [i], self->bsmp) == -1) {
				if (self->sorters [i]->errcode == 1 || self->bsmp->errcode == 1) {goto memoryerror;}
				else if (self->sorters [i]->errcode == 2 || self->bsmp->errcode == 2) {goto iowriteerror;}				
			}
			bclose (self->sorters [i]);
		}			
	}
	
	bseek (self->bsmp, 0);
	bwriteInt (self->bsmp, self->numdoc, 4);	
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
SortMap_merge (SortMap *self, PyObject *args) 
{
	int fdno, docid;	
	int seg;
	int numdoc = 0;	
	//char temp [8];	 edited on 2014.12.21 
	//int _shift;	 edited on 2014.12.21 
	long pointer;
	int size = 4;
	SMI* segment = NULL;
	
	if (!PyArg_ParseTuple(args, "iili", &seg, &fdno, &pointer, &size)) return NULL;
	
	if (self->fdno == -1) self->fdno = fdno;
	
	segment = self->smis->smi [seg];
	bseek (segment->bsmp, pointer + 4);
	for (docid = 0; docid < segment->numdoc; docid++) {
		if (segment->bits && segment->bits [docid >> 3] & (1 << (docid & 7))) {			
			//breadString (segment->bsmp, temp, size); //edited on 2014.12.21 
			segment->bsmp->position += size;
			continue; /* deleted document, skip */
		}
		if (bncopy (segment->bsmp, self->bsmp, size) == -1) {
			if (segment->bsmp->errcode == 1 || self->bsmp->errcode == 1) {return PyErr_NoMemory ();}
			else if (segment->bsmp->errcode == 2 || self->bsmp->errcode == 2) {return PyErr_SetFromErrno (PyExc_IOError);}			
		}		
		numdoc ++;
	}
	
	/* counting docs */
	if (fdno == self->fdno) self->numdoc += numdoc;
	
	Py_INCREF (Py_None);	
	return Py_None;

//edited on 2014.12.21 
//ioreaderror:
//	PyErr_SetFromErrno (PyExc_IOError);
//	return NULL;		
}


static PyObject* 
SortMap_read (SortMap *self, PyObject *args) 
{
	PyObject* pymem;
	Memory* mem;
	int size;
	int max;
	long pointer;
	
	if (!PyArg_ParseTuple(args, "Oili", &pymem, &max, &pointer, &size)) return NULL;
	mem = (Memory*) PyCObject_AsVoidPtr (pymem);
	mem->msr->size = size;
	mem->msr->numdoc = self->numdoc;		
	setmax (mem->msr->bsmp, max);
	
	if (blink (mem->msr->bsmp, self->smp, mem->mutex, pointer + 4, 0) == -1) {
		if (mem->msr->bsmp->errcode == 1) {
			goto memoryerror;
		} else if (mem->msr->bsmp->errcode == 2) {			
			goto ioreaderror;				
		}		
	}
	btranslate (mem->msr->bsmp, pointer + 4);	
	
	Py_INCREF (Py_None);	
	return Py_None;
	
memoryerror:
	PyErr_NoMemory ();
	return NULL;

ioreaderror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;	
}


/****************************************************************
Module Definition
****************************************************************/

static PyMemberDef SortMap_members[] = {
    {"numdoc", T_INT, offsetof(SortMap, numdoc), 0, ""},
    {"numfield", T_INT, offsetof(SortMap, numfield), 0, ""},
    {NULL}
};

static PyMethodDef SortMap_methods[] = {
	{"merge", (PyCFunction) SortMap_merge, METH_VARARGS, ""},
	{"addInt", (PyCFunction) SortMap_addInt, METH_VARARGS, ""},	
	{"addIntList", (PyCFunction) SortMap_addIntList, METH_VARARGS, ""},		
	{"addNorm", (PyCFunction) SortMap_addNorm, METH_VARARGS, ""},	
	{"addShortString", (PyCFunction) SortMap_addShortString, METH_VARARGS, ""},		
	{"read", (PyCFunction) SortMap_read, METH_VARARGS, ""},	
	{"close", (PyCFunction) SortMap_close, METH_VARARGS, ""},
	{"commit", (PyCFunction) SortMap_commit, METH_VARARGS, ""},
	{"setsmis", (PyCFunction) SortMap_setsmis, METH_VARARGS, ""},
	{"initialize", (PyCFunction) SortMap_initialize, METH_VARARGS, ""},	
	{NULL}
};

PyTypeObject SortMapType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"core.SortMap",			 /*tp_name*/
	sizeof (SortMap),			 /*tp_basicsize*/
	0,						 /*tp_itemsize*/
	(destructor) SortMap_dealloc, /*tp_dealloc*/
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
	0, //(iternextfunc) SortMap_iternext,	   /* tp_iternext */
	SortMap_methods,			 /* tp_methods */
	SortMap_members,			 /* tp_members */
	0,						 /* tp_getset */
	0,						 /* tp_base */
	0,						 /* tp_dict */
	0,						 /* tp_descr_get */
	0,						 /* tp_descr_set */
	0,						 /* tp_dictoffset */
	(initproc) SortMap_init,	  /* tp_init */
	0,						 /* tp_alloc */
	SortMap_new,				 			/* tp_new */
};




