import ctypes
import sys

import os
import collections

_ntuple_diskusage = collections.namedtuple('usage', 'total used free')

if hasattr(os, 'statvfs'):  # POSIX
	def disk_usage(path):
		st = os.statvfs(path)
		free = st.f_bavail * st.f_frsize
		total = st.f_blocks * st.f_frsize
		used = (st.f_blocks - st.f_bfree) * st.f_frsize
		return _ntuple_diskusage(total, used, free)

elif os.name == 'nt':	   # Windows
	import ctypes
	import sys

	def disk_usage(path):
		_, total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong(), \
						   ctypes.c_ulonglong()
		if sys.version_info >= (3,) or isinstance(path, unicode):
			fun = ctypes.windll.kernel32.GetDiskFreeSpaceExW
		else:
			fun = ctypes.windll.kernel32.GetDiskFreeSpaceExA
		ret = fun(path, ctypes.byref(_), ctypes.byref(total), ctypes.byref(free))
		if ret == 0:
			raise ctypes.WinError()
		used = total.value - free.value
		return _ntuple_diskusage(total.value, used, free.value)
		
else:
	raise NotImplementedError("platform not supported")

disk_usage.__doc__ = __doc__

if __name__ == '__main__':
	df = disk_usage(r"C:\hdd\lavie")
	f = open ("DISK-FREE-%2.1fGB" % (int (df.free) / 1024. /1024. /1024.,), "wb")
	f.write ("")
	f.close ()
	
