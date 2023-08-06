#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include "analyzer.h"

int
len_remove_end (char *word, WORDLIST *endlist) {
	char *ptr;
	char *index;
	size_t wlen; 
	unsigned i;
	unsigned int initpos = 0;
	
	wlen = strlen (word);
	if (word[0] == '_') initpos = 1;
	for (i = initpos; i < wlen; i++) {
		if ((word[i] & 0xc0) != 0xc0) continue; // is ascii or not unicode first char
		index = (char*)&word[i];
		ptr = (char*) bsearch (&index, endlist->wordlist, endlist->numword, sizeof(endlist->wordlist[0]), cmp_str);
		if (ptr) {
			word [i] = '\0';
			if (i == initpos) return 0; // remove whole word			
			return i;
		}
	}
	return i;
}
