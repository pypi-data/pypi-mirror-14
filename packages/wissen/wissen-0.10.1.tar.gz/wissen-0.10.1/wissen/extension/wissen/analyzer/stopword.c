#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include "analyzer.h"

int cmp_str (const void *s1, const void *s2)
{
     //printf ("%s | %s\n", *(char **)s1, *(char **)s2);
     // s1 is search string, s2 is array
     return (strcmp(*(char **)s1, *(char **)s2));
}

int isstopword (char *word, WORDLIST *stoplist) {
	char* ptr;	
	if (strlen (word) < 2 && strcmp (word, "c") != 0) return TRUE;
	// make sure case insensitive
	ptr = bsearch (&word, stoplist->wordlist, stoplist->numword, sizeof(stoplist->wordlist[0]), cmp_str);
	if (ptr) return TRUE;
	else return FALSE;
}

int isstopword_nocase (char *word, WORDLIST *stoplist) {
	char* ptr;
	char* temp;
	char lword [100];
	unsigned int ndx;	
	
	if (strlen (word) < 2 && strcmp (word, "c") != 0) return TRUE;
	// make sure case insensitive
	for ( ndx= 0, temp = word; *temp != '\0'; ndx++, temp++) {
	  lword [ndx] = (char) tolower(*temp);
	}
	lword [ndx] = '\0';	
	temp = (char*)lword;
	ptr = bsearch (&temp, stoplist->wordlist, stoplist->numword, sizeof(stoplist->wordlist[0]), cmp_str);
	if (ptr) return TRUE;
	else return FALSE;	
}
