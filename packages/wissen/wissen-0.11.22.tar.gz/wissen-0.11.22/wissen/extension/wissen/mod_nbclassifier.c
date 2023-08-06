#include "Python.h"
#include "core.h"
#include "structmember.h"
#include "index/index.h"
#include <stdio.h>


/****************************************************************
Module Memeber Definition
****************************************************************/
typedef struct {
	BFILE *bfile;
	char type;
} SORTER;

typedef struct {
	PyObject_HEAD
	int first_field;
	int numdoc;
	int numfield;
	FILE *smp;
	BFILE *bsmp;	
	SORTER *sorters [255];
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
	unsigned int _uint;
	int i;
	char mode = 'r';
	if (!PyArg_ParseTuple(args, "ic", &self->smp, &self->mode)) return -1;		
	
	self->numdoc = 0;
	self->numfield = 0;
	self->first_field = -1;
		
	if (self->mode == 'r' || self->mode == 'm') {
		self->bsmp = bopen (self->smp, 'r', 8, 0);
		breadInt (self->sbmp, self->numdoc, 4);
		breadInt (self->bsmp, self->numfield, 1);		
		bclose (self->bsmp);
	}
	
	else {
		if (!(self->bsmp = bopen (self->smp, 'w', FILEBUFFER_LENGTH, 0))) {PyErr_NoMemory (); return -1;}
		bwriteInt (self->bsmp, 0, 4);
		bwriteInt (self->bsmp, 0, 1);		
		if (!(self->sorters [0] = (SORTER*) malloc (sizeof (SORTER*) * 255))) {PyErr_NoMemory (); return -1;}
		for (i = 0; i < 255; i++) {
			self->sorters [i] = NULL;
		}
	}		
	return 0;
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
	if (self->mode == 'w') {
		bclose (self->bsmp);
	}
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
SortMap_check (SortMap *self, int fdno, int value, char type) 
{	
	if (self->first_field == -1) {
		self->first_field = fdno;
		self->numdoc = 1;
	} else if (self->first_field == fdno) {
		self->numdoc ++;
	}
	
	if (self->sorters [fdno] == NULL) {
		if (!(self->sorters [fdno] = (SORTER*) malloc (sizeof (SORTER)))) return 0;		
		if (!(self->sorters [fdno]->bfile = bopen (NULL, 'w', FILEBUFFER_LENGTH, 1))) return 0;
		self->sorters [fdno]->type = type;
		self->numfield++;
		return FILEBUFFER_LENGTH;
	}
	return 1;
}
	
static PyObject* 
SortMap_addInt (SortMap *self, PyObject *args) 
{
	int _shift;
	unsigned int _uint;	
	int fdno;	
	int value;
	int isnew;
	
	if (!PyArg_ParseTuple(args, "ii", &fdno, &value)) return NULL;
	
	isnew = SortMap_check (self, fdno, value, 'i');	
	if (!isnew) return PyErr_NoMemory ();
	bwriteInt (self->sorters [fdno]->bfile, value, 4);
	return PyLong_FromLong (isnew); /* mem size */
}

static PyObject* 
SortMap_commit (SortMap *self) 
{
	int i;
	int _shift;	
	unsigned int _uint;
	
	for (i = 0; i < 255; i++) {
		if (self->sorters [i]) {
			if (bcommit (self->sorters [i]->bfile, self->bsmp) == -1) {
				if (self->sorters [i]->bfile->errcode == 1 || self->bsmp->errcode == 1) {PyErr_NoMemory ();}
				else if (self->sorters [i]->bfile->errcode == 2 || self->bsmp->errcode == 2) {PyErr_SetFromErrno (PyExc_IOError);}
				free (self->sorters);
				return NULL;
			}			
			bclose (self->sorters [i]->bfile);
		}
	}
	
	free (self->sorters);	
	bseek (self->bsmp, 0);
	bwriteInt (self->bsmp, self->numdoc, 4);
	bwriteInt (self->bsmp, self->numfield, 1);
	
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject* 
SortMap_merge (SortMap *self, PyObject *args) 
{
	int fdindex, docid;	
	int seg;
	int tnumdoc = 0;	
	char temp [4];	
	int _shift;	
	SMI* segment = NULL;
	
	if (!PyArg_ParseTuple(args, "ii", &seg, &fdindex)) return NULL;
	
	segment = self->smis->smi [seg];
	bseek (segment->bsmp, fdindex * segment->numdoc * 4 + 5);
	for (docid = 0; docid < segment->numdoc; docid++) {
		breadString (segment->bsmp, temp, 4);
		if (segment->bits && segment->bits [docid >> 3] & (1 << (docid & 7))) {			
			breadString (segment->bsmp, temp, 4); 
			continue; /* deleted document, skip */
		}
		if (bncopy (segment->bsmp, self->bsmp, 4) == -1) {
			if (segment->bsmp->errcode == 1 || self->bsmp->errcode == 1) {PyErr_NoMemory ();}
			else if (segment->bsmp->errcode == 2 || self->bsmp->errcode == 2) {PyErr_SetFromErrno (PyExc_IOError);}
			return NULL;	
		}
		tnumdoc ++;
	}
	
	/* counting docs */
	if (fdindex == 0) self->numdoc += tnumdoc;	
	
	/* counting fields */	
	if (fdindex > self->numfield - 1) self->numfield = fdindex + 1; /* get max sort filed index + 1 */	
		
	Py_INCREF (Py_None);	
	return Py_None;	
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
	{"close", (PyCFunction) SortMap_close, METH_VARARGS, ""},
	{"commit", (PyCFunction) SortMap_commit, METH_VARARGS, ""},
	{"setsmis", (PyCFunction) SortMap_setsmis, METH_VARARGS, ""},
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




