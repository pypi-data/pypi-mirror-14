#!/usr/bin/env python
# -*- coding: utf-8 -*-
__all__=["name"]
import os
from os.path import *

dir = dirname(dirname(__file__))
if not dir: dir="."

# default pkgname
name = basename(dir).lower().replace(".py","")#.replace(".","-")


if __name__=="__main__":
    for k in __all__:
        if k in globals():
            print("%s: %s" % (k,globals()[k]))
