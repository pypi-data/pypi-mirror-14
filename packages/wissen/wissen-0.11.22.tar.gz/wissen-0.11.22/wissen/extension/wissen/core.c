#include <Python.h>
#include "core.h"
#include <stdio.h>
//#include <crtdbg.h>

static PyMethodDef coreMethods[] = {
	// py_anlayzer.h
	{"factorial",  def_factorial, METH_VARARGS, 	""},
	{"Rmn",  def_Rmn, METH_VARARGS, 	""},
	{"MImn",  def_MImn, METH_VARARGS, 	""},
	{"ORmn",  def_ORmn, METH_VARARGS, 	""},
	{"IGmn",  def_IGmn, METH_VARARGS, 	""},
	
	{"zcompress",  	def_zcompress, 	METH_VARARGS, 	""},
	{"zdecompress",  	def_zdecompress, 	METH_VARARGS, 	""},
	{"getdiskspace",  	def_getdiskspace, 	METH_VARARGS, 	""},
	
	{"encodeVInt",  	def_writeVInt, 	METH_VARARGS, 	""},
	{"decodeVInt",  	def_readVInt, 	METH_VARARGS, 	""},
	{"encodeVLong",  	def_writeVLong, 	METH_VARARGS, 	""},
	{"decodeVLong",  	def_readVLong, 	METH_VARARGS, 	""},
	{"encodeInt",def_writeInt, METH_VARARGS, ""},
	{"decodeInt",def_readInt, METH_VARARGS, ""},
	
	{"decodeInt1",def_readInt1, METH_VARARGS, ""},
	{"decodeInt2",def_readInt2, METH_VARARGS, ""},
	{"decodeInt3",def_readInt3, METH_VARARGS, ""},
	{"decodeInt4",def_readInt4, METH_VARARGS, ""},
	{"decodeLong5",def_readLong5, METH_VARARGS, ""},
	{"decodeLong6",def_readLong6, METH_VARARGS, ""},
	{"decodeLong7",def_readLong7, METH_VARARGS, ""},
	{"decodeLong8",def_readLong8, METH_VARARGS, ""},	
	{"encodeInt1",def_writeInt1, METH_VARARGS, ""},
	{"encodeInt2",def_writeInt2, METH_VARARGS, ""},
	{"encodeInt3",def_writeInt3, METH_VARARGS, ""},
	{"encodeInt4",def_writeInt4, METH_VARARGS, ""},
	{"encodeLong5",def_writeLong5, METH_VARARGS, ""},
	{"encodeLong6",def_writeLong6, METH_VARARGS, ""},
	{"encodeLong7",def_writeLong7, METH_VARARGS, ""},
	{"encodeLong8",def_writeLong8, METH_VARARGS, ""},
	
	{"SGMLParser", _sgmlop_sgmlparser, 1},
  {"XMLParser", _sgmlop_xmlparser, 1},    
  {NULL, 			NULL, 			0, 				NULL}
};


extern PyTypeObject FastParser_Type;
extern PyTypeObject BitVectorType;
extern PyTypeObject DocumentType;
extern PyTypeObject TermTableType;
extern PyTypeObject PostingType;
extern PyTypeObject TermInfoType;
extern PyTypeObject SortMapType;
extern PyTypeObject MergeInfoType;
extern PyTypeObject MemoryPoolType;
extern PyTypeObject ComputeType;
extern PyTypeObject SelectorType;
extern PyTypeObject ClassifierType;
extern PyTypeObject DBIntType;
extern PyTypeObject CalculatorType;
extern PyTypeObject AnalyzerType;
extern PyTypeObject BinFileType;

#if PY_MAJOR_VERSION >= 3
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "_wissen",     /* m_name */
        "Wissen Core",  /* m_doc */
        -1,                  /* m_size */
        coreMethods,    /* m_methods */
        NULL,                /* m_reload */
        NULL,                /* m_traverse */
        NULL,                /* m_clear */
        NULL,                /* m_free */
    };
#endif


static PyObject* moduleinit (void)
{
    PyObject* m;

/*
#if PY_MAJOR_VERSION >= 3
    PyType_Ready(FastParser_Type);
#else
		FastParser_Type.ob_type = &PyType_Type;
#endif
*/
    if (PyType_Ready(&FastParser_Type) < 0) return NULL; 
    if (PyType_Ready(&BitVectorType) < 0) return NULL; 
    if (PyType_Ready(&DocumentType) < 0) return NULL; 
    if (PyType_Ready(&TermTableType) < 0) return NULL; 
    if (PyType_Ready(&PostingType) < 0) return NULL; 
    if (PyType_Ready(&TermInfoType) < 0) return NULL; 
    if (PyType_Ready(&SortMapType) < 0) return NULL;     
    if (PyType_Ready(&MergeInfoType) < 0) return NULL;     
    if (PyType_Ready(&MemoryPoolType) < 0) return NULL;     
    if (PyType_Ready(&ComputeType) < 0) return NULL;           
    if (PyType_Ready(&SelectorType) < 0) return NULL;           
    if (PyType_Ready(&ClassifierType) < 0) return NULL;           
    if (PyType_Ready(&DBIntType) < 0) return NULL;           
    if (PyType_Ready(&CalculatorType) < 0) return NULL;       
    if (PyType_Ready(&AnalyzerType) < 0) return NULL;       
    if (PyType_Ready(&BinFileType) < 0) return NULL;       

#if PY_MAJOR_VERSION >= 3  
    m = PyModule_Create(&moduledef);
#else    
    m = Py_InitModule3("_wissen", coreMethods, "Wissen Core");
#endif
    
    if (m == NULL) return NULL;
    
    Py_INCREF(&BitVectorType);
    Py_INCREF(&DocumentType);
    Py_INCREF(&TermTableType);
    Py_INCREF(&PostingType);
    Py_INCREF(&TermInfoType);
    Py_INCREF(&SortMapType);
    Py_INCREF(&MergeInfoType);
    Py_INCREF(&MemoryPoolType);
    Py_INCREF(&ComputeType);    
    Py_INCREF(&SelectorType);        
    Py_INCREF(&ClassifierType);   
    Py_INCREF(&DBIntType);   
    Py_INCREF(&CalculatorType);   
    Py_INCREF(&AnalyzerType);   
    Py_INCREF(&BinFileType);
        
    PyModule_AddObject(m, "BitVector", (PyObject *) &BitVectorType);    
    PyModule_AddObject(m, "Document", (PyObject *) &DocumentType);    
    PyModule_AddObject(m, "TermTable", (PyObject *) &TermTableType);    
    PyModule_AddObject(m, "Posting", (PyObject *) &PostingType);    
    PyModule_AddObject(m, "TermInfo", (PyObject *) &TermInfoType);    
    PyModule_AddObject(m, "SortMap", (PyObject *) &SortMapType);    
    PyModule_AddObject(m, "MergeInfo", (PyObject *) &MergeInfoType);    
    PyModule_AddObject(m, "MemoryPool", (PyObject *) &MemoryPoolType);    
    PyModule_AddObject(m, "Compute", (PyObject *) &ComputeType);        
    PyModule_AddObject(m, "Selector", (PyObject *) &SelectorType);    
    PyModule_AddObject(m, "Classifier", (PyObject *) &ClassifierType);        
    PyModule_AddObject(m, "DBInt", (PyObject *) &DBIntType);        
    PyModule_AddObject(m, "Calculator", (PyObject *) &CalculatorType);        
    PyModule_AddObject(m, "Analyzer", (PyObject *) &AnalyzerType);
    PyModule_AddObject(m, "BinFile", (PyObject *) &BinFileType);  
    
    return m;  
}

#if PY_MAJOR_VERSION >= 3
	PyObject* PyInit__wissen (void) {
		return moduleinit ();
	}
#else
	void init_wissen (void) {
		moduleinit ();	
	}
#endif

