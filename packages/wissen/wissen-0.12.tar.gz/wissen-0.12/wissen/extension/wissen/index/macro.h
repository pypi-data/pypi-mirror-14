/*****************************************************************************
buffer direct
*****************************************************************************/
#define writeInt(buffer, i32, buffer_index, int_length) {\
	_uint = i32;\
	_shift = 0;\
	while ((_shift >> 3) < int_length) {\
		buffer [buffer_index++] = (unsigned char)( _uint >> _shift & 0xff);\
    	_shift += 8;\
	}\
}

#define readInt(buffer, i32, buffer_index, int_length) {\
	i32 = 0;\
  _shift = 0;\
  while ((_shift >> 3) < int_length) {\
  	_uchar = buffer [buffer_index++];\
  	i32 |= (unsigned int)_uchar << _shift;\
  	_shift += 8;\
  }\
}

#define writeLong(buffer, i64, buffer_index, int_length) {\
	_shift = 0;\
	_ulong = i64;	\
	while ((_shift >> 3) < int_length) {\
    	buffer [buffer_index++] = (unsigned char)( _ulong >> _shift & 0xff);\
    	_shift += 8;\
	}\
}

#define readLong(buffer, i64, buffer_index, int_length) {\
	_shift = 0;\
  i64 = 0;\
  while ((_shift >> 3) < int_length) {\
  	_uchar = buffer [buffer_index++]; \
  	i64 |= (unsigned long long) _uchar << _shift;\
  	_shift += 8;\
  }\
}


#define writeVInt(buffer, int32, buffer_index) {\
	_uint = (unsigned int) int32;\
    while ((_uint & ~0x7F) != 0) {\
      buffer [buffer_index++] = (unsigned char) ((_uint & 0x7f) | 0x80);\
      _uint >>= 7;\
    }\
    buffer [buffer_index++] = (unsigned char) _uint;\
}

#define readVInt(buffer, int32, buffer_index) {\
	_uchar	 = buffer [buffer_index++];\
    int32 = _uchar & 0x7F;\
    for (_shift = 7; (_uchar & 0x80) != 0; _shift += 7) {\
      	_uchar = buffer [buffer_index++];\
      	int32 |= (_uchar & 0x7F) << _shift;\
    }\
}

#define writeVLong(buffer, int64, buffer_index) {\
	_ulong = int64;\
    while ((_ulong & ~0x7FL) != 0) {\
      buffer [buffer_index++] = (unsigned char) ((_ulong & 0x7FL) | 0x80);\
      _ulong >>= 7;\
    }\
    buffer [buffer_index++] = (unsigned char) _ulong;\
}

#define readVLong(buffer, int64, buffer_index) {\
	_uchar	 = buffer [buffer_index++];\
    int64 = _uchar & 0x7FL;\
    for (_shift = 7; (_uchar & 0x80) != 0; _shift += 7) {\
      	_uchar = buffer [buffer_index++];\
      	int64 |= (unsigned long long) (_uchar & 0x7FL) << _shift;\
    }\
}

#define writeString(buffer, str, len, buffer_index) {\
	for (_shift = 0; _shift < (int) len; _shift ++) {\
		buffer [buffer_index] = str [_shift];\
	}\
}



/*****************************************************************************
to File
*****************************************************************************/

#define fwriteInt(fs, int32, int_length) {\
	_uint = int32;\
	_shift = 0;\
	while ((_shift >> 3) < int_length) {\
		fputc ((unsigned char)( _uint >> _shift & 0xff), fs);\
    	_shift += 8;\
	}\
}

#define freadInt(fs, int32, int_length) {\
	int32 = 0;\
    _shift = 0;\
    while ((_shift >> 3) < int_length) {\
    	_uchar = fgetc (fs);\
    	int32 |= (unsigned int) _uchar << _shift;\
    	_shift += 8;\
    }\
}

#define fwriteLong(fs, int64, int_length) {\
	_shift = 0;\
	_ulong = int64;	\
	while ((_shift >> 3) < int_length) {\
    	fputc ((unsigned char)( _ulong >> _shift & 0xff), fs);\
    	_shift += 8;\
	}\
}

#define freadLong(fs, int64, int_length) {\
	_shift = 0;\
    int64 = 0;\
    while ((_shift >> 3) < int_length) {\
    	_uchar = fgetc (fs); \
    	int64 |= (unsigned long long) _uchar << _shift;\
    	_shift += 8;\
    }\
}


#define fwriteVInt(fs, int32) {\
	_uint = (unsigned int) int32;\
	while ((_uint & ~0x7F) != 0) {\
      fputc ((unsigned char) ((_uint & 0x7f) | 0x80), fs);\
      _uint >>= 7;\
    }\
    fputc ((unsigned char) _uint, fs);\
}

#define freadVInt(fs, int32) {\
	_uchar	 = fgetc (fs);\
    int32 = _uchar & 0x7F;\
    for (_shift = 7; (_uchar & 0x80) != 0; _shift += 7) {\
      	_uchar = fgetc (fs);\
      	int32 |= (_uchar & 0x7F) << _shift;\
    }\
}

#define fwriteVLong(fs, int64) {\
	_ulong = int64;\
    while ((_ulong & ~0x7FL) != 0) {\
      fputc ((unsigned char) ((_ulong & 0x7FL) | 0x80), fs);\
      _ulong >>= 7;\
    }\
    fputc ((unsigned char) _ulong, fs);\
}

#define freadVLong(fs, int64) {\
	_uchar	 = fgetc (fs);\
    int64 = _uchar & 0x7FL;\
    for (_shift = 7; (_uchar & 0x80) != 0; _shift += 7) {\
      	_uchar = fgetc (fs);\
      	int64 |= (unsigned long long) (_uchar & 0x7FL) << _shift;\
    }\
}

#define freadString(fs, str, len) {\
	fread (str, 1, len, fs);\
}

#define fwriteString(fs, str, len) {\
	fwrite (str, 1, len, fs);\
}
