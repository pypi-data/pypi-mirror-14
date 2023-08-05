#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "analyzer.h"

/*
Basic Rules
if lang == de, fr, it, pt, ar ...
	use each stemmer
elif lang == en or others
	if char range == Latin ( < Greek):
		make spaced Tri-gram
	elif enlish (char < 128):
		use stem_en
	else:
		make Bi-gram
*/
void
analyze (POSTOKENS tokens, char *document, char* lang, int stem_level, NGRAMOPTIONS *ngram, WORDLIST *stoplist, WORDLIST *endlist)
{
	unsigned char ch;
	int remove_stopword = stoplist->numword;
	int remove_endword = endlist->numword;
	char token [100];	
	char ngramtoken [100][7];	// unofficially utf8 extensible to 6 bytes
	char prev_lastchar [7];
	char prev_semilastchar [7];
	unsigned int pos = 0;
	size_t len = strlen (document);
	int tokenindex = 0;
	int manipulate;
	int i, j;	
	size_t sl;
	int sizeoftokens;
	int stopword;
	unsigned int tokenpos;
	int numchar; 	
	int multibyte_checksum;
	unsigned char cjk_checksum, cjk_checksum2;
	int has_multibyte = 0;
	int loopnum;
	int has_own_stemmer = 1;
	int (*stopwordfunc)(char *word, WORDLIST *stoplist);
	int (* stemfunc) (char *word, int stem_level);
	int is_trigram;
	int ngram_n = 3, ngram_ignore_space = 0;					
					
	if (stoplist->case_sensitive) {
		stopwordfunc = isstopword;		
	} else {
		stopwordfunc = isstopword_nocase;		
	}
	
	stemfunc = NULL;
	if (stem_level) {
		if (strcmp (lang, "en") == 0 && has_multibyte == 0) stemfunc = stem;
		else if (strcmp (lang, "de") == 0 && stem_level) stemfunc = stem_de;		
		else if (strcmp (lang, "fr") == 0 && stem_level) stemfunc = stem_fr;
		else if (strcmp (lang, "it") == 0 && stem_level) stemfunc = stem_it;
		else if (strcmp (lang, "fi") == 0 && stem_level) stemfunc = stem_fi;
		else if (strcmp (lang, "es") == 0 && stem_level) stemfunc = stem_es;
		else if (strcmp (lang, "hu") == 0 && stem_level) stemfunc = stem_hu;
		else if (strcmp (lang, "pt") == 0 && stem_level) stemfunc = stem_pt;
		else if (strcmp (lang, "sv") == 0 && stem_level) stemfunc = stem_sv;
		else if (strcmp (lang, "ar") == 0 && stem_level) stemfunc = stem_ar;
	}		
	if (stemfunc == NULL) has_own_stemmer = 0;
	if (ngram->n > 3) ngram->n = 3;
	prev_lastchar [0] = '\0'; // initailize
	prev_semilastchar [0] = '\0';
	
	tokens->tsnum = 0;
	tokens->tmpos = 0;
	sizeoftokens = tokens -> tsize;	
	while (pos < len) {
		manipulate = 0;
		ch = document [pos++];

		if (isspace (ch)) {
			manipulate = 1;			
		}
			
		else if (ch == '/' || ch == '-' || ch == '\'') {	
			if (!tokenindex) {
				manipulate = 1;					
			}			
			else if (pos < len && !isunialnum(document [pos])) {
				manipulate = 1;				
			}
				
			else if (\
				(pos < len && (isunialnum(document [pos]) || (document [pos] & 0xc0) == 0xc0)) && \
				(tokenindex < 3 || (pos == len - 1 || (pos < len - 1 && !isunialnum(document [pos + 1])) || (pos < len - 2 && !isunialnum (document [pos + 2]))))\
				) {
				token [tokenindex++] = ch;
			}
				
			else {
				/* this flag means this is a word, and have next term */
				manipulate = 1;
			}			
		} 

		else if (isalnum (ch) || ch=='+' || ch=='#' || ch=='.') {			
			if (ch == '+') { /* c++ */
				if (tokenindex == 1 && token [0] == 'c' && document [pos] == '+' && (pos == len - 2 || document [pos+1] != '+')) {
					token [tokenindex++] = ch;
					token [tokenindex++] = '+';
					pos ++;
				}				
				else {
					manipulate = 1;
				}
			}
			
			else if (ch == '#') { /* c# */
				if (tokenindex == 1 && token[0] == 'c' && (pos == len - 1 ||  document [pos] != '#')) {
					token [tokenindex++] = ch;
				}
				else {
					manipulate = 1;
				}
			}
			
			else if (ch == '.') { /* C.E.O */
				if (tokenindex >= 1 && isupper (document [pos-2]) && (isupper (document [pos]))) {
					token [tokenindex++] = ch;
				}
				else {
					manipulate = 1;
				}
			}
			
			else {
				//token [tokenindex++] = tolower (ch);				
				token [tokenindex++] = ch;
				if (tokenindex >= 100) {
					while (!isspace (ch) && pos < len) ch = document [pos++];
					tokenindex = 0; /* too long term, skip to next */
				}
			}					
		}
		
		else if (ch >= 128) { // multi bytes unicode
			has_multibyte = 1;
			token [tokenindex++] = ch;
			if (tokenindex >= 100) {
				while (!isspace (ch) && pos < len) ch = document [pos++];
				tokenindex = 0; /* too long term, skip to next */
			}
		}
				
		else {			
			manipulate = 1;			
		}
		
		if (ngram->ignore_space && !tokenindex && !isspace (ch)) { // maybe special char, do not join with space ngram
				prev_lastchar [0] = '\0';
				prev_semilastchar [0] = '\0';		
		}
		
		if (!(manipulate || pos == len) || !tokenindex) {			
			continue;
		}
			
		// oh, we've got a token!
		token [tokenindex] = '\0';	
		
		/* step 1. remove endwords ************************/
		if (remove_endword && has_multibyte && !len_remove_end (token, endlist)) {			
			has_multibyte = 0;
			tokenindex = 0;
			continue; // entire removed
		}
		
		/* step 2. remove stopwords ************************/
		if (remove_stopword) {
			stopword = stopwordfunc (token, stoplist);				
			if (stopword) {
				has_multibyte = 0;
				tokenindex = 0;
				continue;
			}
		}
		
		/* step 3. handle token ************************/
		sl = strlen (token);
		//has_own_stemmer = 0;
		if (has_own_stemmer) {
			if (stemfunc (token, stem_level)) {
				strncpy (tokens -> ts [tokens -> tsnum]->token, token, sl+1);
				tokens -> ts [tokens -> tsnum++]->position = tokens->tmpos++;		
			}
	  }
	  
		else {
			if (has_multibyte == 0) { // only < 0xcd00 All Latin
				if (ngram->ignore_space) {
					prev_lastchar [0] = '\0';
					prev_semilastchar [0] = '\0';
				}
				if (stem_level) {	// only english cahrs
					stem (token, stem_level);	// Assume ENGLISH
				}
					
				strncpy (tokens -> ts [tokens -> tsnum]->token, token, sl+1);
				tokens -> ts [tokens -> tsnum++]->position = tokens->tmpos++;
			}

			else if (ngram->n == 0) {
				strncpy (tokens -> ts [tokens -> tsnum]->token, token, sl+1);
				tokens -> ts [tokens -> tsnum++]->position = tokens->tmpos++;									
			}
			
			else { 
				/* n-gram	indexing */
				is_trigram = 1;
				tokenpos = 0;
				numchar = 0;
				i = 0;
				ngramtoken [numchar][0] = '_'; // ngram start mark
				ngramtoken [numchar++][1] = '\0';
				while (tokenpos < sl) {
					numchar++;
					multibyte_checksum = (unsigned int) token [tokenpos];
					if ((multibyte_checksum & 0x80) == 0) {
						ngramtoken [numchar-1][i++] = token [tokenpos++];
					}
					else {
						while ((multibyte_checksum & 0x80) != 0) {
							multibyte_checksum <<= 1;	
							ngramtoken [numchar-1][i++] = token [tokenpos++];						
						}
					}
					ngramtoken [numchar-1][i] = '\0';
					if (is_trigram && i >= 3) { // detectign bigram
						cjk_checksum = (unsigned char) ngramtoken [numchar-1][0];
						cjk_checksum2 = (unsigned char) ngramtoken [numchar-1][1];
						if (i == 3) {
							if (cjk_checksum == 0xeb || cjk_checksum == 0xec) is_trigram = 0; // KO
							else if (cjk_checksum == 0xea && cjk_checksum2 >= 0xb0) is_trigram = 0; // KO
							else if (cjk_checksum == 0xed && cjk_checksum2 <= 0x9f) is_trigram = 0; // KO							
							else if (cjk_checksum >= 0xe3 && cjk_checksum <= 0xe9) is_trigram = 0; //CN, JA
							else if (cjk_checksum == 0xe2 && cjk_checksum2 >= 0xba) is_trigram = 0; // CN
							
							else if (cjk_checksum == 0xe1 && (cjk_checksum2 >= 0x84 && cjk_checksum2 <= 0x87)) is_trigram = 0; // KO	
							else if (cjk_checksum == 0xea && (cjk_checksum2 >= 0xa5 && cjk_checksum2 <= 0xa9)) is_trigram = 0; // KO		
							else if (cjk_checksum == 0xef && (cjk_checksum2 >= 0xbc && cjk_checksum2 <= 0xbf)) is_trigram = 0; // KO			
									
						} else if (i == 4) {
							if ((cjk_checksum > 0xf0 && cjk_checksum2 < 0xf3)) is_trigram = 0;
							else if (cjk_checksum == 0xf0 && cjk_checksum2 >= 0xa0) is_trigram = 0;
							else if (cjk_checksum == 0xf3 && cjk_checksum2 <= 0x9f) is_trigram = 0;
						}	
					}	
					i = 0;
				}
				
				// reconfigure for Latin
				if (is_trigram) {
					ngram_n = 3;
					ngram_ignore_space = 0;
				}	
				else {
					ngram_n = 2;
					ngram_ignore_space = ngram->ignore_space;
				}
				
				if (ngram_n == 1) {
					// 엔그램 => _엔 그 램_
					tokens -> ts [tokens -> tsnum]->token [0] = '_';
					tokens -> ts [tokens -> tsnum]->token [1] = '\0';
					for (i=1; i<numchar; i++) {
						if (i == 1) {
							strncat (tokens -> ts [tokens -> tsnum]->token, ngramtoken [i], strlen (ngramtoken [i]));						
						} else {
							strncpy (tokens -> ts [tokens -> tsnum]->token, ngramtoken [i], strlen (ngramtoken [i]) + 1);
						}
						tokens -> ts [tokens -> tsnum++]->position = tokens->tmpos++;
						if (tokens -> tsnum == sizeoftokens) break;
					}
					if (tokens -> tsnum < sizeoftokens) {
						// last char with end marking
						strncpy (tokens -> ts [tokens -> tsnum]->token, ngramtoken[numchar-1], strlen (ngramtoken[numchar-1]) + 1);
						strncat (tokens -> ts [tokens -> tsnum]->token, "_", 1);
						tokens -> ts [tokens -> tsnum++]->position = tokens->tmpos-1; // 1-gram same position
					}					
				}
				
				else {				
					if (ngram_ignore_space) {
						// 한글	나라 => 한글나 글나라 (tri)
						// 한글	나라 => 글나 (bi)
						// space joint birgam
						if (prev_semilastchar[0]) { // TRI-GRAM							
							strncpy (tokens -> ts [tokens -> tsnum]->token, prev_semilastchar, strlen (prev_semilastchar) + 1);
							strncat (tokens -> ts [tokens -> tsnum]->token, prev_lastchar, strlen (prev_lastchar));
							strncat (tokens -> ts [tokens -> tsnum]->token, ngramtoken [1], strlen (ngramtoken [1]));	
							tokens -> ts [tokens -> tsnum++]->position = tokens->tmpos++;
							prev_semilastchar [0] = '\0';
							if (tokens -> tsnum == sizeoftokens) break;
						}
						if (prev_lastchar[0]) {
							strncpy (tokens -> ts [tokens -> tsnum]->token, prev_lastchar, strlen (prev_lastchar) + 1);
							for (i=1; i < ngram_n && numchar >= ngram_n; i++) {
								strncat (tokens -> ts [tokens -> tsnum]->token, ngramtoken [i], strlen (ngramtoken [i]));						
							}							
							tokens -> ts [tokens -> tsnum++]->position = tokens->tmpos++;
							if (tokens -> tsnum == sizeoftokens) break;
						}
						
						if (!isspace (ch))	{
							prev_lastchar [0] = '\0'; //clear lastchar
						}
						else {
							// reset and reput prev_semilastchar, prev_lastchar
							if (ngram_n == 3) {
								if (numchar == 2) {	
									strncpy (prev_semilastchar, prev_lastchar, strlen (prev_lastchar) + 1);						
								}	else { //numchar > 2
									strncpy (prev_semilastchar, ngramtoken [numchar - 2], strlen (ngramtoken [numchar - 2]) + 1);
								}
							}			
							strncpy (prev_lastchar, ngramtoken [numchar - 1], strlen (ngramtoken [numchar - 1]) + 1);	
						}	
					}
					
					//make ngram
					if (numchar <= ngram_n) { 
						// shorter than ngam NO start, end marking
						i = 1;						
						loopnum = numchar-(ngram_n-1)+1;					
						strncpy (tokens -> ts [tokens -> tsnum]->token, ngramtoken [i], strlen (ngramtoken [i]) + 1);
						for (j=1; j<ngram->n && i+j < numchar; j++) {
							strncat (tokens -> ts [tokens -> tsnum]->token, ngramtoken [i+j], strlen (ngramtoken [i+j]));
						}							
						tokens -> ts [tokens -> tsnum++]->position = tokens->tmpos++;					
						if (tokens -> tsnum == sizeoftokens) break;
					}
					
					else {					
						// add end mark
						ngramtoken [numchar][0] = '_';
						ngramtoken [numchar++][1] = '\0';
						loopnum = numchar-(ngram_n-1);					
						for (i=0; i<loopnum; i++) {						
							strncpy (tokens -> ts [tokens -> tsnum]->token, ngramtoken [i], strlen (ngramtoken [i]) + 1);
							for (j=1; j<ngram_n && i+j < numchar; j++) {
								strncat (tokens -> ts [tokens -> tsnum]->token, ngramtoken [i+j], strlen (ngramtoken [i+j]));
							}
							
							if (i == 0) {
								tokens -> ts [tokens -> tsnum++]->position = tokens->tmpos;
							}	
							else if (i == loopnum-1) {						
								tokens -> ts [tokens -> tsnum++]->position = tokens->tmpos-1;
							}
							else {
								tokens -> ts [tokens -> tsnum++]->position = tokens->tmpos++;
							}	
							if (tokens -> tsnum == sizeoftokens) break;
						}
					}
				}
			}
		}	
		has_multibyte = 0;
		tokenindex = 0;
		if (tokens -> tsnum == sizeoftokens) break;
	}	
}

