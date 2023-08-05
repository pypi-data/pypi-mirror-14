#!/usr/bin/env python
import os
from os.path import *
# me
from fullpath import *
from public import *

@public
def touch(path):
    # todo: add datetime
    if not path: return
    path = fullpath(path)
    if path.find("/")>0 and not exists(dirname(path)):
        os.makedirs(dirname(path))
    try:
        os.utime(path,None)
    except:
        open(path,'a').close()

if __name__=="__main__":
    touch(__file__)
    touch("~/testtest") # fullpath
    os.unlink(fullpath("~/testtest"))

    touch(None) # skip

