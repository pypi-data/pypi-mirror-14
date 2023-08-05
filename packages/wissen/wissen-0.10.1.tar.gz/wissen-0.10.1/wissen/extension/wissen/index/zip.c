#include "zlib.h"
#include "index.h"
#include <stdlib.h>

#define DEFLATED   8
#if MAX_MEM_LEVEL >= 8
#  define DEF_MEM_LEVEL 8
#else
#  define DEF_MEM_LEVEL  MAX_MEM_LEVEL
#endif
#define DEF_WBITS MAX_WBITS

/* The output buffer will be increased in chunks of DEFAULTALLOC bytes. */
#define DEFAULTALLOC (16*1024)


int
zcompress(char *input, int length, BFILE* output, int level)
{
	z_stream zst;
	int err;

	if (!level) {
		level = Z_DEFAULT_COMPRESSION;
	}
		
	zst.avail_out = length + length / 1000 + 12 + 1;
	if (bextend (output, zst.avail_out) == -1) return 0;		
	zst.avail_out = output->max;
	
	zst.zalloc = (alloc_func)NULL;
	zst.zfree = (free_func)Z_NULL;
	zst.next_out = (Byte *) output->buffer;
	zst.next_in = (Byte *)input;
	zst.avail_in = length;
	
	err = deflateInit(&zst, level);

	switch(err) {
		case(Z_OK):
			break;
		case(Z_MEM_ERROR):
			goto error;
		case(Z_STREAM_ERROR):
			goto error;
		default:
			deflateEnd(&zst);			
			goto error;
		}
		err = deflate(&zst, Z_FINISH);
		if (err != Z_STREAM_END) {
			deflateEnd(&zst);
			goto error;
	}

	err=deflateEnd(&zst);
	if (err == Z_OK) {
		bseek (output, zst.total_out);
		return 1;
	}		
	
 error: 	
 	return 0;
}


int
zdecompress(char *input, int length, BFILE* output)
{
	int err;
	int wsize=DEF_WBITS;
	z_stream zst;

	zst.avail_in = length;
	if (bextend (output, DEFAULTALLOC) == -1) return 0;
	
	zst.avail_out = output->max;
	bseek (output, output->max);	
	zst.zalloc = (alloc_func)NULL;
	zst.zfree = (free_func)Z_NULL;
	zst.next_out = (Byte *) output->buffer;
	zst.next_in = (Byte *) input;
	err = inflateInit2(&zst, wsize);

	switch(err) {
		case(Z_OK):
			break;
		case(Z_MEM_ERROR):	
			goto error;
		default:
			inflateEnd(&zst);			
			goto error;
	}

	do {
		err=inflate(&zst, Z_FINISH);
		switch(err) {
			case(Z_STREAM_END):
				break;
			case(Z_BUF_ERROR):
				if (zst.avail_out > 0) {
					inflateEnd(&zst);
					goto error;
				}			
			case(Z_OK):
				/* need more memory */
				if (bextend (output, 0) == -1) { /* + DEFAULTALLOC */
					inflateEnd(&zst);
					goto error;
				}
				zst.next_out = (unsigned char *) output->buffer + btell (output);
				zst.avail_out = output->max - btell (output);
				bseek (output, output->max);				
				break;
				
			default:
				inflateEnd(&zst);				
				goto error;
		}
		
	} while (err != Z_STREAM_END);
	
	err = inflateEnd(&zst);
	if (err != Z_OK) {		
		goto error;
	}
	output->__readsize = zst.total_out; // mark avail end pointer
	bseek (output, zst.total_out);	
	return 1;

 error: 	
 	return 0;
}

