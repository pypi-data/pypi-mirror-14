/*  Spanish stemmer tring to remove inflectional suffixes */
#include <string.h>
#include "analyzer.h"

int stem_es (char *word, int stem_level)
{ 
int len = strlen (word)-1;

if (len > 3) {  
   //removeSpanishAccent(word);
   if (!removeLatinAccents (word)) return 0;
   if ((word[len]=='s') && (word[len-1]=='e') && (word[len-2]=='s') && (word[len-3]=='e')) {
         /*  corteses -> cortes  */
         word[len-1]='\0';
         return strlen (word);
      }
   if ((word[len]=='s') && (word[len-1]=='e') && (word[len-2]=='c')) {
         word[len-2]='z';        /*  dos veces -> una vez  */
         word[len-1]='\0';
         return strlen (word);
      }
   if (word[len]=='s') {  /*  ending with -os, -as  or -es */
      if (word[len-1]=='o' || word[len-1]=='a' || word[len-1]=='e' ) {
         word[len-1]='\0';  /*  remove -os, -as  or -es */
         return strlen (word);
         }
      }
   if (word[len]=='o') {   /*  ending with  -o  */
      word[len]='\0';  
      return strlen (word);
      }
   if (word[len]=='a') {   /*  ending with  -a  */
      word[len]='\0';  
      return strlen (word);
      }
   if (word[len]=='e') {   /*  ending with  -e  */
      word[len]='\0';  
     return strlen (word);
      }
   } /* end if (len > 3) */ 
return strlen (word);
}



