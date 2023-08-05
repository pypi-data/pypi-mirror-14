#ifndef CORE_INDEX_H
#define CORE_INDEX_H

#include <stdio.h>
#include "macro.h"
#include "pthread.h"

#define FILEBUFFER_LENGTH 4096
#define MIN_IOBUFFER 512

#define INDEX_INTERVAL 128
#define SKIP_INTERVAL 16
#define SKIPBUFFER_LENGTH 1024
#define MAXPROX 1000
#define SCORE_CACHE_COUNT 32
#define DELTA_ARRAY_SIZE 32

#define compEQ(a,b) (a->fdno == b->fdno && strcmp (a->term, b->term) == 0)

/************************************************
	File buffering & managed memory architecture
************************************************/
typedef struct {
    int file;
    int extend;
    int max;
    int errcode;
    int __bsize;
    int __clone;
    int __linked;
    int __exbuffer;    
    char *buffer;
    long __tell;
    long __translate;
    long __readpoint;    
    long __readsize;    
    long position;
    char mode;
    pthread_mutex_t __mutex;
} BFILE;

typedef union {
	float score;
	long long sort;
} SCORE;

typedef union {
	float fval;
	long long ival;
} EXTRA;

typedef struct {
	unsigned int docid;
	unsigned short int freq;
	SCORE score;
	EXTRA extra;
} FREQ; // 32 bytes

typedef struct {
	int numdoc;
	int prox [MAXPROX];
	FREQ freq;
} ONEDOC;

typedef struct {
    FREQ *freq;
    int position;
    int max;
    int extend;
    short int type;
    unsigned short int *prox;
} IBUCKET;

/*Posting Decoded*/
typedef struct {
	char type; // F
	char scoring;
	int df;
	BFILE* freq;
	BFILE* prox;
} DPOSTING;


/************************************************
	Memory Pool Architecture
************************************************/

typedef struct {
	int skipnum;
	int needle;
	unsigned int nextdocid;
	unsigned int docid;
	long nextfreqposition;
	long nextproxposition;	
	long freqposition;
	long proxposition;
	BFILE* skip;
} MSKIP;

typedef struct {
	int df;
	int dc; /* posting document count */
	int lastdocid;
	int hasprox;
	int hasextra;
	int hassortkey;
	float weight;
	float idf;
	BFILE* freq;
	BFILE* prox;
	MSKIP* skip;
} MPOSTING;

/* MCOMPUTE */
typedef struct {
	int df;
	int dc;
	int hasprox;	
	int hasextra;
	int hassortkey;
	IBUCKET* freq;
	IBUCKET* prox;
} MCOMPUTE;
	
typedef struct {
	BFILE *btis;	
} MFILE;

typedef struct {
	BFILE *bfdi;
	BFILE *bfda;	
} MSTORED;

/* MSORTMAP */
typedef struct {
	int size;
	int numdoc;	
	BFILE* bsmp;
} MSCORE;

typedef struct {
	int dc;
	BFILE *bfdb;	
} MBFILE;

typedef struct {
	BFILE *bxx0;
	BFILE *bxx1;
	BFILE *bxx2;
} MTEMP;


/************************************************
	Classifier
************************************************/
typedef struct {
	int df;
	int tf;
} FeatureInfo;

typedef struct {
	int classid;
	double score;
} ClassScore;

typedef struct {
	int numpool;
	FeatureInfo *corpus;
	FeatureInfo *feature;
	ClassScore *scores;
	ClassScore *temp [3];
} CLASSIFER;

/************************************************
Memory Architecture
************************************************/
typedef struct {
	int usage;
	int status;
	pthread_mutex_t mutex;
	MFILE* mfi;
	MSTORED* mfd;
	MPOSTING* mpt;
	MCOMPUTE* mco;
	MCOMPUTE* mht;
	MCOMPUTE* mbk;	
	MSCORE* msr;
	MBFILE* mmp;
	MTEMP* tmp;
	CLASSIFER* cla; 
	ONEDOC *odi;
} Memory;


/************************************************
	Term hash table
************************************************/
#define TERMHASHTABLE_SIZE 97777
typedef struct keyTag {
	char *term;
	unsigned char fdno;
} keyType;            /* type of key */

typedef struct recTag {
    struct recTag* next;
    int docid;                  /* optional related data */
    int tf;
    short int *prox;
} recType;

typedef struct nodeTag {
    struct nodeTag *next;       /* next node */
    keyType *key;                /* key */
    recType *firstRec;
    recType *lastRec;
} nodeType;


/************************************************
	Segment Merge Info
************************************************/
typedef struct {
	int numdoc;
	int base;
	unsigned char* bits;
	BFILE* bsmp;
	BFILE* bfda;
	BFILE* bfdi;
	BFILE* bfrq;
	BFILE* bprx;
	BFILE* bnrm;
	int *docmap;
} SMI;

typedef struct {
	int segcount;
	int base;
	SMI *smi [100];
} SMIS;


/************************************************
	Term
************************************************/
typedef struct {
	char term [100];
	unsigned char fdno;
	int df;
	long frqPointer;
	long prxPointer;
	int skipDelta;
	int proxLength;
	long indexPointer;
} Term;

typedef struct {
	char* term;
	unsigned char fdno;
	int df;
	long frqPointer;
	long prxPointer;
	int skipDelta;
	int proxLength;
	long indexPointer;
} MemTerm;


/**************************************************
Function Protos
**************************************************/


/* sorting and search */
int key_compfunc (const void *x, const void *y);
int value_compfunc (const void *x, const void *y);
int hsort (int *buffer[2], int nmemb, int size, int max);
int interpolationsearch (int key, int *base [2], unsigned int num);
int binarysearch (int key, int *base [2], unsigned int num);
int heapsort (void *vbase, int nmemb, int size, int max, int (*compar)(const void *, const void *));


/* Term Hash Table */
nodeType* ht_find(nodeType *hashTable [], keyType *key);
int ht_insert(nodeType *hashTable [], keyType *key, recType *rec);
int ht_delete (nodeType *hashTable [], keyType *key);
keyType** ht_keys (keyType *karr [], int count, nodeType *hashTable []);
int ht_destroy (nodeType *hashTable []);
nodeType ** ht_init (nodeType *hashTable []);
void ht_sort (keyType *karr [], int termnum);
recType* ht_fetchfirst (nodeType *hashTable [], keyType *key);
int ht_occupied (nodeType *hashTable []);


/*Bufferd File Object */
BFILE* bopen (int file, char mode, int max, int extend);
BFILE* bopen2 (char* buffer, char mode, int max, int extend);
BFILE* bdup (BFILE* bfile);
int bclose (BFILE* bfile);
int bflush (BFILE* bfile);
int bcommit (BFILE* bfile, BFILE* target);
int brefill (BFILE* bfile);
long btell (BFILE* bfile);
int bseek (BFILE* bfile, long offset);
int bncopy (BFILE* bfile, BFILE* target, int n);
void btranslate (BFILE* bfile, long offset);
int blink (BFILE* bfile, int file, pthread_mutex_t mutex, long offset, int n);
void bunlink (BFILE* bfile);
int bextend (BFILE* bfile, int extend);
int bsize (BFILE* bfile);
void setmax (BFILE* bfile, int max);

int zcompress(char *input, int length, BFILE *output, int level);
int zdecompress(char *input, int length, BFILE *output);

Memory * memnew (int buffer_size);
int memdel (Memory* memory);
int memusage (Memory* memory);

IBUCKET* iopen (int max, int type);
int iextend (IBUCKET* ibucket, int extend);
int iclose (IBUCKET* ibucket);
int isize (IBUCKET* ibucket);

double factorial (double n);
double log2 (double d);
double odds (int tf, int size, int n);
double mdistance (double baselat, double baselong, double otherlat, double otherlong);

unsigned long long getdiskspace (char* dir) ;

#endif
