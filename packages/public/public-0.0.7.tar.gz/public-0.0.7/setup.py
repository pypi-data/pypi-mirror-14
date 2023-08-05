#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys

dir = os.path.dirname(__file__)
if not dir or dir==".": dir=os.getcwd()
sys.path.append("%s/.setup" % dir)

if __name__=="__main__":
	# import .setup.py/__setup__.py
	import __setup__
