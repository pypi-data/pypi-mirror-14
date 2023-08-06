.. contents:: Table of Contents


Changes
=========

- Add Rocchino full-text classifier
- Changed learner.build() and train() args


Introduce
============

Wissen Search & Classification Engine is a simple search engine mostly written in Python and C in year 2008.

At that time, I would like to study Lucene_ earlier version with Lupy_ and CLucene_. And I also had maden my own search engine for excercise.

Its file format, numeric compressing algorithm, indexing process are quiet similar with Lucene. 

But I got tired reverse engineering, so query and result-fetching parts was built from my imagination. As a result it's entirely unorthodox and possibly very inefficient. Wissen's searching mechanism is similar with DNA-RNA-Protein working model translated into 'Index File-Temporary Small Replication Buffer-Qeury Result'.

* Every searcher (Cell) has a single index file handlers group (DNA group in nuclear)
* Thread has multiple small buffer (RNA) for replicating index as needed part
* Query class (Ribosome) creates qeury result (Protein) by synthesising buffers' inforamtion (RNAs)
* Repeat from 2nd if expected more results

.. _Lucene: https://lucene.apache.org/core/
.. _Lupy: https://pypi.python.org/pypi/Lupy
.. _CLucene: http://clucene.sourceforge.net/


Installation
=============

Wissen contains C extension, so need C compiler.
 
.. code:: bash

  pip install wissen
  

Quick Start
============

All field text type should be str or utf-8 encoded bytes in Python 3.x, and unicode or utf-8 encoded string in Python 2.7. Otherwise encoding should be specified.

Indexing and Searching
-------------------------

Here's an example indexing only one document.

.. code:: python

  import wissen
  
  # indexing
  analyzer = wissen.standard_analyzer (max_term = 3000)
  col = wissen.collection ("./col", wissen.CREATE, analyzer)
  indexer = col.get_indexer ()
  
  song = "violin sonata in c k.301"
  composer = u"wolfgang amadeus mozart"
  birth = 1756
  home = "50.665629/8.048906" # Lattitude / Longitude of Salzurg
  genre = "01011111" # (rock serenade jazz piano symphony opera quartet sonata)
  
  document = wissen.document ()
  
  # object to return, any object serializable by pickle
  document.set_content ([song, composer])
  
  # text content to generating auto snippet by given query terms
  document.set_auto_snippet (song)
  
  # add searchable fields
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
  ['violin sonata in c k.301', 'wofgang amadeus mozart'], # content
  '<b>violin</b> sonata in c k.301', # auto snippet
  14, 0, 0, 0 # additional info
  ]
  ],   
  'sorted': [None, 0], 
  'regex': 'violin|violins',   
  }
  

Learning and Classification
---------------------------

Here's an example guessing one of 'play golf', 'go to bed' by weather conditions.

.. code:: python

   import wissen
   
   analyzer = wissen.standard_analyzer (max_term = 3000)
   
   # learning
   
   mdl = wissen.model ("./mdl", wissen.CREATE, analyzer)
   learner = mdl.get_learner ()
   
   document = wissen.labeled_document ("Play Golf", "cloudy windy warm")
   learner.add_document (document)  
   document = wissen.labeled_document ("Play Golf", "windy sunny warm")
   learner.add_document (document)  
   document = wissen.labeled_document ("Go To Bed", "cold rainy")
   learner.add_document (document)  
   document = wissen.labeled_document ("Go To Bed", "windy rainy warm")
   learner.add_document (document)   
   learner.close ()
   
   mdl = wissen.model ("./mdl", wissen.MODIFY, analyzer)
   learner = mdl.get_learner ()
   learner.listbydf (min_df = 0) # show terms DF (Document Frequency) >= min_df
   learner.close ()
   
   mdl = wissen.model ("./mdl", wissen.MODIFY, analyzer)
   learner = mdl.get_learner ()
   learner.build (dfmin = 2) # build corpus DF >= 2
   learner.close ()
   
   mdl = wissen.model ("./mdl", wissen.MODIFY, analyzer)
   learner = mdl.get_learner ()
   learner.train (
   cl_for = wissen.ALL, # for which classifier
   selector = wissen.CHI2, # feature selecting method
   select = 0.99, # how many features?
   orderby = wissen.MAX, # feature ranking by what?
   dfmin = 2 # exclude DF < 2
   )
   learner.close ()
   
   
   # gusessing
   
   mdl = wissen.model ("./mdl", wissen.READ, analyzer)
   classifier = mdl.get_classifier ()
   print classifier.guess ("rainy cold")
   print classifier.guess ("rainy cold", cl = wissen.FEATUREVOTE)
   print classifier.guess ("rainy cold", cl = wissen.NAIVEBAYES)
   print classifier.guess ("rainy cold", cl = wissen.TFIDF)
   print classifier.guess ("rainy cold", cl = wissen.SIMILARITY)
   classifier.close ()
   

Result will be like this:

.. code:: python

  {
  'code': 200, 
  'total': 1, 
  'time': 5,
  'result': [('Go To Bed', 1.0)],
  'classifier': 'meta'  
  }


Limitation
==============

Before you test Wissen, you should know some limitation.

- Wissen search cannot sort by string type field, but can by int/bit/coord types and TFIDF ranking. 

- Wissen classification doesn't have purporse for accuracy but performance as realtime (means within 1 second) quessing. So I used relatvely simple and fast classification algorithms. If you need accuracy, it's not fit to you.


Configue Wissen
==================

When indexing/learing it's not necessory to configure, but searching/guessing it should be configure. The reason why Wissen allocates memory per thread for searching and classifying on initializing.

.. code:: python

  wissen.configure (
    numthread, 
    logger, 
    io_buf_size = 4096, 
    mem_limit = 256
  )

 
- numthread: number of threads which access to Wissen collections and models. if set to 8, you can open multiple collections (or models) and access with 8 threads. If 9th thread try to access to wissen, it will raise error

- logger: *see next chapter*

- io_buf_size = 4096: Bytes size of flash buffer for repliacting index files

- mem_limit = 256: Memory limit per a thread, but it's not absolute. It can be over during calculation if need, but when calcuation has been finished, would return memory ASAP.


Finally when your app is terminated, call shutdown.

.. code:: python

  wissen.shutdown ()
  

Logger
========

.. code:: python

  from wissen.lib import logger
  
  logger.screen_logger ()
  
  # it will create file '/var/log.wissen.log', and rotated by daily base
  logger.rotate_logger ("/var/log", "wissen", "daily")
  

Standard Analyzer
====================

Analyzer is needed by TEXT, TERM types.

Basic Usage is:

.. code:: python

  analyzer = wissen.standard_analyzer (
    max_term = 8, 
    numthread = 1,
    ngram = True or False,
    stem_level = 0, 1 or 2 (2 is only applied to English Language),
    make_lower_case = True or False,
    stopwords_case_sensitive = True or False,
    ngram_no_space = True or False,
    strip_html = True or False,    
    stopwords = [word,...]
  )

- stem_level: 0 and 1, especially 'en' language has level 2 for hard stemming

- make_lower_case: make lower case for every text

- stopwords_case_sensitive: it will work if make_lower_case is False

- ngram_no_space: if False, '泣斬 馬謖' will be tokenized to _泣, 泣斬, 斬\_, _馬, 馬謖, 謖\_. But if True, addtional bi-gram 斬馬 will be created between 斬\_ and _馬.

- strip_html

- stopwords: Wissen has only English stopwords list, You can use change custom stopwords. Stopwords sould be unicode or utf8 encoded bytes

Wissen has some kind of stemmers and n-gram methods for international languages and can use them by this way:

.. code:: python

  analyzer = standard_analyzer (ngram = True, stem_level = 1)
  col = wissen.collection ("./col", wissen.CREATE, analyzer)
  indexer = col.get_indexer ()
  document.add_field ("default", song, wissen.TEXT, lang = "en")


Implemented Stemmers
---------------------

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


Bi-Gram Index
----------------

If ngram is set to True, these languages will be indexed with bi-gram.

  - cn: Chinese
  - ja: Japanese
  - ko: Korean

Also note that if word contains only alphabet, will be used English stemmer.


Tri-Gram Index
---------------

The other languages will be used English stemmer if all spell is Alphabet. And if ngram is set to True, will be indexed with tri-gram if word has multibytes.

**Methods Spec**

  - analyzer.index (document, lang)
  - analyzer.freq (document, lang)
  - analyzer.stem (document, lang)
  - analyzer.count_stopwords (document, lang)


Collection
==================

Collection manages index files, segments and properties.

.. code:: python

  col = wissen.collection (
    indexdir = [dirs], 
    mode = [ CREATE | READ | APEND ], 
    analyzer = None,
    logger = None 
  )

- indexdir: path or list of path for using multiple disks efficiently
- mode
- analyzer
- logger: # if logger configured by wissen.configure, it's not necessary

Collection has 2 major class: indexer and searcher.



Indexer
---------

For searching documents, it's necessary to indexing text to build Inverted Index for fast term query. 

.. code:: python

  indexer = col.get_indexer (
    max_segments = int,
    force_merge = True or False,
    max_memory = 10000000 (10Mb),
    optimize = True or False
  )

- max_segments: maximum number of segments of index, if it's over, segments will be merged. also note during indexing, segments will be created 3 times of max_segments and when called index.close (), automatically try to merge until segemtns is proper numbers

- force_merge: When called index.close (), forcely try to merge to a single segment. But it's failed if too big index - on 32bit OS > 2GB, 64bit > 10 GB

- max_memory: if it's over, created new segment on indexing

- optimize: When called index.close (), segments will be merged by optimal number as possible


For add docuemtn to indexer, create document object:

.. code:: python

  document = wissen.document ()     

Wissen handle 3 objects as completly different objects between no relationship

- returning content
- snippet generating field
- searcherble fields


**Returning Content**

Wissen serialize returning contents by pickle, so you can set any objects pickle serializable.

.. code:: python

  document.set_content ({"userid": "hansroh", "preference": {"notification": "email", ...}})
  
  or 
  
  document.set_content ([32768, "This is smaple ..."])


**Snippet Generating Field**  

This field should be unicode/utf8 encoded bytes.

.. code:: python

  document.set_auto_snippet ("This is sample...")


**Searchable Fields**

document also recieve searchable fields:

.. code:: python

  document.add_field (name, value, ftype = wissen.TEXT, lang = "un", encoding = None)
  
  document.add_field ("default", "violin sonata in c k.301", wissen.TEXT, "en")
  document.add_field ("composer", "wolfgang amadeus mozart", wissen.TEXT, "en")
  document.add_field ("lastname", "mozart", wissen.STRING)
  document.add_field ("birth", 1756, wissen.INT16)
  document.add_field ("genre", "01011111", wissen.BIT8)
  document.add_field ("home", "50.665629/8.048906", wissen.COORD6)
  
  
- name: if 'default', this field will be searched by simple string, or use 'name:query_text'
- value: unicode/utf8 encode text, or should give encoding arg.
- ftype: *see below*
- encoding: give like 'iso8859-1' if value is not unicode/utf8
- lang: language code for standard_analyzer, "un" (unknown) is default
  
Avalible Field types are:

  - TEXT: analyzable full-text, result-not-sortable
  
  - TERM: analyzable full-text but position data will not be indexed as result can't search phrase, result-not-sortable
  
  - STRING: exactly string match like nation codes, result-not-sortable
  
  - LIST: comma seperated STRING, result-not-sortable
  
  - COORDn, n=4,6,8 decimal precision: comma seperated string 'latitude,longititude', latitude and longititude sould be float type range -90 ~ 90, -180 ~ 180. n is precision of coordinates. n=4 is 10m radius precision, 6 is 1m and 8 is 10cm. result-sortable
  
  - BITn, n=8,16,24,32,40,48,56,64: bitwise operation, bit makred string required by n, result-sortable
  
  - INTn, n=8,16,24,32,40,48,56,64: range, int required, result-sortable


Repeat add_document as you need and close indexer.

.. code:: python

  for ...:  
    document = wissen.document ()
    ...
    indexer.add_document (document) 
    indexer.close ()  

If searchers using this collection runs with another process or thread, searcher automatically reloaded within a few seconds for applying changed index.


Searcher
---------

For running searcher, you should wissen.configure () first and creat searcher.

.. code:: python
  
  searcher = col.get_searcher (
    max_result = 2000,
    num_query_cache = 200
  ) 
  
- max_result: max returned number of searching results. default 2000, if set to 0, unlimited results

- num_query_cache: default is 200, if over 200, removed by access time old


Query is simple:

.. code:: python

  searcher.query (
    qs, 
    offset = 0, 
    fetch = 10, 
    sort = "tfidf", 
    summary = 30, 
    lang = "un"
  )
  
- qs: string (unicode) or utf8 encoded bytes. for detail query syntax, see below
- offset: return start position of result records
- fetch: number of records from offset
- sort: "(+-)tfidf" or "(+-)field name", field name should be int/bit type, and '-' means ascending. if sort is "", records order is index time desc
- summary: number of terms for snippet
- lang: default is "un" (unknown)


For deleting indexed document:

.. code:: python

  searcher.delete (qs)

All documents will be deleted immediatly. And if searchers using this collection run with another process or thread, theses searchers automatically reloaded within a few seconds.

Finally, close searcher.

.. code:: python

  searcher.close ()


**Query Syntax**

  - violin composer:mozart birth:1700~1800 
  
    search 'violin' in default field, 'mozart' in composer field and search range between 1700, 1800 in birth field
    
  - violin allcomposer:wolfgang mozart
  
    search 'violin' in default field and any terms after allcomposer will be searched in composer field
    
  - violin -sonata birth:~1800
  
    not contain sonata in default field
  
  - violin -composer:mozart
  
    not contain mozart in composer field
  
  - violin or piano genre:00001101/all
  
    matched all 5, 6 and 8th bits are 1. also /any or /none is available  
    
  - violin or ((piano composer:mozart) genre:00001101/any)
  
    support unlimited priority '()' and 'or' operators
  
  - (violin or ((allcomposer:mozart wolfgang) -amadeus)) sonata (genre:00001101/none home:50.6656,8.0489~10000)
  
    search home location coordinate (50.6656, 8.0489) within 10 Km
  
  - "violin sonata" genre:00001101/none home:50.6656/8.0489~10
  
    search exaclt phrase "violin sonata"
  
  - "violin^3 piano" -composer:"ludwig van beethoven"

    search loose phrase "violin sonata" within 3 terms

    
Model
=============

Model manages index, train files, segments and properties.

.. code:: python

  mdl = wissen.model (
    indexdir = [dirs],
    mode = [ CREATE | READ | APPEND ], 
    analyzer = None, 
    logger = None
  )


Learner
---------

For building model, on Wissen, there're 3 steps need.

- Step I. Index documents to learn
- Step II. Build Corpus
- Step III. Selecting features and save trained model

**Step I. Index documents** 

Learner use wissen.labeled_document, not wissen.document. And can additional searchable fields if you need. Label is name of category.

.. code:: python
  
  learner = mdl.get_learner ()    
  
  for label, document in trainset:
  
	  labeled_document = wissen.labeled_document (label, document)	  	  
	  
	  # addtional searcherble fields if you need
	  labeled_document.add_field (name, value, ftype = TEXT, lang = "un", encoding = None)
	  
	  learner.add_document (labeled_document)
	  	  
  learner.close ()


**Step II. Building Corpus** 

Document Frequency (DF) is one of major factor of classifier. Low DF is important to searching but not to classifier. One of importance part of learning is selecting valuable terms, but so low DF terms is not very helpful for classifying new document because new document has also low probablity of appearance.

So for learnig/classification efficient, it's useful to eliminate too low and too high DF terms. For example, Let's assume you index 30,000 web pages for learing and there're about 100,000 terms. If you build corpus with all terms, it takes so long time for learing. But if you remove DF < 10 and DF > 7000 terms, 75% - 80% of all terms will be removed.

.. code:: python  
  
  # show terms order by DF for examin
  learner.listbydf (dfmin = 10, dfmax = 7000)
  
  # build corpus and save
  learner.build (dfmin = 10, dfmax = 7000)
  
As a result, corpus built with about 25,000 terms.

Note that once call build(),

- you cannot additional training documents
- you cannot run build () again

The reason why when low/high DF terms are eliminated by build(mindf, maxdf) and related index files will be also unrecoverable shrinked for performance. Then if these works are needed, you should do from step I again. But there's another option: rbuild()

.. code:: python  
  
  # build corpus and save but reindexable mode
  learner.rbuild (dfmin = 10, dfmax = 7000)

rbuild() is very similar with build() but differences are these things: 

- It make SIMILARITY and ROCCHINO classifiers inefficient
- It can add documents additionally with opening model with APPEND mode
- And can rebuild corpus any time 

So rbuild() is useful during classification testing/profiling phase and commit with build() at on service time.


**Step III. Feature Selecting and Saving Model** 

Features means most valuable terms to classify new documents. It is important understanding many/few features is not good for best result. It maybe most important to select good features for classification.

For example of my URL classification into 2 classes works show below results. Classifier is NAIVEBAYES, selector is WSS and min DF is 2. Train set is 20,000, test set is 2,000.

  - features 3,000 => 82.9% matched, 73 documents is unclassified
  - features 2,000 => 82.9% matched, 73 documents is unclassified
  - features 1,500 => 83.4% matched, 75 documents is unclassified
  - features 1,000 => 83.6% matched, 79 documents is unclassified
  - features   500 => 83.1% matched, 86 documents is unclassified
  - features   200 => 81.1% matched, 108 documents is unclassified
  - features   50 => 76.0% matched, 155 documents is unclassified
  - features   10 => 58.7% matched, 326 documents is unclassified

As results show us that over 2,000 snd under 1,000 features will be unchanged or degraded for classification quality. Also fewer features increase unclassified ratio.

.. code:: python  
  
  learner.train (
    cl_for = [
      ALL (default) | NAIVEBAYES | FEATUREVOTE | 
      TFIDF | SIMILARITY | ROCCHINO
    ],
    select = number of features if value is > 1 or ratio,
    selector = [
      CHI2 | GSS | DF | NGL | MI | TFIDF | IG | OR | 
      OR4P | RS | LOR | COS | PPHI | YULE | RMI
    ],
    orderby = [SUM | MAX | AVG],
    dfmin = 0, 
    dfmax = 0
  )
  learner.close ()
  
- cl_for: train for which classifier, if not specified this features used default for every classifiers haven't own feature set. So train () can be called repeatly for each classifiers

- select: number of features if value is > 1 or ratio to all terms. Generally it might be not over 7,000 features for classifying web pages or news articles into 20 classes.

- selector: mathemetical term scoring alorithm to selecting features considering relation between term and term / term and label. Also DF, and term frequency (TF) etc.

- orderby: final scoring method. one of sum, max, average value

- dfmin, dfmax: In spite of it had been already removed by build(), it can be also additional removed for optimal result for specific classifier


**Finding Best Train Options**

Generally, differnce attibutes of data set, it hard to say which options are best. It is stongly necessary number of times repeating process between train () and guess () for best result and that's not easy process.

- train (initial options)
- measure results with guess ()
- train (another options)
- measure results again with guess ()
- ...
- find best tain options fitting with your data

For getting result accuracy, your pre-requisite data should be splitted into train set for tran () and test set for guess () to measure `precision and recall`_.

.. _`precision and recall`: https://en.wikipedia.org/wiki/Precision_and_recall


**Implemented Classifier**

  - NAIVEBAYES: Naive Bayes Probablility
  - FEATUREVOTE: Feature Voting Classifier
  - ROCCHINO: Rocchino Classifier
  - TFIDF: Max TDIDF Score
  - SIMILARITY: Max Cosine Similarity
  - META: default guessing, merging and decide with multiple results guessed by NAIVEBAYES, FEATUREVOTE, ROCCHINO Classifiers

If you need speed most of all, NAIVEBAYES is a good choice. NAIVEBAYES is an old theory but it still works with very high performance at both speed and accuracy if given proper training set.

More detail for each classifier alorithm, googling please.


**Feature Selecting Methods**

  - CHI2 = Chi Square Statistic
  - GSS = GSS Coefficient 
  - DF = Document Frequency
  - NGL = NGL
  - MI = Mutual Information
  - TFIDF = Term Frequecy - Inverted Document Frequency
  - IG = Information Gain
  - OR = Odds Ratio
  - OR4P = Kind of Odds Ratio(? can't remember)
  - RS = Relevancy Score
  - LOR = Log Odds Ratio
  - COS = Cosine Similarity 
  - PPHI = Pearson's PHI
  - YULE = Yule
  - RMI = Residual Mutual Information
  
I personally prefer OR, IG and GSS selectors with MAX method.

Classifier
------------
  
Finally,

.. code:: python  
  
  classifier = mdl.get_classifier ()
  classifier.quess (
    qs, 
    lang = "un", 
    cl = [META(Default) | NAIVEBAYES | FEATUREVOTE | ROCCHINO | TFIDF | SIMILARITY ],
    top = 0,
    cond = ""
  )
  classifier.close ()
  
- qs: full text stream to classify

- lang

- cl: which classifer, META is default

- top: how many high scored classified results, default is 0, means high scored result(s) only

- cond: conditional document selecting query. Some classifier execute calculating with lots of documents like ROCCHINO and SIMILARITY, so it's useful shrinking number of documents. This  only work when you put additional searchable fields using labeled_document.add_field (...).


**Optimizing Each Classifiers**

For give some detail options to a classifier you can use setopt (classfier, option name = option value,...).


.. code:: python  

  classifier = mdl.get_classifier ()
  classifier.setopt (wissen.ROCCHINO, topdoc = 200)
  
SIMILARITY, ROCCHINO classifiers basically have to compare with entire indexed document documents, but Wissen can compare with selected documents by 'topdoc' option. These number of documents will be selected by high TFIDF score for classifying performance reason. Default topdoc value is 100. If you set to 0, Wissen will compare with all documents have one of features at least. But on my experience, there's no critical difference except speed performance.

Also note that currently possible optimizing options is only 'topdoc'.


Change Log
============
  
  0.11 - fix HTML strip and segment merging etc.
  
  0.10 - change version format, remove all str*_s ()
  
  0.9.0.5 - fix long long int, bit type
  
  0.9.0.3 - fix logger encoding

  0.9.0.2 - fix snippet-making
  
  0.9.0.1 - support Python 3.x

  0.8.0.13 - change license from BSD to GPL V3
  
  
*Copyright (c) 2015 by Hans Roh*

