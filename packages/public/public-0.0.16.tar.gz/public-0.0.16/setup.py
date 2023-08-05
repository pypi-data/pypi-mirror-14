#!/usr/bin/env python
# -*- coding: utf-8 -*-
__all__ = []
import os, sys
from os.path import *

repo = abspath(dirname(__file__))

# repo/setup.py 	- this file
# repo/.setup/*.py 	- python files imported by setup.py
setup = join(repo,".setup")
if exists(setup) and isdir(setup):
	sys.path.append(setup)
else:
	raise Exception("%s NOT EXISTS" % setup)

if __name__=="__main__":
	import __setup__
