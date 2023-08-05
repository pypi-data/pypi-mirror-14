#include "Python.h"
#include "core.h"
#include "structmember.h"
#include "index/index.h"
#include <stdio.h>


/****************************************************************
Module Memeber Definition
****************************************************************/
typedef struct {
	PyObject_HEAD
	SMIS smis;
} MergeInfo;

/****************************************************************
Shared Functions
****************************************************************/


/****************************************************************
Contructor / Destructor
****************************************************************/
static PyObject *
MergeInfo_new (PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	MergeInfo *self;
	self = (MergeInfo*)type -> tp_alloc(type, 0);
	return (PyObject*) self;
}

static int
MergeInfo_init (MergeInfo *self, PyObject *args)
{
	// reset segment merge infos
	self->smis.segcount = 0;
	self->smis.base = 0;

	return 0;
}

static void
MergeInfo_dealloc (MergeInfo* self)
{
	Py_TYPE(self)->tp_free ((PyObject*) self);
}


/****************************************************************
Module Methods
****************************************************************/

static PyObject*
MergeInfo_close (MergeInfo* self)
{
	int i;
	for (i=0; i < self->smis.segcount; i++) {
		if (self->smis.smi[i]->docmap) {
			free (self->smis.smi[i]->docmap);
		}
		
		bclose (self->smis.smi[i]->bfrq);
		bclose (self->smis.smi[i]->bprx);
		bclose (self->smis.smi[i]->bfdi);
		bclose (self->smis.smi[i]->bfda);
		bclose (self->smis.smi[i]->bsmp);
		free (self->smis.smi[i]);
	}
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
MergeInfo_get (MergeInfo* self)
{
	return PyCObject_FromVoidPtr (&(self->smis), NULL);
}

static PyObject*
MergeInfo_add (MergeInfo *self, PyObject *args)
{
	int i, numdoc, deleted, seg;
	int frq, prx, fdi, fda, smp;
	PyObject* pybitvector = Py_None;
	unsigned char* bitvector = NULL;

	if (!PyArg_ParseTuple(args, "iiiiii|O",
		&numdoc, &frq, &prx, &fdi, &fda, &smp, &pybitvector)
	) return NULL;

	/* smis array is maximum 100 */
	seg = self->smis.segcount++;
	if (seg > 99) return NULL;

	/* memory allocation */
	if (!(self->smis.smi [seg] = (SMI*) malloc (sizeof (SMI)))) return PyErr_NoMemory ();
	self->smis.smi [seg]->numdoc = numdoc;

	if (!(self->smis.smi [seg]->bprx = bopen (prx, 'r', 4096, 0))) return NULL;
	if (!(self->smis.smi [seg]->bfrq = bopen  (frq, 'r', 4096, 0))) return NULL;
	if (!(self->smis.smi [seg]->bfdi = bopen  (fdi, 'r', 4096, 0))) return NULL;
	if (!(self->smis.smi [seg]->bfda = bopen  (fda, 'r', 4096, 0))) return NULL;
	if (!(self->smis.smi [seg]->bsmp = bopen  (smp, 'r', 4096, 0))) return NULL;

	/* set docid deleted mark and reduce value */
	deleted = 0;
	if (!pybitvector || pybitvector == Py_None) {
		/* no deleted document. assume docid delta is all `0` */
		self->smis.smi [seg]->bits = NULL;
		self->smis.smi [seg]->docmap = NULL;
	}

	else {
		bitvector = (unsigned char*) PyCObject_AsVoidPtr (pybitvector);
		self->smis.smi [seg]->bits = bitvector;
		if (!(self->smis.smi [seg]->docmap = (int*) malloc (sizeof (int) * numdoc))) return PyErr_NoMemory ();

		if (bitvector) {
			for (i = 0; i < numdoc; i++) {
				if (bitvector [i >> 3] & (1 << (i & 7))) {
					// marking deleted document to -1
					self->smis.smi[seg]->docmap [i] = -1;
					deleted ++;
				}
				else {
					/* accumulated deleted document count */
					/* then append posting each docid reduce with this count */
					/* for rebuilding docid continuous */
					self->smis.smi[seg]->docmap [i] = deleted;
				}
			}
		}
	}

	/* set current segment's base docid */
	self->smis.smi [seg]->base = self->smis.base;

	/* set next segment's base docid  */
	self->smis.base += numdoc - deleted;

	Py_INCREF (Py_None);
	return Py_None;
}

/****************************************************************
Module Definition
****************************************************************/

static PyMemberDef MergeInfo_members[] = {
    {NULL}
};

static PyMethodDef MergeInfo_methods[] = {
	{"add", (PyCFunction) MergeInfo_add, METH_VARARGS, ""},
	{"get", (PyCFunction) MergeInfo_get, METH_VARARGS, ""},
	{"close", (PyCFunction) MergeInfo_close, METH_VARARGS, ""},
	{NULL}
};

PyTypeObject MergeInfoType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"core.MergeInfo",			 /*tp_name*/
	sizeof (MergeInfo),			 /*tp_basicsize*/
	0,						 /*tp_itemsize*/
	(destructor) MergeInfo_dealloc, /*tp_dealloc*/
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
	0, //(iternextfunc) MergeInfo_iternext,	   /* tp_iternext */
	MergeInfo_methods,			 /* tp_methods */
	MergeInfo_members,			 /* tp_members */
	0,						 /* tp_getset */
	0,						 /* tp_base */
	0,						 /* tp_dict */
	0,						 /* tp_descr_get */
	0,						 /* tp_descr_set */
	0,						 /* tp_dictoffset */
	(initproc) MergeInfo_init,	  /* tp_init */
	0,						 /* tp_alloc */
	MergeInfo_new,				 			/* tp_new */
};
