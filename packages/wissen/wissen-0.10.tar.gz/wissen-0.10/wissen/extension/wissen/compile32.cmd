python setup.py build %1
copy /y build\lib.win32-2.7\_wissen.pyd ..\..\
rem copy /y ..\libs\pthread2\x86\pthreadVC2.dll ..\..\wissen\
rem copy /y ..\svm\build\lib.win32-2.7\_svm.pyd ..\..\wissen\classifier\svm\

