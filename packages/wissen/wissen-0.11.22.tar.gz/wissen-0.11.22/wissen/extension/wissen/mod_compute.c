#include "Python.h"
#include "core.h"
#include "structmember.h"
#include "index/index.h"
#include <stdio.h>
#include <math.h>

#define LATITUDE1DEGREE 111234.5
#define LONGITUDE1DEGREE 85317.0
#define OP_INTERSECT '*'
#define OP_UNION '+'
#define OP_TRIM '-'

#define AT_HITS_BEGIN_ADD {\
if (hitsfreq->position == hitsfreq->max) {\
	iextend (hitsfreq, 0);\
	hfreq = &hitsfreq->freq [hitsfreq->position];\
}\
}

#define AT_HITS_END_ADD {\
hfreq++;\
hitsfreq->position++;\
}

static float NORM_TABLE [256];
static int norm_table_index = 0;


/****************************************************************
Module Memeber Definition
****************************************************************/
typedef struct {
	Memory* mem;
	MPOSTING* mpt;
	MCOMPUTE* hits;
	MCOMPUTE* iter;
	MCOMPUTE* banks [10];
	MSCORE* scorer;
	ONEDOC *odi;
	MCOMPUTE* temp;
	int numbanks;
	int N;
	int setfreq;
	int predict;
	int withdraw;
	int saved;
	int estimate;
	int randomscan;
	float scorecache [SCORE_CACHE_COUNT];
	float sumofsquaredweight;
} Operator;
	
typedef struct {
	PyObject_HEAD
	Operator* ops;
} Compute;



/****************************************************************
Shared Functions
****************************************************************/
static int
descscore_func (const void *x, const void *y) {
     if ( (*(FREQ* const) x).score.score > (*(FREQ* const) y).score.score ) return 1;
	 if ( (*(FREQ* const) x).score.score < (*(FREQ* const) y).score.score )  return -1;
	 return 0;
}

static int
ascscore_func (const void *x, const void *y) {
     if ( (*(FREQ* const) y).score.score > (*(FREQ* const) x).score.score ) return 1;
	 if ( (*(FREQ* const) y).score.score < (*(FREQ* const) x).score.score )  return -1;
	 return 0;
}

static int
descsortkey_func (const void *x, const void *y) {
     if ( (*(FREQ* const) x).score.sort > (*(FREQ* const) y).score.sort ) return 1;
	 if ( (*(FREQ* const) x).score.sort < (*(FREQ* const) y).score.sort )  return -1;
	 return 0;
}

static int
ascsortkey_func (const void *x, const void *y) {
   if ( (*(FREQ* const) y).score.sort > (*(FREQ* const) x).score.sort ) return 1;
	 if ( (*(FREQ* const) y).score.sort < (*(FREQ* const) x).score.sort )  return -1;
	 return 0;
}

static int
descextraf_func (const void *x, const void *y) {
   if ( (*(FREQ* const) x).extra.fval > (*(FREQ* const) y).extra.fval ) return 1;
	 if ( (*(FREQ* const) x).extra.fval < (*(FREQ* const) y).extra.fval )  return -1;
	 return 0;
}

static int
ascextraf_func (const void *x, const void *y) {
   if ( (*(FREQ* const) y).extra.fval > (*(FREQ* const) x).extra.fval ) return 1;
	 if ( (*(FREQ* const) y).extra.fval < (*(FREQ* const) x).extra.fval )  return -1;
	 return 0;
}

static int
descextrai_func (const void *x, const void *y) {
     if ( (*(FREQ* const) x).extra.ival > (*(FREQ* const) y).extra.ival ) return 1;
	 if ( (*(FREQ* const) x).extra.ival < (*(FREQ* const) y).extra.ival )  return -1;
	 return 0;
}

static int
ascextrai_func (const void *x, const void *y) {
     if ( (*(FREQ* const) y).extra.ival > (*(FREQ* const) x).extra.ival ) return 1;
	 if ( (*(FREQ* const) y).extra.ival < (*(FREQ* const) x).extra.ival )  return -1;
	 return 0;
}

/****************************************************************
Contructor / Destructor
****************************************************************/
static int
ATinit (Operator* ops, Memory* mem, int N)
{
	ops->numbanks = 1;
	ops->N = N;
	ops->setfreq = 0;
	ops->randomscan = 0;
	ops->mem = mem;

	ops->mpt = ops->mem->mpt;
	ops->iter = ops->mem->mco;
	ops->hits = ops->mem->mht;
	ops->banks [0] = ops->mem->mbk;

	ops->scorer = ops->mem->msr;
	ops->odi = ops->mem->odi;

	ops->mpt->dc = -1;
	ops->scorer->size = -1;
	ops->withdraw = 0;
	
	ops->hits->dc = 0;
	ops->hits->hassortkey = 0;
	ops->hits->hasextra = 0;
	ops->sumofsquaredweight = 0.0F;
	return 0;
}

/****************************************************************
Module Methods
****************************************************************/

static int
ATreset (Operator* ops)
{
	ops->mpt->dc = -1;
	ops->mpt->hasextra = 0;
	ops->mpt->hassortkey = 0;
	ops->scorer->size = -1;
	ops->withdraw = 0;
	return 0;
}

static int
ATclose (Operator* ops)
{
	int i;
	for (i = 1; i < ops->numbanks; i++) {
		if (ops->banks [i]) {
			if (ops->banks [i]->freq) iclose (ops->banks [i]->freq);
			if (ops->banks [i]->prox) iclose (ops->banks [i]->prox);
			free (ops->banks [i]);
			ops->banks [i] = NULL;
		}
	}

	ATreset (ops);

	ops->mem->mco = ops->iter;
	ops->mem->mht = ops->hits;
	ops->mem->mbk = ops->banks [0];
	return 0;
}

static int
ATcount (Operator* ops)
{
	if (ops->randomscan)
		return ops->estimate;
	else if (ops->withdraw)
		return ops->banks [ops->saved]->dc;
	else
		return ops->hits->dc;
}

static void 
ATswap (Operator* ops) {
	ops->temp = ops->iter;
	ops->iter = ops->hits;
	ops->hits = ops->temp;

	ops->hits->dc = 0;
	ops->hits->freq->position = 0;
	ops->hits->prox->position = 0;	
	
	ops->hits->hasprox = ops->iter->hasprox;	
	ops->hits->hasextra = ops->iter->hasextra;
	ops->hits->hassortkey = ops->iter->hassortkey;
	
	ops->iter->freq->position = 0;
	ops->iter->prox->position = 0;
}

static int
ATpush (Operator* ops)
{
	if (ops->hits->dc) {
		if (ops->saved == 10) return -1;
		if (ops->saved == ops->numbanks) {
			ops->banks [ops->saved] = NULL;
			if (!(ops->banks [ops->saved] = (MCOMPUTE*) malloc (sizeof (MCOMPUTE)))) goto fail;

			ops->banks [ops->saved]->freq = NULL;
			ops->banks [ops->saved]->prox = NULL;
			if (!(ops->banks [ops->saved]->freq = iopen (1024, 0))) goto fail;
			if (!(ops->banks [ops->saved]->prox = iopen (1024, 1))) goto fail;
			ops->numbanks++;
		}

		ops->temp = ops->banks [ops->saved];
		ops->banks [ops->saved] = ops->hits;
		ops->hits = ops->temp;
		ops->saved++;
	}

	ops->hits->dc = 0;
	ops->hits->hasprox = 0;	
	ops->hits->hassortkey = 0;
	ops->hits->hasextra = 0;
	ops->hits->freq->position = 0;
	ops->hits->prox->position = 0;

	return ops->saved;

fail:
	return -1;
}

static int
ATpop (Operator* ops, int swap)
{
	if (ops->saved) {
		ops->saved--;
		if (swap) {
			ops->temp = ops->hits;
			ops->hits = ops->banks [ops->saved];
			ops->banks [ops->saved] = ops->temp;
		}
		ops->banks [ops->saved]->freq->position = 0;	
		 /* fake */
		ops->mpt->weight = 1.0F;
		ops->mpt->dc = ops->banks [ops->saved]->dc;
		ops->mpt->hasprox = 0; /* no phrase eval */
		ops->mpt->hasextra = ops->banks [ops->saved]->hasextra;
		ops->mpt->hassortkey = ops->banks [ops->saved]->hassortkey;		
		ops->withdraw = 1;		
	}
	return ops->saved;
}

static int 
ATadvance (Operator* ops)
{
	int i;
	int dociddelta, freq, prox;
	int lastprox;
	unsigned char _uchar;
	int _shift;
	float normf;
	char normb [1];
	IBUCKET* bankfreq;
	
	if (ops->withdraw) {
		bankfreq = ops->banks [ops->saved]->freq;
		ops->odi->freq.docid = bankfreq->freq [bankfreq->position].docid;
		
		if (ops->N) {
			ops->odi->freq.score.score = bankfreq->freq [bankfreq->position].score.score;
		} else if (ops->banks [ops->saved]->hassortkey) {
			ops->odi->freq.score.sort = bankfreq->freq [bankfreq->position].score.sort;
		}
		
		if (ops->banks [ops->saved]->hasextra == 1) {
			ops->odi->freq.extra.ival = bankfreq->freq [bankfreq->position].extra.ival;
		} else if (ops->banks [ops->saved]->hasextra == 2) {
			ops->odi->freq.extra.fval = bankfreq->freq [bankfreq->position].extra.fval;
		}
				
		bankfreq->position++;
		ops->odi->numdoc++;
		return 1;
	}
	
	breadVInt (ops->mpt->freq, dociddelta);
	freq = 0;
	if (dociddelta & 1) {
		freq = 1;
	}
	else {
		breadVInt (ops->mpt->freq, freq);
	}

	dociddelta >>= 1;
	ops->mpt->lastdocid += dociddelta;
	ops->odi->freq.docid = ops->mpt->lastdocid;
	
	if (ops->N) {	
		if (ops->scorer->size > 0) {
			bseek (ops->scorer->bsmp, ops->mpt->lastdocid);
			breadString (ops->scorer->bsmp, normb, 1);
			normf = NORM_TABLE [normb [0] & 0xFF];
		} else {
			normf = 1.0F;
		}		
		if (freq < SCORE_CACHE_COUNT) {			
			ops->odi->freq.score.score = normf * ops->scorecache [freq];
		}	else {			
			ops->odi->freq.score.score = normf * (float) (sqrt (freq) * ops->mpt->weight * ops->mpt->idf);
		}
	}
	
	ops->odi->freq.freq = (unsigned short int) freq;
	/* decoding prox data */
	if (ops->mpt->hasprox) {
		lastprox = 0;
		for (i = 0; i < freq; i++) {
			breadVInt (ops->mpt->prox, prox);
			lastprox += prox + 1;
			ops->odi->prox [i] = (unsigned short int) lastprox;
		}
	}
	ops->odi->numdoc++;
	return 1;

ioreaderror:
	return 0;
}

static int ATsearch (Operator* ops, unsigned int docid)
{
	int ic;
	unsigned char _uchar;
	int _shift;
	int docdelta, freqPointerDelta, proxPointerDelta;
	MSKIP* skip;
	int proceed;
	int hasid = 0;
	int final = 0;
	
	if (ops->odi->freq.docid == docid && ops->odi->numdoc) return 1;	/* prev fetched */
	skip = ops->mpt->skip;
	
	//printf ("docid:%d self->mpt->dc: %d, skip->skipnum: %d\n", docid, ops->mpt->dc, skip->skipnum);
	if (skip->skipnum) proceed = SKIP_INTERVAL;	
	else {
		final = 1;
		proceed = SKIP_INTERVAL + (ops->mpt->dc % SKIP_INTERVAL);
	}	
	
	//printf ("proceed: %d\n", proceed);
	if (docid < skip->docid || docid < ops->odi->freq.docid) return -1;
	
	if (docid > skip->nextdocid && !skip->needle) {
		while (skip->skipnum) {
			skip->docid = skip->nextdocid;
			skip->freqposition = skip->nextfreqposition;
			skip->proxposition = skip->nextproxposition;
			
			breadVInt (skip->skip, docdelta);
			breadVInt (skip->skip, freqPointerDelta);
			breadVInt (skip->skip, proxPointerDelta);
			skip->nextdocid = skip->docid + docdelta;
			skip->nextfreqposition = skip->freqposition + freqPointerDelta;
			skip->nextproxposition = skip->proxposition + proxPointerDelta;
			skip->skipnum--;
			
			//printf ("$$$docid:%d, skip->docid:%d, skip->nextdocid:%d\n", docid, skip->docid, skip->nextdocid);
			if (docid >= skip->docid && docid <= skip->nextdocid) {
				ops->mpt->lastdocid = skip->docid;
				bseek (ops->mpt->freq, skip->freqposition);
				if (ops->mpt->hasprox) {
					bseek (ops->mpt->prox, skip->proxposition);
				}
				hasid = 1;
				break;
			}		
		}
		
		if (!hasid) {
			//printf ("*************\n");
			ops->mpt->lastdocid = skip->nextdocid;
			bseek (ops->mpt->freq, skip->nextfreqposition);
			if (ops->mpt->hasprox) {
				bseek (ops->mpt->prox, skip->nextproxposition);
			}
			skip->needle += SKIP_INTERVAL;
			if (!final) {
				proceed += ops->mpt->dc % SKIP_INTERVAL;
			}	
		}
	}
	
	for (ic = proceed; ic; ic--) {
		if (!skip->skipnum) {
			skip->needle++;
			//printf ("needle: %d\n", skip->needle);
			if (skip->needle > proceed) return -2;
		}
		if (!ATadvance (ops)) return 0;
		//printf ("ops->odi->freq.docid:%d docid:%d\n", ops->odi->freq.docid, docid);
		if (ops->odi->freq.docid == docid) return 1;		
		else if (ops->odi->freq.docid > docid) return -1;
	}

	return -1;

ioreaderror:
	return 0;
}

static int
ATset (Operator* ops, int df, float weight)
{
	float tempscore;
	int i, p, pc;
	IBUCKET* hitsfreq, *hitsprox;
	FREQ *hfreq;
	unsigned short int *hprox;
	
	ops->mpt->weight = weight;
	
	if (ops->N) {
		if (!df) df = 1;
		ops->mpt->idf = (float) (log (ops->N / (df + 1.0)) + 1.0);		
		tempscore = (float) (weight * ops->mpt->idf);
		for (i = 0; i < SCORE_CACHE_COUNT; i++) {
			ops->scorecache [i] = tempscore * (float) sqrt (i);
		}		
		ops->sumofsquaredweight += (tempscore * tempscore);
	}
	
	if (ops->hits->dc) {
		return ops->mpt->dc;
	}

	hitsfreq = ops->hits->freq;
	hitsprox = ops->hits->prox;
	hfreq = &hitsfreq->freq [0];
	hprox = &hitsprox->prox [0];
	hitsfreq->position = 0;
	hitsprox->position = 0;

	ops->hits->df = ops->mpt->df;
	ops->hits->hasprox = ops->mpt->hasprox;
	if (ops->setfreq) ops->hits->hasextra = 1;
	
	for (i = ops->mpt->dc; i-- ;) {
		if (!ATadvance (ops)) return -1;
		
		AT_HITS_BEGIN_ADD
		hfreq->docid = ops->odi->freq.docid;

		if (ops->setfreq) {
			hfreq->extra.ival = ops->odi->freq.freq;
		}
		if (ops->N) {
			hfreq->score.score = ops->odi->freq.score.score;
		}

		if (ops->mpt->hasprox) {
			hfreq->freq = ops->odi->freq.freq;
			for (p=0, pc = ops->odi->freq.freq; pc-- ; p++) {
				if (hitsprox->position == hitsprox->max) {
					iextend (hitsprox, 0);
					hprox = &hitsprox->prox [hitsprox->position];
				}
				*hprox = ops->odi->prox [p];
				hprox++;
				hitsprox->position++;
			}
		}
		AT_HITS_END_ADD
	}
	
	ops->hits->dc = hitsfreq->position;
	ATreset (ops);	
	return ops->hits->dc;
}


/**********************************************************************
Operations
**********************************************************************/
static int
ATintersect (Operator* ops, int near, int loose)
{
	int q, qc, nfreq;
	int found;
	int mindist = 0, dist = 0;
	int i, ic, p, proceedprox = 0;
	IBUCKET* hitsfreq, *hitsprox, *iterfreq, *iterprox;
	FREQ *ifreq, *hfreq;
	unsigned short int *iprox, *hprox;
	int hasextra = 0, hassortkey = 0;
	
	if (ops->mpt->dc == -1) return ops->hits->dc;

	ATswap (ops);

	/* shirtcuts for quick access */
	hitsfreq = ops->hits->freq;
	hitsprox = ops->hits->prox;
	iterfreq = ops->iter->freq;
	iterprox = ops->iter->prox;
	ifreq = &iterfreq->freq [0];
	iprox = &iterprox->prox [0];
	hfreq = &hitsfreq->freq [0];
	hprox = &hitsprox->prox [0];

	ops->hits->df = ops->mpt->df;
	ops->hits->hasprox = ops->mpt->hasprox;
	ops->odi->freq.docid = 0;
	ops->odi->numdoc = 0;
	
	if (ops->mpt->hassortkey && ops->withdraw) {
		hassortkey = 21;		
		ops->hits->hassortkey = ops->mpt->hassortkey;
	}
	else if (ops->iter->hassortkey) hassortkey = 11;		
	if (ops->mpt->hasextra && ops->withdraw) {
		/****************************************** 
			it cannot be set in swap or pop, because of mpt->hasextra has meaning in only intersect and union.
			else who care?
		******************************************/
		ops->hits->hasextra = ops->mpt->hasextra; 
		if (abs (ops->mpt->hasextra) == 1) hasextra = 21;			
		else  hasextra = 22;
	}	
	else if (ops->iter->hasextra) {
		if (abs (ops->iter->hasextra) == 1) hasextra = 11;
		else  hasextra = 12;
	}
	
	if (ops->mpt->hasprox && ops->iter->hasprox) proceedprox = 1;

	/* fast docid search */
	if (!ops->withdraw && ops->mpt->dc > SKIP_INTERVAL && ops->iter->dc && ops->mpt->dc / ops->iter->dc > (SKIP_INTERVAL >> 1)) {
		for (ic = ops->iter->dc; ic--; iterfreq->position++, ifreq++) {
			found = ATsearch (ops, ifreq->docid);
			//printf ("##found: %d\n", found);
			if (!found) return -1;
			if (found == -2) break;
			if (found == -1) {
				if (proceedprox) { for (p = ifreq->freq; p-- ; iprox++) {} }
				continue;
			}

			AT_HITS_BEGIN_ADD
			if (proceedprox) {
				nfreq = 0;
				q = 0;
				for (p = ifreq->freq; p-- ; iprox++) {
					qc = ops->odi->freq.freq - q;
					if (qc < 0) break;
					for (; qc--; q++) {
						if (ops->odi->prox [q] > *iprox + near) {
							break;
						}

						if (ops->odi->prox [q] < *iprox + 1) {
							continue;
						}
						if (loose || ops->odi->prox [q] == *iprox + near) {
							if (hitsprox->position == hitsprox->max) {
								iextend (hitsprox, 0);
								hprox = &hitsprox->prox [hitsprox->position];
							}
							*hprox = ops->odi->prox [q];
							hprox++;
							hitsprox->position++;
							nfreq++;
						}
						if (loose) {
							dist = ops->odi->prox [q] - *iprox;
							if (!mindist || dist < mindist) mindist = dist;
						}
					}
				}

				if (!nfreq) {
					continue;
				}

				hfreq->freq = nfreq;
			}

			hfreq->docid = ops->odi->freq.docid;
			/* extra information setting */
			if (ops->setfreq) {				
				hfreq->extra.ival = ifreq->extra.ival;
			} else if (hasextra) {
				if (hasextra == 11)
					hfreq->extra.ival = ifreq->extra.ival;
				else if (hasextra == 12)
					hfreq->extra.fval = ifreq->extra.fval;
				else if (hasextra == 21)
					hfreq->extra.ival = ops->odi->freq.extra.ival;	
				else if (hasextra == 22)
					hfreq->extra.fval = ops->odi->freq.extra.fval;	
			}
												
			if (ops->N) {
				hfreq->score.score = ifreq->score.score + ops->odi->freq.score.score;
			} else if (hassortkey) {				
				if (hassortkey == 11)
					hfreq->score.sort = ifreq->score.sort;
				else if (hassortkey == 21)
					hfreq->score.sort = ops->odi->freq.score.sort;				
			}
			AT_HITS_END_ADD
		}
	}
	/* end of quick search */

	else {
		for (i = ops->mpt->dc; i -- ;) {
			if (!ATadvance (ops)) return -1;
			ic = ops->iter->dc - iterfreq->position;
			
			if (ic < 0) break;
			for (; ic--; iterfreq->position++, ifreq++) {
				//printf ("---ifreq->docid: %d/ops->odi->freq.docid: %d\n\n", ifreq->docid, ops->odi->freq.docid);
				if (ifreq->docid > ops->odi->freq.docid) break;
				if (ifreq->docid < ops->odi->freq.docid) {
					if (proceedprox) iprox += ifreq->freq;
					continue;
				}

				AT_HITS_BEGIN_ADD
				if (proceedprox) {
					nfreq = 0;
					q = 0;
					for (p = ifreq->freq; p-- ; iprox++) {
						qc = ops->odi->freq.freq - q;
						if (qc < 0) break;
						for (; qc--; q++) {
							if (ops->odi->prox [q] > *iprox + near) {
								break;
							}
							if (ops->odi->prox [q] < *iprox) {
								continue;
							}

							if (loose || ops->odi->prox [q] == *iprox + near) {
								if (hitsprox->position == hitsprox->max) {
									iextend (hitsprox, 0);
									hprox = &hitsprox->prox [hitsprox->position];
								}
								*hprox = ops->odi->prox [q];
								hprox++;
								hitsprox->position++;
								nfreq++;
							}

							if (loose) {
								dist = ops->odi->prox [q] - *iprox;
								if (!mindist || dist < mindist) mindist = dist;
							}
						}
					}

					if (!nfreq) {
						ifreq++;
						iterfreq->position++;
						break;
					}

					hfreq->freq = nfreq;
				}

				hfreq->docid = ops->odi->freq.docid;

				/* extra information setting */
				if (ops->setfreq) {				
					hfreq->extra.ival = ifreq->extra.ival;
				} else if (hasextra) {
					if (abs (ops->iter->hasextra) == 1)
						hfreq->extra.ival = ifreq->extra.ival;
					else if (abs (ops->iter->hasextra) == 2)
						hfreq->extra.fval = ifreq->extra.fval;
					else if (abs (ops->mpt->hasextra) == 1)
						hfreq->extra.ival = ops->odi->freq.extra.ival;	
					else if (abs (ops->mpt->hasextra) == 2)
						hfreq->extra.fval = ops->odi->freq.extra.fval;	
				}
													
				if (ops->N) {
					hfreq->score.score = ifreq->score.score + ops->odi->freq.score.score;
				} else if (hassortkey) {				
					if (ops->iter->hassortkey)
						hfreq->score.sort = ifreq->score.sort;
					else if (ops->withdraw && ops->mpt->hassortkey)
						hfreq->score.sort = ops->odi->freq.score.sort;				
				}
				
				ifreq++;
				iterfreq->position++;
				AT_HITS_END_ADD
				break;
			}
		}
	}

	ops->hits->dc = hitsfreq->position;
	ATreset (ops);
	return ops->hits->dc;
}


static int
ATunion (Operator* ops)
{
	int i, ic;
	IBUCKET* hitsfreq, *iterfreq;
	FREQ *ifreq, *hfreq;
	int hasextra = 0, hassortkey = 0;

	if (ops->mpt->dc == -1) return ops->hits->dc;

	ATswap (ops);
	
	hitsfreq = ops->hits->freq;
	iterfreq = ops->iter->freq;
	ifreq = &iterfreq->freq [0];
	hfreq = &hitsfreq->freq [0];
	ops->odi->freq.docid = 0;
	ops->odi->numdoc = 0;
	
	if (ops->mpt->hassortkey && ops->withdraw) {
		hassortkey = 21;		
		ops->hits->hassortkey = ops->mpt->hassortkey;
	}
	else if (ops->iter->hassortkey) hassortkey = 11;
	if (ops->mpt->hasextra && ops->withdraw) {
		ops->hits->hasextra = ops->mpt->hasextra;
		if (abs (ops->mpt->hasextra) == 1) hasextra = 21;
		else  hasextra = 22;
	}	
	else if (ops->iter->hasextra) {
		if (abs (ops->iter->hasextra) == 1) hasextra = 11;
		else  hasextra = 12;
	}
	
	/* union makes useless sortkey or extra value, need to rebuild */
	if (ops->hits->hassortkey > 0) ops->hits->hassortkey *= -1;
	if (ops->hits->hasextra > 0) ops->hits->hasextra *= -1;	
	
	//printf ("\n###hitsfreq->position: %d hitsfreq->position: %d\n",hitsfreq->position, iterfreq->position);
	//printf ("\n###ops->mpt->dc: %d ops->hits->dc:%d ops->iter->dc:%d\n\n",ops->mpt->dc, ops->hits->dc, ops->iter->dc);
	
	for (i = ops->mpt->dc; i-- ;) {
		if (!ATadvance (ops)) return -1;
		
		ic = ops->iter->dc - iterfreq->position;
		if (ic > 0) {
			for (; ic--; iterfreq->position++, ifreq++) {
				if (ifreq->docid >= ops->odi->freq.docid) break;
	
				AT_HITS_BEGIN_ADD
				hfreq->docid = ifreq->docid;
				if (ops->N) {
					hfreq->score.score = ifreq->score.score;				
				}  else if (hassortkey) {				
					if (hassortkey == 11)
						hfreq->score.sort = ifreq->score.sort;						
					else
						hfreq->score.sort = -1;
				}
				
				if (hasextra) {
					if (hasextra == 11)
						hfreq->extra.ival = ifreq->extra.ival;
					else if (hasextra == 12)
						hfreq->extra.fval = ifreq->extra.fval;
					else if (hasextra == 21)
						hfreq->extra.ival = -1;	
					else if (hasextra == 22)
						hfreq->extra.fval = -1.0F;	
				}
				AT_HITS_END_ADD
			}
		}	

		AT_HITS_BEGIN_ADD
		if (ifreq->docid == ops->odi->freq.docid) {
			hfreq->docid = ifreq->docid;
			if (ops->N) {
				hfreq->score.score = ifreq->score.score + ops->odi->freq.score.score;
			} else if (hassortkey) {				
				if (hassortkey == 11)
					hfreq->score.sort = ifreq->score.sort;
				else
					hfreq->score.sort = ops->odi->freq.score.sort;				
			}
			
			if (hasextra) {
				if (hasextra == 11)
					hfreq->extra.ival = ifreq->extra.ival;
				else if (hasextra == 12)
					hfreq->extra.fval = ifreq->extra.fval;
				else if (hasextra == 21)
					hfreq->extra.ival = ops->odi->freq.extra.ival;	
				else if (hasextra == 22)
					hfreq->extra.fval = ops->odi->freq.extra.fval;	
			}
					
			ifreq++;
			iterfreq->position++;	
		}

		else {
			hfreq->docid = ops->odi->freq.docid;
			if (ops->N) {
				hfreq->score.score = ops->odi->freq.score.score;
			} else if (hassortkey) {				
				if (hassortkey == 11)
					hfreq->score.sort = -1;						
				else
					hfreq->score.sort = ops->odi->freq.score.sort;
			}
			if (hasextra) {
				if (hasextra == 11)
					hfreq->extra.ival = -1;
				else if (hasextra == 12)
					hfreq->extra.fval = -1.0F;
				else if (hasextra == 21)
					hfreq->extra.ival = ops->odi->freq.extra.ival;	
				else if (hasextra == 22)
					hfreq->extra.fval = ops->odi->freq.extra.fval;	
			}				
		}
		AT_HITS_END_ADD
	}
	
	//printf ("\n---hitsfreq->position: %d\n\n",hitsfreq->position);
	
	ic = ops->iter->dc - iterfreq->position;
	if (ic > 0) {
		for (; ic--; iterfreq->position++, ifreq++)	 {
			
			AT_HITS_BEGIN_ADD
			hfreq->docid =ifreq->docid;
			if (ops->N) {
				hfreq->score.score = ifreq->score.score;
			} else if (hassortkey) {				
				if (hassortkey == 11)
					hfreq->score.sort = ifreq->score.sort;						
				else
					hfreq->score.sort = -1;
			}
			if (hasextra) {
				if (hasextra == 11)
					hfreq->extra.ival = ifreq->extra.ival;
				else if (hasextra == 12)
					hfreq->extra.fval = ifreq->extra.fval;
				else if (hasextra == 21)
					hfreq->extra.ival = -1;	
				else if (hasextra == 22)
					hfreq->extra.fval = -1.0F;	
			}
			AT_HITS_END_ADD
		}
	}
	
	ops->hits->dc = hitsfreq->position;
	ATreset (ops);
	return ops->hits->dc;
}


static int
ATtrim (Operator* ops)
{
	int i, ic;
	int found;
	IBUCKET* hitsfreq, *iterfreq;
	FREQ *ifreq, *hfreq;
	int hasextra = 0, hassortkey = 0;

	if (ops->mpt->dc == -1) return ops->hits->dc;

	ATswap (ops);

	hitsfreq = ops->hits->freq;
	iterfreq = ops->iter->freq;
	ifreq = &iterfreq->freq [0];
	hfreq = &hitsfreq->freq [0];
	ops->odi->freq.docid = 0;
	ops->odi->numdoc = 0;
	
	if (ops->iter->hassortkey) hassortkey = 11;
	if (ops->iter->hasextra) {
		if (abs (ops->iter->hasextra) == 1) hasextra = 11;
		else  hasextra = 12;
	}
	
	if (!ops->withdraw && ops->mpt->dc > SKIP_INTERVAL && ops->iter->dc && ops->mpt->dc / ops->iter->dc > (SKIP_INTERVAL >> 1)) {
		for (ic = ops->iter->dc; ic--; iterfreq->position++, ifreq++) {
			found = ATsearch (ops, ifreq->docid);

			if (!found) return -1;
			if (found == -2) break;
			if (found == 1) continue;

			AT_HITS_BEGIN_ADD
			hfreq->docid = ifreq->docid;			
			if (ops->N) {
				hfreq->score.score = ifreq->score.score;
			} else if (hassortkey) {				
				hfreq->score.sort = ifreq->score.sort;				
			}
			
			if (hasextra) {
				if (hasextra == 11)
					hfreq->extra.ival = ifreq->extra.ival;
				else
					hfreq->extra.fval = ifreq->extra.fval;
			}			
			AT_HITS_END_ADD
		}
	}

	else {
		for (i = ops->mpt->dc; i -- ;) {
			if (!ATadvance (ops)) return -1;
			ic = ops->iter->dc - iterfreq->position;
			if (ic <= 0) break;
			for (; ic--; iterfreq->position++, ifreq++)	 {
				if (ifreq->docid > ops->odi->freq.docid) {
					break;
				}

				else if (ifreq->docid == ops->odi->freq.docid) {
					ifreq++;
					iterfreq->position++;
					break;
				}

				AT_HITS_BEGIN_ADD
				hfreq->docid = ifreq->docid;
				if (ops->N) {
					hfreq->score.score = ifreq->score.score;
				} else if (hassortkey) {				
					hfreq->score.sort = ifreq->score.sort;				
				}
				if (hasextra) {
					if (hasextra == 11)
						hfreq->extra.ival = ifreq->extra.ival;
					else
						hfreq->extra.fval = ifreq->extra.fval;
				}
				AT_HITS_END_ADD
			}				
		}
	}
	
	ic = ops->iter->dc - iterfreq->position;
	if (ic > 0) {
		for (; ic--; iterfreq->position++, ifreq++) {
			
			AT_HITS_BEGIN_ADD
			hfreq->docid = ifreq->docid;
			if (ops->N) {
				hfreq->score.score = ifreq->score.score;
			} else if (hassortkey) {				
				hfreq->score.sort = ifreq->score.sort;				
			}			
			if (hasextra) {
				if (hasextra == 11)
					hfreq->extra.ival = ifreq->extra.ival;
				else
					hfreq->extra.fval = ifreq->extra.fval;
			}
			AT_HITS_END_ADD
		}
	}

	ops->hits->dc = hitsfreq->position;
	ATreset (ops);
	return ops->hits->dc;
}


static int
ATbetween (Operator* ops, long long min, long long max, char operate, int set, int want)
{
	int _shift;
	unsigned char _uchar;
	int i, ic, k, prev = 0;
	long long sortkey;
	IBUCKET* hitsfreq, *iterfreq;
	FREQ *ifreq, *hfreq;
	int match, load = 0;
	BFILE* bfile;
	int size;
	int hasextra = 0, hassortkey = 0;
	
	if (!ops->hits->dc) {
		load = 1;
	}
	else {
		ATswap (ops);
		load = 0;
	}

	hitsfreq = ops->hits->freq;
	iterfreq = ops->iter->freq;
	ifreq = &iterfreq->freq [0];
	hfreq = &hitsfreq->freq [0];
	bfile = ops->scorer->bsmp;
	size = ops->scorer->size;
	
	if (set) ops->hits->hassortkey = 1;
	else if (ops->iter->hassortkey) hassortkey = 11;
	if (ops->iter->hasextra) {
		if (abs (ops->iter->hasextra) == 1) hasextra = 11;
		else  hasextra = 12;
	}
			
	if (load) {
		i = 0;
		/* fetch random */
		if (want != -1 && min == -1 && max == -1) i = ops->scorer->numdoc - want;
		if (i < 0) i = 0;
		for (ic  = ops->scorer->numdoc - i; ic-- ; i++) {
			bseek (bfile, i * size);
			breadInt (bfile, sortkey, size);

			if (min != -1 && sortkey < min) continue;
			if (max != -1 && sortkey >= max) continue;

			AT_HITS_BEGIN_ADD
			hfreq->docid = i;
			if (ops->N) {
				hfreq->score.score = 0.0F;
			} else if (set) {
				hfreq->score.sort = sortkey;			
			}
			AT_HITS_END_ADD
		}
		
		ops->hits->dc = hitsfreq->position;
		ATreset (ops);
		return ops->hits->dc;
	}
	
	else if (operate == OP_UNION) {
		if (!set && ops->hits->hassortkey > 0) ops->hits->hassortkey *= -1;
		if (ops->hits->hasextra > 0) ops->hits->hasextra *= -1;
		
		for (k = ops->iter->dc; k-- ; ifreq++) {
			for (i=prev; i <= (int) ifreq->docid; i++) {
				bseek (bfile, i * size);
				breadInt (bfile, sortkey, size);
				if (i != (int) ifreq->docid) {
					if (min != -1 && sortkey < min) continue;
					if (max != -1 && sortkey >= max) continue;
				}
	
				AT_HITS_BEGIN_ADD
				hfreq->docid = i;
				if (ops->N) {
					if (i == ifreq->docid) hfreq->score.score = ifreq->score.score;				
					else hfreq->score.score = 0.0F;
				} else if (set) {
					hfreq->score.sort = sortkey;
				} else if (hassortkey) {
					if (i == ifreq->docid) hfreq->score.sort = ifreq->score.sort;
					else hfreq->score.sort = -1;
				}
				if (hasextra) {
					if (hasextra == 11) {
						if (i == ifreq->docid) hfreq->extra.ival = ifreq->extra.ival;
						else hfreq->extra.ival = -1;
					}		
					else {
						if (i == ifreq->docid) hfreq->extra.fval = ifreq->extra.fval;
						else hfreq->extra.fval = -1.0F;
					}					
				}
				AT_HITS_END_ADD
			}			
			prev = ifreq->docid + 1;
		}
		
		for (i = prev; i < ops->scorer->numdoc; i++) {
			bseek (bfile, i * size);
			breadInt (bfile, sortkey, size);

			if (min != -1 && sortkey < min) continue;
			if (max != -1 && sortkey >= max) continue;

			AT_HITS_BEGIN_ADD
			hfreq->docid = i;
			if (ops->N) {
				hfreq->score.score = 0.0F;
			} else if (set) {
				hfreq->score.sort = sortkey;
			} else if (hassortkey) {
				hfreq->score.sort = -1;
			}
			if (hasextra) {
				if (hasextra == 11) {
					hfreq->extra.ival = -1;
				}
				else {
					hfreq->extra.fval = -1.0F;
				}					
			}
			AT_HITS_END_ADD
		}
		ops->hits->dc = hitsfreq->position;
		ATreset (ops);
		return ops->hits->dc;		
	}
	
	for (i = ops->iter->dc; i -- ; ifreq++) {
		/* set sort key */
		bseek (bfile, ifreq->docid * size);
		breadInt (bfile, sortkey, size);

		match = 1;
		if (min != -1 && sortkey < min) match = 0;
		if (max != -1 && sortkey >= max) match = 0;
		if (operate == OP_INTERSECT && !match) continue;
		else if (operate == OP_TRIM && match) continue;

		AT_HITS_BEGIN_ADD
		hfreq->docid = ifreq->docid;		
		if (ops->N) {
			hfreq->score.score = ifreq->score.score;
		} else if (set) {
			hfreq->score.sort = sortkey;
		} else if (hassortkey) {
			hfreq->score.sort = ifreq->score.sort;				
		}
		
		if (hasextra) {
			if (hasextra == 11)
				hfreq->extra.ival = ifreq->extra.ival;
			else
				hfreq->extra.fval = ifreq->extra.fval;
		}		
		AT_HITS_END_ADD
	}

	ops->hits->dc = hitsfreq->position;
	ATreset (ops);
	return ops->hits->dc;

ioreaderror:
	return -1;
}

static int
ATbit (Operator* ops, long long bit, char* smode, char operate, int set, int want)
{
	int _shift;
	unsigned char _uchar;
	int i, ic, mode = 0, k, prev = 0;
	long long bitkey;
	IBUCKET* hitsfreq, *iterfreq;
	FREQ *ifreq, *hfreq;
	int match, load = 0;
	BFILE* bfile;
	int size;
	int hasextra = 0, hassortkey = 0;

	/*
	[mode]
		0: AND
		1: OR
		2: XOR
	*/
	
	if (strcmp (smode, "all") == 0) mode = 0;
	else if (strcmp (smode, "any") == 0) mode = 1;
	else if (strcmp (smode, "none") == 0) mode = 2;

	if (!ops->hits->dc) {
		load = 1;
	}
	
	else {
		ATswap (ops);
		load = 0;
	}

	hitsfreq = ops->hits->freq;
	iterfreq = ops->iter->freq;
	ifreq = &iterfreq->freq [0];
	hfreq = &hitsfreq->freq [0];
	bfile = ops->scorer->bsmp;
	size = ops->scorer->size;
	if (set) ops->hits->hassortkey = 1;
	else if (ops->iter->hassortkey) hassortkey = 11;
	if (ops->iter->hasextra) {
		if (abs (ops->iter->hasextra) == 1) hasextra = 11;
		else  hasextra = 12;
	}
	
	if (load) {
		i = 0;
		if (want != -1 && bit == -1) i = ops->scorer->numdoc - want;
		if (i < 0) i = 0;
		for (ic  = ops->scorer->numdoc - i; ic-- ; i++) {
			bseek (bfile, i * size);
			breadInt (bfile, bitkey, size);

			if (mode == 0 && (bit & bitkey) != bit) continue;
			else if (mode == 1 && (bit & bitkey) == 0) continue;
			else if (mode == 2 && (bit & bitkey) == bit) continue;

			AT_HITS_BEGIN_ADD
			hfreq->docid = i;
			if (ops->N) {
				hfreq->score.score = 0.0F;
			} else if (set) {
				hfreq->score.sort = bitkey;	
			}
			AT_HITS_END_ADD
		}
		
		ops->hits->dc = hitsfreq->position;
		ATreset (ops);
		return ops->hits->dc;
	}
	
	else if (operate == OP_UNION) {
		if (!set && ops->hits->hassortkey > 0) ops->hits->hassortkey *= -1;
		if (ops->hits->hasextra > 0) ops->hits->hasextra *= -1;
		
		for (k = ops->iter->dc; k-- ; ifreq++) {			
			for (i=prev; i <= (int) ifreq->docid; i++) {
				bseek (bfile, i * size);
				breadInt (bfile, bitkey, size);
				if (i != (int) ifreq->docid) {
					if (mode == 0 && (bit & bitkey) != bit) continue;
					else if (mode == 1 && (bit & bitkey) == 0) continue;
					else if (mode == 2 && (bit & bitkey) == bit) continue;
				}		
	
				AT_HITS_BEGIN_ADD
				hfreq->docid = i;				
				if (ops->N) {
					if (i == ifreq->docid) hfreq->score.score = ifreq->score.score;				
					else hfreq->score.score = 0.0F;
				} else if (set) {
					hfreq->score.sort = bitkey;
				} else if (hassortkey) {
					if (i == ifreq->docid) hfreq->score.sort = ifreq->score.sort;
					else hfreq->score.sort = -1;
				}
				if (hasextra) {
					if (hasextra == 11) {
						if (i == ifreq->docid) hfreq->extra.ival = ifreq->extra.ival;
						else hfreq->extra.ival = -1;
					}		
					else {
						if (i == ifreq->docid) hfreq->extra.fval = ifreq->extra.fval;
						else hfreq->extra.fval = -1.0F;
					}
				}
				AT_HITS_END_ADD
			}			
			prev = ifreq->docid + 1;
		}
		
		for (i = prev; i < ops->scorer->numdoc; i++) {
			bseek (bfile, i * size);
			breadInt (bfile, bitkey, size);

			if (mode == 0 && (bit & bitkey) != bit) continue;
			else if (mode == 1 && (bit & bitkey) == 0) continue;
			else if (mode == 2 && (bit & bitkey) == bit) continue;

			AT_HITS_BEGIN_ADD			
			hfreq->docid = i;
			if (ops->N) {
				hfreq->score.score = 0.0F;
			} else if (set) {
				hfreq->score.sort = bitkey;	
			} else if (hassortkey) {
				hfreq->score.sort = -1;	
			}			
			
			if (hasextra) {
				if (hasextra == 11)
					hfreq->extra.ival = -1;
				else 
					hfreq->extra.fval = -1.0F;								
			}			
			AT_HITS_END_ADD
		}
		ops->hits->dc = hitsfreq->position;
		ATreset (ops);
		return ops->hits->dc;
	}
	
	for (i = ops->iter->dc; i -- ; ifreq++) {
		/* set sort key */
		bseek (bfile, ifreq->docid * size);
		breadInt (bfile, bitkey, size);

		match = 1;
		if (mode == 0 && (bit & bitkey) != bit) match = 0;
		else if (mode == 1 && (bit & bitkey) == 0) match = 0;
		else if (mode == 2 && (bit & bitkey) == bit) match = 0;
		if (operate == OP_INTERSECT && !match) continue;
		else if (operate == OP_TRIM && match) continue;

		AT_HITS_BEGIN_ADD		
		hfreq->docid = ifreq->docid;
		if (ops->N) {
			hfreq->score.score = ifreq->score.score;
		} else if (set) {
			hfreq->score.sort = bitkey;	
		} 
		else if (hassortkey) {
			hfreq->score.sort = ifreq->score.sort;				
		}
		
		if (hasextra) {
			if (hasextra == 11)
				hfreq->extra.ival = ifreq->extra.ival;
			else
				hfreq->extra.fval = ifreq->extra.fval;
		}
		AT_HITS_END_ADD
	}

	ops->hits->dc = hitsfreq->position;
	ATreset (ops);
	return ops->hits->dc;

ioreaderror:
	return -1;

}

static int
ATdistance (Operator* ops, long long baselat, long long baselong, int pydistance, char operate, int set)
{
	int _shift;
	unsigned char _uchar;
	int i, ic, k, prev = 0;
	IBUCKET* hitsfreq, *iterfreq;
	FREQ *ifreq, *hfreq;
	long long otherlat, otherlong, delta;
	double distance;
	int load = 0;
	long long maxlat, minlat, maxlong, minlong;
	double tdistance;
	int eachsize;
	double baselatf, baselongf;
	BFILE* bfile;
	int size;
	int hassortkey = 0, hasextra = 0;
	double precision;

	eachsize = ops->scorer->size / 2;
	precision = pow (10.0, (double)(ops->scorer->size - 2));	
	
	distance = (double) pydistance;
	baselatf = (baselat / precision) - 180.0;
	baselongf = (baselong / precision) - 180.0;

	delta = (long long) (distance / (LATITUDE1DEGREE / precision)); /* meters per 1 / 10000 degree */
	maxlat = baselat + delta;
	minlat = baselat - delta;
	delta = (long long) (distance / (LONGITUDE1DEGREE / precision));
	maxlong = baselong + delta;
	minlong = baselong - delta;
	
	if (!ops->hits->dc) {
		load = 1;
	}
	else {
		ATswap (ops);
		load = 0;
	}
	
	hitsfreq = ops->hits->freq;
	iterfreq = ops->iter->freq;
	ifreq = &iterfreq->freq [0];
	hfreq = &hitsfreq->freq [0];
	bfile = ops->scorer->bsmp;
	size = ops->scorer->size;
	
	if (ops->iter->hassortkey) hassortkey = 11;
	if (set) ops->hits->hasextra = 2;
	else if (ops->iter->hasextra) {
		if (abs (ops->iter->hasextra) == 1) hasextra = 11;
		else  hasextra = 12;
	}	
		
	if (load) {
		for (ic  = ops->scorer->numdoc, i = 0; ic-- ; i++) {
			bseek (bfile, i * size);
			breadInt (bfile, otherlat, eachsize);
						
			/* eleminate too large latitude */
			if (otherlat == 0 || otherlat > maxlat || otherlat < minlat) {
				breadInt (ops->scorer->bsmp, otherlong, eachsize);				
				continue;
			}
			breadInt (bfile, otherlong, eachsize);			
			if (otherlong > maxlong || otherlong < minlong) {
				continue;
			}
			/*
				Simple Measurement
				tdistance = sqrt (pow (LATITUDE1DEGREE * ((double)(otherlat - baselat) / precision), 2.0) + pow (LONGITUDE1DEGREE * ((double)(otherlong - baselong) / precision), 2.0));
			*/
			tdistance = mdistance (baselatf, baselongf, (double)(otherlat / precision - 180.0), (double)(otherlong / precision - 180.0));
			if (tdistance > distance) continue;

			AT_HITS_BEGIN_ADD
			hfreq->docid = i;
			if (ops->N) {
				hfreq->score.score = 0.0F;
			}			
			if (set) hfreq->extra.fval = (float) (tdistance / 1000.0);
			AT_HITS_END_ADD
		}
		
		ops->hits->dc = hitsfreq->position;		
		ATreset (ops);
		return ops->hits->dc;		
	}
	
	else if (operate == OP_UNION) {
		ops->hits->hassortkey = 0; /* useless sortkey, must rebuyild */
		if (!set && ops->hits->hasextra > 0) ops->hits->hasextra *= -1;
		if (ops->hits->hassortkey > 0) ops->hits->hassortkey *= -1;
			
		for (k = ops->iter->dc; k-- ; ifreq++) {
			for (i=prev; i <= (int) ifreq->docid; i++) {
				bseek (bfile, i * size);
				breadInt (bfile, otherlat, eachsize);
				if (i != ifreq->docid) {
					/* eleminate too large latitude */
					if (otherlat == 0 || otherlat > maxlat || otherlat < minlat) {
						breadInt (ops->scorer->bsmp, otherlong, eachsize);
						continue;
					}
				}	
				breadInt (bfile, otherlong, eachsize);
				if (i != ifreq->docid) {
					if (otherlong > maxlong || otherlong < minlong) {
						continue;
					}
				}	
				/*
					Simple Measurement
					tdistance = sqrt (pow (LATITUDE1DEGREE * ((double)(otherlat - baselat) / precision), 2.0) + pow (LONGITUDE1DEGREE * ((double)(otherlong - baselong) / precision), 2.0));
				*/
				tdistance = mdistance (baselatf, baselongf, (double)(otherlat / precision - 180.0), (double)(otherlong / precision - 180.0));
				if (i != ifreq->docid) {
					if (tdistance > distance) continue;
				}
				AT_HITS_BEGIN_ADD
				hfreq->docid = i;
				if (ops->N) {
					if (i == ifreq->docid) hfreq->score.score = ifreq->score.score;				
					else hfreq->score.score = 0.0F;
				} else if (hassortkey) {
					if (i == ifreq->docid) hfreq->score.sort = ifreq->score.sort;
					else hfreq->score.sort = -1;	
				}
				
				if (set) hfreq->extra.fval = (float) (tdistance / 1000.0);
				else if (hasextra)	{
					if (hasextra == 11) {
						if (i == ifreq->docid) hfreq->extra.ival = ifreq->extra.ival;
						else hfreq->extra.ival = -1;
					}		
					else {
						if (i == ifreq->docid) hfreq->extra.fval = ifreq->extra.fval;
						else hfreq->extra.fval = -1.0F;
					}		
				}				
				AT_HITS_END_ADD
			}
			prev = ifreq->docid + 1;
		}
		
		for (i = prev; i < ops->scorer->numdoc; i++) {
			bseek (bfile, i * size);
			breadInt (bfile, otherlat, eachsize);
			/* eleminate too large latitude */
			if (otherlat == 0 || otherlat > maxlat || otherlat < minlat) {
				breadInt (ops->scorer->bsmp, otherlong, eachsize);
				continue;
			}
			breadInt (bfile, otherlong, eachsize);
			if (otherlong > maxlong || otherlong < minlong) {
				continue;
			}
			/*
				Simple Measurement
				tdistance = sqrt (pow (LATITUDE1DEGREE * ((double)(otherlat - baselat) / precision), 2.0) + pow (LONGITUDE1DEGREE * ((double)(otherlong - baselong) / precision), 2.0));
			*/
			tdistance = mdistance (baselatf, baselongf, (double)(otherlat / precision - 180.0), (double)(otherlong / precision - 180.0));
			if (tdistance > distance) continue;

			AT_HITS_BEGIN_ADD
			hfreq->docid = i;
			if (ops->N) {
				hfreq->score.score = 0.0F;
			} else if (hassortkey) {
				hfreq->score.sort = -1;	
			}			
			if (set) hfreq->extra.fval = (float) (tdistance / 1000.0);
			else if (hasextra) {
				if (hasextra == 11)
					hfreq->extra.ival = -1;
				else 
					hfreq->extra.fval = -1.0F;								
			}
			AT_HITS_END_ADD
		}
		ops->hits->dc = hitsfreq->position;
		ATreset (ops);
		return ops->hits->dc;
	}
	
	for (i = ops->iter->dc; i -- ; ifreq++) {
		bseek (bfile, ifreq->docid * size);
		breadInt (bfile, otherlat, eachsize);
		if (otherlat == 0 || otherlat > maxlat || otherlat < minlat) {
			breadInt (ops->scorer->bsmp, otherlong, eachsize);
			continue;
		}
		breadInt (ops->scorer->bsmp, otherlong, eachsize);
		if (otherlong > maxlong || otherlong < minlong) {
			continue;
		}
		tdistance = mdistance (baselatf, baselongf, (double)(otherlat / precision - 180.0), (double)(otherlong / precision - 180.0));
		if (operate == OP_INTERSECT && tdistance > distance) continue;
		else if (operate == OP_TRIM && tdistance <= distance) continue;

		AT_HITS_BEGIN_ADD		
		hfreq->docid = ifreq->docid;
		
		if (ops->N) {
			hfreq->score.score = ifreq->score.score;
		} else if (hassortkey) {
			hfreq->score.sort = ifreq->score.sort;	
		}
		
		if (set) hfreq->extra.fval = (float) (tdistance / 1000.0);
		else if (hasextra) {
			if (hasextra == 11)
				hfreq->extra.ival = ifreq->extra.ival;
			else
				hfreq->extra.fval = ifreq->extra.fval;
		}		
		AT_HITS_END_ADD
	}

	ops->hits->dc = hitsfreq->position;
	ATreset (ops);
	return ops->hits->dc;

ioreaderror:
	return -1;
}



/**********************************************************************
Sort Key Setting
**********************************************************************/

static int ATsortset_key (Operator* ops) {
	unsigned char _uchar;
	int _shift, i;
	FREQ* hfreq;
	//printf ("ops->hits->hassortkey: %d\n", ops->hits->hassortkey);
	if (ops->hits->hassortkey > 0) return ops->hits->dc;
	/* sort by sortmap*/
	hfreq = &ops->hits->freq->freq [0];
	for (i = ops->hits->dc; i ; i--, hfreq++) {
		if (ops->hits->hassortkey < 0 && hfreq->score.sort != -1) continue;		
		/* set sort key */
		bseek (ops->scorer->bsmp, hfreq->docid * ops->scorer->size);
		breadInt (ops->scorer->bsmp, hfreq->score.sort, ops->scorer->size);
	}
	ops->hits->hassortkey = 1;
	return ops->hits->dc;
	
ioreaderror:
	return -1;	
}

static int ATsortset_coord (Operator* ops, long long baselat, long long baselong) {
	unsigned char _uchar;
	int _shift, i;
	FREQ* hfreq;
	long long otherlat, otherlong, eachsize;
	double tdistance, baselatf, baselongf;
	double precision;
	
	//printf ("ops->hits->hasextra: %d\n", ops->hits->hasextra);
	if (ops->hits->hasextra > 0) return ops->hits->dc;
	
	eachsize = ops->scorer->size / 2;	
	precision = pow (10.0, (double)(ops->scorer->size - 2));
	
	baselatf = (baselat / precision) - 180.0;
	baselongf = (baselong / precision) - 180.0;
	hfreq = &ops->hits->freq->freq [0];
	
	for (i = ops->hits->dc; i ; i--, hfreq++) {
		if (ops->hits->hasextra < 0 && hfreq->extra.fval != -1.0F) continue;
		bseek (ops->scorer->bsmp, hfreq->docid * ops->scorer->size);
		breadInt (ops->scorer->bsmp, otherlat, eachsize);			
		breadInt (ops->scorer->bsmp, otherlong, eachsize);
		tdistance = mdistance (baselatf, baselongf, (double)(otherlat / precision - 180.0), (double)(otherlong / precision - 180.0));
		hfreq->extra.fval = (float) (tdistance / 1000.0);
	}
	ops->hits->hasextra = 2;
	return ops->hits->dc;
	
ioreaderror:
	return -1;
}

static int
ATsort (Operator* ops, int want, int sortorder, int bysortkey, int byextra)
{
	int (*compar)(const void *, const void *);
	compar = ascsortkey_func; //sortorder == 1
	
	if (!want || want > ops->hits->dc) want = ops->hits->dc;
	if (bysortkey && ops->hits->hassortkey) {
		if (sortorder == -1) compar = descsortkey_func;
		heapsort (ops->hits->freq->freq, ops->hits->dc, sizeof (FREQ), want, compar);
	}

	else if (byextra && ops->hits->hasextra) {
		if (sortorder == 1) {
		 	/* sort asc */
			if (ops->hits->hasextra == 2) compar = ascextraf_func;
			else compar = ascextrai_func;
		}
		else if (sortorder == -1) {
			if (ops->hits->hasextra == 2) compar = descextraf_func;
			else compar = descextrai_func;
		}
		heapsort (ops->hits->freq->freq, ops->hits->dc, sizeof (FREQ), want, compar);
	}

	else if (ops->N && sortorder) {
		if (sortorder == -1) compar = descscore_func;
		else compar = ascscore_func;
		heapsort (ops->hits->freq->freq, ops->hits->dc, sizeof (FREQ), want, compar);
	}

	return 0;
}



/***************************************************************
Exporting Methods
****************************************************************/
static PyObject *
Compute_new (PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	Compute *self;
	self = (Compute*) type -> tp_alloc(type, 0);
	return (PyObject*) self;
}

static int
Compute_init (Compute *self, PyObject *args)
{
	PyObject* pymem;
	int N = 0;
	
	self->ops = (Operator*) malloc (sizeof (Operator));
	if (!self->ops) return -1;	
	
	if (!PyArg_ParseTuple(args, "O|i", &pymem, &N)) return -1;
	
	ATinit (self->ops, (Memory*) PyCObject_AsVoidPtr (pymem), N);
	
	if (norm_table_index == 0) {
		for (norm_table_index = 0; norm_table_index < 256; norm_table_index++) {
			NORM_TABLE [norm_table_index] = norm_table_index / 2550.0F;
		}
	}
	return 0;
}

static void
Compute_dealloc (Compute* self)
{
	Py_TYPE(self)->tp_free ((PyObject*) self);
}

static PyObject*
Compute_reuse (Compute *self) {
	self->ops->temp = self->ops->iter;
	self->ops->iter = self->ops->hits;
	self->ops->hits = self->ops->temp;
	self->ops->hits->freq->position = 0;
	self->ops->hits->prox->position = 0;
	self->ops->iter->freq->position = 0;
	self->ops->iter->prox->position = 0;	
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
Compute_push (Compute *self) {
	int saved;
	saved = ATpush (self->ops);
	if (saved == -1)
		return PyErr_NoMemory ();
	return PyLong_FromLong (saved);
}

static PyObject* 
Compute_popright (Compute *self)
{
	return PyLong_FromLong (ATpop (self->ops, 0));
}

static PyObject* 
Compute_popleft (Compute *self)
{
	return PyLong_FromLong (ATpop (self->ops, 1));
}

static PyObject*
Compute_abort (Compute *self)
{
	ATreset (self->ops);
	self->ops->hits->dc = 0;
	self->ops->hits->freq->position = 0;
	self->ops->hits->prox->position = 0;
	return PyLong_FromLong (0);
}

static PyObject*
Compute_reset (Compute *self)
{
	ATreset (self->ops);
	Py_INCREF (Py_None);
	return Py_None;
}


static PyObject*
Compute_count (Compute *self)
{
	return PyLong_FromLong (ATcount (self->ops));	
}

static PyObject*
Compute_setcount (Compute *self, PyObject *args)
{
	if (!PyArg_ParseTuple(args, "i", &self->ops->estimate)) return NULL;
	self->ops->randomscan = 1;
	return PyLong_FromLong (self->ops->estimate);
}

static PyObject*
Compute_saved (Compute *self, PyObject *args)
{
	return PyLong_FromLong (self->ops->saved);
}

static PyObject*
Compute_withdrawed (Compute *self, PyObject *args)
{
	return PyLong_FromLong (self->ops->withdraw);
}
	
static PyObject*
Compute_newscan (Compute *self, PyObject *args)
{
	self->ops->saved = 0;
	self->ops->predict = 0;
	self->ops->estimate = 0;
	self->ops->randomscan = 0;

	self->ops->hits->dc = 0;
	self->ops->hits->hasprox = 0;
	self->ops->hits->hassortkey = 0;
	self->ops->hits->hasextra = 0;
	
	self->ops->hits->freq->position = 0;
	self->ops->hits->prox->position = 0;
	
	self->ops->iter->dc = 0;		
	
	ATreset (self->ops);
	return PyLong_FromLong (self->ops->N);
}

static PyObject*
Compute_setfreq (Compute *self, PyObject *args)
{
	/* 
	1: set freq for current term
	2: add freq for current term and previous value
	*/	
	if (!PyArg_ParseTuple(args, "i", &self->ops->setfreq)) return NULL;
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject*
Compute_close (Compute *self, PyObject *args) {
	Py_BEGIN_ALLOW_THREADS
	ATclose (self->ops);
	Py_END_ALLOW_THREADS
	free (self->ops);
	self->ops = NULL;
	Py_INCREF (Py_None);
	return Py_None;
}	

static PyObject*
Compute_hitdoc (Compute *self, PyObject *args)
{
	PyObject *list = NULL, *tuple, *pybits = Py_None, *result;
	Operator* ops;
	int i, index = 0;
	unsigned char* bits = NULL;
	int seg, want = 0;
	int docid, loop;
	FREQ* afreq = NULL;
	float normq = 1.0;

	if (!PyArg_ParseTuple(args, "i|iO", &seg, &want, &pybits)) return NULL;

	if (pybits != Py_None) {
		bits = PyCObject_AsVoidPtr (pybits);
	}
	
	ops = self->ops;
		
	if (!want || want > ops->hits->dc) want = ops->hits->dc;

	list = PyList_New (want);
	loop = ops->hits->dc;

	if (loop) {
		afreq = &ops->hits->freq->freq [loop - 1];
	}
	
	/* query normalization factor */
	if (ops->N) {
		normq = (float) sqrt(ops->sumofsquaredweight);
		if (!normq) {
			normq = 1.0F;
		}
		else {
			normq = 1.0F / normq;
		}
	}
	
	for (i = 0; i < loop; i++) {
		docid = afreq->docid;

		if (bits && (bits[docid >> 3] & (1 << (docid & 7)))) {
			if (ops->randomscan) ops->estimate--;
			else ops->hits->dc--;
			afreq--;
			continue;
		}

		if (ops->N) {			
			if (ops->hits->hasextra == 2)
				tuple = Py_BuildValue ("iiff", seg, docid, afreq->extra.fval, afreq->score.score * normq);
			else if (ops->hits->hasextra == 1)
				tuple = Py_BuildValue ("iiif", seg, docid, afreq->extra.ival, afreq->score.score * normq);
			else
				tuple = Py_BuildValue ("iiif", seg, docid, 0, afreq->score.score * normq);
		}

		else if (ops->hits->hassortkey) {
			if (ops->hits->hasextra == 2)
				tuple = Py_BuildValue ("iifi", seg, docid, afreq->extra.fval, afreq->score.sort);
			else if (ops->hits->hasextra == 1)
				tuple = Py_BuildValue ("iiii", seg, docid, afreq->extra.ival, afreq->score.sort);
			else
				tuple = Py_BuildValue ("iiii", seg, docid, 0, afreq->score.sort);
		}

		else {
			if (ops->hits->hasextra == 2)
				tuple = Py_BuildValue ("iifi", seg, docid, afreq->extra.fval, 0);
			else if (ops->hits->hasextra == 1)
				tuple = Py_BuildValue ("iiii", seg, docid, afreq->extra.ival, 0);
			else
				tuple = Py_BuildValue ("iiii", seg, docid, 0, 0);
		}

		PyList_SetItem (list, index, tuple);

		afreq--;
		index++;
		if (index == want) break;
	}

	if (!index) {
		Py_DECREF (list);
		return PyList_New (0);
	}
	
	else if (index < want) {
		result = PyList_GetSlice (list, 0, index);
		Py_DECREF (list);
		return result;
	}
	
	return list;
}

static PyObject*
Compute_set (Compute *self, PyObject *args) {
	int res;
	float weight = 1.0F;
	int df = 0;
	if (!PyArg_ParseTuple(args, "|if", &df, &weight)) return NULL;
	
	Py_BEGIN_ALLOW_THREADS	
	res = ATset (self->ops, df, weight);	
	Py_END_ALLOW_THREADS
	if (res == -1) {PyErr_SetFromErrno (PyExc_IOError); return NULL;}
	return PyLong_FromLong (res);
}

static PyObject*
Compute_intersect (Compute *self, PyObject *args) {
	int res;
	int near = 1, loose = 0;	
	if (!PyArg_ParseTuple(args, "|ii", &near, &loose)) return NULL;
	
	Py_BEGIN_ALLOW_THREADS
	res = ATintersect (self->ops, near, loose);
	Py_END_ALLOW_THREADS
	if (res == -1) {PyErr_SetFromErrno (PyExc_IOError); return NULL;}
	return PyLong_FromLong (res);
}

static PyObject*
Compute_trim (Compute *self, PyObject *args) {
	int res;
	
	Py_BEGIN_ALLOW_THREADS
	res = ATtrim (self->ops);
	Py_END_ALLOW_THREADS
	if (res == -1) {PyErr_SetFromErrno (PyExc_IOError); return NULL;}
	return PyLong_FromLong (res);
}

static PyObject*
Compute_union (Compute *self, PyObject *args) {
	int res;
	Py_BEGIN_ALLOW_THREADS
	res = ATunion (self->ops);
	Py_END_ALLOW_THREADS
	if (res == -1) {PyErr_SetFromErrno (PyExc_IOError); return NULL;}
	return PyLong_FromLong (res);
}

static PyObject*
Compute_between (Compute *self, PyObject *args) {
	int res;
	long long min = -1, max = -1;
	int want = -1, set = 0;
	char operate = '*';
	if (!PyArg_ParseTuple(args, "LL|cii", &min, &max, &operate, &set, &want)) return NULL;
	
	Py_BEGIN_ALLOW_THREADS
	res = ATbetween (self->ops, min, max, operate, set, want);
	Py_END_ALLOW_THREADS
	if (res == -1) {PyErr_SetFromErrno (PyExc_IOError); return NULL;}
	return PyLong_FromLong (res);
}

static PyObject*
Compute_bit (Compute *self, PyObject *args) {
	int res;
	long long bit = -1;
	int want = -1, set = 0;
	char operate = '*';
	char* smode;
	
	if (!PyArg_ParseTuple(args, "Ls|cii", &bit, &smode, &operate, &set, &want)) return NULL;
	
	Py_BEGIN_ALLOW_THREADS
	res = ATbit (self->ops, bit, smode, operate, set, want);
	Py_END_ALLOW_THREADS
	if (res == -1) {PyErr_SetFromErrno (PyExc_IOError); return NULL;}
	return PyLong_FromLong (res);
}

static PyObject*
Compute_distance (Compute *self, PyObject *args) {
	int res;
	long long baselat, baselong;
	int pydistance, set;
	char operate = '*';	
	if (!PyArg_ParseTuple(args, "LLi|ci", &baselat, &baselong, &pydistance, &operate, &set)) return NULL;	
	Py_BEGIN_ALLOW_THREADS
	res = ATdistance (self->ops, baselat, baselong, pydistance, operate, set);
	Py_END_ALLOW_THREADS
	if (res == -1) {PyErr_SetFromErrno (PyExc_IOError); return NULL;}
	return PyLong_FromLong (res);
}

static PyObject*
Compute_sortset_key (Compute *self, PyObject *args) {
	int res;
	Py_BEGIN_ALLOW_THREADS
	res = ATsortset_key (self->ops);
	Py_END_ALLOW_THREADS
	if (res == -1) {PyErr_SetFromErrno (PyExc_IOError); return NULL;}
	return PyLong_FromLong (res);
}

static PyObject*
Compute_sortset_coord (Compute *self, PyObject *args) {
	int res;
	long long baselat, baselong;
		
	if (!PyArg_ParseTuple(args, "LL", &baselat, &baselong)) return NULL;
	
	Py_BEGIN_ALLOW_THREADS
	res = ATsortset_coord (self->ops, baselat, baselong);
	Py_END_ALLOW_THREADS
	if (res == -1) {PyErr_SetFromErrno (PyExc_IOError); return NULL;}
	return PyLong_FromLong (res);
}

static PyObject*
Compute_sort (Compute *self, PyObject *args) {
	int res;
	int bysortkey, sortorder, byextra, want;
	if (!PyArg_ParseTuple(args, "iiii", &want, &sortorder, &bysortkey, &byextra)) return NULL;
	
	Py_BEGIN_ALLOW_THREADS
	res = ATsort (self->ops, want, sortorder, bysortkey, byextra);
	Py_END_ALLOW_THREADS
	if (res == -1) {PyErr_SetFromErrno (PyExc_IOError); return NULL;}
	return PyLong_FromLong (res);
}



/****************************************************************
Module Definition
****************************************************************/

static PyMemberDef Compute_members[] = {
    //{"N", T_INT, offsetof(Compute, N), 0, ""},
    {NULL}
};

static PyMethodDef Compute_methods[] = {
	{"set", (PyCFunction) Compute_set, METH_VARARGS, ""},
	{"count", (PyCFunction) Compute_count, METH_VARARGS, ""},
	{"saved", (PyCFunction) Compute_saved, METH_VARARGS, ""},
	{"intersect", (PyCFunction) Compute_intersect, METH_VARARGS, ""},
	{"union", (PyCFunction) Compute_union, METH_VARARGS, ""},
	{"trim", (PyCFunction) Compute_trim, METH_VARARGS, ""},
	{"between", (PyCFunction) Compute_between, METH_VARARGS, ""},
	{"distance", (PyCFunction) Compute_distance, METH_VARARGS, ""},
	{"bit", (PyCFunction) Compute_bit, METH_VARARGS, ""},
	{"push", (PyCFunction) Compute_push, METH_VARARGS, ""},
	{"popright", (PyCFunction) Compute_popright, METH_VARARGS, ""},
	{"popleft", (PyCFunction) Compute_popleft, METH_VARARGS, ""},
	{"reuse", (PyCFunction) Compute_reuse, METH_VARARGS, ""},
	{"hitdoc", (PyCFunction) Compute_hitdoc, METH_VARARGS, ""},
	{"sort", (PyCFunction) Compute_sort, METH_VARARGS, ""},
	{"newscan", (PyCFunction) Compute_newscan, METH_VARARGS, ""},
	{"abort", (PyCFunction) Compute_abort, METH_VARARGS, ""},
	{"close", (PyCFunction) Compute_close, METH_VARARGS, ""},
	{"setfreq", (PyCFunction) Compute_setfreq, METH_VARARGS, ""},
	{"reset", (PyCFunction) Compute_reset, METH_VARARGS, ""},
	{"setcount", (PyCFunction) Compute_setcount, METH_VARARGS, ""},
	{"withdrawed", (PyCFunction) Compute_withdrawed, METH_VARARGS, ""},
	{"sortset_coord", (PyCFunction) Compute_sortset_coord, METH_VARARGS, ""},
	{"sortset_key", (PyCFunction) Compute_sortset_key, METH_VARARGS, ""},
	{NULL}
};

PyTypeObject ComputeType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"core.Compute",			 /*tp_name*/
	sizeof (Compute),			 /*tp_basicsize*/
	0,						 /*tp_itemsize*/
	(destructor) Compute_dealloc, /*tp_dealloc*/
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
	0, //(iternextfunc) Compute_iternext,	   /* tp_iternext */
	Compute_methods,			 /* tp_methods */
	Compute_members,			 /* tp_members */
	0,						 /* tp_getset */
	0,						 /* tp_base */
	0,						 /* tp_dict */
	0,						 /* tp_descr_get */
	0,						 /* tp_descr_set */
	0,						 /* tp_dictoffset */
	(initproc) Compute_init,	  /* tp_init */
	0,						 /* tp_alloc */
	Compute_new,				 			/* tp_new */
};
