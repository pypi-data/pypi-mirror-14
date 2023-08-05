#include <stdio.h>

#ifdef __unix__
#include <unistd.h> 
#define _read read
#define _write write
#define _close close
#define _dup dup
#define _lseek lseek

#else
#include <io.h>

#endif

#include <stdlib.h>
#include "index.h"
#include "pthread.h"

#ifdef __unix__
long _tell(int fd)
{
    return (long) lseek(fd, 0, SEEK_CUR);
}
#endif

static pthread_mutex_t global_mutex;
static int global_mutex_inited = 0;

BFILE* bopen (int file, char mode, int max, int extend)
{
	BFILE* bfile;	
	if (!global_mutex_inited) {
		pthread_mutex_init (&global_mutex, NULL);
		global_mutex_inited = 1;	
	}	
	
	bfile = malloc (sizeof (BFILE));
	if (!bfile) {		
		return NULL;
	}
	bfile->__bsize = max;
	bfile->max = bfile->__bsize;
	bfile->buffer = malloc (max);		
	if (!bfile->buffer) {
		free (bfile);
		return NULL;
	}	
	bfile->file = file;
	bfile->mode = mode;
	bfile->extend = extend;
	bfile->position = 0;
	bfile->errcode = 0;	
	bfile->__tell = 0;
	bfile->__translate = 0;
	bfile->__readpoint = 0;
	bfile->__readsize = 0;
	bfile->__clone = 0;
	bfile->__mutex = global_mutex;		
	bfile->__linked = 1;
	bfile->__exbuffer = 0;
		
	if (file > -1) {
		bfile->__mutex = global_mutex;
		bfile->__linked = 0;
		
		if (mode == 'r') {
			if (brefill (bfile) == -1) {
				if (bfile->__readsize == 0) return bfile; /* NOT ERROR, ZERO SIZE FILE */
				free (bfile->buffer);
				free (bfile);		
				return NULL;
			}	
		}
	}
	return bfile;
}

BFILE* bopen2 (char* buffer, char mode, int max, int extend)
{
	BFILE* bfile;
	
	bfile = malloc (sizeof (BFILE));
	if (!bfile) return NULL;
	bfile->max = max;
	bfile->__bsize = max;
	bfile->buffer = buffer;
	bfile->file = -1;
	bfile->mode = mode;
	bfile->extend = extend;
	bfile->position = 0;
	bfile->__tell = 0;
	bfile->__translate = 0;
	bfile->__readsize = max;
	bfile->__readpoint = 0;
	bfile->__linked = 0;
	bfile->__clone = 0;
	bfile->__mutex = global_mutex;	
	bfile->__linked = 1;
	bfile->__exbuffer = 1;
	
	return bfile;
}

int blink (BFILE* bfile, int file, pthread_mutex_t mutex, long offset, int n)
{
	bfile->__translate	= 0;
	bfile->file = file;
	bfile->__mutex = mutex;
		
	if (bfile->mode == 'r') {
		if (bfile->extend && bfile->max < n) {
			if (bextend (bfile, n) == -1) {
				bfile->errcode = 1;
				return -1;
			}	
		}	
		else if (!n || n > bfile->max) n = bfile->max;
		pthread_mutex_lock(&bfile->__mutex);
		if (_lseek (bfile->file, offset, SEEK_SET) == -1) {
			goto ioerror;
		}
		bfile->__tell = _tell (bfile->file);
		if (bfile->__tell == -1) {
			goto ioerror;
		}
		bfile->__readsize = _read (bfile->file, bfile->buffer, n);
		if (bfile->__readsize <= 0) {
			goto ioerror;
		}
		bfile->__readpoint = _tell (bfile->file);
		if (bfile->__readpoint == -1) {
			goto ioerror;
		}
		pthread_mutex_unlock(&bfile->__mutex);
		bfile->position = 0;
	}
	
	else {
		bfile->__readpoint = 0;
		bfile->__readsize = 0;
		
		pthread_mutex_lock(&bfile->__mutex);
		bfile->__tell = _tell (bfile->file);		
		if (bfile->__tell == -1) {
			goto ioerror;
		}
		pthread_mutex_unlock(&bfile->__mutex);	
		bfile->position = 0;
	}
	
	return 0;

ioerror:
	bfile->errcode = 2;
	pthread_mutex_unlock (&bfile->__mutex);
	return -1;
}

void bunlink (BFILE* bfile)
{
	bfile->__readpoint = 0;
	bfile->__readsize = 0;
	bfile->__tell = 0;	
	bfile->file = -1;
	bfile->position = 0;
	bfile->__mutex = global_mutex;
	bfile->__translate	= 0;
}

BFILE* bdup (BFILE* bfile) 
{
	BFILE* dupbfile;
	
	dupbfile = bopen (_dup (bfile->file), bfile->mode, bfile->max, bfile->extend);
	dupbfile->__clone = 1;	
	return dupbfile;
}

int bextend (BFILE* bfile, int extend)
{
	int basesize;
	
	if (!extend) {
		basesize = bfile->__bsize / bfile->extend;
		bfile->extend ++;
		bfile->__bsize = basesize * bfile->extend;
		bfile->__readsize = bfile->__bsize;
		bfile->max = bfile->__bsize;
		bfile->buffer = (char*) realloc (bfile->buffer, bfile->__bsize);		
	}
	
	else if (bfile->__bsize < extend) {
		bfile->__bsize = extend;
		bfile->max = bfile->__bsize;
		bfile->__readsize = bfile->__bsize;
		bfile->buffer = (char*) realloc (bfile->buffer, bfile->__bsize);		
	}
	
	else {
		bfile->__readsize = extend;
	}
	
	if (!bfile->buffer) {
		bfile->errcode = 1;
		return -1;
	}
		
	return bfile->__bsize;
}

void btranslate (BFILE* bfile, long offset)
{
	bfile->__translate	= offset;	
}	

int bclose (BFILE* bfile)
{
	if (bfile) {
		if (bfile->file > -1) {			
			if (bfile->mode == 'w') {		
				if (bflush (bfile) == -1) goto ioerror;		
			}
			if (bfile->__clone) {
				_close (bfile->file);
			}
		}		
		if (!bfile->__exbuffer && bfile->buffer) free (bfile->buffer);
		free (bfile);
	}	
	return 0;

ioerror:
	//if (!bfile->__linked && bfile->__mutex) {
	//	pthread_mutex_destroy (&bfile->__mutex);
	//}
	if (bfile->buffer) free (bfile->buffer);
	if (bfile) free (bfile);
	return -1;	
}

int bcommit (BFILE* bfile, BFILE* target)
{
	int i;
	
	for (i = 0; i < bfile->position; i++) {
		if (target->position >= target->max)  {
			if (bflush (target) == -1) return -1;
		}	
		target->buffer[target->position++] = bfile->buffer [i];
	}
	bfile->position = 0; /*reset buffer */
	return bfile->position;
}

int bncopy (BFILE* bfile, BFILE* target, int n)
{
	int i, tlen;
	
	if (n == -1) tlen = bfile->position;
	else tlen = n;
		
	for (i = 0; i < tlen; i++) {
		if (target->position >= target->max) {
			if (bflush (target) == -1) goto ioerror;
		}
		if (bfile->position >= bfile->max) {
			if (brefill (bfile) == -1) goto ioerror;
		}	
		target->buffer[target->position++] = bfile->buffer [bfile->position++];
	}
	target->__readsize = target->position;	
	return target->max;

ioerror:
	return -1;
}

int bflush (BFILE* bfile)
{
	if (bfile->extend) {
		return bextend (bfile, 0);
	}
	
	else if (bfile->position) {
		pthread_mutex_lock(&bfile->__mutex); 
		if (bfile->position != _write (bfile->file, bfile->buffer, bfile->position)) goto ioerror;
		bfile->__tell = _tell (bfile->file);
		if (bfile->__tell == -1) goto ioerror;
		pthread_mutex_unlock(&bfile->__mutex);
		bfile->position = 0;
		bfile->__readsize = 0;
	}	
	return 0;

ioerror:
	bfile->errcode = 2;
	pthread_mutex_unlock(&bfile->__mutex);			
	return -1;	
}

int brefill (BFILE* bfile)
{
	pthread_mutex_lock(&bfile->__mutex);
	if (_lseek (bfile->file, bfile->__readpoint, SEEK_SET) == -1) {
		goto ioerror;
	}
	bfile->__tell = _tell (bfile->file);
	if (bfile->__tell == -1) {
		goto ioerror;
	}
	
	bfile->__readsize = _read (bfile->file, bfile->buffer, bfile->max);
	if (bfile->__readsize <= 0) {
		goto ioerror;
	}	
	
	bfile->__readpoint = _tell (bfile->file);
	if (bfile->__readpoint == -1) {
		goto ioerror;
	}
	pthread_mutex_unlock(&bfile->__mutex);	
	bfile->position = 0;
	return bfile->__readsize;
	
ioerror:
	bfile->errcode = 2;
	pthread_mutex_unlock(&bfile->__mutex);			
	return -1;			
}

long btell (BFILE* bfile)
{
	if (bfile->file == -1) {		
		return bfile->position;
	}	
	return bfile->__tell - bfile->__translate + bfile->position;		
}

int bseek (BFILE* bfile, long offset)
{
	if (bfile->file > -1) {
		if (bfile->mode == 'r') {
			bfile->position += (offset - (bfile->__tell - bfile->__translate + bfile->position));
			/* overflowed, refill */
			if (bfile->position >= bfile->max || bfile->position < 0) {
				bfile->__readpoint = bfile->__translate + offset;
				if (brefill (bfile) == -1) goto ioerror;
				return offset;
			}
			return offset;
		}
		
		else {	
			if (bflush (bfile) == -1) goto ioerror;
			pthread_mutex_lock(&bfile->__mutex); 
			if (_lseek (bfile->file, bfile->__translate + offset, SEEK_SET) == -1) goto ioerror;
			bfile->__tell = _tell (bfile->file);
			if (bfile->__tell == -1) goto ioerror;
			pthread_mutex_unlock(&bfile->__mutex);
			return offset;
		}
	}
	
	else {
		bfile->position = offset;
		if (offset > bfile->max) return bfile->max;
		return offset;
	}
	

ioerror:	
	bfile->errcode = 1;
	pthread_mutex_unlock(&bfile->__mutex); 
	return -1;
}

int bsize (BFILE* bfile)
{
	return bfile->__bsize;
}

void setmax (BFILE* bfile, int max) {
	if (!max || max > bfile->__bsize)
		bfile->max = bfile->__bsize;
	else if (max < 1024)
		bfile->max = 1024;	
	else
		bfile->max = max;	
}



