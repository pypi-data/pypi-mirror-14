#include "Python.h"
#include "core.h"
#include "structmember.h"
#include "index/index.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define FEATSEL_INIT {\
	if (!PyArg_ParseTuple(args, "|i", &how)) return NULL;\
	for (i =0; i < self->numpool; i++) {\
		tdf += self->feature [i].df;\
		ttf += self->feature [i].tf;\
	}\
}

#define FEATSEL_SETVAL {\
	if (how == 0) score += 1;\
	else if (how == 1) { if (score > max_score) max_score = score; }\
	else score += (double) (self->feature [i].tf/ttf) * score;\
}

#define FEATSEL_RETVAL {\
	if (how == 0) return PyFloat_FromDouble (score);\
	else if (how == 1) return PyFloat_FromDouble (max_score);\
	else return PyFloat_FromDouble (score / (double) self->numpool);\
}
		
/****************************************************************
Module Memeber Definition
****************************************************************/
typedef struct {
	PyObject_HEAD
	int numpool;
	int numdoc;
	int numterm;
	int poolindex;
	int ctf;
	int ccf;
	FeatureInfo *corpus;
	FeatureInfo *feature;
} Selector;


/****************************************************************
Shared Functions
****************************************************************/


/****************************************************************
Contructor / Destructor
****************************************************************/
static PyObject *
Selector_new (PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	Selector *self;
	self = (Selector*)type -> tp_alloc(type, 0);
	return (PyObject*) self;
}

static int
Selector_init (Selector *self, PyObject *args)
{
	if (!PyArg_ParseTuple(args, "iii", &self->numpool, &self->numdoc,  &self->numterm)) return -1;

	if (!(self->corpus = (FeatureInfo*) malloc (sizeof (FeatureInfo) * self->numpool))) {PyErr_NoMemory (); return -1;}
	if (!(self->feature= (FeatureInfo*) malloc (sizeof (FeatureInfo) * self->numpool))) {PyErr_NoMemory (); return -1;}
	self->poolindex = 0;
	return 0;
}

static void
Selector_dealloc (Selector* self)
{
	Py_TYPE(self)->tp_free ((PyObject*) self);
}


/****************************************************************
Module Methods
****************************************************************/

static PyObject*
Selector_close (Selector *self, PyObject *args)
{
	free (self->feature);
	free (self->corpus);

	Py_INCREF (Py_None);
	return Py_None;
}

static void
Selector_set (Selector *self, PyObject *pyfi, FeatureInfo *fi)
{
	PyObject *o;
	int i;

	for (i = 0; i <PyList_Size (pyfi); i ++) {
		o = PyList_GetItem (pyfi, i);
		fi [i].df = (int) PyLong_AsLong (PyTuple_GetItem (o, 0));
		fi [i].tf =(int) PyLong_AsLong (PyTuple_GetItem (o, 1));
	}
}

static PyObject*
Selector_addCorpus (Selector *self, PyObject *args)
{
	PyObject* pyfi;
	int i;

	if (!PyArg_ParseTuple(args, "O", &pyfi)) return NULL;
	Selector_set (self, pyfi, self->corpus);

	for (i = 0; i <PyList_Size (pyfi); i ++) {
		self->ctf += self->corpus [i].tf;
		self->ccf += self->corpus [i].df;
	}
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
Selector_add (Selector *self, PyObject *args)
{
	PyObject* pyfi;

	if (!PyArg_ParseTuple(args, "O", &pyfi)) return NULL;
	Selector_set (self, pyfi, self->feature);
	Py_INCREF (Py_None);
	return Py_None;
}

/*
[NGLSUM]
		   |	c	| ^c
	-----------------------
	  t	|	A	|  B
	-----------------------
	  ^t   |	C	|  D

					  sqrt (N) * ((AD - CB))
	chi2 (t, c) = ----------------------------
					  sqrt ((A+C)(B+D)(A+B)(C+D))
	chi2max (t) = MAX (chi2 (t, ci))
*/

PyObject *
Selector_ngl (Selector *self, PyObject *args)
{
	int A, B, C, D;	
	int how = 1;	
	int i, ttf = 0, tdf = 0;
	double max_score = -1.79769e300, score = 0.;
		
	FEATSEL_INIT;
	for (i =0; i < self->numpool; i++) {
		A = self->feature [i].df;
		B = tdf - A;
		C = self->corpus [i].df - A;
		D = self->numdoc - (A + B + C);
		score = (double) (self->numdoc * (pow ((double)(A * D - C * B), 2.0))) / (double)((A+C) * (B+D) * (A+B) * (C+D));		
		FEATSEL_SETVAL;
	}	
	FEATSEL_RETVAL;	
}

/*
[GSS]
	GSS (t, c) = (AD - CB)					
*/

PyObject *
Selector_gss (Selector *self, PyObject *args)
{
	int A, B, C, D;
	int how = 1;	
	int i, ttf = 0, tdf = 0;
	double max_score = -1.79769e300, score = 0.;	
	
	FEATSEL_INIT;		
	for (i =0; i < self->numpool; i++) {
		A = self->feature [i].df;
		B = tdf - A;
		C = self->corpus [i].df - A;
		D = self->numdoc - (A + B + C);
		score = (double)(A * D - C * B);
		FEATSEL_SETVAL;
	}
	FEATSEL_RETVAL;
}


/*
[Chi2]
		   |	c	| ^c
	-----------------------
	  t	|	A	|  B
	-----------------------
	  ^t   |	C	|  D

					  N * ((AD - CB) ** 2)
	chi2 (t, c) = ----------------------------
					  (A+C)(B+D)(A+B)(C+D)
	chi2max (t) = MAX (chi2 (t, ci))
*/

PyObject *
Selector_chi (Selector *self, PyObject *args)
{
	int A, B, C, D;
	int how = 1; // MAX DEFAULT
	int i, ttf = 0, tdf = 0;
	double max_score = -1.79769e300, score = 0.;	
	
	FEATSEL_INIT;	
	for (i =0; i < self->numpool; i++) {
		A = self->feature [i].df;
		B = tdf - A;
		C = self->corpus [i].df - A;
		D = self->numdoc - (A + B + C);
		score = (double) (self->numdoc * (pow ((double)(A * D - C * B), 2.0))) / (double)((A+C) * (B+D) * (A+B) * (C+D));		
		FEATSEL_SETVAL;
	}
	FEATSEL_RETVAL;
}

/*
[OR]
		    |	c	| ^c
	-----------------------
	   t	|	A	|  B
	-----------------------
	  ^t    |	C	|  D

					  AD
	OR (t, c) = ---------------
					  BC
			    (if BC == 0, then 1)			    
	OR (t) = SIGMA (OR (t, c))
*/

PyObject *
Selector_or4p (Selector *self, PyObject *args)
{
	int A, B, C, D;
	int how = 1; // MAX DEFAULT
	int i, ttf = 0, tdf = 0;
	double max_score = -1.79769e300, score = 0.;	
	
	FEATSEL_INIT;
	for (i =0; i < self->numpool; i++) {
		A = self->feature [i].df;
		B = tdf - A;
		C = self->corpus [i].df - A;
		D = self->numdoc - (A + B + C);
		if (!B || !C) score = 1.0;
		else score = (double) ((A*D) / (B*C));
		FEATSEL_SETVAL;
	}
	FEATSEL_RETVAL;
}

/*
[Mutual Information]
	                                 AN
	MI (t, c) = log(2) (-----------------)
	                            (A+C)(A+B)
        MImax (t) = MAX (MI (t, ci))
*/
PyObject *
Selector_mi (Selector *self, PyObject *args)
{
	int A, B, C;
	int how = 1; // MAX DEFAULT
	int i, ttf = 0, tdf = 0;
	double max_score = -1.79769e300, score = 0.;

	FEATSEL_INIT;
	for (i =0; i < self->numpool; i++) {
		A = self->feature [i].df;
		B = tdf - A;
		C = self->corpus [i].df - A;
		score = (double) (self->feature [i].tf/ttf) * (log2 (((double) (A * self->numdoc) / (double)((A + C) * (A + B)))));		
		FEATSEL_SETVAL;
	}
	FEATSEL_RETVAL;
}

/*
[TFIDF]
	tfidf = tf * IDF
	tf = tf / TF
	IDF = N / df
*/
PyObject *
Selector_tfidf (Selector *self, PyObject *args)
{
	int how = 1; // MAX DEFAULT
	int i, ttf = 0, tdf = 0, ctf = 0;
	double max_score = -1.79769e300, score = 0.;

	FEATSEL_INIT;
	for (i =0; i < self->numpool; i++) {
		ctf += self->corpus [i].tf;
	}
	for (i =0; i < self->numpool; i++) {
		score = (double) ((double) self->feature [i].tf / ctf) * (log ((double) self->numdoc / tdf));
		FEATSEL_SETVAL;
	}
	FEATSEL_RETVAL;
}


/*
DF = P (df/C)
*/
PyObject *
Selector_df (Selector *self, PyObject *args)
{
	int how = 1; // MAX DEFAULT
	int i, ttf = 0, tdf = 0;
	double max_score = -1.79769e300, score = 0.;

	FEATSEL_INIT;

	for (i =0; i < self->numpool; i++) {
		score = (double) (self->feature [i].tf/ttf) * (double) (self->feature [i].df/tdf);		
		FEATSEL_SETVAL;
	}
	FEATSEL_RETVAL;
}

/*
IG (t) = -SIGMA Pr(Ci)log Pr(Ci)
		+ (Pr|t) * SIGMA (Pr(Ci|t) * log Pr(Ci|t)))
		+ (Pr|^t) * SIGMA (Pr(Ci|^t) * log Pr(Ci|^t)))

		               Pr (t|Ci) * Pr (Ci)
		Pr (Ci|t) =  -----------------------
		                     Pr (t)
*/
PyObject *
Selector_ig (Selector *self, PyObject *args)
{
	double positive = 0.0, negative = 0.0, prob = 0.0, temp, score;
	int ttf = 0, ctf = 0;
	int i;	
		
	for (i =0; i < self->numpool; i++) {
		ttf += self->feature [i].tf;
		ctf += self->corpus [i].tf;
		temp = (double) self->corpus[i].df / (double) self->numdoc;
		prob += temp * log (temp);
	}

	for (i =0; i < self->numpool; i++) {
		if (self->feature[i].tf) {
			temp = (double)self->feature[i].tf / (double) ttf;
			positive += temp * log (temp);
		}
		temp = ((double) self->corpus[i].tf - (double) self->feature[i].tf) / ((double) ctf - (double) ttf);
		negative += temp * log (temp);
	}

	score = -1.0 * prob + ((double) ttf / (double) self->numterm) * positive + (((double) self->numterm - (double) ttf) / (double) self->numterm) * negative;
	return PyFloat_FromDouble (score);
}

/*
[TF-orient]
       P(W|C1) (1-P(W|C2))
log -----------------------
      (1-P(W|C1)) P(W|C2)

               odds (W|pos)
= log -------------------------
               odds (W|neg)

odds(W) = (1/n^2) / (1 - 1/n^2) ; p(W) = 0
        = (1 - 1/n^2) / (1/n^2); P(W) = 1
        = P(W) / (1 - P(W)) ; P(W) != 0 and P(W) != 1

n: number of examples
*/
PyObject *
Selector_or (Selector *self, PyObject *args)
{
	int ttf = 0, ctf = 0;
	double positive, negative;
	int how = 0; // SUM DEFAULT
	int i;
	double max_score = -1.79769e300, score = 0.;
	
	if (!PyArg_ParseTuple(args, "|i", &how)) return NULL;
	
	for (i =0; i < self->numpool; i++) {
		ttf += self->feature [i].tf;
		ctf += self->corpus [i].tf;
	}

	for (i =0; i < self->numpool; i++) {

		positive = odds (self->feature [i].tf, (self->corpus [i].tf), ctf);
		negative = odds ((ttf - self->feature [i].tf), (ctf - self->corpus [i].tf), ctf);

		//printf ("%d %d / %f %f %f %f\n", self->feature [i].tf, self->corpus [i].tf, positive,negative, positive / negative, log (positive / negative));
		score = log (positive / negative);		
		FEATSEL_SETVAL;
	}
	FEATSEL_RETVAL;
}

/*
Relevancy Score
		P(positive)  + d         P (Tk/Ci) + d
RS = ------------------------ = ---------------
        P(negative)  + d        P (^Tk/Ci) + d
*/
PyObject *
Selector_rs (Selector *self, PyObject *args)
{
	int ttf = 0, ctf = 0;
	double positive, negative;
	int how = 0; // SUM DEFAULT
	int i;
	double max_score = -1.79769e300, score = 0.;
	
	if (!PyArg_ParseTuple(args, "|i", &how)) return NULL;\
		
	for (i =0; i < self->numpool; i++) {
		ttf += self->feature [i].tf;
		ctf += self->corpus [i].tf;
	}

	for (i =0; i < self->numpool; i++) {
		positive = self->feature [i].tf / self->corpus [i].tf + 1;
		negative = (ttf - self->feature [i].tf) / (ctf - self->corpus [i].tf) + 1;
		score = log (positive / negative);		
		FEATSEL_SETVAL;
	}
	FEATSEL_RETVAL;
}

/*
[DF-orient]
By definition, the odds ratio, OR, is
             [a/(a+b)] / [b/(a+b)]
     OR  =  -----------------------,    (1)
             [c/(c+d)] / [d/(c+d)]

but this reduces to
                a/b
     OR  = ------,                     (2)
                c/d

or, as OR is usually calculated,
                       ad
     OR  =log ------.                      (3)
                       bc
*/
PyObject *
Selector_lor (Selector *self, PyObject *args)
{
	int tdf = 0, ttf = 0, cdf = 0;
	double positive, negative;
	int how = 0; // SUM DEFAULT
	int i;
	double max_score = -1.79769e300, score = 0.;
	
	if (!PyArg_ParseTuple(args, "|i", &how)) return NULL;\
		
	for (i =0; i < self->numpool; i++) {
		tdf += self->feature [i].df;
		cdf += self->corpus [i].df;
		ttf += self->feature [i].tf;
	}

	for (i =0; i < self->numpool; i++) {
		positive = odds (self->feature [i].df, (self->corpus [i].df), cdf);
		negative = odds ((tdf - self->feature [i].df), (cdf - self->corpus [i].df), cdf);
		score = log (positive / negative);		
		FEATSEL_SETVAL;
	}
	FEATSEL_RETVAL;
}

/*                                     a
COS (t) =       ----------------------------------
                            sqaure (a+b) * (a + c)
*/
PyObject *
Selector_cos (Selector *self, PyObject *args)
{
	int A, B, C;
	int how = 1; // MAX DEFAULT
	int i, ttf = 0, tdf = 0;
	double max_score = -1.79769e300, score = 0.;

	FEATSEL_INIT;
	for (i =0; i < self->numpool; i++) {
		A = self->feature [i].df;
		B = tdf - A;
		C = self->corpus [i].df - A;
		if (A)
			score =  (double) A / sqrt ((double)((A + B) * (A + C)));
		else
			score = 0.0;
		FEATSEL_SETVAL;
	}
	FEATSEL_RETVAL;
}

/*
                                             ad-bc
Pearson's PHI = ----------------------------------------
                             sqrt ((a+b)(a+c)(b+d) (c+d))
*/

PyObject *
Selector_pphi (Selector *self, PyObject *args)
{
	int A, B, C, D;
	int how = 1; // MAX DEFAULT
	int i, ttf = 0, tdf = 0;
	double max_score = -1.79769e300, score = 0.;

	FEATSEL_INIT;
	for (i =0; i < self->numpool; i++) {
		A = self->feature [i].df;
		B = tdf - A;
		C = self->corpus [i].df - A;
		D = self->numdoc - (A + B + C);
		score =  (double) (A * D - B * C) / sqrt ((double)((A + B) * (A + C) *(B + D) * (C + D)));
		FEATSEL_SETVAL;
	}
	FEATSEL_RETVAL;
}


/*
                     square (ad) - square (bc)
Yule = ----------------------------------------
                     square (ad) + square (bc)
*/

PyObject *
Selector_yule (Selector *self, PyObject *args)
{
	int A, B, C, D;
	int how = 1; // MAX DEFAULT
	int i, ttf = 0, tdf = 0;
	double max_score = -1.79769e300, score = 0.;

	FEATSEL_INIT;
	for (i =0; i < self->numpool; i++) {
		A = self->feature [i].df;
		B = tdf - A;
		C = self->corpus [i].df - A;
		D = self->numdoc - (A + B + C);
		score =  (sqrt ((double)A * (double)D) - sqrt ((double)B * (double)C)) / (sqrt ((double)A * (double)D) + sqrt ((double)B * (double)C));
		FEATSEL_SETVAL;
	}
	FEATSEL_RETVAL;
}


/*
                     log(2)N + log(2)A - log (2)((a+b)(a+c))
RMI = ----------------------------------------------------------
                                        log(2)N - log (2)A
*/

PyObject *
Selector_rmi (Selector *self, PyObject *args)
{
	int A, B, C;
	int how = 1; // MAX DEFAULT
	int i, ttf = 0, tdf = 0;
	double max_score = -1.79769e300, score = 0.;

	FEATSEL_INIT;
	for (i =0; i < self->numpool; i++) {
		A = self->feature [i].df;
		B = tdf - A;
		C = self->corpus [i].df - A;
		score =  ((log2 (self->numdoc) + log2 (A)) - (log2 ((A + B) * (A +C)))) / (log2 (self->numdoc) - log2 (A));;
		FEATSEL_SETVAL;
	}
	FEATSEL_RETVAL;
}

/****************************************************************
Module Definition
****************************************************************/

static PyMemberDef Selector_members[] = {
	{"numdoc", T_INT, offsetof(Selector, numdoc), 0, ""},
	{"numterm", T_INT, offsetof(Selector, numterm), 0, ""},
	{"numpool", T_INT, offsetof(Selector, numpool), 0, ""},
	{NULL}
};

static PyMethodDef Selector_methods[] = {
	{"close", (PyCFunction) Selector_close, METH_VARARGS, ""},
	{"addCorpus", (PyCFunction) Selector_addCorpus, METH_VARARGS, ""},
	{"add", (PyCFunction) Selector_add, METH_VARARGS, ""},
	{"chi", (PyCFunction) Selector_chi, METH_VARARGS, ""},
	{"gss", (PyCFunction) Selector_gss, METH_VARARGS, ""},
	{"df", (PyCFunction) Selector_df, METH_VARARGS, ""},
	{"ngl", (PyCFunction) Selector_ngl, METH_VARARGS, ""},
	{"mi", (PyCFunction) Selector_mi, METH_VARARGS, ""},
	{"tfidf", (PyCFunction) Selector_tfidf, METH_VARARGS, ""},
	{"ig", (PyCFunction) Selector_ig, METH_VARARGS, ""},
	{"or", (PyCFunction) Selector_or, METH_VARARGS, ""},	
	{"or4p", (PyCFunction) Selector_or4p, METH_VARARGS, ""},	
	{"rs", (PyCFunction) Selector_rs, METH_VARARGS, ""},	
	{"lor", (PyCFunction) Selector_lor, METH_VARARGS, ""},
	{"cos", (PyCFunction) Selector_cos, METH_VARARGS, ""},
	{"pphi", (PyCFunction) Selector_pphi, METH_VARARGS, ""},
	{"yule", (PyCFunction) Selector_yule, METH_VARARGS, ""},
	{"rmi", (PyCFunction) Selector_rmi, METH_VARARGS, ""},
	{NULL}
};

PyTypeObject SelectorType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"core.Selector",			 /*tp_name*/
	sizeof (Selector),			 /*tp_basicsize*/
	0,						 /*tp_itemsize*/
	(destructor) Selector_dealloc, /*tp_dealloc*/
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
	0, //(iternextfunc) Selector_iternext,	   /* tp_iternext */
	Selector_methods,			 /* tp_methods */
	Selector_members,			 /* tp_members */
	0,						 /* tp_getset */
	0,						 /* tp_base */
	0,						 /* tp_dict */
	0,						 /* tp_descr_get */
	0,						 /* tp_descr_set */
	0,						 /* tp_dictoffset */
	(initproc) Selector_init,	  /* tp_init */
	0,						 /* tp_alloc */
	Selector_new,				 			/* tp_new */
};
