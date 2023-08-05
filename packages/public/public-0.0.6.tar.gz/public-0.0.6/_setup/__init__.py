#!/usr/bin/env python
# -*- coding: utf-8 -*-
__all__ = [] # args passed to setup(name=name,**kwargs)
import imp
import os
import sys
from os.path import *

setuptools=True
if sys.argv[-1]=="--manifest-only":
    setuptools=False

try:
    # pypi.python.org/pypi/setuptools
    # features:
    # python setup.py develop
    if setuptools:
        from setuptools import setup
    else:
        from distutils.core import setup
except ImportError:
    # standart library
    # features:
    # python setup.py sdist --manifest-only
    from distutils.core import setup
import sys
import warnings

# https://docs.python.org/2/distutils/setupscript.html
# https://docs.python.org/3/distutils/setupscript.html

def pyfiles(dir):
    list = os.listdir(dir)
    list = filter(lambda l:splitext(l)[1]==".py" and l.find("__")<0,list)
    return list

def module_kwargs(module):
    kwargs=dict()
    for k in getattr(module,"__all__"):
        if getattr(module,k):
            kwargs[k] = getattr(module,k)
    return kwargs

def load_module(path):
    with open(path,'rb') as fp:
        # .hidden.py invisible for mdfind
        module = imp.load_module(path,fp,path,('.py', 'rb', imp.PY_SOURCE))  
        # __all__ required
        if not hasattr(module,'__all__'):
            raise ValueError("ERROR: %s __all__ required" % path)
        return module

def update(**kwargs):
    for k,v in kwargs.items():
        if k not in sys.modules[__name__].__all__:
            sys.modules[__name__].__all__.append(k)
        setattr(sys.modules[__name__],k,v)

def main():
    dir = dirname(dirname(__file__))
    if not dir or dir==".": dir=os.getcwd()
    os.chdir(dir)
    sys.path+=[dir,dirname(__file__)]

    files = pyfiles(dirname(__file__))
    # RuntimeWarning: Parent module 'modname' not found while handling absolute import
    warnings.simplefilter("ignore", RuntimeWarning)

    for file in files:
        try:
            fullpath=join(dirname(__file__),file)
            module = load_module(fullpath)
            kwargs=module_kwargs(module)
            update(**kwargs)
            if len(sys.argv)==1 and len(kwargs)>0:
                print("%s: %s" % (file[1:],kwargs))
        except AttributeError: # variable from __all__ not initialized
            continue
    # ~/.setup_kwargs.py
    fullpath=join(os.environ["HOME"],".setup_kwargs.py")
    if exists(fullpath):
        module = load_module(fullpath)
        setup_kwargs = module_kwargs(module)

        update(**setup_kwargs)
        if len(sys.argv)==1 and len(setup_kwargs)>0: # debug
            print("%s: %s" % ("~/.setup_kwargs.py",setup_kwargs))

    def isstring(object):
        try:
            int(object)
            return False
        except ValueError:
            return True
        except:
            return False

    kwargs = module_kwargs(sys.modules[__name__])
    if "name" in kwargs:
        name = kwargs["name"]
        del kwargs["name"]

    if len(sys.argv)==1 and kwargs: # debug
        print('\nsetup(name="%s",' % name)
        # for i,(k,v) in enumerate(sorted(kwargs.iteritems(),key=lambda (k,v):k),1): # python2
        for i,k in enumerate(sorted(list(kwargs.keys())),1): # python3
            v=kwargs[k]
            print("    %s = %s%s" % (k,'"%s"' % v if isstring(v) else v,"," if i!=len(kwargs) else ""))
        print(')')  

    if len(sys.argv)==1: return
    setup(name=name,**kwargs)

#if __name__=="__main__":
main()
