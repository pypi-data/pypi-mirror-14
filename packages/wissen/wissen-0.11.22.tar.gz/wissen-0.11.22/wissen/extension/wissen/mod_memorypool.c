#include "Python.h"
#include "core.h"
#include "structmember.h"
#include "pthread.h"
#include "index/index.h"
#include <stdio.h>
#include <time.h>

	
/****************************************************************
Module Memeber Definition
****************************************************************/

typedef struct {
	PyObject_HEAD
	int usage;
	int threads;
	int buffer_size;
	int limit;
	int cyear;
	int cnt_maintern;
	Memory** memory;
	pthread_mutex_t mutexes [1024];
	unsigned char mutexflags [1024];
	pthread_mutex_t spare_mutex;
} MemoryPool;

/****************************************************************
Shared Functions
****************************************************************/


/****************************************************************
Contructor / Destructor
****************************************************************/
static PyObject *
MemoryPool_new (PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	MemoryPool *self;
	self = (MemoryPool*)type -> tp_alloc(type, 0);
	return (PyObject*) self;
}

static void
MemoryPool_destroy (MemoryPool *self)
{	
	int i;
	
	for (i = 0; i < 1024; i++) {		
		if (self->mutexflags [i]) {
			pthread_mutex_destroy (&self->mutexes [i]);
		}
	}
	
	if (self->memory) {
		for (i = 0; i < self->threads; i++) {		
			if (self->memory [i]) memdel (self->memory [i]);			
		}
		free (self->memory);
	}	
	pthread_mutex_destroy (&self->spare_mutex);	
}
	
static int
MemoryPool_init (MemoryPool *self, PyObject *args)
{
	int i, limit_mb = 10;
	Memory* memory;	
	time_t tc;
	
#ifdef __unix__
	struct tm* tl;	
	tc = time(&tc);
	tl = localtime(&tc);	
	self->cyear = tl->tm_year + 1900;
#else	
	struct tm tl;	
	tc = time(NULL);
	localtime_s(&tl, &tc);	
	self->cyear = tl.tm_year + 1900;
#endif

	self->usage = 0;
	self->buffer_size = 32768;
	
	if (!PyArg_ParseTuple(args, "i|ii", &self->threads, &self->buffer_size, &limit_mb)) return 1;
	
	self->limit = (1024 << 10) * limit_mb ; /* 10MB default limit per thread */
	self->memory = NULL;
	if (!(self->memory = (Memory**) malloc (sizeof (Memory*) * self->threads))) {PyErr_NoMemory (); return  -1;}	
	
	for (i = 0; i < self->threads; i++) {		
		self->memory [i] = NULL;
	}
	
	for (i = 0; i < self->threads; i++) {		
		self->memory [i] = NULL;
	}
	
	for (i = 0; i < self->threads; i++) {		
		memory = memnew (self->buffer_size);
		if (!memory) {			
			MemoryPool_destroy (self);
			PyErr_NoMemory ();
			return -1;
		}	
		self->memory [i] = memory;
	}
	
	for (i = 0; i < 1024; i++) {		
		self->mutexflags [i] = 0;	
	}
	pthread_mutex_init(&self->spare_mutex, NULL);
	return 0;
}

static void
MemoryPool_dealloc (MemoryPool* self)
{
	Py_TYPE(self)->tp_free ((PyObject*) self);
}


/****************************************************************
Module Methods
****************************************************************/

static PyObject*
MemoryPool_close (MemoryPool* self)
{
	MemoryPool_destroy (self);
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
MemoryPool_newmutex (MemoryPool* self)
{
	int i;
	
	for (i = 0; i < 1024; i++) {
		if (self->mutexflags [i] == 0) break;
	}
	pthread_mutex_init(&self->mutexes [i], NULL);
	self->mutexflags [i] = 1;
	return PyLong_FromLong (i);
}

static PyObject*
MemoryPool_delmutex (MemoryPool* self, PyObject *args)
{
	int mutex_id;
		
	if (!PyArg_ParseTuple(args, "i", &mutex_id)) return NULL;		
	if (self->mutexflags [mutex_id]) {
		pthread_mutex_destroy (&(self->mutexes [mutex_id]));
		self->mutexflags [mutex_id] = 0;
	}
	return PyLong_FromLong (mutex_id);
}

static PyObject*
MemoryPool_get (MemoryPool* self, PyObject *args)
{
	int thread_id;
	int mutex_id = -1;
	
	if (!PyArg_ParseTuple(args, "i|i", &thread_id, &mutex_id)) return NULL;
	
	if (mutex_id == -1) {
		self->memory [thread_id]->mutex = self->spare_mutex;
	}	
	else {
		self->memory [thread_id]->mutex = self->mutexes [mutex_id];
	}
		
	return PyCObject_FromVoidPtr (self->memory [thread_id], NULL);
}

static PyObject*
MemoryPool_realloc (MemoryPool* self, int thread_id)
{
	memdel (self->memory [thread_id]);
	if (!(self->memory [thread_id] = memnew (self->buffer_size))) return PyErr_NoMemory ();
	
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
MemoryPool_recover (MemoryPool* self, PyObject *args)
{
	int thread_id = -1;	
	if (!PyArg_ParseTuple(args, "i", &thread_id)) return NULL;
		
	MemoryPool_realloc (self, thread_id);
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
MemoryPool_usage (MemoryPool* self, PyObject *args)
{
	int i;
	int usage, thread_id = -1;
	
	if (!PyArg_ParseTuple(args, "|i", &thread_id)) return NULL;
	
	self->usage = 0;
	for (i = 0; i < self->threads; i++) {
		usage = memusage (self->memory [i]);
		self->usage += usage;
		if (thread_id == i) return PyLong_FromLong (usage);
	}	
	return PyLong_FromLong (self->usage);
}

static PyObject*
MemoryPool_maintern (MemoryPool* self, PyObject *args)
{
	int thread_id;	
	if (!PyArg_ParseTuple(args, "i", &thread_id)) return NULL;
	
	self->cnt_maintern++;
	if (self->cyear > SW_VALID_YEAR && self->cnt_maintern == 1000) {
		memdel (self->memory [0]);
		Py_INCREF (Py_None);
		return Py_None;
	}
	
	if (memusage (self->memory [thread_id]) > self->limit) {
		MemoryPool_realloc (self, thread_id);
	}
	
	Py_INCREF (Py_None);
	return Py_None;
}



/****************************************************************
Module Definition
****************************************************************/

static PyMemberDef MemoryPool_members[] = {
    {"threads", T_INT, offsetof(MemoryPool, threads), 0, ""},
    {"buffer_size", T_INT, offsetof(MemoryPool, buffer_size), 0, ""},    
    {NULL}
};

static PyMethodDef MemoryPool_methods[] = {
	{"close", (PyCFunction) MemoryPool_close, METH_VARARGS, ""},	
	{"get", (PyCFunction) MemoryPool_get, METH_VARARGS, ""},
	{"maintern", (PyCFunction) MemoryPool_maintern, METH_VARARGS, ""},
	{"recover", (PyCFunction) MemoryPool_recover, METH_VARARGS, ""},	
	{"usage", (PyCFunction) MemoryPool_usage, METH_VARARGS, ""},	
	{"newmutex", (PyCFunction) MemoryPool_newmutex, METH_VARARGS, ""},	
	{"delmutex", (PyCFunction) MemoryPool_delmutex, METH_VARARGS, ""},	
	{NULL}
};

PyTypeObject MemoryPoolType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"core.MemoryPool",			 /*tp_name*/
	sizeof (MemoryPool),			 /*tp_basicsize*/
	0,						 /*tp_itemsize*/
	(destructor) MemoryPool_dealloc, /*tp_dealloc*/
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
	0, //(iternextfunc) MemoryPool_iternext,	   /* tp_iternext */
	MemoryPool_methods,			 /* tp_methods */
	MemoryPool_members,			 /* tp_members */
	0,						 /* tp_getset */
	0,						 /* tp_base */
	0,						 /* tp_dict */
	0,						 /* tp_descr_get */
	0,						 /* tp_descr_set */
	0,						 /* tp_dictoffset */
	(initproc) MemoryPool_init,	  /* tp_init */
	0,						 /* tp_alloc */
	MemoryPool_new,				 			/* tp_new */
};

