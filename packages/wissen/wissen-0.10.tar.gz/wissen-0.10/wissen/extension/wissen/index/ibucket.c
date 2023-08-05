#include <stdio.h>
#include <stdlib.h>
#include "index.h"

IBUCKET* iopen (int max, int type)
{
	IBUCKET* ibucket;
		
	ibucket = malloc (sizeof (IBUCKET));
	if (!ibucket) return NULL;
	ibucket->position = 0;
	ibucket->max = max;
	ibucket->type = type;
	
	if (type == 0) {
		ibucket->freq = (FREQ*) malloc (max * sizeof (FREQ));
		if (!ibucket->freq) {
			free (ibucket);
			return NULL;
		}	
	}	
	else {
		ibucket->prox = (unsigned short int*) malloc (max * sizeof (unsigned short int));	
		if (!ibucket->prox) {
			free (ibucket);
			return NULL;
		}	
	}
		
	ibucket->extend = 1;	
	return ibucket;
}

int iextend (IBUCKET* ibucket, int extend)
{
	int basesize;	
	if (!extend) {
		basesize = ibucket->max / ibucket->extend;
		ibucket->extend ++;
		ibucket->max = basesize * ibucket->extend;
	}
	
	else if (ibucket->max < extend) {
		ibucket->max = extend;		
	}
	
	if (ibucket->type == 0) {
		ibucket->freq = (FREQ*) realloc (ibucket->freq, ibucket->max * sizeof (FREQ));
		if (!ibucket->freq) return 0;		
	}	
	else {
		ibucket->prox = (unsigned short int*) realloc (ibucket->prox, ibucket->max * sizeof (unsigned short int));
		if (!ibucket->prox) return 0;		
	}
	
	return ibucket->max;
}

int iclose (IBUCKET* ibucket)
{
	if (ibucket->type == 0) {
		if (ibucket->freq) free (ibucket->freq);
	}
	else {
		if (ibucket->prox)	free (ibucket->prox);
	}	
	free (ibucket);
	return 1;
}


int isize (IBUCKET* ibucket) {
	if (ibucket->type == 0) 
		return ibucket->max * sizeof (FREQ);
	else
		return ibucket->max * sizeof (unsigned short int);
}

