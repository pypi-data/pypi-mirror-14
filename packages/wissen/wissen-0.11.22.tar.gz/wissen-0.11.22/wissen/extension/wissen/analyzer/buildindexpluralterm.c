#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include "analyzer.h"

extern char **stoplist;

#define IsVowel(c)        ('a'==(c)||'e'==(c)||'i'==(c)||'o'==(c)||'u'==(c))
#define IsSpecial(c)        ('x'==(c)||'o'==(c)||'s'==(c))

#define ADDPLURAL {\
if (addplural && tokens->tsnum < tokens->tsize) {\
		strcpy (tokens->ts [tokens->tsnum]->token, word);\
		tokens->ts [tokens->tsnum++]->position = tokens->tmpos;\
	}\
}	
#define ADDWORD {\
	if (tokens->tsnum < tokens->tsize) {\
		strcpy (tokens->ts [tokens->tsnum]->token, word);\
		tokens->ts [tokens -> tsnum++]->position = tokens->tmpos++;\
	}\
}
	
static int 
custom_modify (char* word) {
	int modified = 0;
	
	if (strcmp (word, "IT") == 0) { modified = 1; word = "it"; }
	return modified;		
}


int 
buildindexpluralterm (POSTOKENS tokens, char *word, int addplural, int ignoresw) {	
	char *ptr;
	char *index;
	unsigned int ndx;
	size_t wlen;
	unsigned char w,x,y,z;
	
	wlen = strlen (word);	
	if (wlen == 1) {
		if (tolower (word [0]) == 'c') {
			ADDWORD;
			return TRUE;
		}
		return FALSE;
	}	
	
	if (wlen == 2) {
		if (isupper (word [0]) && isupper (word [1])) {
			ignoresw = 1; // forcely insert
		}
	}
		
	if (custom_modify (word)) {
		ADDWORD;
		return TRUE;
	}
	
	for ( ndx= 0, index = word; *index != '\0'; ndx++, index++) {
	      word [ndx] = (char) tolower(*index);
	}
	
	if (!ignoresw) {
		ptr = bsearch (&word, stoplist, sizeof (stoplist) / sizeof (stoplist [0]), sizeof(stoplist[0]), cmp_str);
		if (ptr) return FALSE;
	}
	
	if (wlen <= 3) {
		ADDWORD;
		return TRUE;	
	}
	
	z = (unsigned char) wlen - 1;	
	y = (unsigned char) wlen - 2;
	if (word [z] == 'y' && !IsVowel (word [y])) {
		word [z] = 'i';
		ADDWORD;
		return TRUE;
	}
	
	x = (unsigned char) wlen - 3;
	if (word [z] == 'e' && (word [y] == 'f' || IsSpecial (word [y]) || (word [y] == 'h' && (word [x] == 'c' || word [x] == 's')))) {
		word [z] = EOS;
		ADDWORD;
		return TRUE;
	}
	
	if (word [z] != 's') {
		ADDWORD;
		return TRUE;
	}
	
	if (word [y] == 's') {
		ADDWORD;
		return TRUE;
	}
	
	if (word [y] != 'e' || wlen <= 4) {
		ADDPLURAL;
		word [z] = EOS;
		ADDWORD;
		return TRUE;	
	}
	
	w = (unsigned char) wlen - 4;	
	ADDPLURAL;
	if (IsSpecial (word [x]) || (word [x] == 'h' && (word [w] == 'c' || word [w] == 's')))
		word [y] = EOS;	
	else if (word [x] == 'i')
		word [y] = EOS;
	else if (word [x] == 'v') {
		word [x] = 'f';
		word [y] = EOS;
	}
	else 
		word [z] = EOS;
	ADDWORD;
	return TRUE;
}
