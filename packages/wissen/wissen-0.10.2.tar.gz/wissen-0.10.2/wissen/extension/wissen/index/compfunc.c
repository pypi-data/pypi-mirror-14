// docid compare fun
int
key_compfunc (const void *x, const void *y) {
     if ( *(const int *)x > *(const int *)y ) return 1;
	 else if ( *(const int *)x < *(const int *)y ) return -1;
	 return 0;
}

// value compare fun
int
value_compfunc (const void *x, const void *y) {
     if ( *((const int *)x+1) > *((const int *)y+1) ) return -1;
	 else if ( *((const int *)x+1) < *((const int *)y+1) ) return 1;
	 return 0;
}


