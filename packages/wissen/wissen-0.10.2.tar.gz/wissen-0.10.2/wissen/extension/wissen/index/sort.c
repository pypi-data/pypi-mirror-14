#include "index.h"
#include <stdlib.h>

extern int heapsort(void *members, int nmemb, int size, int max, int (*compar)(const void *, const void *));

int hsort (int *buffer[2], int nmemb, int size, int max) {
	int i, until, temp [2];
		
	if (heapsort (buffer, nmemb, size, max, value_compfunc) == -1)
		return -1;
	
	if (nmemb > max * 2) until = max;
	else until = nmemb / 2;
	
	for (i=0; i < until; i++) {
		temp [0] = buffer [i][0];
		temp [1] = buffer [i][1];
		buffer [i][0] = buffer [nmemb - i - 1][0];
		buffer [i][1] = buffer [nmemb - i - 1][1];		
		buffer [nmemb - i - 1][0] = temp [0];
		buffer [nmemb - i - 1][1] = temp [1];
	}
	return 0;
}

/*
DECODED* fsort (DECODED* base, int crop) {
	char type = 'X';
	type = base->type;
	qsort (base->dl, base->df, 8, key_compfunc);	
	if (crop && base->df > crop) {		
		base = (DECODED*) realloc (base, 9 + crop * sizeof (int) * 2);
		if (!base) return NULL;
		base->df = crop;		
	}
	return base;
}


DECODED* psort (DECODED *base, int crop, int maxsort) {
	if (hsort (base->dl, base->df, 8, maxsort) == -1) {
		free (base);
		return NULL;
	}
	
	if (crop && base->df > crop) {		
		base = (DECODED*) realloc (base, 9 + crop * sizeof (int) * 2);
		if (!base) return NULL;
		base->df = crop;		
	}
	return base;
}


DECODED* concat (DECODED *base, DECODED *iter) {
	int lastvalue;
	
	lastvalue = base->dl [base->df - 1][1];
	base = realloc (base, 9 + (base->df + iter->df) * sizeof (int) * 2);
	if (!base) {		
		free (iter);
		return NULL;
	}	
	base->dl [base->df - 1][1] = lastvalue;
	memcpy (base->dl [base->df], iter->dl [0], iter->df * sizeof (int) * 2);
	base->df += iter->df;	
	free (iter);
	return base;
}

*/
