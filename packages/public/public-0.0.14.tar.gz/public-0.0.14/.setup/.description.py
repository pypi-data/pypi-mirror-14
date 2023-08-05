#!/usr/bin/env python
# -*- coding: utf-8 -*-
__all__=["description"]
from os.path import *

repo = dirname(dirname(__file__))
if not repo: repo="."

file = join(repo,"description")
if exists(file):
    description = open(file).read().lstrip().rstrip()
else:
    if __name__=="__main__":
        print("SKIP: description NOT EXISTS")

if __name__=="__main__":
	for k in __all__:
		if k in globals():
			print("%s: %s" % (k,globals()[k]))

