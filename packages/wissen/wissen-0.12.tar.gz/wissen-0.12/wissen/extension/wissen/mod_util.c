#include "Python.h"
#include "index/index.h"
#include <math.h>

PyObject *
def_zcompress (PyObject *self, PyObject *args) {
	char* c;
	int len;
	BFILE* zd;
	PyObject* res;
	
	if (!PyArg_ParseTuple(args, "s#", &c, &len)) return NULL;
	
	if (!(zd = bopen (-1, 'w', 1024, 1))) return PyErr_NoMemory ();
	zcompress (c, len, zd, 0);	
  res = PyBytes_FromStringAndSize (zd->buffer, zd->position);
  bclose (zd);        
  return res;
}

PyObject *
def_zdecompress (PyObject *self, PyObject *args) {
	char* c;
	int len;
	BFILE* zd;
	PyObject* res;
	
	if (!PyArg_ParseTuple(args, "s#", &c, &len)) return NULL;
	
	if (!(zd = bopen (-1, 'w', 1024, 1))) return PyErr_NoMemory ();
	zdecompress (c, len, zd);
	
        res = PyBytes_FromStringAndSize (zd->buffer, zd->position);
        bclose (zd);
        return res;
}

PyObject*
def_getdiskspace (PyObject *self, PyObject *args) {	
	char* dir;
	if (!PyArg_ParseTuple(args, "s", &dir)) return NULL;
	
	return PyLong_FromLongLong (getdiskspace (dir));
}

PyObject*
def_factorial (PyObject *self, PyObject *args) {	
	int n, f = 0;
	if (!PyArg_ParseTuple(args, "i", &n)) return NULL;
	for (; n; f += n--)	{
	}
	return PyLong_FromLong (f);
}

PyObject *
def_Rmn (PyObject *self, PyObject *args)
{
	int _D, _m, _n, _co;
	double D, m, n, co;
	double P, R;
	
	if (!PyArg_ParseTuple(args, "iiii", &_D, &_m, &_n, &_co)) return NULL;	
	
	D=_D; m=_m; n=_n, co=_co;
	P = (m / D) * (n / D);
	R = pow (P, co) * pow ((1.- P), D - co) * (factorial (D) / (factorial (_co) * factorial (_D - _co)));
	if (!R) {
		return PyFloat_FromDouble (100.);
	}
	R = -1. * log (R);
	return PyFloat_FromDouble (R);	
}

PyObject *
def_MImn (PyObject *self, PyObject *args)
{
	int _D, _m, _n, _co;
	double D, m, n, co;
	double R;	
	if (!PyArg_ParseTuple(args, "iiii", &_D, &_m, &_n, &_co)) return NULL;		
	D=_D; m=_m; n=_n, co=_co;
	R = log ((co * D) / ((co + m) * (co + n)));
	return PyFloat_FromDouble (R);	
}


PyObject *
def_ORmn (PyObject *self, PyObject *args)
{
	int _D, _m, _n, _co;
	double D, m, n, co;
	double R;	
	if (!PyArg_ParseTuple(args, "iiii", &_D, &_m, &_n, &_co)) return NULL;		
	D=_D; m=_m; n=_n, co=_co;
	R = log ((co * (D - m - n)) / (m * n));
	return PyFloat_FromDouble (R);	
}

PyObject *
def_IGmn (PyObject *self, PyObject *args)
{
	int _D, _m, _n, _co;
	double D, m, n, co;
	double R, MI;
	
	if (!PyArg_ParseTuple(args, "iiii", &_D, &_m, &_n, &_co)) return NULL;	
	D=_D; m=_m; n=_n, co=_co;
	MI = log ((co * D) / (m * n));
	R = 0;
	R += (co / D);
	R += (m / D);
	R += (n / D);
	R += ((D-(m+n-co)) / D);
	return PyFloat_FromDouble (R * MI);
}

