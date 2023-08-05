#include <stdlib.h>
#include "index.h"

Memory * 
memnew (int buffer_size) 
{
	Memory* memory = NULL;
	int i;
	
	if (!(memory = (Memory*) malloc (sizeof (Memory)))) return NULL;
	memory->usage = 0;
	memory->status = 1;
	//memory->mutex = global_mutext;
	
	memory->mfi = NULL;	
	memory->mfd = NULL;
	memory->msr = NULL;
	memory->mpt = NULL;
	memory->mco = NULL;
	memory->mht = NULL;
	memory->mbk = NULL;	
	memory->cla = NULL;
	memory->mmp = NULL;
	memory->tmp = NULL;
	memory->odi = NULL; // One Doc
	
	/* for stored field file */
	if (!(memory->mfi = (MFILE*) malloc (sizeof (MFILE)))) {memdel (memory); return NULL;}
	memory->mfi->btis = NULL;
	if (!(memory->mfi->btis = bopen (-1, 'r', 1024, 0))) {memdel (memory); return NULL;}
		
	if (!(memory->mfd = (MSTORED*) malloc (sizeof (MSTORED)))) {memdel (memory); return NULL;}
	memory->mfd->bfdi = NULL;
	memory->mfd->bfda = NULL;	
	if (!(memory->mfd->bfdi = bopen (-1, 'r', 1024, 0))) {memdel (memory); return NULL;}
	if (!(memory->mfd->bfda = bopen (-1, 'r', buffer_size, 0))) {memdel (memory); return NULL;}
	
	/* for sortmap */	
	if (!(memory->msr = (MSCORE*) malloc (sizeof (MSCORE)))) {memdel (memory); return NULL;}
	memory->msr->bsmp = NULL;
	if (!(memory->msr->bsmp = bopen (-1, 'r', buffer_size, 0))) {memdel (memory); return NULL;}
	
	/* for posting */	
	if (!(memory->mpt = (MPOSTING*) malloc (sizeof (MPOSTING)))) {memdel (memory); return NULL;}
	memory->mpt->freq = NULL;
	memory->mpt->prox = NULL;
	memory->mpt->skip = NULL;
	
	if (!(memory->mpt->freq = bopen (-1, 'r', buffer_size, 0))) {memdel (memory); return NULL;}
	if (!(memory->mpt->prox = bopen (-1, 'r', buffer_size, 0))) {memdel (memory); return NULL;}
	
	if (!(memory->mpt->skip = (MSKIP*) malloc (sizeof (MSKIP)))) {memdel (memory); return NULL;}
	memory->mpt->skip->skip = NULL;
	if (!(memory->mpt->skip->skip = bopen (-1, 'r', buffer_size, 0))) {memdel (memory); return NULL;}
	
	/* for compute */	
	if (!(memory->mco = (MCOMPUTE*) malloc (sizeof (MCOMPUTE)))) {memdel (memory); return NULL;}
	memory->mco->freq = NULL;
	memory->mco->prox = NULL;
	if (!(memory->mco->freq = iopen (buffer_size, 0))) {memdel (memory); return NULL;}
	if (!(memory->mco->prox = iopen (buffer_size, 1))) {memdel (memory); return NULL;}
		
	if (!(memory->mht = (MCOMPUTE*) malloc (sizeof (MCOMPUTE)))) {memdel (memory); return NULL;}
	memory->mht->freq = NULL;
	memory->mht->prox = NULL;	
	if (!(memory->mht->freq = iopen (buffer_size, 0))) {memdel (memory); return NULL;}
	if (!(memory->mht->prox = iopen (buffer_size, 1))) {memdel (memory); return NULL;}
	
	/* for banking banking queue */	
	if (!(memory->mbk = (MCOMPUTE*) malloc (sizeof (MCOMPUTE)))) {memdel (memory); return NULL;}
	memory->mbk->freq = NULL;
	memory->mbk->prox = NULL;
	if (!(memory->mbk->freq = iopen (buffer_size, 0))) {memdel (memory); return NULL;}
	if (!(memory->mbk->prox = iopen (buffer_size, 1))) {memdel (memory); return NULL;}
	
	/* dbint */
	if (!(memory->mmp = (MBFILE*) malloc (sizeof (MBFILE)))) {memdel (memory); return NULL;}		
	memory->mmp->bfdb = NULL;
	if (!(memory->mmp->bfdb = bopen (-1, 'r', buffer_size, 0))) {memdel (memory); return NULL;}
		
	/* for classifier */	
	if (!(memory->cla = malloc (sizeof (CLASSIFER)))) {memdel (memory); return NULL;}
	memory->cla->numpool = 8;
	memory->cla->corpus = NULL;
	memory->cla->feature = NULL;
	memory->cla->scores = NULL;
	for (i=0;i<3;i++) {
		memory->cla->temp [i] = NULL;
	}
	if (!(memory->cla->corpus = (FeatureInfo*) malloc (sizeof (FeatureInfo) * memory->cla->numpool))) {memdel (memory); return NULL;}
	if (!(memory->cla->feature = (FeatureInfo*) malloc (sizeof (FeatureInfo) * memory->cla->numpool))) {memdel (memory); return NULL;}
	if (!(memory->cla->scores = (ClassScore*) malloc (sizeof (ClassScore) * memory->cla->numpool))) {memdel (memory); return NULL;}
	for (i=0;i<3;i++) {
		if (!(memory->cla->temp [i] = (ClassScore*) malloc (sizeof (ClassScore) * memory->cla->numpool))) {memdel (memory); return NULL;}
	}
	
	/* for temp buffers */
	if (!(memory->tmp = (MTEMP*) malloc (sizeof (MTEMP)))) {memdel (memory); return NULL;}
	memory->tmp->bxx0 = NULL;
	memory->tmp->bxx1 = NULL;
	memory->tmp->bxx2 = NULL;
	if (!(memory->tmp->bxx0 = bopen (-1, 'w', buffer_size, 1))) {memdel (memory); return NULL;}
	if (!(memory->tmp->bxx1 = bopen (-1, 'w', buffer_size, 1))) {memdel (memory); return NULL;}		
	if (!(memory->tmp->bxx2 = bopen (-1, 'w', buffer_size, 1))) {memdel (memory); return NULL;}		
		
	/* for one posting */
	if (!(memory->odi = malloc (sizeof (ONEDOC)))) {memdel (memory); return NULL;}
	
	return memory;
}

int
memdel (Memory* memory) 
{
	int i;
	
	if (memory) {
		if (memory->mfi) {			
			if (memory->mfi->btis) bclose (memory->mfi->btis);			
			free (memory->mfi);			
		}
		
		if (memory->mfd) {			
			if (memory->mfd->bfdi) bclose (memory->mfd->bfdi);		
			if (memory->mfd->bfda) bclose (memory->mfd->bfda);		
			free (memory->mfd);			
		}
		
		if (memory->msr){				
			if (memory->msr->bsmp) bclose (memory->msr->bsmp);
			free (memory->msr);			
		}
		
		if (memory->mpt) {				
			if (memory->mpt->freq) bclose (memory->mpt->freq);
			if (memory->mpt->prox) bclose (memory->mpt->prox);	
			if (memory->mpt->skip) {
				if (memory->mpt->skip->skip) {
					bclose (memory->mpt->skip->skip);					
				}
				free (memory->mpt->skip);				
			}		
			free (memory->mpt);
		}	
		
		if (memory->mco) {				
			if (memory->mco->freq) iclose (memory->mco->freq);
			if (memory->mco->prox) iclose (memory->mco->prox);	
			free (memory->mco);			
		}	
		
		if (memory->mht) {
			if (memory->mht->freq) iclose (memory->mht->freq);
			if (memory->mht->prox) iclose (memory->mht->prox);	
			free (memory->mht);			
		}
		
		if (memory->mbk) {
			if (memory->mbk->freq) iclose (memory->mbk->freq);
			if (memory->mbk->prox) iclose (memory->mbk->prox);	
			free (memory->mbk);			
		}	
		
		if (memory->mmp) {
			if (memory->mmp->bfdb) bclose (memory->mmp->bfdb);
			free (memory->mmp);		
		}
		
		if (memory->tmp) {
			if (memory->tmp->bxx0) bclose (memory->tmp->bxx0);
			if (memory->tmp->bxx1) bclose (memory->tmp->bxx1);
			if (memory->tmp->bxx2) bclose (memory->tmp->bxx2);
			free (memory->tmp);
		}
		
		if (memory->cla) {
			if (memory->cla->corpus) free (memory->cla->corpus);
			if (memory->cla->feature) free (memory->cla->feature);	
			if (memory->cla->scores) free (memory->cla->scores);	
			for (i = 0; i < 3; i++) {
				if (memory->cla->temp [i]) {
					free (memory->cla->temp [i]);
				}	
			}	
			free (memory->cla);
		}
		if (memory->odi) free (memory->odi);
		free (memory);		
	}
	
	memory = NULL;
	return 1;
}

int
memusage (Memory* memory) 
{
	if (memory) {
		memory->usage = 0;
		
		memory->usage += bsize (memory->mfi->btis);
		
		memory->usage += bsize (memory->mfd->bfdi);
		memory->usage += bsize (memory->mfd->bfda);
		
		memory->usage += bsize (memory->mpt->freq);
		memory->usage += bsize (memory->mpt->prox);
		memory->usage += bsize (memory->mpt->skip->skip);
		
		memory->usage += bsize (memory->msr->bsmp);
		
		memory->usage += isize (memory->mco->freq);
		memory->usage += isize (memory->mco->prox);	
		
		memory->usage += isize (memory->mht->freq);
		memory->usage += isize (memory->mht->prox);
		
		memory->usage += isize (memory->mbk->freq);
		memory->usage += isize (memory->mbk->prox);
		
		memory->usage += bsize (memory->tmp->bxx0);
		memory->usage += bsize (memory->tmp->bxx1);		
		memory->usage += bsize (memory->tmp->bxx2);
		
		memory->usage += sizeof (FeatureInfo) * memory->cla->numpool * 2;
		memory->usage += sizeof (ClassScore) * memory->cla->numpool * 4;
		
		memory->usage += bsize (memory->mmp->bfdb);
		
		memory->usage += sizeof (ONEDOC);
		return memory->usage;
	}
	return -1;
}


