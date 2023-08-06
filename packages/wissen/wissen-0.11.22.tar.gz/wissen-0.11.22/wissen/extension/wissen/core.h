#ifndef CORE_CORE_H
#define CORE_CORE_H

#include "Python.h"
//#include "capsulethunk.h"

#define PyCObject_FromVoidPtr(pointer, destructor) \
	(PyCapsule_New(pointer, NULL, destructor))

#define PyCObject_AsVoidPtr(capsule) \
  (PyCapsule_GetPointer(capsule, NULL))
    
#if PY_VERSION_HEX >= 0x02000000
#define SGMLOP_GC
#endif

#define SW_VALID_YEAR 3000

PyObject* CoreError;
PyObject*_sgmlop_sgmlparser(PyObject* self, PyObject* args);
PyObject* _sgmlop_xmlparser(PyObject* self, PyObject* args);

/* integrated into Analyzer Class at 2014.6.12
PyObject * def_stem (PyObject *self, PyObject *args);
PyObject * def_weakstem (PyObject *self, PyObject *args);
PyObject * def_isstopword (PyObject *self, PyObject *args);
*/

PyObject * def_writeVInt (PyObject *self, PyObject *args);
PyObject * def_readVInt (PyObject *self, PyObject *args);
PyObject * def_writeVLong (PyObject *self, PyObject *args);
PyObject * def_readVLong (PyObject *self, PyObject *args);

PyObject * def_readInt (PyObject *self, PyObject *args);
PyObject * def_writeInt (PyObject *self, PyObject *args);

PyObject * def_writeInt1 (PyObject *self, PyObject *args);
PyObject * def_writeInt2 (PyObject *self, PyObject *args);
PyObject * def_writeInt3 (PyObject *self, PyObject *args);
PyObject * def_writeInt4 (PyObject *self, PyObject *args);
PyObject * def_writeLong5 (PyObject *self, PyObject *args);
PyObject * def_writeLong6 (PyObject *self, PyObject *args);
PyObject * def_writeLong7 (PyObject *self, PyObject *args);
PyObject * def_writeLong8 (PyObject *self, PyObject *args);

PyObject * def_readInt1 (PyObject *self, PyObject *args);
PyObject * def_readInt2 (PyObject *self, PyObject *args);
PyObject * def_readInt3 (PyObject *self, PyObject *args);
PyObject * def_readInt4 (PyObject *self, PyObject *args);
PyObject * def_readLong5 (PyObject *self, PyObject *args);
PyObject * def_readLong6 (PyObject *self, PyObject *args);
PyObject * def_readLong7 (PyObject *self, PyObject *args);
PyObject * def_readLong8 (PyObject *self, PyObject *args);

PyObject * def_zcompress (PyObject *self, PyObject *args);
PyObject * def_zdecompress (PyObject *self, PyObject *args);

PyObject * def_getdiskspace (PyObject *self, PyObject *args);
PyObject * def_factorial (PyObject *self, PyObject *args);
PyObject * def_Rmn (PyObject *self, PyObject *args);
PyObject * def_MImn (PyObject *self, PyObject *args);
PyObject * def_ORmn (PyObject *self, PyObject *args);
PyObject * def_IGmn (PyObject *self, PyObject *args);


/*****************************************************************************
buffered file
*****************************************************************************/

#define bwriteInt(bfile, i32, int_length) {\
	_uint = i32;\
	_shift = 0;\
	while ((_shift >> 3) < int_length) {\
		if (bfile->position == bfile->max) {\
			if (bflush (bfile) == -1) {\
				if (bfile->errcode == 1) { goto memoryerror;}\
				else if (bfile->errcode == 2) { goto iowriteerror;}\
			}\
		}\
		bfile->buffer [bfile->position++] = (unsigned char)( _uint >> _shift & 0xff);\
    	_shift += 8;\
	}\
}

#define breadInt(bfile, i32, int_length) {\
			i32 = 0;\
    	_shift = 0;\
    	while ((_shift >> 3) < int_length) {\
    		if (bfile->position == bfile->__readsize) {\
    			if (brefill (bfile) == -1) {\
    				if (bfile->errcode == 2) { goto ioreaderror; }\
    			}\
    		}\
    		_uchar = bfile->buffer [bfile->position++];\
    		if (int_length <= 4) {\
    			i32 |= (unsigned int)_uchar << _shift;\
    		} else {\
    			i32 |= (unsigned long long)_uchar << _shift;\
    		}\
    		_shift += 8;\
    	}\
}

#define bwriteLong(bfile, i64, int_length) {\
	_shift = 0;\
	_ulong = i64;	\
	while ((_shift >> 3) < int_length) {\
		if (bfile->position == bfile->max) {\
			if (bflush (bfile) == -1) {\
				if (bfile->errcode == 1) { goto memoryerror; }\
				else if (bfile->errcode == 2) { goto iowriteerror;}\
			}\
		}\
    		bfile->buffer [bfile->position++] = (unsigned char)( _ulong >> _shift & 0xff);\
    		_shift += 8;\
	}\
}

#define breadLong(bfile, i64, int_length) {\
		 _shift = 0;\
    	i64 = 0;\
    	while ((_shift >> 3) < int_length) {\
    		if (bfile->position == bfile->__readsize) {\
    			if (brefill (bfile) == -1) {\
    				if (bfile->errcode == 2) { goto ioreaderror; }\
    			}\
    		}\
    		_uchar = bfile->buffer [bfile->position++]; \
    		i64 |= (unsigned long long) _uchar << _shift;\
    		_shift += 8;\
    	}\
}

#define bwriteVInt(bfile, i32) {\
	_uint = (unsigned int) i32;\
    	while ((_uint & ~0x7F) != 0) {\
    		if (bfile->position == bfile->max) {\
			if (bflush (bfile) == -1) {\
				if (bfile->errcode == 1) { goto memoryerror;}\
				else if (bfile->errcode == 2) { goto iowriteerror;}\
			}\
		}\
	    	bfile->buffer [bfile->position++] = (unsigned char) ((_uint & 0x7f) | 0x80);\
	    	_uint >>= 7;\
    	}\
    	if (bfile->position == bfile->max) {\
		bflush (bfile);\
		if (bfile->buffer == NULL) { goto memoryerror;}\
	}\
    	bfile->buffer [bfile->position++] = (unsigned char) _uint;\
}

#define breadVInt(bfile, i32) {\
	if (bfile->position == bfile->__readsize) {\
		if (brefill (bfile) == -1) {\
			if (bfile->errcode == 2) { goto ioreaderror; }\
		}\
	}\
	_uchar	 = bfile->buffer [bfile->position++];\
	i32 = _uchar & 0x7F;\
	for (_shift = 7; (_uchar & 0x80) != 0; _shift += 7) {\
		if (bfile->position == bfile->__readsize) {\
			if (brefill (bfile) == -1) {\
				if (bfile->errcode == 2) { goto ioreaderror; }\
			}\
		}\
		_uchar = bfile->buffer [bfile->position++];\
		i32 |= (_uchar & 0x7F) << _shift;\
	}\
}

#define bwriteVLong(bfile, i64) {\
	_ulong = (unsigned long long) i64;\
	while ((_ulong & ~0x7FL) != 0) {\
  	if (bfile->position == bfile->max) {\
			if (bflush (bfile) == -1) {\
				if (bfile->errcode == 1) { goto memoryerror;}\
			else if (bfile->errcode == 2) { goto iowriteerror;}\
			}\
		}\
    bfile->buffer [bfile->position++] = (unsigned char) ((_ulong & 0x7FL) | 0x80);\
    _ulong >>= 7;\
  }\
  if (bfile->position == bfile->max) {\
		bflush (bfile);\
		if (bfile->buffer == NULL) {PyErr_NoMemory (); ; goto iowriteerror;}\
	}\
  bfile->buffer [bfile->position++] = (unsigned char) _ulong;\
}

#define breadVLong(bfile, i64) {\
	if (bfile->position == bfile->__readsize) {\
		if (brefill (bfile) == -1) {\
			if (bfile->errcode == 2) { goto ioreaderror; }\
		}\
	}\
	_uchar	 = bfile->buffer [bfile->position++];\
    	i64 = _uchar & 0x7FL;\
    	for (_shift = 7; (_uchar & 0x80) != 0; _shift += 7) {\
    		if (bfile->position == bfile->__readsize) {\
    			if (brefill (bfile) == -1) {\
    				if (bfile->errcode == 2) { goto ioreaderror; }\
    			}\
    		}\
      		_uchar = bfile->buffer [bfile->position++];\
      		i64 |= (unsigned long long) (_uchar & 0x7FL) << _shift;\
    	}\
}

#define bwriteString(bfile, string, len) {\
	for (_shift = 0; _shift < (int) len; _shift ++) {\
		if (bfile->position == bfile->max) {\
			if (bflush (bfile) == -1) {\
				if (bfile->errcode == 1) { goto memoryerror;}\
				else if (bfile->errcode == 2) { goto iowriteerror;}\
			}\
		}\
		bfile->buffer [bfile->position++] = string [_shift];\
	}\
}

#define breadString(bfile, string, len) {\
	for (_shift = 0; _shift < (int) len; _shift ++) {\
		if (bfile->position == bfile->__readsize) {\
    			if (brefill (bfile) == -1) {\
    				if (bfile->errcode == 2) { goto ioreaderror; }\
    			}\
    		}\
		string [_shift] = bfile->buffer [bfile->position++];\
	}\
}

#endif

