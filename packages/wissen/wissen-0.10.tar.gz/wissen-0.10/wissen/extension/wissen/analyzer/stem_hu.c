#include <string.h>
#include "analyzer.h"

/* 
   Hungarian stemmer trying to remove the suffixes corresponding to
   the different cases, the possessive and the number (plural) for Hungarian nouns.
   We assume that the accents are removed.  The procedure expects only characters coded using 7 bits (ASCII).

   Done by J. Savoy (University of Neuchatel, www.unine.ch/info/clef/)
*/

static char *remove_case(char *word);
static char *remove_possessive(char *word);
static char *remove_plural(char *word);
static char *normalize(char *word);

/* usage   IsVowel(*word)   */
#define IsVowel(c) ('a'==(c)||'e'==(c)||'i'==(c)||'o'==(c)||'u'==(c)||'y'==(c))


/* A light stemmer for the Hungarian language  */
int stem_hu (char *word, int stem_level)
{ 
   remove_case(word);
   remove_possessive(word);
   remove_plural(word);
   normalize(word);
   return strlen (word);
}


static char *normalize(char *word)
{ 
int len = strlen (word)-1;
/* For some words, the suggested stemming rules may produce an incorrect stem
   e.g. salata  --> salata
        salatat --> salat
   We try to reduce this kind of errors
*/

if (len > 2) {  
     /* -{aoe} */
   if ((word[len]=='o') || (word[len]=='e') || (word[len]=='a') ||
        (word[len]=='i')) {  
      word[len]='\0';
      return(word);
      }
   }  /* end if len > 2 */
return(word); 
}


/* Remove one of the various suffixes corresponding to a given case */
static char *remove_case(char *word)
{ 
int len = strlen (word)-1;

if (len > 5) {  
     /* -kent  modal */
   if ((word[len]=='t') && (word[len-1]=='n') && 
       (word[len-2]=='e') && (word[len-3]=='k')) {  
      word[len-3]='\0';
      return(word);
      }
   }  /* end if len > 5 */

if (len > 4) {  
     /* -n{ae}k dative  */
   if ((word[len]=='k') && (word[len-2]=='n') && 
       ((word[len-1]=='a') || (word[len-1]=='e'))) {  
      word[len-2]='\0';
      return(word);
      }
     /* -C(ae}l instrumentive  (the consonant C is duplicated) */
   if ((word[len]=='l') && (word[len-2]==word[len-3]) && 
       (! IsVowel(word[len-2])) &&
       ((word[len-1]=='a') || (word[len-1]=='e'))) {  
      word[len-2]='\0';
      return(word);
      }
     /* -v(ae}l instrumentive  */
   if ((word[len]=='l') && (word[len-2]=='v') && 
       ((word[len-1]=='a') || (word[len-1]=='e'))) {  
      word[len-2]='\0';
      return(word);
      }
     /* -ert  goal */
   if ((word[len]=='t') && 
       (word[len-1]=='r') && (word[len-2]=='e')) {  
      word[len-2]='\0';
      return(word);
      }
     /* -rol  delative */
   if ((word[len]=='l') && 
       (word[len-1]=='o') && (word[len-2]=='r')) {  
      word[len-2]='\0';
      return(word);
      }
     /* -b{ae}n  inessive */
   if ((word[len]=='n') && (word[len-2]=='b') && 
       ((word[len-1]=='a') || (word[len-1]=='e'))) {  
      word[len-2]='\0';
      return(word);
      }
     /* -b{o"o}l  elative */
   if ((word[len]=='l') && (word[len-2]=='b') && 
       (word[len-1]=='o')) {  
      word[len-2]='\0';
      return(word);
      }
     /* -n{ae}l  adessive */
   if ((word[len]=='l') && (word[len-2]=='n') && 
       ((word[len-1]=='a') || (word[len-1]=='e'))) {  
      word[len-2]='\0';
      return(word);
      }
     /* -h{oe"o}z  allative */
   if ((word[len]=='z') && (word[len-2]=='h') && 
       ((word[len-1]=='o') || (word[len-1]=='e'))) {  
      word[len-2]='\0';
      return(word);
      }
     /* -t{o"o}l  ablative */
   if ((word[len]=='l') && (word[len-2]=='t') && 
       (word[len-1]=='o')) {  
      word[len-2]='\0';
      return(word);
      }
   }  /* end if len > 4 */

if (len > 3) {  
     /* -{aeo}t  accusative */
   if ((word[len]=='t') && 
       ((word[len-1]=='a') || (word[len-1]=='o') || (word[len-1]=='e'))) {  
      word[len-1]='\0';
      return(word);
      }
     /* -C(ae} transformative  (the consonant C is duplicated) */
   if ((word[len-1]==word[len-2]) && (!IsVowel(word[len-1])) && 
       ((word[len]=='a') || (word[len]=='e'))) {  
      word[len-1]='\0';
      return(word);
      }
     /* -v(ae} transformative  */
   if ((word[len-1]=='v') && 
       ((word[len]=='a') || (word[len]=='e'))) {  
      word[len-1]='\0';
      return(word);
      }
     /* C-{oe}n superessive (the consonant C is duplicated)  */
   if ((word[len]=='n') &&  (!IsVowel(word[len-2])) &&
       ((word[len-1]=='o') || (word[len-1]=='e'))) {  
      word[len-1]='\0';
      return(word);
      }
     /* -r{ae} sublative  */
   if ((word[len-1]=='r') && 
       ((word[len]=='a') || (word[len]=='e'))) {  
      word[len-1]='\0';
      return(word);
      }
     /* -b{ae}  illative */
   if ((word[len-1]=='b') && 
       ((word[len]=='a') || (word[len]=='e'))) {  
      word[len-1]='\0';
      return(word);
      }
     /* -ul  essive */
   if ((word[len]=='l') &&  (word[len-1]=='u')) {
      word[len-1]='\0';
      return(word);
      }
     /* -ig  terminative */
   if ((word[len]=='g') &&  (word[len-1]=='i')) {
      word[len-1]='\0';
      return(word);
      }
     /* -t  accusative */
   if (word[len]=='t') {
      word[len]='\0';
      return(word);
      }
     /* -n superessive  */
   if (word[len]=='n') {
      word[len]='\0';
      return(word);
      }
   }  /* end if len > 3 */

return(word); 
}

/* remove the possessive suffix added to the end of a noun */
static char *remove_possessive(char *word)
{ 
int len = strlen (word)-1;

/*  We need to make the distinction between four possibilities:
    - a single object (object:singular or o:sing) 
              is the property of one(p:sing) or more(p:plur) beings;
    - two (or more) objects (object:plural or o:plur)
              are the property of a single (p:sing) or not (p:plur)
*/

if (len > 5) {  
     /* C-{ao}tok  your (p:plur; o:singl) (with a consonant C) */
   if ((word[len]=='k') && (word[len-2]=='t') && 
       (word[len-1]=='o') && (!IsVowel(word[len-4])) &&
       ((word[len-3]=='a') || (word[len-3]=='o'))) {  
      word[len-3]='\0';
      return(word);
      }
     /* C-etek  your (p:plur; o:singl) (with a consonant C) */
   if ((word[len]=='k') && (word[len-2]=='t') && 
       (word[len-1]=='e') && (!IsVowel(word[len-4])) &&
       (word[len-3]=='e')) {  
      word[len-3]='\0';
      return(word);
      }
     /* -it(eo)k  your (p:plur; o:plur) */
   if ((word[len]=='k') && (word[len-2]=='t') && (word[len-3]=='i') && 
       ((word[len-1]=='e') || (word[len-1]=='o'))) {
      word[len-3]='\0';
      return(word);
      }
   }  /* end if len > 5 */

if (len > 4) {  
     /* C-{u"u}nk  our (p:plur; o:sing) (with a consonant C) */
   if ((word[len]=='k') && (!IsVowel(word[len-3])) &&  
       (word[len-1]=='n') && (word[len-2]=='u')) {  
      word[len-2]='\0';
      return(word);
      }
     /* C-t{oe}k  your (p:plur; o:sing) (with a consonant C) */
   if ((word[len]=='k') && (word[len-2]=='t') && (!IsVowel(word[len-3])) &&
       ((word[len-1]=='o') || (word[len-1]=='e'))) {  
      word[len-2]='\0';
      return(word);
      }
     /* V-juk  their (p:plur; o:sing) (with a vowel V) */
   if ((word[len]=='k') && (word[len-1]=='u') && 
       (word[len-2]=='j') && (IsVowel(word[len-3]))) {  
      word[len-2]='\0';
      return(word);
      }
     /* -ink  our (p:plur; o:plur) */
   if ((word[len]=='k') && (word[len-1]=='n') && 
       (word[len-2]=='i')) {  
      word[len-2]='\0';
      return(word);
      }
   }  /* end if len > 4 */

if (len > 3) {  
     /* C-{aoe}m  my (p:sing; o:sing) (with a consonant C) */
   if ((word[len]=='m') && (!IsVowel(word[len-2])) &&
       ((word[len-1]=='a') || (word[len-1]=='e') || (word[len-1]=='o'))) {
      word[len-1]='\0';
      return(word);
      }
     /* C-{aoe}d  your (p:sing; o:sing) (with a consonant C) */
   if ((word[len]=='d') && (!IsVowel(word[len-2])) &&
       ((word[len-1]=='a') || (word[len-1]=='e') || (word[len-1]=='o'))) {
      word[len-1]='\0';
      return(word);
      }
     /* C-uk  their  (p:plur; o:sing) (with a consonant C) */
   if ((word[len]=='k') && (word[len-1]=='u') &&
       (!IsVowel(word[len-2]))) {  
      word[len-1]='\0';
      return(word);
      }
     /* V-nk  our (p:plur; o:sing) (with a vowel V) */
   if ((word[len]=='k') && (IsVowel(word[len-2])) &&  
       (word[len-1]=='n')) {  
      word[len-1]='\0';
      return(word);
      }
     /* V-j(ae)  her/his (p:sing; o:sing) (with a vowel V) */
   if ((word[len-1]=='j') && (IsVowel(word[len-2])) &&
       ((word[len]=='a') || (word[len]=='e'))) {
      word[len-1]='\0';
      return(word);
      }
     /* -im  my   (p:sing; o:plur)  */
     /* -id  your (p:sing; o:plur)  */
     /* -ik  their (p:plur; o:plur)  */
   if ((word[len-1]=='i') &&
       ((word[len]=='m') || (word[len]=='d') || (word[len]=='k'))) {
      word[len-1]='\0';
      return(word);
      }
   }  /* end if len > 3 */
if (len > 2) {  
     /* C-(ae}  her/his (p:sing; o:sing) (with a consonant C)  */
   if (((word[len]=='a') || (word[len]=='e')) && (!IsVowel(word[len-1]))) {  
      word[len]='\0';
      return(word);
      }
     /* V-m  my (p:sing; o:sing) (with a vowel V) */
   if ((word[len]=='m') && (IsVowel(word[len-1]))) {
      word[len]='\0';
      return(word);
      }
     /* V-d  your (p:sing; o:sing)  (with a vowel V) */
   if ((word[len]=='d') && (IsVowel(word[len-1]))) {
      word[len]='\0';
      return(word);
      }
     /* -i his/her (p:sing; o:plur) */
   if (word[len]=='i') {
      word[len]='\0';
      return(word);
      }
   }  /* end if len > 2 */

return(word); 
}


/* to remove the plural suffix, usually the -k */
static char *remove_plural(char *word)
{ 
int len = strlen (word)-1;

if (len > 3) {  
     /* -{aoe}k  plural */
   if ((word[len]=='k') && 
       ((word[len-1]=='o') || (word[len-1]=='e') || 
        (word[len-1]=='a'))) {  
      word[len-1]='\0';
      return(word);
      }
   }  /* end if len > 3 */
if (len > 2) {  
     /* -k  plural */
   if (word[len]=='k') {
      word[len]='\0';
      return(word);
      }
   }  /* end if len > 2 */
return(word); 
}

