python setup.py build %1
copy /y build\lib.win-amd64-2.7\_wissen.pyd ..\..\wissen\
copy /y ..\libs\pthread2\x64\pthreadVC2.dll ..\..\wissen\
copy /y ..\svm\build\lib.win-amd64-2.7\_svm.pyd ..\..\wissen\classifier\svm\

