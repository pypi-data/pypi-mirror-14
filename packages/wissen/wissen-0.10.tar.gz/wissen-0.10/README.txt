Wissen Full-Text Search & Classify Engine
===========================================

Copyright (c) 2015 by Hans Roh

License: GPLv3


Introduce
----------

Wissen Search & Classify Engine is a simple search engine mostly written in Python and C in year 2008.

At that time, I would like to study Lucene_ earlier version. But I hate Java, so I had studied with Lupy_ and CLucene_. And I also had maden my own search engine for excercise.

Its file format, numeric compressing algorithm, indexing process are quiet similar with Lucene. But I got tired reverse engineering, so query and result-fetching parts was built from my imagination. As a result it's entirely unorthodox and possibly very inefficient.

But It's relatively simple and easy modifiable, I has been using some works.

.. _Lucene: https://lucene.apache.org/core/
.. _Lupy: https://pypi.python.org/pypi/Lupy
.. _CLucene: http://clucene.sourceforge.net/


Install
---------

.. code:: python

    sudo pip install wissen
    

Quick Start
-------------

**Full Text Index and Search**

.. code:: python

    import wissen
    
    # indexing
    analyzer = wissen.standard_analyzer (max_term = 3000)
    col = wissen.collection ("./col", wissen.CREATE, analyzer)
    indexer = col.get_indexer ()
    
    song = u"violin sonata in c k.301"
    composer = u"wolfgang amadeus mozart"
    birth = 1756
    home = u"50.665629/8.048906" # Lattitude / Longitude of Salzurg
    genre = u"01011111" # (rock serenade jazz piano symphony opera quartet sonata)
    
    document = wissen.document ()
    document.set_content ([song, composer])
    document.set_auto_snippet (song)
    
    document.add_field ("default", song, wissen.TEXT)
    document.add_field ("composer", composer, wissen.TEXT)
    document.add_field ("birth", birth, wissen.INT16)
    document.add_field ("genre", genre, wissen.BIT8)
    document.add_field ("home", home, wissen.COORD)
    
    indexer.add_document (document)
    indexer.close ()
        
    # searching
    analyzer = wissen.standard_analyzer (max_term = 8)
    col = wissen.collection ("./col", wissen.READ, analyzer)
    searcher = col.get_searcher ()
    print searcher.query (u'violin', offset = 0, fetch = 2, sort = "tfidf", summary = 30)
    searcher.close ()
    

Result will be like this:

.. code:: python
    
    {
    	'code': 200, 
    	'time': 0, 
    	'total': 1
    	'result': [
    		[
	    			[u'violin sonata in c k.301', u'wofgang amadeus mozart'], # content
	    			'<b>violin</b> sonata in c k.301', # auto snippet
	    			14, 0, 0, 0 # additional info
    		]
    	],     	
    	'sorted': [None, 0], 
    	'regex': 'violin|violins',     	
    }
    

**Full Text Classification**

.. code:: python

   import wissen
   
   # learning
   mdl = wissen.model ("./mdl", wissen.CREATE)
   learner = mdl.get_learner ()
   
   document = wissen.labeled_document ("Play Golf", "cloudy windy warm")
   learner.add_document (document)	
   document = wissen.labeled_document ("Play Golf", "windy sunny warm")
   learner.add_document (document)	
   document = wissen.labeled_document ("Go To Bed", "cold rainy")
   learner.add_document (document)	
   document = wissen.labeled_document ("Go To Bed", "windy rainy warm")
   learner.add_document (document)
   
   learner.build (min_df = 0) # build corpus
   learner.train (wissen.ALL, prune_df_max = 100, selector = wissen.CHI2, select_way = wissen.MAX, select_ratio = 0.99)
   
   learner.close ()
   
   
   # gusessing
   
   mdl = wissen.model ("./mdl")
   classifier = mdl.get_classifier ()
   print classifier.guess ("rainy cold")
   print classifier.guess ("rainy cold", wissen.FEATUREVOTE)
   print classifier.guess ("rainy cold", wissen.NAIVEBAYES)
   print classifier.guess ("rainy cold", wissen.TFIDF)
   print classifier.guess ("rainy cold", wissen.SIMILARITY)
   classifier.close ()
   

Result will be like this:

.. code:: python

    {
    	'code': 200, 
    	'total': 1, 
    	'time': 5,
    	'result': [
    		('Go To Bed', 1.0)
    	]
    }


Searchable Field Types
----------------------

- TEXT: analyzable full-text
- TERM: analyzable full-text but position data will not be indexed
- STRING: exactly string match like nation codes
- LIST: comma seperated STRING
- COORDn, n=4,6,8 decimal precision: latitude, longititude, result-sortable
- BITn, n=8,16,24,32,40,48,56,64: bitwise operation 
- INTn, n=8,16,24,32,40,48,56,64: range, result-sortable

For more information, see wissen/\_\_init\_\_.py


Stemming & N-Gram For International Languages
----------------------------------------------

Wissen has some kind of stemmers and n-gram methods for international languages and can use them by this way:

.. code:: python

    analyzer = standard_analyzer (ngram = True, stem_level = 1)
    col = wissen.collection ("./col", wissen.CREATE, analyzer)
    indexer = col.get_indexer ()
    document.add_field ("default", song, wissen.TEXT, lang = "en")


The default strategy of standard_analyzer is (ngram = True, stem_level = 1):

- Step 1: index to bigram for CJK (Chinese, Japanese, Korean)
- Step 2: stemming text by lang parameter if lang has stemmer
- Step 3: index to tri-gram for the other langugaes

**Automatic Bi-Gram**

If ngram is set to True, These languages will be indexed with bi-gram.

- cn: Chinese
- jp: Japanese
- ko: Korean


**Implemented Stemmers**

Except English stemmer, all stemmers can be obtained at `IR Multilingual Resources at UniNE`__.

- ar: Arabic
- de: German
- en: English
- es: Spanish
- fi: Finnish
- fr: French
- hu: Hungarian
- it: Italian
- pt: Portuguese
- sv: Swedish

 
.. __: http://members.unine.ch/jacques.savoy/clef/index.html

    

Query Syntax
--------------

- violin composer:mozart birth:1700~1800
- violin allcomposer:wolfgang mozart
- violin -sonata birth:~1800
- violin -composer:mozart
- violin or piano genre:00001101/all
- violin or ((piano composer:mozart) genre:00001101/any)
- (violin or ((allcomposer:mozart wolfgang) -amadeus)) sonata (genre:00001101~none home:50.6656,8.0489~10)
- "violin sonata" genre:00001101/none
- "violin^3 piano" -composer:"ludwig van beethoven"
- "violin sonata" genre:00001101/none home:50.6656/8.0489~10 # within 10M from (50.6656, 8.0489)


Full-Text Classifiers
----------------------

- META: default guessing, merging results with below classifiers
- NAIVEBAYES
- FEATUREVOTE
- TFIDF
- SIMILARITY

For more information, see wissen/classifier/classifiers/\*.py


Note for Multi-threading and Multiple Collection
------------------------------------------------

Indexing & learning support only single thread.

Searching & guessing is thread-safe, only if you use threads-pool way.

If you create 8 threads for search, you should configure wissen.

.. code:: python

    wissen.configure (numthread = 8)
    

Now you can open multiple collections (or models) and access with 8 threads.

If 9th thread try to access to wissen, it will raise error.


Core Class & Function Prototypes
----------------------------------

.. code:: python
    
    # logger
    from wissen.lib import logger    
    logger.screen_logger ()
    logger.rotate_logger ("/var/log/wissen")    
        
    # for multi threadiong env, init wissen
    wissen.configure (numthread, logger, io_buf_size = 8192, mem_limit = 256, max_segment_size = 0)
    
    #fianlly,
    wissen.shutdown ()
    
    wissen.standard_analyzer (max_term = 8, numthread = 1, **karg)
    
    karg will be:
      ngram = True or False
      stem_level = 1 or 2 (2 is only applied to English Language)
      stopwords_case_sensitive = True or False
      ngram_no_space = True or False
      strip_html = True or False

    col = wissen.collection (indexdir, mode = wissen.READ, analyzer = None, logger = None)
    col.setopt (key = value, ...)
    
    keys and default values will be:
      merge_factor = int
      force_merge = True or False
      max_memory = 10000000 (10Mb)
      optimize = True or False
      max_result = 2000
      num_query_cache = 200
    
    mdl = wissen.model (indexdir, mode = wissen.READ, analyzer = None, logger = None)
    mdl.setopt (key = value, ...)
    
    keys and default values will be:
      use_features_top = 0 # use all features


Documentation
--------------

Not yet.



Change Log
-------------
  
  0.10 - change version format, remove all str*_s ()
  
  0.9.0.5 - fix long long int, bit type
  
  0.9.0.3 - fix logger encoding

  0.9.0.2 - fix snippet-making
  
  0.9.0.1 - support Python 3.x

  0.8.0.13 - change license from BSD to GPL V3
  
	
