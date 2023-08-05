#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import *
from isbinaryfile import *
from read import *
from public import *
from write import *

class Exception(Exception): pass

@public
def isshebang(l):
    """return True if line is shebang"""
    return l and l.find("#!")==0

@public
def shebang(path):
    """return file/string shebang"""
    if not path: return
    path = str(path)
    if not exists(path): return
    if isbinaryfile(path): return
    content = read(path)
    lines = content.splitlines()
    if lines:
        l=lines[0] # first line
        if isshebang(l):
            l = l.replace("#!","",1)
            return l.lstrip().rstrip()

if __name__=="__main__":
    print(shebang(__file__)) # /usr/bin/env python
    print(shebang(None)) # None
    print(shebang("/bin/ls")) # None


