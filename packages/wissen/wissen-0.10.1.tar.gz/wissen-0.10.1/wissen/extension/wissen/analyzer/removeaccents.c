#include <string.h>
#include <stdio.h>

int removeLatinAccents (char* word) {
	int pos = 0, len;
	unsigned char *ar;
	unsigned char buf [100];
	int bpos = 0;
	
	len = strlen (word);	
	if (len > 99) return 1;

	ar = (unsigned char *) word;
	
	while (pos < len) {		
		if (ar [pos] == 0xc3) {			
			pos ++;
			if (pos == len) break;
			
			if (ar [pos] >= 0xa0 && ar [pos] <= 0xa5) buf [bpos++] = 'a';
			else if (ar [pos] == 0xa7) buf [bpos++] = 'c';
			else if (ar [pos] >= 0xa8 && ar [pos] <= 0xab) buf [bpos++] = 'e';		
			else if (ar [pos] >= 0xac && ar [pos] <= 0xaf) buf [bpos++] = 'i';		
			else if (ar [pos] >= 0xb2 && ar [pos] <= 0xb6) buf [bpos++] = 'o';		
			else if (ar [pos] >= 0xb9 && ar [pos] <= 0xbc) buf [bpos++] = 'u';
			else if (ar [pos] >= 0x80 && ar [pos] <= 0x85) buf [bpos++] = 'A';
			else if (ar [pos] == 0x87) buf [bpos++] = 'C';
			else if (ar [pos] >= 0x88 && ar [pos] <= 0x8b) buf [bpos++] = 'E';	
			else if (ar [pos] >= 0x8c && ar [pos] <= 0x8f) buf [bpos++] = 'I';	
			else if (ar [pos] >= 0x92 && ar [pos] <= 0x96) buf [bpos++] = 'O';	
			else if (ar [pos] >= 0x99 && ar [pos] <= 0x9c) buf [bpos++] = 'U';
		}	
		else {
			buf [bpos++] = ar [pos];
		}
		pos++;
	}
	
	buf [bpos] = '\0';	
	strcpy (word, (char*) buf);	
	return bpos;
}
