#include "analyzer.h"
#include <string.h>

/*  Arabic stemmer (stem2) tring to remove common prefixes and suffixes */
/*  more conservative than stem3 (see J. Savoy, Y. Rasolofo, TREC 2002) */

static char *removeArabicSuffix2(char *word);
static char *removeArabicPrefix2(char *word);
static char *removeArabicSuffix3(char *word);
static char *removeArabicPrefix3(char *word);
/* For the Arabic language */

int stem_ar (char *word, int stem_level)
{ 
   if (!convertArabicToAlpha (word))
   	return 0;
   	
   if (stem_level == 1 ) {
	   removeArabicSuffix2(word);
	   removeArabicPrefix2(word);
	 }
	 else {
	 	 removeArabicSuffix3(word);
	   removeArabicPrefix3(word);
	 }	 
   return strlen (word);
}

static char D8 [] = "AAwAyAbptvjHxdOrzsPSDTZEg"; //162
static char D9 [] = "fqklmnhwYX"; //129
static char D9D [] = "0123456789"; //160
static char D9A [] = "bqAAA"; //160

int convertArabicToAlpha (char* word) {
	unsigned char buf [100];
	unsigned char* ar;
	int pos = 0, len;
	int bpos = 0;
	ar = (unsigned char*) word;
	
	len = strlen (word);
	if (len > 99) return 1;
		
	while (pos < len) {
		if (ar [pos] == 0xe2) {
			pos += 2;
			continue;
		}	
		else if (ar [pos] == 0xd8) {
			pos ++;
			if (pos == len) break;
			if (ar [pos] == 0x8c || ar [pos] == 0x9b || ar [pos] == 0x9f) buf [bpos++] = ' ';
			else if (ar [pos] >= 0xa2 && ar [pos] <= 0xba) buf [bpos++] = D8 [ar [pos] - 0xa2];
		}
		else if (ar [pos] == 0xd9) {
			pos ++;
			if (pos == len) break;
			if (ar [pos] == 0x8a && ar [pos+1] == 0xd8 && ar [pos+2] == 0xa1) {
				buf [bpos++] = 'Y';
				pos += 2;
				continue;
			}	
			else if (ar [pos] >= 0x81 && ar [pos] <= 0x8a) buf [bpos++] = D9 [ar [pos] - 0x81];
			else if (ar [pos] >= 0xa0 && ar [pos] <= 0xa9) buf [bpos++] = D9D [ar [pos] - 0xa0];	
			else if (ar [pos] >= 0xae && ar [pos] <= 0xb3) buf [bpos++] = D9A [ar [pos] - 0xae];		
			else if (ar [pos] == 0xb5) buf [bpos++] = 'A';		
			else if (ar [pos] == 0xb6) buf [bpos++] = 'w';		
			else if (ar [pos] == 0xb8) buf [bpos++] = 'y';
			else if (ar [pos] == 0xaa || ar [pos] == 0xad) buf [bpos++] = ' ';	
		}
		pos ++;
	}
	buf [bpos] = '\0';
	strcpy (word, (char*) buf);	
	return bpos;
}


static char *removeArabicSuffix2(char *word)
{ 
int len = strlen (word)-1;

if (len > 4) {   
              /* -A{nt}    */
   if ((word[len-1]=='A') && ((word[len]=='t') || (word[len]=='n'))) {  
      word[len-1]='\0'; 
      return(word); 
      }
              /* -hA    */
   if ((word[len]=='A') && (word[len-1]=='h')) {  
      word[len-1]='\0'; 
      return(word); 
      }
              /* -Y{phn}    */
   if ((word[len-1]=='Y') && ((word[len]=='p') || (word[len]=='h') ||
                             (word[len]=='n'))) {  
      word[len-1]='\0'; 
      return(word); 
      }
              /* -wn    */
   if ((word[len-1]=='w') && (word[len]=='n')) {  
      word[len-1]='\0'; 
      return(word); 
      }
   }  /* end if len > 4 */

if (len > 3) {   
             /* -{Yph}  -> -  */
   if ((word[len]=='Y') || (word[len]=='p') || (word[len]=='h')) {
      word[len]='\0';
      return(word);  
      }
   }  /* end if len > 3 */

return(word);
}


static char *removeArabicPrefix2(char *word)
{ 
int pos;
int len = strlen (word)-1;

if (len > 5) {   
              /* {fXbw}Al-- -> --    */
   if ((word[2]=='l') && (word[1]=='A') && ((word[0]=='f') || 
        (word[0]=='X') || (word[0]=='b') || (word[0]=='w'))) {  
      pos = 0;
      while (word[pos+3] != '\0') {
         word[pos] = word[pos+3];
         pos++;
         }
      word[pos]= '\0';
      return(word);
      }  
   }  /* end if len > 5 */

if (len > 4) {   
              /* Al-- -> --    */
   if ((word[0]=='A') && (word[1]=='l')) {  
      pos = 0;
      while (word[pos+2] != '\0') {
         word[pos] = word[pos+2];
         pos++;
         }
      word[pos]= '\0';
      return(word);
      }  
   }  /* end if len > 4 */

if (len > 3) {   
             /* {wY}--  -> --  */
   if ((word[0]=='w') || (word[0]=='Y')) {  
      pos = 0;
      while (word[pos] != '\0') {
         word[pos] = word[pos+1];
         pos++;
         }
      return(word);  
      }
   }  /* end if len > 3 */

return(word);
}


//==============================================================

static char *removeArabicSuffix3(char *word)
{ 
int len = strlen (word)-1;

if (len > 4) {   
              /* -A{nt}    */
   if ((word[len-1]=='A') && ((word[len]=='t') || (word[len]=='n'))) {  
      word[len-1]='\0'; 
      return(word); 
      }
              /* -hA    */
   if ((word[len]=='A') && (word[len-1]=='h')) {  
      word[len-1]='\0'; 
      return(word); 
      }
              /* -Y{phn}    */
   if ((word[len-1]=='Y') && ((word[len]=='p') || (word[len]=='h') ||
                             (word[len]=='n'))) {  
      word[len-1]='\0'; 
      return(word); 
      }
              /* -wn    */
   if ((word[len-1]=='w') && (word[len]=='n')) {  
      word[len-1]='\0'; 
      return(word); 
      }
   }  /* end if len > 4 */

if (len > 3) {   
             /* -{Yph}  -> -  */
   if ((word[len]=='Y') || (word[len]=='p') || (word[len]=='h')) {
      word[len]='\0';
      return(word);  
      }
   }  /* end if len > 3 */

return(word);
}


static char *removeArabicPrefix3(char *word)

{ 
int pos;
int len = strlen (word)-1;

if (len > 5) {   
              /* {fXbw}Al-- -> --    */
   if ((word[2]=='l') && (word[1]=='A') && ((word[0]=='f') || 
        (word[0]=='X') || (word[0]=='b') || (word[0]=='w'))) {  
      pos = 0;
      while (word[pos+3] != '\0') {
         word[pos] = word[pos+3];
         pos++;
         }
      word[pos]= '\0';
      return(word);
      }  
   }  /* end if len > 5 */

if (len > 4) {   
              /* Al-- -> --    */
   if ((word[0]=='A') && (word[1]=='l')) {  
      pos = 0;
      while (word[pos+2] != '\0') {
         word[pos] = word[pos+2];
         pos++;
         }
      word[pos]= '\0';
      return(word);
      }  
   }  /* end if len > 4 */

if (len > 3) {   
             /* {wY}--  -> --  */
   if ((word[0]=='w') || (word[0]=='Y')) {  
      pos = 0;
      while (word[pos] != '\0') {
         word[pos] = word[pos+1];
         pos++;
         }
      return(word);  
      }
   }  /* end if len > 3 */

return(word);
}
