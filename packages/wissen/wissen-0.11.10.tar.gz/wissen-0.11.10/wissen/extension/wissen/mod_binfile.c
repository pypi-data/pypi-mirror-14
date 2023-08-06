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
	int dc;
	BFILE *bfdb;
	BFILE *bstr; // pointer of tmp->bxx0
	BFILE *bzfi; // pointer of tmp->bxx1
	long long *deltan;	
	char **deltas;
	long long N;
} MPACK;

typedef struct {
	PyObject_HEAD
	int file;
	char *mode;
	char *format;
	int packsize;
	MPACK* mmp;
	int skippable;
	pthread_mutex_t mutex;	
} BinFile;

/****************************************************************
Shared Functions
****************************************************************/


/****************************************************************
Contructor / Destructor
****************************************************************/
static PyObject *
BinFile_new (PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	BinFile *self;
	self = (BinFile*)type -> tp_alloc(type, 0);	
	return (PyObject*) self;
}

static int
BinFile_init (BinFile *self, PyObject *args)
{
	char f;
	int i;
	
	self->format = "";
	self->packsize = 0;
	
	if (!PyArg_ParseTuple(args, "i|ss#", &self->file, &self->mode, &self->format, &self->packsize)) return -1;
	pthread_mutex_init(&self->mutex, NULL);
	self->mmp = NULL;	
	if (!(self->mmp = (MPACK*) malloc (sizeof (MPACK)))) {PyErr_NoMemory (); return -1;}			
	self->mmp->bfdb = NULL;	
	self->mmp->bzfi = NULL;	
	self->mmp->bstr = NULL;	
	
	if (self->mode [0] == 'w') {
		if (!(self->mmp->bfdb = bopen (self->file, 'w', FILEBUFFER_LENGTH, 0))) {PyErr_NoMemory (); return -1;}
	}
	else {
		if (!(self->mmp->bfdb = bopen (self->file, 'r', FILEBUFFER_LENGTH, 0))) {PyErr_NoMemory (); return -1;}		
	}
	if (!(self->mmp->bzfi = bopen (-1, 'w', FILEBUFFER_LENGTH, 1))) goto fail;
	if (!(self->mmp->bstr = bopen (-1, 'w', FILEBUFFER_LENGTH, 1))) goto fail;	
	
	self->mmp->deltan = (long long*) malloc (sizeof(long long) * self->packsize);	
	self->mmp->deltas = (char**) malloc (sizeof(char*) * self->packsize);	
	for (i=0;i<self->packsize;i++) {
		self->mmp->deltan [i] = 0;
		self->mmp->deltas [i] = (char*) malloc (sizeof (char) * 128);
		self->mmp->deltas [i] = "";
	}
	self->skippable = 0;
	for (i=0;i<self->packsize;i++) {
		f = self->format [i];
		if (i >= 1) {
			if (f >= 49 && f <= 56) self->skippable += f - 48;
			else if (f >= 65 && f <= 72) self->skippable += f - 64;			
			else {
				self->skippable = 0;
				break;
			}
		}	
	}
			
	return 0;

fail:
	PyErr_NoMemory ();
	return -1;		
}

static void
BinFile_dealloc (BinFile* self)
{
	Py_TYPE(self)->tp_free ((PyObject*) self);
}


/****************************************************************
Module Methods
****************************************************************/
static PyObject* 
BinFile_close (BinFile *self, PyObject *args) 
{
	if (self->mmp) {
		if (self->mmp->bfdb) bclose (self->mmp->bfdb);
		if (self->mmp->bzfi) bclose (self->mmp->bzfi);
		if (self->mmp->bstr) bclose (self->mmp->bstr);	
		free (self->mmp);
	}
	
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
BinFile_seek (BinFile *self, PyObject *args) {
	int point;
	if (!PyArg_ParseTuple (args, "i", &point)) return NULL;		
	bseek (self->mmp->bfdb, point);	
	return PyLong_FromLong (point);
}

static PyObject*
BinFile_read (BinFile *self, PyObject *args) {
	int _shift;
	long size;
	if (!PyArg_ParseTuple (args, "l", &size)) return NULL;
	breadString (self->mmp->bfdb, self->mmp->bstr->buffer, size);	
	return PyBytes_FromStringAndSize (self->mmp->bstr->buffer, size);

ioreaderror:
	return PyErr_SetFromErrno (PyExc_IOError);
}

static PyObject*
BinFile_write (BinFile *self, PyObject *args) {
	long size;
	char* str;
	int _shift;
	if (!PyArg_ParseTuple (args, "s#", &str, &size)) return NULL;
	bwriteString (self->mmp->bfdb, str, size);
	return PyLong_FromLong (size);
	
iowriteerror:
	return PyErr_SetFromErrno (PyExc_IOError);

memoryerror:
	return PyErr_NoMemory ();	
}

static PyObject*
BinFile_tell (BinFile *self, PyObject *args) {
	return PyLong_FromLong (btell (self->mmp->bfdb));
}

static PyObject*
BinFile_flush (BinFile *self, PyObject *args) {
	bflush (self->mmp->bfdb);
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
BinFile_writeVInt (BinFile *self, PyObject *args) {
	int i;
	unsigned int _uint;
	
	if (!PyArg_ParseTuple(args, "i", &i)) return NULL;
	bwriteVInt (self->mmp->bfdb, i);
	Py_INCREF (Py_None);
	return Py_None;
	
iowriteerror:
	return PyErr_SetFromErrno (PyExc_IOError);
	
memoryerror:
	return PyErr_NoMemory ();
}

static PyObject*
BinFile_readVInt (BinFile *self, PyObject *args) {
	unsigned char _uchar;
	int _shift;
	int N;
	
	breadVInt (self->mmp->bfdb, N);
	return PyLong_FromLong ((int) N);	
	
ioreaderror:
	return PyErr_SetFromErrno (PyExc_IOError);	
}

static PyObject*
BinFile_writeVLong (BinFile *self, PyObject *args) {
	long long i;
	unsigned long long _ulong;
	
	if (!PyArg_ParseTuple(args, "L", &i)) return NULL;
	bwriteVLong (self->mmp->bfdb, i);
	Py_INCREF (Py_None);
	return Py_None;
	
iowriteerror:
	return PyErr_SetFromErrno (PyExc_IOError);	

memoryerror:
	return PyErr_NoMemory ();	
}

static PyObject*
BinFile_readVLong (BinFile *self, PyObject *args) {
	unsigned char _uchar;
	int _shift;
	long long N;
	
	breadVLong (self->mmp->bfdb, N);
	return PyLong_FromLongLong (N);	
	
ioreaderror:
	return PyErr_SetFromErrno (PyExc_IOError);	
}

static PyObject*
BinFile_writeInt1 (BinFile *self, PyObject *args) {
	int i;
	unsigned int _uint;
	int _shift;
	
	if (!PyArg_ParseTuple(args, "i", &i)) return NULL;
	bwriteInt (self->mmp->bfdb, i, 1);
	Py_INCREF (Py_None);
	return Py_None;
	
iowriteerror:
	return PyErr_SetFromErrno (PyExc_IOError);
	
memoryerror:
	return PyErr_NoMemory ();
}

static PyObject*
BinFile_readInt1 (BinFile *self, PyObject *args) {
	unsigned char _uchar;
	int _shift;
	int N;
	
	breadInt (self->mmp->bfdb, N, 1);
	return PyLong_FromLong ((int) N);	
	
ioreaderror:
	return PyErr_SetFromErrno (PyExc_IOError);	
}

static PyObject*
BinFile_writeInt2 (BinFile *self, PyObject *args) {
	int i;
	unsigned int _uint;
	int _shift;
	
	if (!PyArg_ParseTuple(args, "i", &i)) return NULL;
	bwriteInt (self->mmp->bfdb, i, 2);
	Py_INCREF (Py_None);
	return Py_None;
	
iowriteerror:
	return PyErr_SetFromErrno (PyExc_IOError);	

memoryerror:
	return PyErr_NoMemory ();	
}

static PyObject*
BinFile_readInt2 (BinFile *self, PyObject *args) {
	unsigned char _uchar;
	int _shift;
	int N;
	
	breadInt (self->mmp->bfdb, N, 2);
	return PyLong_FromLong ((int) N);
	
ioreaderror:
	return PyErr_SetFromErrno (PyExc_IOError);	
}

static PyObject*
BinFile_writeInt3 (BinFile *self, PyObject *args) {
	int i;
	unsigned int _uint;
	int _shift;
	
	if (!PyArg_ParseTuple(args, "i", &i)) return NULL;
	bwriteInt (self->mmp->bfdb, i, 3);
	Py_INCREF (Py_None);
	return Py_None;
	
iowriteerror:
	return PyErr_SetFromErrno (PyExc_IOError);
	
memoryerror:
	return PyErr_NoMemory ();	
}

static PyObject*
BinFile_readInt3 (BinFile *self, PyObject *args) {
	unsigned char _uchar;
	int _shift;
	int N;
	
	breadInt (self->mmp->bfdb, N, 3);
	return PyLong_FromLong ((int) N);	
	
ioreaderror:
	return PyErr_SetFromErrno (PyExc_IOError);	
}

static PyObject*
BinFile_writeInt4 (BinFile *self, PyObject *args) {
	int i;
	unsigned int _uint;
	int _shift;
	
	if (!PyArg_ParseTuple(args, "i", &i)) return NULL;
	bwriteInt (self->mmp->bfdb, i, 4);
	Py_INCREF (Py_None);
	return Py_None;
	
iowriteerror:
	return PyErr_SetFromErrno (PyExc_IOError);	

memoryerror:
	return PyErr_NoMemory ();	
}

static PyObject*
BinFile_readInt4 (BinFile *self, PyObject *args) {
	unsigned char _uchar;
	int _shift;
	int N;
	
	breadInt (self->mmp->bfdb, N, 4);
	return PyLong_FromLong ((int) N);	
	
ioreaderror:
	return PyErr_SetFromErrno (PyExc_IOError);	
}

static PyObject*
BinFile_writeLong5 (BinFile *self, PyObject *args) {
	unsigned long long i;
	unsigned long long _ulong;
	int _shift;
	
	if (!PyArg_ParseTuple(args, "L", &i)) return NULL;
	bwriteLong (self->mmp->bfdb, i, 5);
	Py_INCREF (Py_None);
	return Py_None;
	
iowriteerror:
	return PyErr_SetFromErrno (PyExc_IOError);	

memoryerror:
	return PyErr_NoMemory ();	
}

static PyObject*
BinFile_readLong5 (BinFile *self, PyObject *args) {
	unsigned char _uchar;
	int _shift;
	long long N;
	
	breadLong (self->mmp->bfdb, N, 5);
	return PyLong_FromLongLong (N);	
	
ioreaderror:
	return PyErr_SetFromErrno (PyExc_IOError);	
}


static PyObject*
BinFile_writeLong6 (BinFile *self, PyObject *args) {
	unsigned long long i;
	unsigned long long _ulong;
	int _shift;
	
	if (!PyArg_ParseTuple(args, "L", &i)) return NULL;
	bwriteLong (self->mmp->bfdb, i, 6);
	Py_INCREF (Py_None);
	return Py_None;
	
iowriteerror:
	return PyErr_SetFromErrno (PyExc_IOError);
	
memoryerror:
	return PyErr_NoMemory ();	
}

static PyObject*
BinFile_readLong6 (BinFile *self, PyObject *args) {
	unsigned char _uchar;
	int _shift;
	long long N;
	
	breadLong (self->mmp->bfdb, N, 6);
	return PyLong_FromLongLong (N);
	
ioreaderror:
	return PyErr_SetFromErrno (PyExc_IOError);	
}

static PyObject*
BinFile_writeLong7 (BinFile *self, PyObject *args) {
	unsigned long long i;
	unsigned long long _ulong;
	int _shift;
	
	if (!PyArg_ParseTuple(args, "L", &i)) return NULL;
	bwriteLong (self->mmp->bfdb, i, 7);
	Py_INCREF (Py_None);
	return Py_None;
	
iowriteerror:
	return PyErr_SetFromErrno (PyExc_IOError);
	
memoryerror:
	return PyErr_NoMemory ();	
}

static PyObject*
BinFile_readLong7 (BinFile *self, PyObject *args) {
	unsigned char _uchar;
	int _shift;
	long long N;
	
	breadLong (self->mmp->bfdb, N, 7);
	return PyLong_FromLongLong (N);	
	
ioreaderror:
	return PyErr_SetFromErrno (PyExc_IOError);
}

static PyObject*
BinFile_writeLong8 (BinFile *self, PyObject *args) {
	unsigned long long i;
	unsigned long long _ulong;
	int _shift;
	
	if (!PyArg_ParseTuple(args, "L", &i)) return NULL;
	bwriteLong (self->mmp->bfdb, i, 8);
	Py_INCREF (Py_None);
	return Py_None;
	
iowriteerror:
	return PyErr_SetFromErrno (PyExc_IOError);
	
memoryerror:
	return PyErr_NoMemory ();	
}

static PyObject*
BinFile_readLong8 (BinFile *self, PyObject *args) {
	unsigned char _uchar;
	int _shift;
	long long N;
	
	breadLong (self->mmp->bfdb, N, 8);
	return PyLong_FromLongLong (N);	
	
ioreaderror:
	PyErr_SetFromErrno (PyExc_IOError);
	return NULL;
}


static PyObject*
BinFile_writeString (BinFile *self, PyObject *args) {
	unsigned int _uint;
	char * str;
	int _shift, len;
	
	if (!PyArg_ParseTuple(args, "s#", &str, &len)) return NULL;
	bwriteVInt (self->mmp->bfdb, len);
	bwriteString (self->mmp->bfdb, str, len);
	Py_INCREF (Py_None);
	return Py_None;
	
iowriteerror:
	return PyErr_SetFromErrno (PyExc_IOError);
	
memoryerror:
	return PyErr_NoMemory ();	
}

static PyObject*
BinFile_readString (BinFile *self, PyObject *args) {
	unsigned char _uchar;	
	int _shift;
	int N;
	
	breadVInt (self->mmp->bfdb, N);
	bextend (self->mmp->bstr, (int) N);
	breadString (self->mmp->bfdb, self->mmp->bstr->buffer, N);

#if PY_MAJOR_VERSION >= 3
	return PyUnicode_FromStringAndSize (self->mmp->bstr->buffer, (int) N);	
#else
	return PyString_FromStringAndSize (self->mmp->bstr->buffer, (int) N);
#endif
	
ioreaderror:
	return PyErr_SetFromErrno (PyExc_IOError);
}

static PyObject*
BinFile_writeBytes (BinFile *self, PyObject *args) {
	return BinFile_writeString (self, args);
}

static PyObject*
BinFile_readBytes (BinFile *self, PyObject *args) {
	unsigned char _uchar;	
	int _shift;
	int N;
	
	breadVInt (self->mmp->bfdb, N);
	bextend (self->mmp->bstr, (int) N);
	breadString (self->mmp->bfdb, self->mmp->bstr->buffer, N);
	return PyBytes_FromStringAndSize (self->mmp->bstr->buffer, (int) N);
	
ioreaderror:
	return PyErr_SetFromErrno (PyExc_IOError);
}

static PyObject*
BinFile_writeZString (BinFile *self, PyObject *args) {
	unsigned int _uint;
	char* str;
	int _shift, len;
	
	if (!PyArg_ParseTuple(args, "s#", &str, &len)) return NULL;
	if (!zcompress (str, (int) len, self->mmp->bzfi, 6)) return PyErr_NoMemory ();
	bwriteVInt (self->mmp->bfdb, btell (self->mmp->bzfi));
	bwriteString (self->mmp->bfdb, self->mmp->bzfi->buffer, btell (self->mmp->bzfi));
	Py_INCREF (Py_None);
	return Py_None;
	
iowriteerror:
	return PyErr_SetFromErrno (PyExc_IOError);

memoryerror:
	return PyErr_NoMemory ();
}


static PyObject*
BinFile_readZString (BinFile *self, PyObject *args) {
	unsigned char _uchar;
	int _shift;
	int res;
	int N;
	
	breadVInt (self->mmp->bfdb, N);
	bextend (self->mmp->bstr, (int)N);
	breadString (self->mmp->bfdb, self->mmp->bstr->buffer, N);
	res = zdecompress (self->mmp->bstr->buffer, (int)N, self->mmp->bzfi);
	if (!res) {
		res = -2;
		goto error;
	}	

#if PY_MAJOR_VERSION >= 3
	return PyUnicode_FromStringAndSize (self->mmp->bzfi->buffer, self->mmp->bzfi->position);
#else	
	return PyString_FromStringAndSize (self->mmp->bzfi->buffer, self->mmp->bzfi->position);
#endif	
	
ioreaderror:
	return PyErr_SetFromErrno (PyExc_IOError);
	
error:
	if (res == -1) {
		PyErr_SetFromErrno (PyExc_IOError);
		return NULL;
	}	
	return PyErr_NoMemory ();	
}

static PyObject*
BinFile_writeZBytes (BinFile *self, PyObject *args) {
	return BinFile_writeZString (self, args);
}

static PyObject*
BinFile_readZBytes (BinFile *self, PyObject *args) {
	unsigned char _uchar;
	int _shift;
	int res;
	int N;
	
	breadVInt (self->mmp->bfdb, N);
	bextend (self->mmp->bstr, (int)N);
	breadString (self->mmp->bfdb, self->mmp->bstr->buffer, N);
	res = zdecompress (self->mmp->bstr->buffer, (int)N, self->mmp->bzfi);
	if (!res) {
		res = -2;
		goto error;
	}	
	return PyBytes_FromStringAndSize (self->mmp->bzfi->buffer, self->mmp->bzfi->position);
	
ioreaderror:
	return PyErr_SetFromErrno (PyExc_IOError);
	
error:
	if (res == -1) {
		PyErr_SetFromErrno (PyExc_IOError);
		return NULL;
	}	
	return PyErr_NoMemory ();	
}


static PyObject*
BinFile_writepack_meta (BinFile *self, PyObject *o)
{
	unsigned int _uint;
	unsigned long long _ulong;
	int _shift;	
	int j, k;
	int size = 0, lenint;
	int numpack = 0;
	PyObject *x;
	char f;
	char *tdelta, *last_string, *p;
	MPACK* mmp;
	long long N;
	
	mmp = self->mmp;
	for  (j=0; j < self->packsize; j++) {
		f = self->format [j];
		lenint = 0;
		x = PyTuple_GetItem (o, j);
		if (f == 's') {			
			size = (int) PyBytes_Size (x);
			bwriteVInt (mmp->bfdb, size);			
			bwriteString (mmp->bfdb, PyBytes_AsString (x), size);
		}
		else if (f == 'S') {
			last_string = mmp->deltas [j];
			p = PyBytes_AsString (x);
			tdelta = p;
			for (k = 0; k < 128; k++) {
				if (*last_string++ != *tdelta++) {
					tdelta--;
					break;
				}
			}
			bwriteVInt (mmp->bfdb, k); /* prefix len */
			bwriteVInt (mmp->bfdb, strlen (tdelta)); /* suffix len */
			bwriteString (mmp->bfdb, tdelta, strlen (tdelta)); /* suffix */
			strcpy (mmp->deltas [j], p);
		}
		else if (f == 'z') {
			if (!zcompress (PyBytes_AsString (x), (int) PyBytes_Size (x), mmp->bzfi, 6)) return PyErr_NoMemory ();
			bwriteVInt (mmp->bfdb, btell (mmp->bzfi));
			bwriteString (mmp->bfdb, mmp->bstr->buffer, btell (mmp->bzfi));	
		}
		else {
			N = PyLong_AsLongLong (PyTuple_GetItem (o, j));
			if (f == 'V' || f == 'L' || (f >= 65 && f <= 72)) {
				N = N - mmp->deltan [j];
				mmp->deltan [j] += N;
			}
			if (f == 'v' || f == 'V') {
				bwriteVInt (mmp->bfdb, N);	
			}
			else if (f == 'l' || f == 'L') {
				bwriteVLong (mmp->bfdb, N);	
			}
			else {
				if (f >= 49 && f <= 56) lenint = f - 48;
				else if (f >= 65 && f <= 72) lenint = f - 64;			
				if (lenint == 0) {
					return PyErr_SetFromErrno (PyExc_TypeError);
				}
				else if (lenint <= 4) {
					bwriteInt (mmp->bfdb, (int) N, lenint);
				}
				else {
					bwriteLong (mmp->bfdb, N, lenint);	
				}						
			}
		}
	}	
	numpack ++;	
	return PyLong_FromLong (btell (mmp->bfdb));

iowriteerror:
	return PyErr_SetFromErrno (PyExc_IOError);	

memoryerror:
	return PyErr_NoMemory ();	
}

static PyObject*
BinFile_readpack (BinFile *self)
{
	int j;
	int res;	
	PyObject *o, *x;
	char f;
	int n;
	unsigned char _uchar;
	int _shift;
	int lenint;
	int prefixlen, surfixlen, lenstr;
	char* p;
	MPACK* mmp;	
	long long N;
	
	mmp = self->mmp;	
	o = PyTuple_New (self->packsize);
	for (j = 0; j < self->packsize; j ++) {	
		f = self->format [j];
		if (f == 's') {
			breadVInt (mmp->bfdb, n);
			bextend (mmp->bstr, n);
			mmp->bstr->position = n;
			breadString (mmp->bfdb, mmp->bstr->buffer, n);
			x = PyBytes_FromStringAndSize (mmp->bstr->buffer, n);
			PyTuple_SetItem (o, j, x);
		}
		else if (f == 'S') {
			breadVInt (mmp->bfdb, prefixlen); /*prefix len */
			breadVInt (mmp->bfdb, surfixlen); /*suffix len */
			
			lenstr = prefixlen + surfixlen;
			p = mmp->bstr->buffer;
			strncpy (p, mmp->deltas [j], prefixlen); /*copy prefix */
			p += prefixlen;
			breadString (mmp->bfdb, p, surfixlen);
			strncpy (mmp->deltas [j], mmp->bstr->buffer, lenstr);
			x = PyBytes_FromStringAndSize (mmp->bstr->buffer, lenstr);
			PyTuple_SetItem (o, j, x);
		}
		else if (f == 'z') {
			breadVInt (mmp->bfdb, n);
			bextend (mmp->bzfi, n);
			breadString (mmp->bfdb, mmp->bzfi->buffer, n);
			res = zdecompress (mmp->bzfi->buffer, n, mmp->bstr);
			if (!res) {
				res = -2;
				goto error;
			}
			x = PyBytes_FromStringAndSize (mmp->bstr->buffer, mmp->bstr->position);
			PyTuple_SetItem (o, j, x);
		}
		else {
			lenint = 0;
			if (f == 'v' || f == 'V') {
				breadVInt (mmp->bfdb, N);		
				lenint = 4;			
			}
			else if (f == 'l' || f == 'L') {
				breadVLong (mmp->bfdb, N);					
				lenint = 8;
			}
			else {
				if (f >= 49 && f <= 56) lenint = f - 48;
				else if (f >= 65 && f <= 72) lenint = f - 64;
				
				if (lenint == 0) {
					return PyErr_SetFromErrno (PyExc_TypeError);
				}
				else if (lenint <= 4) {
					breadInt (mmp->bfdb, N, lenint);					
				}
				else {
					breadLong (mmp->bfdb, N, lenint);					
				}						
			}	
			if (f == 'L' || f == 'V' || (f >= 65 && f <= 72)) {
				N += mmp->deltan [j];
				mmp->deltan [j] = N;
			}
			if (lenint <= 4) {
				PyTuple_SetItem (o, j, PyLong_FromLong ((int)N));
			} 
			else {
				PyTuple_SetItem (o, j, PyLong_FromLongLong (N));
			}	
			
		}			
	}	
	return o;

ioreaderror:
	return PyErr_SetFromErrno (PyExc_IOError);	
	
error:
	if (res == -1) {
		return PyErr_SetFromErrno (PyExc_IOError);		
	}	
	return PyErr_NoMemory ();	
}

static PyObject*
BinFile_writepack (BinFile *self, PyObject *args)
{
	PyObject *o, *x;
	if (!PyArg_ParseTuple(args, "O", &x)) return NULL;
	o = BinFile_writepack_meta (self, x);
	if (!o) return NULL;
	Py_DECREF (o);	
	return PyLong_FromLong (1);
}

static PyObject*
BinFile_writepacks (BinFile *self, PyObject *args)
{
	int i;
	PyObject *d, *o, *x;
	int numpack;	
	
	if (!PyArg_ParseTuple(args, "O", &d)) return NULL;		
	numpack = (int) PyList_Size (d);
	for (i = 0; i < numpack; i++) {
		x = PyList_GetItem (d, i);
		o = BinFile_writepack_meta (self, x);
		if (!o) return NULL;
		Py_DECREF (o);
	}
	return PyLong_FromLong (numpack);
}

static PyObject*
BinFile_readpacks (BinFile *self, PyObject *args)
{
	int i;
	PyObject *d, *o;
	int numpack;
	
	if (!PyArg_ParseTuple(args, "i", &numpack)) return NULL;	
	d = PyList_New (numpack);
	
	for (i = 0; i < numpack; i++) {
		o = BinFile_readpack (self);
		if (!o) {
			Py_DECREF (d);
			return NULL;
		}
		PyList_SetItem (d, i, o);
	}
	return d;
}

static PyObject*
BinFile_findn (BinFile *self, PyObject *args)
{
	int i;
	PyObject *x, *o;
	int limit;
	long long key, fkey;
	
	if (!PyArg_ParseTuple(args, "l|i", &fkey, &limit)) return NULL;	
	for (i = 0; i < limit; i++) {
		o = BinFile_readpack (self);
		if (!o) {
			PyErr_Clear ();
			Py_INCREF (Py_None);
			return Py_None;
		}
		x = PyTuple_GetItem (o, 0);
		key = PyLong_AsLongLong (x);
		if (fkey == key) {
			return o;
		}		
		else if (fkey < key) {
			Py_DECREF (o);
			Py_INCREF (Py_None);
			return Py_None;
		}
		else {
			Py_DECREF (o);
		}
	}
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
BinFile_finds (BinFile *self, PyObject *args)
{
	int i;
	PyObject *x, *o;
	int limit;
	char *key, *fkey;
	int match;
	
	if (!PyArg_ParseTuple(args, "s|i", &fkey, &limit)) return NULL;	
	for (i = 0; i < limit; i++) {
		o = BinFile_readpack (self);
		if (!o) {
			PyErr_Clear ();
			Py_INCREF (Py_None);
			return Py_None;
		}
		x = PyTuple_GetItem (o, 0);
		key = PyBytes_AsString (x);
		match = strcmp (fkey, key);
		if (match == 0) {
			return o;
		}		
		else if (match == -1) {
			Py_DECREF (o);
			Py_INCREF (Py_None);
			return Py_None;
		}
		else {
			Py_DECREF (o);
		}		
	}
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
BinFile_memlink (BinFile *self, PyObject *args)
{
	long doff = 0;
	PyObject* pymem;	
	Memory* mem;
		
	if (!PyArg_ParseTuple(args, "O|l", &pymem, &doff)) return NULL;	
	mem = (Memory*) PyCObject_AsVoidPtr (pymem);	
	
	if (blink (mem->mmp->bfdb, self->file, mem->mutex, doff, 0) == -1) {
		if (mem->mmp->bfdb->errcode == 1) {
			return PyErr_NoMemory ();
		} else if (mem->mmp->bfdb->errcode == 2) {
			return PyErr_SetFromErrno (PyExc_IOError);
		}
	}
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
BinFile_setdelta (BinFile *self, PyObject *args) {
	PyObject *o, *x, *pyl = NULL;
	int i, index;
	
	if (!PyArg_ParseTuple(args, "|O", &pyl)) return NULL;		
	if (!pyl) {
		for (i = 0; i < self->packsize; i++) {
			self->mmp->deltan [i] = 0;
			self->mmp->deltas [i] = "";
		}		
		Py_INCREF (Py_None);
		return Py_None;
	}
	
	for (i = 0; i < PyList_Size (pyl); i++) {
		o = PyList_GetItem (pyl, i);		
		x = PyTuple_GetItem (o, 0);
		index = (int) PyLong_AsLong (x);
		x = PyTuple_GetItem (o, 1);
		if (PyBytes_Check (x)) {
			self->mmp->deltas [index] = PyBytes_AsString (x);						
		}
		else {
			self->mmp->deltan [index] = PyLong_AsLongLong (x);
		}
	}
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
BinFile_getformat (BinFile* self)
{
	return PyBytes_FromStringAndSize (self->format, self->packsize);
}

static PyObject*
BinFile_setformat (BinFile* self, PyObject *args)
{
	if (!PyArg_ParseTuple (args, "s#", &self->format, &self->packsize)) return NULL;
		Py_INCREF (Py_None);	
		return Py_None;
}

static PyObject*
BinFile_fileno (BinFile* self, PyObject *args)
{
	return PyLong_FromLong (self->file);
}

/****************************************************************
Module Definition
****************************************************************/

static PyMemberDef BinFile_members[] = {
    {"format", T_CHAR, offsetof(BinFile, format), 0, ""},
    {"mode", T_CHAR, offsetof(BinFile, mode), 0, ""},
    {"packsize", T_INT, offsetof(BinFile, packsize), 0, ""},    
    {NULL}
};

static PyMethodDef BinFile_methods[] = {
	{"read", (PyCFunction) BinFile_read, METH_VARARGS, ""},
	{"write", (PyCFunction) BinFile_write, METH_VARARGS, ""},
	{"seek", (PyCFunction) BinFile_seek, METH_VARARGS, ""},
	{"tell", (PyCFunction) BinFile_tell, METH_VARARGS, ""},
	{"close", (PyCFunction) BinFile_close, METH_VARARGS, ""},
	{"flush", (PyCFunction) BinFile_flush, METH_VARARGS, ""},
	{"fileno", (PyCFunction) BinFile_fileno, METH_VARARGS, ""},	
	
	{"writeInt1", (PyCFunction) BinFile_writeInt1, METH_VARARGS, ""},
	{"readInt1", (PyCFunction) BinFile_readInt1, METH_VARARGS, ""},
	{"writeInt2", (PyCFunction) BinFile_writeInt2, METH_VARARGS, ""},
	{"readInt2", (PyCFunction) BinFile_readInt2, METH_VARARGS, ""},
	{"writeInt3", (PyCFunction) BinFile_writeInt3, METH_VARARGS, ""},
	{"readInt3", (PyCFunction) BinFile_readInt3, METH_VARARGS, ""},
	{"writeInt4", (PyCFunction) BinFile_writeInt4, METH_VARARGS, ""},
	{"readInt4", (PyCFunction) BinFile_readInt4, METH_VARARGS, ""},
	{"writeLong5", (PyCFunction) BinFile_writeLong5, METH_VARARGS, ""},
	{"readLong5", (PyCFunction) BinFile_readLong5, METH_VARARGS, ""},
	{"writeLong6", (PyCFunction) BinFile_writeLong6, METH_VARARGS, ""},
	{"readLong6", (PyCFunction) BinFile_readLong6, METH_VARARGS, ""},
	{"writeLong7", (PyCFunction) BinFile_writeLong7, METH_VARARGS, ""},
	{"readLong7", (PyCFunction) BinFile_readLong7, METH_VARARGS, ""},
	{"writeLong8", (PyCFunction) BinFile_writeLong8, METH_VARARGS, ""},
	{"readLong8", (PyCFunction) BinFile_readLong8, METH_VARARGS, ""},
	{"writeVInt", (PyCFunction) BinFile_writeVInt, METH_VARARGS, ""},
	{"readVInt", (PyCFunction) BinFile_readVInt, METH_VARARGS, ""},
	{"writeVLong", (PyCFunction) BinFile_writeVLong, METH_VARARGS, ""},
	{"readVLong", (PyCFunction) BinFile_readVLong, METH_VARARGS, ""},
	{"writeString", (PyCFunction) BinFile_writeString, METH_VARARGS, ""},
	{"readString", (PyCFunction) BinFile_readString, METH_VARARGS, ""},
	{"writeBytes", (PyCFunction) BinFile_writeBytes, METH_VARARGS, ""},
	{"readBytes", (PyCFunction) BinFile_readBytes, METH_VARARGS, ""},
	{"writeZString", (PyCFunction) BinFile_writeZString, METH_VARARGS, ""},
	{"readZString", (PyCFunction) BinFile_readZString, METH_VARARGS, ""},		
	{"writeZBytes", (PyCFunction) BinFile_writeZBytes, METH_VARARGS, ""},
	{"readZBytes", (PyCFunction) BinFile_readZBytes, METH_VARARGS, ""},
	
	{"readpack", (PyCFunction) BinFile_readpack, METH_VARARGS, ""},
	{"writepack", (PyCFunction) BinFile_writepack, METH_VARARGS, ""},
	{"readpacks", (PyCFunction) BinFile_readpacks, METH_VARARGS, ""},
	{"writepacks", (PyCFunction) BinFile_writepacks, METH_VARARGS, ""},
	
	{"findn", (PyCFunction) BinFile_findn, METH_VARARGS, ""},
	{"finds", (PyCFunction) BinFile_finds, METH_VARARGS, ""},
	
	{"memlink", (PyCFunction) BinFile_memlink, METH_VARARGS, ""},
	{"setdelta", (PyCFunction) BinFile_setdelta, METH_VARARGS, ""},
	{"setformat", (PyCFunction) BinFile_setformat, METH_VARARGS, ""},
	{"getformat", (PyCFunction) BinFile_getformat, METH_VARARGS, ""},		
	{NULL}
};



PyTypeObject BinFileType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"core.BinFile",			 /*tp_name*/
	sizeof (BinFile),			 /*tp_basicsize*/
	0,						 /*tp_itemsize*/
	(destructor) BinFile_dealloc, /*tp_dealloc*/
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
	0, //(iternextfunc) BinFile_iternext,	   /* tp_iternext */
	BinFile_methods,			 /* tp_methods */
	BinFile_members,			 /* tp_members */
	0,						 /* tp_getset */
	0,						 /* tp_base */
	0,						 /* tp_dict */
	0,						 /* tp_descr_get */
	0,						 /* tp_descr_set */
	0,						 /* tp_dictoffset */
	(initproc) BinFile_init,	  /* tp_init */
	0,						 /* tp_alloc */
	BinFile_new,				 			/* tp_new */
};




