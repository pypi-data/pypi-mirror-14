#!/usr/bin/env python

f = open ("wissen/__init__.py", "r")
for line in f:
	if line.startswith ("VERSION"):		
		__VER__ = line [10:].strip ()[1:-1]
		break
f.close ()

import os
import glob
from warnings import warn

try:
	from setuptools import setup, Extension
except ImportError:	
	from distutils.core import setup, Extension
from distutils.sysconfig import get_python_lib		
import platform
import sys

if sys.argv[-1] == 'publish':
	os.system('python setup.py sdist upload') # bdist_wininst --target-version=2.7
	sys.exit()

modules = []

dirv = "%d.%d" % sys.version_info [:2]
osbit, _dummy = platform.architecture()
dira = osbit == "32bit" and "x86" or "x64"

if os.name == "nt":
	include_dirs = [
		"wissen/win32inclib/zlib/%s" % dira, 
		"wissen/win32inclib/pthread2/%s" % dira
	]
	library_dirs = include_dirs
	libraries = ["zlib", "pthreadVC2"]
		
else:
	include_dirs = ["/usr/include/x86_64-linux-gnu", "/usr/include"]
	library_dirs = ["/usr/lib/x86_64-linux-gnu", "/usr/lib"]
	libraries = ["z", "pthread"]

module = Extension(
	'wissen._wissen',
	sources = [
		'wissen/extension/wissen/core.c', 
		'wissen/extension/wissen/analyzer/analyzer.c',		
		'wissen/extension/wissen/analyzer/stopword.c', 
		'wissen/extension/wissen/analyzer/endword.c', 
		'wissen/extension/wissen/analyzer/formalizer.c', 		
		'wissen/extension/wissen/analyzer/stem.c',
		'wissen/extension/wissen/analyzer/stem_de.c',
		'wissen/extension/wissen/analyzer/stem_fr.c',
		'wissen/extension/wissen/analyzer/stem_it.c',
		'wissen/extension/wissen/analyzer/stem_fi.c',
		'wissen/extension/wissen/analyzer/stem_es.c',
		'wissen/extension/wissen/analyzer/stem_hu.c',
		'wissen/extension/wissen/analyzer/stem_pt.c',
		'wissen/extension/wissen/analyzer/stem_sv.c',
		'wissen/extension/wissen/analyzer/stem_ar.c',
		'wissen/extension/wissen/analyzer/removeaccents.c',
		'wissen/extension/wissen/index/sort.c', 
		'wissen/extension/wissen/index/osutil.c', 
		'wissen/extension/wissen/index/search.c', 
		'wissen/extension/wissen/index/compfunc.c',
		'wissen/extension/wissen/index/heapsort.c', 
		'wissen/extension/wissen/index/termhashtable.c', 
		'wissen/extension/wissen/index/generichash.c',
		'wissen/extension/wissen/index/bfile.c', 
		'wissen/extension/wissen/index/zip.c',
		'wissen/extension/wissen/index/mempool.c',
		'wissen/extension/wissen/index/ibucket.c',
		'wissen/extension/wissen/index/util.c',
		'wissen/extension/wissen/mod_analyzer.c',		
		'wissen/extension/wissen/mod_util.c', 
		'wissen/extension/wissen/mod_int.c', 
		'wissen/extension/wissen/mod_bits.c', 
		'wissen/extension/wissen/mod_mergeinfo.c', 
		'wissen/extension/wissen/mod_document.c',
		'wissen/extension/wissen/mod_posting.c', 
		'wissen/extension/wissen/mod_termtable.c',
		'wissen/extension/wissen/mod_terminfo.c',
		'wissen/extension/wissen/mod_sortmap.c',   
		'wissen/extension/wissen/mod_memorypool.c',		
		'wissen/extension/wissen/mod_selector.c',		
		'wissen/extension/wissen/mod_classifier.c',
		'wissen/extension/wissen/mod_dbint.c',
		'wissen/extension/wissen/mod_calculator.c',
		'wissen/extension/wissen/mod_binfile.c',		
		'wissen/extension/wissen/mod_sgmlparser.c',
		'wissen/extension/wissen/mod_compute.c',
	],
	include_dirs = include_dirs,
	library_dirs = library_dirs,
	libraries = libraries
)
modules.append (module)

packages = [
	'wissen',
	'wissen.analyzers',
	'wissen.analyzers.util',
	'wissen.searcher',	
	'wissen.searcher.segment',
	'wissen.classifier',	
	'wissen.classifier.classifiers',
	'wissen.classifier.segment',	
	'wissen.cluster',
	'wissen.util',
	'wissen.lib'
]

package_dir = {
	'wissen': 'wissen'
}
   
data_files = [
	"README.md",
	"extension/wissen/*.*",
	"extension/wissen/analyzer/*.*",
	"extension/wissen/index/*.*",	
	"extension/wissen/win32/*.*",	
	"win32inclib/pthread2/msvcr90.dll",
	"win32inclib/pthread2/x64/*.*",
	"win32inclib/pthread2/x86/*.*",
	"win32inclib/zlib/x64/*.*",
	"win32inclib/zlib/x86/*.*"
]

if os.name == "nt" and ("build" in sys.argv or "install" in sys.argv):
	import shutil		
	if os.path.isfile ("wissen/pthreadVC2.dll"):
		os.remove ("wissen/pthreadVC2.dll")
	shutil.copy ("wissen/win32inclib/pthread2/%s/pthreadVC2.dll" % dira, "wissen/pthreadVC2.dll")
	
	if os.path.isfile ("wissen/msvcr90.dll"):
		os.remove ("wissen/msvcr90.dll")
	shutil.copy ("wissen/win32inclib/pthread2/msvcr90.dll", "wissen/msvcr90.dll")
	
	data_files.extend (["pthreadVC2.dll", "msvcr90.dll"])
	
package_data = {
	"wissen": data_files
}

classifiers = [
  'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
  'Development Status :: 2 - Pre-Alpha',
  'Environment :: Console',	
	'Topic :: Software Development :: Libraries :: Python Modules',
	'Intended Audience :: Developers',
	'Intended Audience :: Science/Research',
	'Programming Language :: Python',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3',
	'Topic :: Text Processing :: Indexing'	
]


setup (
	name = 'wissen',
	version = __VER__,
	author = 'Hans Roh',
	description='Wissen Full-Text Search & Classify Engine',
	author_email = 'hansroh@gmail.com',
	url = 'http://osp.skitai.com',
	packages=packages,
	package_dir=package_dir,
	package_data = package_data,
	license='BSD',
	platforms = ["posix", "nt"],
	download_url = "https://pypi.python.org/pypi/wissen",
	classifiers=classifiers,
	ext_modules = modules
)

