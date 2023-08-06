#include "Python.h"
#include "core.h"
#include "structmember.h"
#include "index/index.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/****************************************************************
Module Memeber Definition
****************************************************************/
typedef struct {
	PyObject_HEAD
	Memory* mem;
	int numdoc;
	int numvoca;
	int numpool;
	int inited;
	int ctf;
	int ccf;
	FeatureInfo *corpus;
	FeatureInfo *feature;
	ClassScore *scores;
	ClassScore *temp [3];
} Classifier;


/****************************************************************
Shared Functions
****************************************************************/
static int
sorter (const void *a, const void *b) {
    	if ((*(ClassScore *)a).score > (*(ClassScore *)b).score) return -1;
	else if ((*(ClassScore *)a).score < (*(ClassScore *)b).score) return 1;
	return 0;
}


/****************************************************************
Contructor / Destructor
****************************************************************/
static PyObject *
Classifier_new (PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	Classifier *self;
	self = (Classifier*)type -> tp_alloc(type, 0);
	return (PyObject*) self;
}

static int
Classifier_init (Classifier *self, PyObject *args)
{
	PyObject* pymem, *pycorpus, *o;
	int i, j;
	self->inited = 0;
	if (!PyArg_ParseTuple(args, "OOii", &pymem, &pycorpus, &self->numvoca, &self->numdoc)) return -1;

	self->mem = (Memory*) PyCObject_AsVoidPtr (pymem);
	self->numpool = (int) PyList_Size (pycorpus);

	if (self->numpool > self->mem->cla->numpool) {
		if (!(self->mem->cla->corpus = (FeatureInfo*) realloc (self->mem->cla->corpus, sizeof (FeatureInfo) * self->numpool))) goto fail;
		if (!(self->mem->cla->feature = (FeatureInfo*) realloc (self->mem->cla->feature, sizeof (FeatureInfo) * self->numpool))) goto fail;
		if (!(self->mem->cla->scores = (ClassScore*) realloc (self->mem->cla->scores, sizeof (ClassScore) * self->numpool))) goto fail;	
		for (i = 0; i < 3; i++) {
			if (!(self->mem->cla->temp [i] = (ClassScore*) realloc (self->mem->cla->temp [i], sizeof (ClassScore) * self->numpool))) goto fail;			
		}
		self->mem->cla->numpool = self->numpool;
	}
	self->corpus = self->mem->cla->corpus;
	self->feature = self->mem->cla->feature;
	self->scores = self->mem->cla->scores;
	for (i = 0; i < 3; i++) {
		self->temp [i] = self->mem->cla->temp [i];
		for (j = 0; j < self->numpool; j++) {
			self->temp [i][j].score = 0.0;
		}
	}
		
	self->ctf = 0;
	self->ccf = 0;

	for (i = 0; i < self->numpool; i++) {
		o = PyList_GetItem (pycorpus, i);
		self->corpus [i].df = (int) PyLong_AsLong (PyTuple_GetItem (o, 0));
		self->corpus [i].tf = (int) PyLong_AsLong (PyTuple_GetItem (o, 1));
		self->scores [i].classid = i;
		self->ctf += self->corpus [i].tf; /* total tf */
		self->ccf += self->corpus [i].df; /* total df */
		self->scores [i].score = 0.0;
	}

	return 0;

fail:
	PyErr_NoMemory ();
	return -1;
}

static void
Classifier_reset (Classifier *self)
{
	int i;
	for (i = 0; i < self->numpool; i++) {
		self->scores [i].score = 0.0;
	}
	self->inited = 0;
}

static void
Classifier_dealloc (Classifier* self)
{
	Py_TYPE(self)->tp_free ((PyObject*) self);
}


/****************************************************************
Module Methods
****************************************************************/

static PyObject*
Classifier_close (Classifier *self, PyObject *args)
{
	Py_INCREF (Py_None);
	return Py_None;
}


/*
[Naive Bayes algorithm]
	P(C|d) = k * P(C) * PRODUCT P(Wi|Cj)
	* Laplace probability estimate used:
                               Freq (W, C) + 1
	P (W|C) = --------------------------------
                     SIGMA Freq (Wi, C) + |Vocabulrary|

                      feaure [i].tf + 1
	 = --------------------------------
	     corpus [i].tf + |Vocabulrary|
*/
PyObject *
Classifier_bayes (Classifier *self, PyObject *args)
{
	int i;
	int dtf = 1;
	int has_prob = 0;
	
	if (!PyArg_ParseTuple(args, "|i", &dtf)) return NULL;

	if (!self->inited) {
		for (i = 0; i < self->numpool; i++) {
			self->scores [i].score = (double) self->corpus [i].df / (double) self->ccf;			
		}
		self->inited = 1;
	}
	
	for (i = 0; i <self->numpool; i++) {		
		self->scores [i].score *= (double)(1 + self->feature [i].tf) / (double) (self->corpus [i].tf + self->numvoca);
		// for fast abort
		if (has_prob == 0 && self->scores [i].score != 0.0) {
			has_prob = 1;
		}
	}
	return PyLong_FromLong (has_prob);	
}


/*
[Feature Value Voting]
	P(C|d) = argmax SIGMA V (Fi, Ci)
	F = LOR (Fi, Ci)
*/
PyObject *
Classifier_featurevote (Classifier *self, PyObject *args)
{
	double positive, negative;
	int tdf = 0;
	int i;
	int dtf;
	double weight = 1.0;

	if (!PyArg_ParseTuple(args, "|i", &dtf)) return NULL;
	weight = 1.0 + log (dtf);
	for (i =0; i < self->numpool; i++) {
		tdf += self->feature [i].df;
	}

	for (i =0; i < self->numpool; i++) {
		positive = odds (self->feature [i].df, self->corpus [i].df, self->ccf);
		negative = odds (tdf - self->feature [i].df, self->ccf - self->corpus [i].df, self->ccf);		
		//printf ("%d-%d, %d, %d\n", tdf, self->feature [i].df, self->ccf - self->corpus [i].df, self->ccf);
		self->scores [i].score += log (positive / negative) * weight;
		//printf ("%f %f = %f\n", positive, negative, log (positive / negative) * weight);
	}
	Py_INCREF (Py_None);
	return Py_None;
}

PyObject*
Classifier_scorefeature (Classifier *self, PyObject *args)
{
	double positive, negative;
	int tdf = 0;
	int i;
	double fvmax = -1.7976931348623157E+308;
	double fv;

	for (i =0; i < self->numpool; i++) {
		tdf += self->feature [i].df;
	}

	for (i =0; i < self->numpool; i++) {
		positive = odds (self->feature [i].df, (self->corpus [i].df), self->ccf);
		negative = odds ((tdf - self->feature [i].df), (self->ccf - self->corpus [i].df), self->ccf);
		fv = log (positive / negative);
		if (fv > fvmax) {
			fvmax = fv;
		}
	}
	return PyFloat_FromDouble (fvmax);
}

static PyObject*
Classifier_load (Classifier *self, PyObject *args)
{
	int i, _shift;
	unsigned char _uchar;
	int last_classid = 0;
	int classdelta;
	int classid, df, tf;

	for (i = 0; i < self->numpool; i ++) {
		self->feature [i].df = 0;
		self->feature [i].tf = 0;
	}

	self->mem->mmp->bfdb->position = 0;
	for (i = 0; i < self->mem->mmp->dc; i ++) {
		breadVInt (self->mem->mmp->bfdb, classdelta);
		classid = last_classid + classdelta;
		breadVInt (self->mem->mmp->bfdb, df);
		breadVInt (self->mem->mmp->bfdb, tf);

		self->feature [classid].df = df;
		self->feature [classid].tf = tf;

		last_classid = classid;
	}

	Py_INCREF (Py_None);
	return Py_None;

ioreaderror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;
}

PyObject *
Classifier_getf (Classifier *self, PyObject *args)
{
	int i, size = 0;
	PyObject *d;
	
	for (i = 0; i < self->numpool; i++) {
		if (self->feature [i].df) 
			size++;
	}
	d = PyList_New (size);	
	size = 0;
	for (i = 0; i < self->numpool; i++) {
		if (self->feature [i].df) {
			PyList_SetItem (d, size++, Py_BuildValue ("iii", i, self->feature [i].df, self->feature [i].tf));
		}	
	}
	return d;
}

PyObject *
Classifier_get (Classifier *self, PyObject *args)
{
	int i, k, offset = -1, fetch = -1;
	PyObject *d;

	if (!PyArg_ParseTuple(args, "|ii", &offset, &fetch)) return NULL;

	qsort (self->scores, self->numpool, sizeof (ClassScore), sorter);
	if (offset == -1) offset = 0;
	else if (offset >= self->numpool) return PyList_New (0);

	if (fetch == -1) fetch = self->numpool - offset;
	if (offset + fetch > self->numpool) fetch = self->numpool - offset;

	d = PyList_New (fetch);
	k = 0;
	for (i = offset; i < offset + fetch; i++) {
		PyList_SetItem (d, k++, Py_BuildValue ("id", self->scores[i].classid, self->scores[i].score));
	}

	return d;
}


/*
[Uncertainity Measure #1: Confidence]
	                      P(Ci|d) - P(Cj|d)
	U:confidence (d) = -----------------------
                              P(Ci|d)
    * P(ci|d) : maximum probability
    * P(cj|d) : sencond probability
*/
PyObject *
Classifier_confidence (Classifier *self, PyObject *args)
{
	double x, y, c;

	if (!self->numpool)
		return PyFloat_FromDouble (0.0);
	else if (self->numpool == 1)
		return PyFloat_FromDouble (1.0);
	else {
		if (self->scores [self->numpool - 1].score < 0.0) {
			x = self->scores [0].score - self->scores [self->numpool - 1].score;
			y = self->scores [1].score - self->scores [self->numpool - 1].score;
		}
		else {
			x = self->scores [0].score;
			y = self->scores [1].score;
		}
		c = (x - y) / x;
		return PyFloat_FromDouble (c);
	}
}


/*
[Uncertainity Measure #2: MAD (Mean Absolute Deviation)]
                SIGMA (i=0,|C|) (P(Ci|d) - u)
    U:MAD (d) = --------------------------------
                             |C|

         SIGMA (i=0,|C|) P(Ci|d)
    u = --------------------------
                   |C|
*/
PyObject *
Classifier_mad (Classifier *self, PyObject *args)
{
	int i;
	double t = 0.0, u, mad;

	if (!self->numpool)
		return PyFloat_FromDouble (0.0);
	else if (self->numpool == 1)
		return PyFloat_FromDouble (1.0);
	else {
		for (i=0; i<self->numpool; i++) {
			t += self->scores [i].score;
		}
		u = t / (double) self->numpool;

		t = 0.0;
		for (i = 0; i < self->numpool;i++) {
			t += (double) self->scores [i].score - u;
		}
		mad = t / (double) self->numpool;
		return PyFloat_FromDouble (mad);
	}
}



/****************************************************************
Module Definition
****************************************************************/

static PyMemberDef Classifier_members[] = {
	{"numdoc", T_INT, offsetof(Classifier, numdoc), 0, ""},
	{"numvoca", T_INT, offsetof(Classifier, numvoca), 0, ""},
	{"numpool", T_INT, offsetof(Classifier, numpool), 0, ""},
	{NULL}
};

static PyMethodDef Classifier_methods[] = {
	{"close", (PyCFunction) Classifier_close, METH_VARARGS, ""},
	{"load", (PyCFunction) Classifier_load, METH_VARARGS, ""},
	{"get", (PyCFunction) Classifier_get, METH_VARARGS, ""},
	{"getf", (PyCFunction) Classifier_getf, METH_VARARGS, ""},
	{"confidence", (PyCFunction) Classifier_confidence, METH_VARARGS, ""},
	{"mad", (PyCFunction) Classifier_mad, METH_VARARGS, ""},
	{"scorefeature", (PyCFunction) Classifier_scorefeature, METH_VARARGS, ""},
	{"featurevote", (PyCFunction) Classifier_featurevote, METH_VARARGS, ""},
	{"bayes", (PyCFunction) Classifier_bayes, METH_VARARGS, ""},
	{"reset", (PyCFunction) Classifier_reset, METH_VARARGS, ""},
	{NULL}
};

PyTypeObject ClassifierType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"core.Classifier",			 /*tp_name*/
	sizeof (Classifier),			 /*tp_basicsize*/
	0,						 /*tp_itemsize*/
	(destructor) Classifier_dealloc, /*tp_dealloc*/
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
	0, //(iternextfunc) Classifier_iternext,	   /* tp_iternext */
	Classifier_methods,			 /* tp_methods */
	Classifier_members,			 /* tp_members */
	0,						 /* tp_getset */
	0,						 /* tp_base */
	0,						 /* tp_dict */
	0,						 /* tp_descr_get */
	0,						 /* tp_descr_set */
	0,						 /* tp_dictoffset */
	(initproc) Classifier_init,	  /* tp_init */
	0,						 /* tp_alloc */
	Classifier_new,				 			/* tp_new */
};
