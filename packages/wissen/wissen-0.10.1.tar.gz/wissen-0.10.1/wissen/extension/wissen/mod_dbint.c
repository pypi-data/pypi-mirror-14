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
	int fdb;
	char mode;
	BFILE* bfdb;
} DBInt;


/****************************************************************
Shared Functions
****************************************************************/


/****************************************************************
Contructor / Destructor
****************************************************************/
static PyObject *
DBInt_new (PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	DBInt *self;
	self = (DBInt*)type -> tp_alloc(type, 0);
	return (PyObject*) self;
}

static int
DBInt_init (DBInt *self, PyObject *args)
{
	if (!PyArg_ParseTuple(args, "i|c", &self->fdb, &self->mode)) return -1;

	if (self->mode == 'w') {
		if (!(self->bfdb = bopen (self->fdb, 'w', FILEBUFFER_LENGTH, 0))) return -1;
	}
	
	return 0;
}

static void
DBInt_dealloc (DBInt* self)
{
	Py_TYPE(self)->tp_free ((PyObject*) self);
}


/****************************************************************
Module Methods
****************************************************************/
static PyObject*
DBInt_initialize (DBInt* self)
{
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
DBInt_commit (DBInt* self)
{
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
DBInt_tell (DBInt* self)
{
	return Py_BuildValue ("l", btell (self->bfdb));
}

static PyObject*
DBInt_close (DBInt* self)
{
	if (self->mode == 'w') {
		bclose (self->bfdb);
	}	
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
DBInt_write (DBInt *self, PyObject *args)
{
	unsigned int _uint;
	int i, j, ident, first;
	
	int identdelta, df = 0;
	PyObject *pyposting, *o;
	int last_ident = 0;
	int haskey = 0, ignore_when_firstzero = 1;

	if (!PyArg_ParseTuple(args, "O|ii", &pyposting, &haskey, &ignore_when_firstzero)) return NULL;

	for (i = 0; i < PyList_Size (pyposting); i++) {
		o = PyList_GetItem (pyposting, i);
		if (haskey) {
			ident = (int) PyLong_AsLong (PyTuple_GetItem (o, 0));
			j = 1;
		}
		else {
			ident = i;
			j = 0;
		}

		first = (int) PyLong_AsLong (PyTuple_GetItem (o, j));
		if (!ignore_when_firstzero || first) {
			identdelta = ident - last_ident;
			bwriteVInt (self->bfdb, identdelta);
			last_ident = ident;
			bwriteVInt (self->bfdb, first);
			j++;

			for  (; j < PyTuple_Size (o); j++) {
				bwriteVInt (self->bfdb, (int) PyLong_AsLong (PyTuple_GetItem (o, j)));
			}
			df ++;
		}
	}
	return Py_BuildValue ("il", df, btell (self->bfdb));

iowriteerror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

memoryerror:
	PyErr_NoMemory ();
	return NULL;
}

static PyObject*
DBInt_read (DBInt *self, PyObject *args)
{
	int df;
	int skip;
	long doff;

	PyObject* pymem;
	Memory* mem;
	MBFILE* mmp;

	if (!PyArg_ParseTuple(args, "Oili", &pymem, &df, &doff, &skip)) return NULL;

	mem = (Memory*) PyCObject_AsVoidPtr (pymem);
	mmp = mem->mmp;	
	mmp->dc = df;	
	if (blink (mmp->bfdb, self->fdb, mem->mutex, doff, skip) == -1) {
		if (mmp->bfdb->errcode == 1) {
			return PyErr_NoMemory ();
		} else if (mmp->bfdb->errcode == 2) {
			return PyErr_SetFromErrno (PyExc_IOError);
		}
	}
	return Py_BuildValue ("i", 1); /* confidecial posting document count */
}

static PyObject*
DBInt_get (DBInt *self, PyObject *args)
{
	unsigned char _uchar;
	int i, j, _shift;
	int packsize, df;
	long doff;
	int data, ident, last_ident = 0;
	int identdelta;
	PyObject *d, *o;
	PyObject* pymem;
	Memory* mem;
	MBFILE* mmp;

	if (!PyArg_ParseTuple(args, "Oili", &pymem, &df, &doff, &packsize)) return NULL;
	mem = (Memory*) PyCObject_AsVoidPtr (pymem);
	mmp = mem->mmp;

	if (blink (mmp->bfdb, self->fdb, mem->mutex, doff, 1024) == -1) {
		if (mmp->bfdb->errcode == 1) {
			return PyErr_NoMemory ();
		} else if (mmp->bfdb->errcode == 2) {
			return PyErr_SetFromErrno (PyExc_IOError);
		}
	}	
	mmp->bfdb->position = 0;
	d = PyList_New (df);
	for (i = 0; i < df; i++) {
		o = PyTuple_New (packsize);
		breadVInt (mmp->bfdb, identdelta);
		ident = identdelta + last_ident;
		last_ident = ident;
		PyTuple_SetItem (o, 0, PyLong_FromLong (ident));
		for (j = 1; j < packsize; j ++) {
			breadVInt (mmp->bfdb, data);
			PyTuple_SetItem (o, j, PyLong_FromLong (data));
		}
		PyList_SetItem (d, i, o);
	}	
	return d;

ioreaderror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;	
}

static PyObject*
DBInt_getbyid (DBInt *self, PyObject *args)
{
	unsigned char _uchar;
	int i, j, _shift;
	int doff, df;
	int packsize;
	int data, ident, want_ident, last_ident = 0;
	int identdelta;
	PyObject *o;
	PyObject* pymem;
	Memory* mem;
	MBFILE* mmp;

	if (!PyArg_ParseTuple(args, "Oiili",&pymem, &want_ident, &df, &doff, &packsize)) return NULL;
	mem = (Memory*) PyCObject_AsVoidPtr (pymem);
	mmp = mem->mmp;
	
	if (blink (mmp->bfdb, self->fdb, mem->mutex, doff, 1024) == -1) {
		if (mmp->bfdb->errcode == 1) {
			return PyErr_NoMemory ();
		} else if (mmp->bfdb->errcode == 2) {
			return PyErr_SetFromErrno (PyExc_IOError);
		}
	}
	
	mmp->bfdb->position = 0;
	for (i = 0; i < df; i++) {
		breadVInt (mmp->bfdb, identdelta);
		ident = identdelta + last_ident;
		last_ident = ident;
		if (want_ident == ident) {
			o = PyTuple_New (packsize);
			PyTuple_SetItem (o, 0, PyLong_FromLong (ident));		
			for (j = 1; j < packsize; j ++) {
				breadVInt (mmp->bfdb, data);
				PyTuple_SetItem (o, j, PyLong_FromLong (data));
			}
			return o;		
		}
		else if (ident > want_ident) {
			Py_INCREF (Py_None);
			return Py_None;
		}
		else {
			for (j = 1; j < packsize; j ++) {
				breadVInt (mmp->bfdb, data);
			}
		}
	}
	Py_INCREF (Py_None);
	return Py_None;

ioreaderror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;	
}

static PyObject*
DBInt_writelist (DBInt *self, PyObject *args)
{
	unsigned int _uint;
	int i, num, _shift;
	int size = 1;	
	PyObject *pylist;
	
	if (!PyArg_ParseTuple(args, "O|i", &pylist, &size)) return NULL;

	for (i = 0; i < PyList_Size (pylist); i++) {
		num = (int) PyLong_AsLong (PyList_GetItem (pylist, i));
		bwriteInt (self->bfdb, num, size);		
	}
	return Py_BuildValue ("i", btell (self->bfdb));

iowriteerror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;

memoryerror:
	PyErr_NoMemory ();
	return NULL;
}

static PyObject*
DBInt_listgetat (DBInt *self, PyObject *args)
{
	unsigned char _uchar;
	int i, num, _shift;
	int doff, size = 1, fetch = 1;
	PyObject* pymem, *o;
	Memory* mem;
	MBFILE* mmp;
	
	if (!PyArg_ParseTuple(args, "Oli|i", &pymem, &doff, &size, &fetch)) return NULL;		
	mem = (Memory*) PyCObject_AsVoidPtr (pymem);
	mmp = mem->mmp;
	
	if (blink (mmp->bfdb, self->fdb, mem->mutex, doff, 0) == -1) {
		if (mmp->bfdb->errcode == 1) {
			return PyErr_NoMemory ();
		} else if (mmp->bfdb->errcode == 2) {
			return PyErr_SetFromErrno (PyExc_IOError);
		}
	}
	mmp->bfdb->position = 0;
	o = PyTuple_New (fetch);
	for (i=0;i<fetch;i++) {
		breadInt (mmp->bfdb, num, size);
		PyTuple_SetItem (o, i, PyLong_FromLong (num));
	}
	return o;

ioreaderror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;
}


/****************************************************************
Module Definition
****************************************************************/

static PyMemberDef DBInt_members[] = {
	//{"mode", T_CHAR, offsetof(DBInt, mode), 0, ""},
	{NULL}
};

static PyMethodDef DBInt_methods[] = {
	{"close", (PyCFunction) DBInt_close, METH_VARARGS, ""},
	{"tell", (PyCFunction) DBInt_tell, METH_VARARGS, ""},
	{"write", (PyCFunction) DBInt_write, METH_VARARGS, ""},
	{"read", (PyCFunction) DBInt_read, METH_VARARGS, ""},
	{"get", (PyCFunction) DBInt_get, METH_VARARGS, ""},
	{"getbyid", (PyCFunction) DBInt_getbyid, METH_VARARGS, ""},
	{"listgetat", (PyCFunction) DBInt_listgetat, METH_VARARGS, ""},
	{"writelist", (PyCFunction) DBInt_writelist, METH_VARARGS, ""},
	{"commit", (PyCFunction) DBInt_commit, METH_VARARGS, ""},
	{"initialize", (PyCFunction) DBInt_initialize, METH_VARARGS, ""},
	{NULL}
};

PyTypeObject DBIntType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"core.DBInt",			 /*tp_name*/
	sizeof (DBInt),			 /*tp_basicsize*/
	0,						 /*tp_itemsize*/
	(destructor) DBInt_dealloc, /*tp_dealloc*/
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
	0, //(iternextfunc) DBInt_iternext,	   /* tp_iternext */
	DBInt_methods,			 /* tp_methods */
	DBInt_members,			 /* tp_members */
	0,						 /* tp_getset */
	0,						 /* tp_base */
	0,						 /* tp_dict */
	0,						 /* tp_descr_get */
	0,						 /* tp_descr_set */
	0,						 /* tp_dictoffset */
	(initproc) DBInt_init,	  /* tp_init */
	0,						 /* tp_alloc */
	DBInt_new,				 			/* tp_new */
};
