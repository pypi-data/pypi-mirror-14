/*
 * SGMLOP
 * $Id: //modules/sgmlop/sgmlop.c#20 $
 *
 * The sgmlop accelerator module
 *
 * This module provides a FastParser type, which is designed to speed
 * up the standard sgmllib and xmllib modules.  The parser can be
 * configured to support either basic SGML (enough of it to process
 * HTML documents, at least) or XML.
 *
 * History:
 * 1998-04-04 fl  Created (for coreXML)
 * 1998-04-05 fl  Added close method
 * 1998-04-06 fl  Added parse method, revised callback interface
 * 1998-04-14 fl  Fixed parsing of PI tags
 * 1998-05-14 fl  Cleaned up for first public release
 * 1998-05-19 fl  Fixed xmllib compatibility: handle_proc, handle_special
 * 1998-05-22 fl  Added attribute parser
 * 1999-06-20 fl  Added Element data type, various bug fixes.
 * 2000-05-28 fl  Fixed data truncation error (@XML1)
 * 2000-05-28 fl  Added temporary workaround for unicode problem (@XML2)
 * 2000-05-28 fl  Removed optional close argument (@XML3)
 * 2000-05-28 fl  Raise exception on recursive feed (@XML4)
 * 2000-07-05 fl  Fixed attribute handling in empty tags (@XML6) (release 1.0)
 * 2001-10-01 fl  Release buffer on close
 * 2001-10-01 fl  Added built-in support for standard entities (@XML8)
 * 2001-10-01 fl  Removed experimental Element data type
 * 2001-10-01 fl  Added support for hexadecimal character references
 * 2001-10-02 fl  Improved support for doctype parsing
 * 2001-10-02 fl  Optional well-formedness checker
 * 2001-12-18 fl  Flag missing entity handler only in strict mode (@XML12)
 * 2001-12-29 fl  Fixed compilation under gcc -Wstrict
 * 2002-01-13 fl  Resolve entities in attributes 
 * 2002-03-26 fl  PyArg_NoArgs is deprecated; replace with PyArg_ParseTuple
 * 2002-05-26 fl  Don't mess up on <empty/> tags (@XML20)
 * 2002-11-13 fl  Changed handling of large character entities (@XML15)
 * 2002-11-13 fl  Added support for garbage collection (@XML15)
 * 2003-09-07 fl  Fixed parsing of short PI's (@XMLTOOLKIT24)
 * 2003-09-07 fl  Fixed garbage collection support for Python 2.2 and later
 * 2004-04-04 fl  Fixed parsing of non-ascii attribute values (@XMLTOOLKIT38)
 *
 * Copyright (c) 1998-2003 by Secret Labs AB
 * Copyright (c) 1998-2003 by Fredrik Lundh
 * 
 * fredrik@pythonware.com
 * http://www.pythonware.com
 *
 * By obtaining, using, and/or copying this software and/or its
 * associated documentation, you agree that you have read, understood,
 * and will comply with the following terms and conditions:
 * 
 * Permission to use, copy, modify, and distribute this software and its
 * associated documentation for any purpose and without fee is hereby
 * granted, provided that the above copyright notice appears in all
 * copies, and that both that copyright notice and this permission notice
 * appear in supporting documentation, and that the name of Secret Labs
 * AB or the author not be used in advertising or publicity pertaining to
 * distribution of the software without specific, written prior
 * permission.
 * 
 * SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO
 * THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
 * FITNESS.  IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
 * OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

/* FIXME: basic well-formedness checking */
/* FIXME: add (some kind of) unicode support */
/* FIXME: suppress trailing > after dtd endtag */
/* FIXME: basic structural validation? */

static char copyright[] =
    " SGMLOP 1.1 Copyright (c) 1998-2003 by Secret Labs AB ";

#include "Python.h"
#include <ctype.h>

#ifdef SGMLOP_UNICODE_SUPPORT
/* use wide character set (experimental) */
/* FIXME: under Python 1.6, the current version converts Unicode
   strings to UTF-8, and parses the result as if it was an ASCII
   string. */
#define CHAR_T  Py_UNICODE
#define ISALNUM Py_UNICODE_ISALNUM
#define TOLOWER Py_UNICODE_TOLOWER
#else
/* 8-bit character set */
#define CHAR_T  unsigned char
#define ISALNUM isalnum
#define TOLOWER tolower
#endif

#if PY_VERSION_HEX >= 0x02000000
/* use garbage collection (requires Python 2.0 or later) */
#define SGMLOP_GC

/* from http://python.ca/nas/python/type-gc.html */
#if defined(Py_TPFLAGS_GC) && !defined(Py_TPFLAGS_HAVE_GC)
/* Python 2.2 GC compatibility macros */
#define Py_TPFLAGS_HAVE_GC Py_TPFLAGS_GC
#define PyObject_GC_New PyObject_New
#define PyObject_GC_Del PyObject_Del
#define PyObject_GC_Track PyObject_GC_Init
#define PyObject_GC_UnTrack PyObject_GC_Fini
#endif

#ifndef Py_TPFLAGS_HAVE_GC
/* no GC */
#define Py_TPFLAGS_HAVE_GC 0
#define PyObject_GC_New PyObject_New
#define PyObject_GC_Del PyObject_Del
#define PyObject_GC_Track
#define PyObject_GC_UnTrack
#define PyGC_HEAD_SIZE 0
typedef int (*visitproc)(PyObject *, void *);
typedef int (*traverseproc)(PyObject *, visitproc, void *);
#endif

#endif


