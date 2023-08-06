/*  Portuguese stemmer tring to remove inflectional suffixes for nouns and adjectives */
#include <string.h>
#include "analyzer.h"

static char *remove_PTsuffix(char *word);
static char *normFemininPortuguese(char *word);
static char *finalVowelPortuguese(char *word);

int stem_pt (char *word, int stem_level)
{ 
int len = strlen (word)-1;

   if (len > 2) {
      remove_PTsuffix(word);
      normFemininPortuguese(word);
      finalVowelPortuguese(word);
      //removeAllPTAccent(word); 
      if (!removeLatinAccents (word)) return 0;
   }
return strlen (word);       
}

static char * finalVowelPortuguese(char *word)
{ 
int len = strlen (word)-1;

   if (len > 3) {
      if ((word[len]=='e') || (word[len]=='a') || (word[len]=='o')) {
         word[len]='\0';  /* remove final -e or -a or -o */
         return(word);
         }
   }
return(word);         
}

 
/* Remove plural and feminine form of Portuguese words */

static char * remove_PTsuffix (char *word)
{ 
int len = strlen (word)-1;

if (len > 3) {   /* plural in -es when sing form ends with -r, -s, -l or -z*/
   if ((word[len]=='s') && (word[len-1]=='e') && 
       ((word[len-2]=='r') || (word[len-2]=='s') || 
        (word[len-2]=='z') || (word[len-2]=='l'))) {
      word[len-1]='\0';  /* doutores (plur) --> doutor (sing) */
      return(word);
      }
   }  /* len > 3 */

if (len > 2) {   /* when sing form ends with -em, change -m in -n in plur */
   if ((word[len]=='s') && (word[len-1]=='n')) {
      word[len-1]='m';     /* homens (plur) --> homem (sing) */
      word[len]='\0'; 
      return(word);
      }
   } /* len > 2 */

if (len > 3) {   /* when sing form ends with -el, change -el in -eis  */
   if (((word[len]=='s') && (word[len-1]=='i')) && 
       ((word[len-2]=='e') || (word[len-2]=='e'))) {
      word[len-2]='e';     /* papeis (plur) --> papel (sing) */
      word[len-1]='l';     /* error:  faceis (plur) --> facil (sing) */
      word[len]='\0'; 
      return(word);
      }
   } /* len > 3 */

if (len > 3) {   /* when sing form ends with -ais, change -ais in -al in plur */
   if ((word[len]=='s') && (word[len-1]=='i') && (word[len-2]=='a')) {
      word[len-1]='l';     /* normais (plur) --> normal (sing) */
      word[len]='\0'; 
      return(word);
      }
   } /* len > 3 */

if (len > 3) {   /* when sing form ends with -'ois, change -ais in -al in plur */
   if ((word[len]=='s') && (word[len-1]=='i') && (word[len-2]=='o')) {
      word[len-2]='o';     /* lencois (plur) --> lencol (sing) */
      word[len-1]='l';     
      word[len]='\0'; 
      return(word);
      }
   } /* len > 3 */

if (len > 3) {   /* when sing form ends with -is, change -is in -il in plur */
   if ((word[len]=='s') && (word[len-1]=='i')) {
      word[len]='l';     /* barris (plur) --> barril (sing) */
      return(word);
      }
   } /* len > 3 */

if (len > 2) {   /* when plur form ends with -oes, change -oes in -ao  */
   if ((word[len]=='s') && (word[len-1]=='e') && (word[len-2]=='o')) {
      word[len-2]='a';     /* botoes (plur) --> botao (sing) */    
      word[len-1]='o';        
      word[len]='\0'; 
      return(word);
      }         /* when plur form ends with -aes, change -aes in -ao  */   
   if ((word[len]=='s') && (word[len-1]=='e') && (word[len-2]=='a')) {
      word[len-1]='o';     /* caes (plur) --> cao (sing) */    
      word[len]='\0'; 
      return(word);
      }         
   } /* len > 2 */

if (len > 5) {   /* for adverb -mente */
   if ((word[len]=='e') && (word[len-1]=='t') && (word[len-2]=='n') &&
       (word[len-3]=='e') && (word[len-4]=='m')) {
      word[len-4]='\0'; 
      return(word);
      }
   } /* len > 5 */

if (len > 2) {   /* usually plural in -s */
   if (word[len]=='s') {
      word[len]='\0';   /* of course, invariable word, pires->pires */
      len--;
      }
   } /* len > 2 */

return(word);         
}


static char * normFemininPortuguese(char *word)
{ 
int len = strlen (word)-1;

   if ((len < 3) || (word[len]!='a')) { 
      return(word);
      }
   if (len > 6) {  
      /*  -inha  -> inho */
      if ((word[len-1]=='h') && (word[len-2]=='n') && (word[len-3]=='i')) {
         word[len]='o'; 
         return(word);
         }
      /*  -iaca  -> iaco */
      if ((word[len-1]=='c') && (word[len-2]=='a') && (word[len-3]=='i')) {
         word[len]='o'; 
         return(word);
         }
      /*  -eira  -> eiro */
      if ((word[len-1]=='r') && (word[len-2]=='i') && (word[len-3]=='e')) {
         word[len]='o'; 
         return(word);
         }
   } /* len > 6 */

   if (len > 5) {  
       /*  -ona  -> ao */
      if ((word[len-1]=='n') && (word[len-2]=='o')) {
         word[len-2]='a'; 
         word[len-1]='o'; 
         word[len]='\0'; 
         return(word);
         }
      /*  -ora  -> or */
      if ((word[len-1]=='r') && (word[len-2]=='o')) {
         word[len]='\0'; 
         return(word);
         }
      /*  -osa  -> oso */
      if ((word[len-1]=='s') && (word[len-2]=='o')) {
         word[len]='o'; 
         return(word);
         }
      /*  -esa  -> es */
      if ((word[len-1]=='s') && (word[len-2]=='e')) {
         word[len-2]='e'; 
         word[len]='\0'; 
         return(word);
         }
      /*  -ica  -> ico */
      if ((word[len-1]=='c') && (word[len-2]=='i')) {
         word[len]='o'; 
         return(word);
         }
      /*  -ida  -> ido */
      if ((word[len-1]=='d') && (word[len-2]=='i')) {
         word[len]='o'; 
         return(word);
         }
      /*  -ada  -> ido */
      if ((word[len-1]=='d') && (word[len-2]=='a')) {
         word[len]='o'; 
         return(word);
         }
      /*  -iva  -> ivo */
      if ((word[len-1]=='v') && (word[len-2]=='i')) {
         word[len]='o'; 
         return(word);
         }
      /*  -ama  -> imo */
      if ((word[len-1]=='m') && (word[len-2]=='a')) {
         word[len]='o'; 
         return(word);
         }
      /*  -na  -> no */
      if (word[len-1]=='n') {
         word[len]='o'; 
         return(word);
         }
   } /* len > 5 */

return(word);         
}

 /* EOF */
