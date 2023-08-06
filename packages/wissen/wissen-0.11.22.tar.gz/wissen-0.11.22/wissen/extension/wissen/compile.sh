#!/bin/bash

python setup.py build --force 
cp build/lib.linux-x86_64-2.7/_wissen.so /data/skitai/skitai/site-packages/wissen/

