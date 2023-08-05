#include "index/index.h"
#include "Python.h"


/****************************************************************
Shared Functions
****************************************************************/


/****************************************************************
Function Definition
****************************************************************/
PyObject *
def_writeVInt (PyObject *self, PyObject *args) {
	unsigned int _uint;
	
	int int32;
	int i = 0;
	unsigned char buffer [8];
	
	if (!PyArg_ParseTuple(args, "i", &int32)) return NULL;
	writeVInt(buffer, (unsigned int) int32, i);
  return PyBytes_FromStringAndSize ((const char *)buffer, i);
}

PyObject *
def_readVInt (PyObject *self, PyObject *args) {
    int _shift;
    unsigned char _uchar;
    
    PyObject *pystr;
    char *snum;
    unsigned int int32;
    int i = 0;
    
    if (!PyArg_ParseTuple(args, "O", &pystr)) return NULL;	
	snum = PyBytes_AsString (pystr);
	
	readVInt(snum, int32, i);
	return PyLong_FromLong (int32);
}

PyObject *
def_writeVLong (PyObject *self, PyObject *args) {
	unsigned long long _ulong;
	
	long long int64;
	int i = 0;
	unsigned char buffer [10];
	
	if (!PyArg_ParseTuple(args, "L", &int64)) return NULL;
	writeVLong(buffer, (unsigned long long) int64, i);
    return PyBytes_FromStringAndSize ((const char *)buffer, i);
}

PyObject *
def_readVLong (PyObject *self, PyObject *args) {
    int _shift;
    unsigned char _uchar;
    
    PyObject *pystr;
    char *snum;
    unsigned long long int64;
    int i = 0;
    
    if (!PyArg_ParseTuple(args, "O", &pystr)) return NULL;	
	snum = PyBytes_AsString (pystr);
	
	readVLong(snum, int64, i);
	return PyLong_FromLongLong (int64);
}

#define readIntN(length) {\
	int _shift;\
  unsigned char _uchar;\
  PyObject *pystr;\
  char *snum;\
  unsigned int i32;\
  int i = 0;\
  if (!PyArg_ParseTuple(args, "O", &pystr)) return NULL;	\
	snum = PyBytes_AsString (pystr);	\
	readInt(snum, i32, i, length);\
	return PyLong_FromLong (i32);\
}

#define readLongN(length) {\
	int _shift;\
  unsigned char _uchar;\
  PyObject *pystr;\
  char *snum;\
  unsigned long long i64;\
  int i = 0;\
  if (!PyArg_ParseTuple(args, "O", &pystr)) return NULL;\
	snum = PyBytes_AsString (pystr);\
	readLong(snum, i64, i, length);\
	return PyLong_FromLongLong (i64);\
}

#define writeIntN(length) {\
	unsigned int _uint;\
	int _shift;\
	int int32;\
	int i = 0;\
	unsigned char buffer [4];\
	if (!PyArg_ParseTuple(args, "i", &int32)) return NULL;\
	writeInt(buffer, (unsigned int) int32, i, length);\
    return PyBytes_FromStringAndSize ((const char *)buffer, i);\
}

#define writeLongN(length) {\
	unsigned long long _ulong;\
	int _shift;\
	long long int64;\
	int i = 0;\
	unsigned char buffer [8];\
	if (!PyArg_ParseTuple(args, "L", &int64)) return NULL;\
	writeLong(buffer, (unsigned long long) int64, i, length);\
    return PyBytes_FromStringAndSize ((const char *)buffer, i);\
}

PyObject * def_writeInt (PyObject *self, PyObject *args) writeIntN(4);
PyObject * def_readInt (PyObject *self, PyObject *args) readIntN(4);
PyObject * def_writeInt1 (PyObject *self, PyObject *args) writeIntN(1);
PyObject * def_writeInt2 (PyObject *self, PyObject *args) writeIntN(2);
PyObject * def_writeInt3 (PyObject *self, PyObject *args) writeIntN(3);
PyObject * def_writeInt4 (PyObject *self, PyObject *args) writeIntN(4);
PyObject * def_writeLong5 (PyObject *self, PyObject *args) writeLongN(5);
PyObject * def_writeLong6 (PyObject *self, PyObject *args) writeLongN(6);
PyObject * def_writeLong7 (PyObject *self, PyObject *args) writeLongN(7);
PyObject * def_writeLong8 (PyObject *self, PyObject *args) writeLongN(8);
PyObject * def_readInt1 (PyObject *self, PyObject *args) readIntN(1);
PyObject * def_readInt2 (PyObject *self, PyObject *args) readIntN(2);
PyObject * def_readInt3 (PyObject *self, PyObject *args) readIntN(3);
PyObject * def_readInt4 (PyObject *self, PyObject *args) readIntN(4);
PyObject * def_readLong5 (PyObject *self, PyObject *args) readLongN(5);
PyObject * def_readLong6 (PyObject *self, PyObject *args) readLongN(6);
PyObject * def_readLong7 (PyObject *self, PyObject *args) readLongN(7);
PyObject * def_readLong8 (PyObject *self, PyObject *args) readLongN(8);

