/* hash table */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "index.h"
#include "generichash.h"

static
int compare (const void *p1, const void *p2) {
	if ( (* (keyType * const *)p1)->fdno == (* (keyType * const *)p2)->fdno ) {
		return strcmp ( (char *) ((* (keyType * const *)p1)->term), (char *) ((* (keyType * const *)p2)->term) );
	}
	else {
		 if ( (* (keyType * const *)p1)->fdno > (* (keyType * const *)p2)->fdno ) return 1;
		 if ( (* (keyType * const *)p1)->fdno < (* (keyType * const *)p2)->fdno )  return -1;
		 return 0;
	}

}

static
unsigned int hash (keyType *key) {
	unsigned long long hs;
	//hs = ELFHash (key->term, strlen (key->term));
	hs = DEKHash (key->term, (unsigned int) strlen (key->term));
	hs += key->fdno << 17;
	return (unsigned int) (hs % TERMHASHTABLE_SIZE);
}

nodeType* ht_find(nodeType *hashTable [], keyType *key) {
    nodeType *p;

    p = hashTable[hash(key)];
    while (p && !compEQ(p->key, key)) {
    	p = p->next;
    }
    if (!p) return NULL;
    return p;
}

recType* ht_fetchfirst (nodeType *hashTable [], keyType *key) {
    nodeType *p;

    p = hashTable[hash(key)];
    while (p && !compEQ(p->key, key)) {
    	p = p->next;
    }
    if (!p) return NULL;
    return p->firstRec;
}


int ht_occupied (nodeType *hashTable []) {
    int count = 0;
    int i;

    for (i=0; i<TERMHASHTABLE_SIZE; i++)
		if (hashTable [i]) count++;
    return count;
}

int ht_insert(nodeType *hashTable [], keyType *key, recType *rec) {
    nodeType *p, *p0;
    int bucket;

    rec->next = NULL;
    p = ht_find (hashTable, key);

    if (p) {
    	p->lastRec->next = rec;
    	p->lastRec = rec;
    	/* no use free */
    	free (key->term);
    	free (key);
    	return 0;
    }

    /* insert node at beginning of list */
    else {
    	bucket = hash(key);
    	if (!(p = malloc(sizeof(nodeType)))) return -1;
	p0 = hashTable[bucket];
	hashTable[bucket] = p;
	p->next = p0;
	p->key = key;
	p->firstRec = rec;
	p->lastRec = rec;
	return 1;
    }

}

int ht_delete (nodeType *hashTable [], keyType *key) {
    nodeType *p0, *p;
    recType *r, *r0;
    int bucket;

    p0 = 0;
    bucket = hash(key);
    p = hashTable[bucket];
    while (p && !compEQ(p->key, key)) {
        p0 = p;
        p = p->next;
    }
    if (!p) return 2;

    if (p0)
        /* not first node, p0 points to previous node */
        p0->next = p->next;
    else
        /* first node on chain */
        hashTable[bucket] = p->next;

    r = p->firstRec;
    while (r) {
    	r0 = r->next;
    	free (r->prox);
    	free (r);
    	r = r0;
    }

    free (p->key->term);
    free (p->key);
    free (p);
    return 0;
}

keyType** ht_keys (keyType *karr [], int count, nodeType *hashTable []) {
	int i, c;
	nodeType *p;

	if (!(karr = (keyType**) malloc (count * sizeof (keyType**)))) return NULL;
	c = 0;
	for (i = 0; i < TERMHASHTABLE_SIZE; i++) {
		p = hashTable [i];
		if (!p) continue;
		while (p) {
			karr [c++] = p->key;
			//printf ("karr [c]->term:%s\n", karr [c]->term);
			p = p->next;
		}
	}
	return karr;
}

int ht_destroy (nodeType *hashTable []) {
	int i;
	nodeType *p, *p0;
	recType *r, *r0;

	for (i = 0; i < TERMHASHTABLE_SIZE; i++) {
		p = hashTable [i];
		if (!p) continue;
		while (p) {
			p0 = p->next;
			r = p->firstRec;
		    while (r) {
		    	r0 = r->next;
		    	if (r->prox) free (r->prox);
		    	free (r); /* free rec */
		    	r = r0;
		    }
		    free (p->key->term); /* free term */
		    free (p->key); /* free key */
		    free (p); /* free node */
		    p = p0;
		}
	}
	free (hashTable); /* free hashTable */
	return 0;
}

nodeType ** ht_init (nodeType *hashTable []) {
	int i;
	if (!(hashTable = (nodeType **) malloc (sizeof (nodeType*) * TERMHASHTABLE_SIZE))) return NULL;
	for (i=0; i<TERMHASHTABLE_SIZE; i++)
		hashTable [i] = NULL;
	return hashTable;
}


void ht_sort (keyType *karr [], int numterm){
	qsort (karr, numterm, sizeof (keyType *), compare);
}


int _main (int argc, char **argv) {
    int i, j;
    recType *rec;
    keyType *key;
    keyType _key;
    int err;
    nodeType **hashTable = NULL;
    nodeType *found;
    recType *p;
    char *term = "tsetingmode";
    keyType **karr = NULL;
    size_t sizeterm;

    /* command-line:
     *
     *   has maxnum hashTableSize [random]
     *
     *   has 2000 100
     *       processes 2000 records, tablesize=100, sequential numbers
     *   has 4000 200 r
     *       processes 4000 records, tablesize=200, random numbers
     *
     */

    hashTable = ht_init (hashTable);
    for (i=0; i<TERMHASHTABLE_SIZE; i++)
		hashTable [i] = NULL;

	for (i=0; i<3; i++) {
		for (j=0; j<50; j++) {
	    	key = (keyType*) malloc (sizeof (keyType));
	    	rec = (recType*) malloc (sizeof (recType));
	    	sizeterm = strlen (term) + 1;
	    	key->term = (char *) malloc (sizeterm);
				strncpy (key->term, term, sizeterm);
	    	key->fdno = j;
	    	rec->docid = j;
	    	rec->tf = j*2;
	    	err = ht_insert(hashTable, key, rec);
	        if (err) printf("pt1, i=%d\n", j);
	    }
	}

  printf ("seq ht, 150 items, %d hashTable\n", 10);

	_key.fdno = 1;
	_key.term = term;
    found = ht_find (hashTable, &_key);
    if (found) {
    	//printf ("found %d/%d/%d\n", found->firstRec->docid, found->firstRec->tf, found->firstRec->next);
    	p = found->firstRec->next;
    	while (p) {
    		//printf ("found %d/%d/%d\n", p->docid, p->tf, p->next);
    		p = p->next;
    	}
    }

    karr = ht_keys (karr, i, hashTable);
    for (j=0; j<i; j++) {
    	printf ("%s/%d\n", karr [j]->term, karr [j]->fdno);
    }

    /*
    for (i = maxnum-1; i >= 0; i--) {
        err = delete(hashTable, key);
        if (err) printf("pt3, i=%d\n", i);
    }
    */
    ht_sort (karr, i);

    ht_destroy (hashTable);
    free (karr);

    return 0;
}
