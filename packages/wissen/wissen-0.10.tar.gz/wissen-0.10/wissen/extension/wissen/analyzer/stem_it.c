/*  Italian stemmer tring to remove inflectional suffixes */
#include <string.h>
#include "analyzer.h"

int stem_it (char *word, int stem_level)

{ 
int len = strlen (word)-1;

if (len > 4) {
   //removeItalianAccent(word);
   if (!removeLatinAccents (word)) return 0;
   if (word[len]=='e') {  /*  ending with -ie or -he  */
      if (word[len-1]=='i' || word[len-1]=='h') {
         word[len-1]='\0';
         return 1;
         }
      word[len]='\0';  /*  ending with -e  */
      return strlen (word);
      }
   if (word[len]=='i') {  /*  ending with -hi or -ii */
      if ((word[len-1]=='h') || (word[len-1]=='i')) {
         word[len-1]='\0';
         return strlen (word);
         }
      word[len]='\0';  /*  ending with -i  */
      return strlen (word);
      }
   if (word[len]=='a') {  /*  ending with -ia  */
      if (word[len-1]=='i') {
         word[len-1]='\0';
         return strlen (word);
         }
      word[len]='\0';  /*  ending with -a  */
      return 1;
      }
   if (word[len]=='o') {  /*  ending with -io  */
      if (word[len-1]=='i') {
         word[len-1]='\0';
         return strlen (word);
         }
      word[len]='\0';  /*  ending with -o  */
      return strlen (word);
      }

   } /* end if (len > 4) */ 
return strlen (word);        
}




