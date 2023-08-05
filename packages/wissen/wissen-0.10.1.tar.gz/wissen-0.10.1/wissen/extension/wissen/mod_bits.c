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
	int numdoc;
	int bcount;	
	unsigned char* bits;	
} BitVector;



/****************************************************************
Shared Functions
****************************************************************/

const static unsigned char BYTE_COUNTS [] = {
	0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4,
	1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
	1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
	2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
	1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
	2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
	2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
	3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
	1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
	2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
	2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
	3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
	2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
	3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
	3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
	4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8
};

/****************************************************************
Contructor / Destructor
****************************************************************/

static PyObject *
BitVector_new (PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	BitVector *self;
	self = (BitVector*)type -> tp_alloc(type, 0);	
	return (PyObject*) self;
}

/* forward proto declare */
static PyObject* BitVector_fromFile (BitVector *self, PyObject *args);

static int
BitVector_init (BitVector *self, PyObject *args)
{
	PyObject* maybefp = NULL;
		
	self->bcount = -1;
	self->numdoc = 0;
	self->bits = NULL;	
	
	if (!PyArg_ParseTuple(args, "|O", &maybefp)) return -1;
	if (maybefp) {
		if (BitVector_fromFile (self, args) == NULL) return -1;
	}
	return 0;
}

/* proto type of close */
static PyObject* BitVector_close (BitVector *self);

static void
BitVector_dealloc (BitVector* self)
{
	BitVector_close (self);	
	Py_TYPE(self)->tp_free ((PyObject*) self);
}


/****************************************************************
Module Methods
****************************************************************/

static PyObject* 
BitVector_close (BitVector *self) {
	if (self->bits) free (self->bits);
	self->bits = NULL;
	Py_INCREF (Py_None);
	return Py_None;
}
	
static PyObject* 
BitVector_count (BitVector *self) 
{
	int c = 0;
	int i = 0;
	int bytes;
	
	if (!self->bits) {
		return PyLong_FromLong (0);
	}	
	
	bytes = (self->numdoc >> 3) + 1;	
	if (self->bcount == -1) {		
		for (i=0; i < bytes; i++) {		
			c += BYTE_COUNTS [self->bits [i] & 0xFF];
		}	
		self->bcount = c;
	}	
	return PyLong_FromLong (self->bcount);
}

static PyObject* 
BitVector_set (BitVector *self, PyObject *args) 
{
	int i;
	if (!PyArg_ParseTuple(args, "i", &i)) return NULL;
		
	self->bits[i >> 3] |= 1 << (i & 7)	;	
	self->bcount = -1;
	
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject* 
BitVector_clear (BitVector *self, PyObject *args) 
{
	int i;
	if (!PyArg_ParseTuple(args, "i", &i)) return NULL;
	self->bits[i >> 3] &= ~(1 << (i & 7));
	self->bcount = -1;
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
BitVector_fromFile (BitVector *self, PyObject *args)
{
	FILE *fp;
	char *fn;
	int _shift, want, size;
	unsigned char _uchar;
	
	if (!PyArg_ParseTuple(args, "s", &fn)) return NULL;		
	
	if (self->bits) free (self->bits);
	self->bits = NULL;
	
	fp = fopen (fn, "rb");
	fseek (fp, 0, SEEK_SET);
	freadInt (fp, self->numdoc, 4);
	freadInt (fp, self->bcount, 4);
	
	if (!self->bits) {
		if (!(self->bits = (unsigned char*) malloc ((self->numdoc >> 3) + 1))) return PyErr_NoMemory ();	
	}	
	want = (self->numdoc >> 3) + 1;	
	if ((size = fread (self->bits, 1, want, fp)) != want) {
		return NULL;
	}
	fclose (fp);
	Py_INCREF (Py_None);
	return Py_None;
}		

static PyObject* 
BitVector_create (BitVector *self, PyObject *args) 
{
	int n;
	if (!PyArg_ParseTuple(args, "i", &n)) return NULL;
	
	if (self->bits) free (self->bits);
	self->bits = NULL;
	
	if (!(self->bits = (unsigned char*) malloc ((n >> 3) + 1))) return PyErr_NoMemory ();	
	memset ((void *) self->bits, '\0', (n >> 3) + 1);
	self->numdoc = n;
	
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
BitVector_toFile (BitVector *self, PyObject *args)
{
	char *fn;
	FILE *fp;
	int _shift;
	unsigned int _uint;	
	
	if (!PyArg_ParseTuple(args, "s", &fn)) return  NULL;	
	/* counting */
	BitVector_count (self);
	
	fp = fopen (fn, "wb");
	fseek (fp, 0, SEEK_SET);
	fwriteInt (fp, self->numdoc, 4);
	fwriteInt (fp, self->bcount, 4);			
	fwrite (self->bits, 1, (self->numdoc >> 3) + 1, fp);
	fclose (fp);
	
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject* 
BitVector_get (BitVector *self, PyObject *args) 
{
	int i;	
	if (!PyArg_ParseTuple(args, "i", &i)) return NULL;
	
	if (!self->bits) {
		return PyLong_FromLong (0);	
	}
	return PyLong_FromLong (self->bits[i >> 3] & (1 << (i & 7)));
}

static PyObject* 
BitVector_toString (BitVector *self, PyObject *args) 
{
	if (self->bits) {
		return PyBytes_FromStringAndSize ((const char *) self->bits, (self->numdoc >> 3) + 1);	
	}
	Py_INCREF (Py_None);	
	return Py_None;	
}

static PyObject* 
BitVector_toBytes (BitVector *self, PyObject *args) {
	return BitVector_toString (self, args); 
}

static PyObject* 
BitVector_getbits (BitVector *self, PyObject *args) 
{
	if (self->bits) {
		return PyCObject_FromVoidPtr (self->bits, NULL);
	}
	Py_INCREF (Py_None);	
	return Py_None;	
}



/****************************************************************
Module Definition
****************************************************************/

static PyMemberDef BitVector_members[] = {
    {"numdoc", T_INT, offsetof(BitVector, numdoc), 0, ""},
    {"bcount", T_INT, offsetof(BitVector, bcount), 0, ""},
    {NULL}
};

static PyMethodDef BitVector_methods[] = {
	{"getbits", (PyCFunction) BitVector_getbits, METH_VARARGS, ""},
	{"get", (PyCFunction) BitVector_get, METH_VARARGS, ""},
	{"close", (PyCFunction) BitVector_close, METH_VARARGS, ""},
	{"set", (PyCFunction) BitVector_set, METH_VARARGS, ""},
	{"clear", (PyCFunction) BitVector_clear, METH_VARARGS, ""},
	{"create", (PyCFunction) BitVector_create, METH_VARARGS, ""},
	{"count", (PyCFunction) BitVector_count, METH_VARARGS, ""},
	{"toString", (PyCFunction) BitVector_toString, METH_VARARGS, ""},	
	{"toBytes", (PyCFunction) BitVector_toBytes, METH_VARARGS, ""},		
	{"toFile", (PyCFunction) BitVector_toFile, METH_VARARGS, ""},	
	{"commit", (PyCFunction) BitVector_toFile, METH_VARARGS, ""},
	{"fromFile", (PyCFunction) BitVector_fromFile, METH_VARARGS, ""},		
	{NULL}
};

PyTypeObject BitVectorType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"core.BitVector",			 /*tp_name*/
	sizeof (BitVector),			 /*tp_basicsize*/
	0,						 /*tp_itemsize*/
	(destructor) BitVector_dealloc, /*tp_dealloc*/
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
	0,					   /* tp_iter */
	0,					   /* tp_iternext */
	BitVector_methods,			 /* tp_methods */
	BitVector_members,			 /* tp_members */
	0,						 /* tp_getset */
	0,						 /* tp_base */
	0,						 /* tp_dict */
	0,						 /* tp_descr_get */
	0,						 /* tp_descr_set */
	0,						 /* tp_dictoffset */
	(initproc) BitVector_init,	  /* tp_init */
	0,						 /* tp_alloc */
	BitVector_new,				 			/* tp_new */
};

