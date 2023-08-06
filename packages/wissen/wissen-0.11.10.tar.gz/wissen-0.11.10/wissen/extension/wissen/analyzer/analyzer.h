#ifndef Core_ANALYZER_H
#define Core_ANALYZER_H

#define MAXPROX 1000
#define FALSE                         0
#define TRUE                          1
#define EOS '\0'

#define isunialnum(ch) (isalnum (ch) || (ch & 0xc0) == 0xc0)
// same as #define isunialnum(ch) (isalnum (ch) || (unsigned int)ch >= 128)

typedef struct {
	int tokencount;
	char tokenlist [1][100];
} *TOKENS;

typedef struct {
	int position;
	char token [100];
} WORD;

typedef struct {
	int tsnum;
	int tsize;
	int tmpos;
	int stopwords;	
	WORD* ts [];
} *POSTOKENS;

typedef struct {
	int numword;
	int iscreated;
	int case_sensitive;
	char **wordlist;	
} WORDLIST;

typedef struct {
	int n;
	int ignore_space;	
} NGRAMOPTIONS;

int cmp_str (const void *s1, const void *s2);
int removeLatinAccents (char* word);
int convertArabicToAlpha (char* word);
int stem (char *word, int stem_level);
int stem_de (char* word, int stem_level);
int stem_es (char* word, int stem_level);
int stem_fi (char* word, int stem_level);
int stem_fr (char* word, int stem_level);
int stem_hu (char* word, int stem_level);
int stem_it (char* word, int stem_level);
int stem_pt (char* word, int stem_level);
int stem_sv (char* word, int stem_level);
int stem_ar (char* word, int stem_level);

//int weakstem (char *word);
int isstopword (char *word, WORDLIST *stoplist);
int isstopword_nocase (char *word, WORDLIST *stoplist);
int len_remove_end (char *word, WORDLIST *endlist);
char* formalize (char* buffer, char *document, int len);

void analyze (POSTOKENS tokens, char *document, char* lang, int stem_level, NGRAMOPTIONS *ngram, WORDLIST *stoplist, WORDLIST *endlist);
//int buildindexpluralterm (POSTOKENS tokens, char *word, int addplural, int ignoresw);
int ischar (char ch);
int isunicode (char a, char b);
int iseuckr (char a, char b);
int isksc5601 (char a, char b);

#endif
