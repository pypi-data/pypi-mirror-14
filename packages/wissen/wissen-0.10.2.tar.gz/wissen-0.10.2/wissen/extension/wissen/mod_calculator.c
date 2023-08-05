#include "Python.h"
#include "core.h"
#include "structmember.h"
#include "index/index.h"
#include "pthread.h"
#include <stdio.h>
#include <math.h>


/****************************************************************
Module Memeber Definition
****************************************************************/

typedef struct {
	PyObject_HEAD
	int numterm;
	int numdoc;
	int sumtf;
	int sumdf;
	double log2;
} Calculator;



/****************************************************************
Shared Functions
****************************************************************/

/****************************************************************
Contructor / Destructor
****************************************************************/

static PyObject *
Calculator_new (PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	Calculator *self;
	self = (Calculator*)type -> tp_alloc(type, 0);	
	return (PyObject*) self;
}

static int
Calculator_init (Calculator *self, PyObject *args)
{
	self->numterm = 0;
	self->numdoc = 0;
	self->sumdf = 0;
	self->sumtf = 0;
	
	if (!PyArg_ParseTuple(args, "|iiii", &self->numdoc, &self->numterm, &self->sumdf, &self->sumtf)) return -1;
	
	self->log2 = log (2.0);
	
	return 0;
}

static void
Calculator_dealloc (Calculator* self)
{
	Py_TYPE(self)->tp_free ((PyObject*) self);
}


/****************************************************************
Module Methods
****************************************************************/

static PyObject* 
Calculator_close (Calculator *self) {
	Py_INCREF (Py_None);
	return Py_None;
}
	
static PyObject* 
Calculator_termMI (Calculator *self, PyObject *args) 
{
	int x, y, xy;
	
	if (!PyArg_ParseTuple(args, "iii", &x, &y, &xy)) return NULL;	
	if (xy == 0)
		return PyFloat_FromDouble (log (((double)1.0 / pow (self->numterm, 2) / (double)self->numterm) / (((double)x / (double)self->numterm) * ((double)y / (double)self->numterm))) / self->log2);	
	else
		return PyFloat_FromDouble (log (((double)xy / (double)self->numterm) / (((double)x / (double)self->numterm) * ((double)y / (double)self->numterm))) / self->log2);	
}


/****************************************************************
Module Definition
****************************************************************/

static PyMemberDef Calculator_members[] = {
    {"numdoc", T_INT, offsetof(Calculator, numdoc), 0, ""},    
    {"numterm", T_INT, offsetof(Calculator, numterm), 0, ""},    
    {"sumtf", T_INT, offsetof(Calculator, sumtf), 0, ""},    
    {"sumdf", T_INT, offsetof(Calculator, sumdf), 0, ""},    
    
    {NULL}
};

static PyMethodDef Calculator_methods[] = {
	{"close", (PyCFunction) Calculator_close, METH_VARARGS, ""},
	{"termMI", (PyCFunction) Calculator_termMI, METH_VARARGS, ""},	
	{NULL}
};

PyTypeObject CalculatorType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"core.Calculator",			 /*tp_name*/
	sizeof (Calculator),			 /*tp_basicsize*/
	0,						 /*tp_itemsize*/
	(destructor) Calculator_dealloc, /*tp_dealloc*/
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
	Calculator_methods,			 /* tp_methods */
	Calculator_members,			 /* tp_members */
	0,						 /* tp_getset */
	0,						 /* tp_base */
	0,						 /* tp_dict */
	0,						 /* tp_descr_get */
	0,						 /* tp_descr_set */
	0,						 /* tp_dictoffset */
	(initproc) Calculator_init,	  /* tp_init */
	0,						 /* tp_alloc */
	Calculator_new,				 			/* tp_new */
};

