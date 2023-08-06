#include "Python.h"
#include "core.h"
#include "structmember.h"
#include "index/index.h"
#include <stdio.h>
#include <stdlib.h>

/****************************************************************
Module Memeber Definition
****************************************************************/

typedef struct {
	PyObject_HEAD
	int numterm;
	int index;
	int return_flag;
	nodeType** table;
	keyType** keys;
} TermTable;


/****************************************************************
Shared Functions
****************************************************************/



/****************************************************************
Contructor / Destructor
****************************************************************/
static PyObject *
TermTable_new (PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	TermTable *self;
	self = (TermTable*)type -> tp_alloc(type, 0);
	return (PyObject*) self;
}

static int
TermTable_init (TermTable *self, PyObject *args)
{
	self->index = 0;
	self->numterm = 0;
	self->return_flag = 0;
	self->table = NULL;
	self->keys = NULL;
	if (!(self->table = ht_init (self->table))) {PyErr_NoMemory (); return -1;}
	return 0;
}

static void
TermTable_dealloc (TermTable* self)
{
	Py_TYPE(self)->tp_free ((PyObject*) self);
}


/****************************************************************
Module Methods
****************************************************************/

static PyObject*
TermTable_set_return_flag (TermTable *self, PyObject *args)
{
	if (!PyArg_ParseTuple(args, "i", &self->return_flag)) return NULL;
	Py_INCREF (Py_None);
	return Py_None;
}


static PyObject*
TermTable_close (TermTable *self, PyObject *args)
{
	if (self->keys) {
		free (self->keys);
		self->keys = NULL;
	}
	if (self->table) {
		ht_destroy (self->table);
		self->table = NULL;
	}

	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
TermTable_add (TermTable *self, PyObject *args)
{
	char *term;
	int fdno, docid, tf;
	keyType* key;
	recType* rec;
	PyObject* pyprox = NULL;
	int i = 0;
	int inserted = 0;
	int usage = 0;

	if (!PyArg_ParseTuple(args, "siii|O", &term, &fdno, &docid, &tf, &pyprox)) return NULL;

	if (!(key = (keyType*) malloc (sizeof (keyType)))) return PyErr_NoMemory ();
	if (!(rec = (recType*) malloc (sizeof (recType)))) return PyErr_NoMemory ();
	if (!(key->term = (char*) malloc (strlen (term) + 1))) return PyErr_NoMemory ();

	strcpy (key->term, term);
	key->fdno = (unsigned char) fdno;

	rec->docid = docid;
	rec->tf = tf;

	if (pyprox != Py_None && pyprox && PyList_Size (pyprox)) {
		if (!(rec->prox = (short int*) malloc (sizeof (unsigned short int) * tf))) return PyErr_NoMemory ();
		for (i = 0; i < tf; i++) {
			//printf ("%d: %d/", i, PyLong_AsLong (PyList_GetItem (pyprox, i)));
			rec->prox [i] = (unsigned short) PyLong_AsLong (PyList_GetItem (pyprox, i));
		}
		usage += sizeof (unsigned short int) * tf;
	}
	else
		rec->prox = NULL;

	inserted = ht_insert (self->table, key, rec);
	if (inserted == -1) return PyErr_NoMemory ();

	self->numterm += inserted;
	usage += sizeof (recType);
	if (inserted) {
		usage += sizeof (keyType) + (int) strlen (term) + 1 + sizeof(nodeType);
	}

	return PyLong_FromLong (usage);
}


static PyObject*
TermTable_iternext (TermTable *self)
{
	keyType* key;
	recType* rec;
	PyObject* posting, *o, *tp;
	int i;

	if (!self->index) {
		if (!(self->keys = ht_keys (self->keys, self->numterm, self->table))) return PyErr_NoMemory ();
		ht_sort (self->keys, self->numterm);
	}
	if (self->index >= self->numterm) goto fail;

	key = self->keys [self->index ++];
	rec = ht_fetchfirst (self->table, key);

	if (self -> return_flag) {
		posting = PyList_New (0);
		i = 0;
		while (rec) {
			o = Py_BuildValue ("ii", rec->docid, rec->tf);
			PyList_Append (posting, o);
			Py_DECREF (o);
			i++;
			rec = rec->next;
		}
		tp = Py_BuildValue ("siO", key->term, key->fdno, posting);
		Py_DECREF (posting);
	}

	else {
		o = PyCObject_FromVoidPtr (rec, NULL);
		tp = Py_BuildValue ("siO", key->term, key->fdno, o);
		Py_DECREF (o);
	}

	return tp;

fail:
	self->index = 0;
	return NULL;
}


/****************************************************************
Module Definition
****************************************************************/

static PyMemberDef TermTable_members[] = {
    {"numterm", T_INT, offsetof(TermTable, numterm), 0, ""},
    {NULL}
};

static PyMethodDef TermTable_methods[] = {
	{"add", (PyCFunction) TermTable_add, METH_VARARGS, ""},
	{"close", (PyCFunction) TermTable_close, METH_VARARGS, ""},
	{"set_return_flag", (PyCFunction) TermTable_set_return_flag, METH_VARARGS, ""},
	{NULL}
};

PyTypeObject TermTableType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"core.TermTable",			 /*tp_name*/
	sizeof (TermTable),			 /*tp_basicsize*/
	0,						 /*tp_itemsize*/
	(destructor) TermTable_dealloc, /*tp_dealloc*/
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
	PyObject_SelfIter,					   /* tp_iter */
	(iternextfunc) TermTable_iternext,	   /* tp_iternext */
	TermTable_methods,			 /* tp_methods */
	TermTable_members,			 /* tp_members */
	0,						 /* tp_getset */
	0,						 /* tp_base */
	0,						 /* tp_dict */
	0,						 /* tp_descr_get */
	0,						 /* tp_descr_set */
	0,						 /* tp_dictoffset */
	(initproc) TermTable_init,	  /* tp_init */
	0,						 /* tp_alloc */
	TermTable_new,				 			/* tp_new */
};
