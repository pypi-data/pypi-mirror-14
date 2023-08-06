/*  German stemmer tring to remove inflectional suffixes */
#include <string.h>
#include "analyzer.h"

static char *remove_Step1(char *word);
static char *remove_Step2(char *word);
static int STEnding(char aLetter);

int stem_de (char *word, int stem_level)
{ 
   //removeGermanAccent(word);
   if (!removeLatinAccents (word)) return 0;
   remove_Step1(word);
   remove_Step2(word);
return strlen (word);
}


static int STEnding (aLetter)
char aLetter;
{ 
   if (aLetter=='b' || aLetter=='d' || aLetter=='f' ||
       aLetter=='g' || aLetter=='h' || aLetter=='k' ||
       aLetter=='l' || aLetter=='m' || aLetter=='n' ||
       aLetter=='t')
      return(1);
return(0);         
}


static char *remove_Step1 (char *word)
{ 
int len = strlen (word)-1;

if (len > 4) {
   if (word[len]=='n' && word[len-1]=='r' && word[len-2]=='e') {  
      word[len-2]='\0';  /*  ending with -ern ->   */
      return(word);
      }
   }
if (len > 3) {
   if (word[len]=='m' && word[len-1]=='e') {  
      word[len-1]='\0';  /*  ending with -em ->  */
      return(word);
      }
   if (word[len]=='n' && word[len-1]=='e') {  
      word[len-1]='\0';  /*  ending with -en ->  */
      return(word);
      }
   if (word[len]=='r' && word[len-1]=='e') {  
      word[len-1]='\0';  /*  ending with -er ->  */
      return(word);
      }
   if (word[len]=='s' && word[len-1]=='e') {  
      word[len-1]='\0';  /*  ending with -es ->  */
      return(word);
      }
   }
if (len > 2) {
   if (word[len]=='e') {  
      word[len]='\0';  /*  ending with -e ->  */
      return(word);
      }
   if (word[len]=='s' && STEnding(word[len-1])) {  
      word[len]='\0';  /*  ending with -s ->  */
      return(word);
      }
   } 
return(word);         
}

static char *remove_Step2 (word)
char *word;
{ 
int len = strlen (word)-1;

if (len > 4) {
   if (word[len]=='t' && word[len-1]=='s' && word[len-2]=='e') {  
      word[len-2]='\0';  /*  ending with -est ->   */
      return(word);
      }
   }
if (len > 3) {
   if (word[len]=='r' && word[len-1]=='e') {  
      word[len-1]='\0';  /*  ending with -er ->  */
      return(word);
      }
   if (word[len]=='n' && word[len-1]=='e') {  
      word[len-1]='\0';  /*  ending with -en ->  */
      return(word);
      }
   if (word[len]=='t' && word[len-1]=='s' && STEnding(word[len-2])) {  
      word[len-1]='\0';  /*  ending with -st ->  */
      return(word);
      }
   }
return(word);         
}



