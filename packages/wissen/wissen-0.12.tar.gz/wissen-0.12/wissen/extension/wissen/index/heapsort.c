#include <sys/types.h>
#include <stdlib.h>
#include <stdio.h>

/*
 * Swap two areas of size number of bytes.  Although qsort(3) permits random
 * blocks of memory to be sorted, sorting pointers is almost certainly the
 * common case (and, were it not, could easily be made so).  Regardless, it
 * isn't worth optimizing; the SWAP's get sped up by the cache, and pointer
 * arithmetic gets lost in the time required for comparison function calls.
 */
#define	SWAP(a, b, count, size, tmp) { \
	count = size; \
	do { \
		tmp = *a; \
		*a++ = *b; \
		*b++ = tmp; \
	} while (--count); \
}

/* Copy one block of size size to another. */
#define COPY(a, b, count, size, tmp1, tmp2) { \
	count = size; \
	tmp1 = a; \
	tmp2 = b; \
	do { \
		*tmp1++ = *tmp2++; \
	} while (--count); \
}

/*
 * Build the list into a heap, where a heap is defined such that for
 * the records K1 ... KN, Kj/2 >= Kj for 1 <= j/2 <= j <= N.
 *
 * There are two cases.  If j == nmemb, select largest of Ki and Kj.  If
 * j < nmemb, select largest of Ki, Kj and Kj+1.
 */
#define CREATE(initval, nmemb, par_i, child_i, par, child, size, count, tmp) { \
	for (par_i = initval; (child_i = par_i * 2) <= nmemb; \
	    par_i = child_i) { \
		child = base + child_i * size; \
		if (child_i < nmemb && compar(child, child + size) < 0) { \
			child += size; \
			++child_i; \
		} \
		par = base + par_i * size; \
		if (compar(child, par) <= 0) \
			break; \
		SWAP(par, child, count, size, tmp); \
	} \
}

#define SELECT(par_i, child_i, nmemb, par, child, size, k, count, tmp1, tmp2) { \
	for (par_i = 1; (child_i = par_i * 2) <= nmemb; par_i = child_i) { \
		child = base + child_i * size; \
		if (child_i < nmemb && compar(child, child + size) < 0) { \
			child += size; \
			++child_i; \
		} \
		par = base + par_i * size; \
		COPY(par, child, count, size, tmp1, tmp2); \
	} \
	for (;;) { \
		child_i = par_i; \
		par_i = child_i / 2; \
		child = base + child_i * size; \
		par = base + par_i * size; \
		if (child_i == 1 || compar(k, par) < 0) { \
			COPY(child, k, count, size, tmp1, tmp2); \
			break; \
		} \
		COPY(child, par, count, size, tmp1, tmp2); \
	} \
}


int
heapsort(void *vbase, int nmemb, int size, int max, int (*compar)(const void *, const void *))	
{
	register int cnt, i, j, l, m;
	register char tmp, *tmp1, *tmp2;
	char *base, *k, *p, *t;

	if (nmemb <= 1)
		return (0);

	if (!size) {
		return (-1);
	}

	if ((k = malloc(size)) == NULL)
		return (-1);

	/*
	 * Items are numbered from 1 to nmemb, so offset from size bytes
	 * below the starting address.
	 */
	base = (char *)vbase - size;

	for (l = nmemb / 2 + 1; --l;)
		CREATE(l, nmemb, i, j, t, p, size, cnt, tmp);

	/*
	 * For each element of the heap, save the largest element into its
	 * final slot, save the displaced element (k), then recreate the
	 * heap.
	 */
	if (max == 0) m = 1;
	else {
		m = nmemb - max;
		if (m < 1) m = 1;
	}
	
	while (nmemb > m) {
		COPY(k, base + nmemb * size, cnt, size, tmp1, tmp2);
		COPY(base + nmemb * size, base + size, cnt, size, tmp1, tmp2);
		--nmemb;
		SELECT(i, j, nmemb, t, p, size, k, cnt, tmp1, tmp2);
	}
	free(k);
	return (0);
}

