#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

char* formalize (char* buffer, char *document, int len)
{
	char lch = ' ', ch;
	char *n;
	n = buffer;
	
	while (len) {
		len--;
		ch = *document++;
		if (ch == '\0') continue;
		if (ch == '\r' || ch == '\n' || ch=='\t') ch = ' ';
		if (isspace (ch) && isspace (lch)) continue;
		*buffer++ = ch;
		lch = ch;
	}
	*buffer = '\0';
	return n;
}

