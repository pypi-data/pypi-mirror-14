#define MEGA (1024*1024) 

#ifdef __unix__
#include <sys/statvfs.h>
unsigned long long getdiskspace (char* dir) {
  struct statvfs buf;
  if (!statvfs((const char*) dir, &buf)) {
 		return (unsigned long long) (buf.f_bfree * buf.f_bsize) / MEGA;
  }	
  return 0;
}

#else
#include <windows.h>  
unsigned long long getdiskspace (char* dir)   
{   
	ULARGE_INTEGER lpFreeBytesAvailableToCaller;     
	ULARGE_INTEGER lpTotalNumberOfBytes;        
	ULARGE_INTEGER lpTotalNumberOfFreeBytes; 
	GetDiskFreeSpaceEx( 
		dir,
		&lpFreeBytesAvailableToCaller,   
		&lpTotalNumberOfBytes,   
		&lpTotalNumberOfFreeBytes  
	);
	
	//printf("%I64u %I64u %I64u \n",
	//lpFreeBytesAvailableToCaller.QuadPart/MEGA,     
	//lpTotalNumberOfBytes.QuadPart/MEGA,        
	//lpTotalNumberOfFreeBytes.QuadPart/MEGA);
	return (unsigned long long) lpFreeBytesAvailableToCaller.QuadPart/MEGA;
} 
#endif

