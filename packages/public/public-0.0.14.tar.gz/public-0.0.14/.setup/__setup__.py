#!/usr/bin/env python
# -*- coding: utf-8 -*-
import imp
import os
from os.path import *
import sys
import warnings

# 1) distutils (Python Standart Library)
#   docs.python.org/2/distutils/setupscript.html
#   docs.python.org/3/distutils/setupscript.html
# python setup.py --manifest-only
# 2) setuptools (+easy_install tool)
#   pypi.python.org/pypi/setuptools
#   pythonhosted.org/setuptools/setuptools.html

# setuptools additional setup(name,**kwargs) keywords
setuptools_kwargs=[
    "include_package_data", # True/False
    "exclude_package_data", # True/False
    "package_data", # True/False
    "zip_safe", # True/False
    "install_requires", # [...]
    "entry_points", # [...]
    "extras_require", # [...]
    "setup_requires", # [...]
    "dependency_links", # [...]
    "namespace_packages", # [...]
    "test_suite", # ''
    "tests_require", # ''
    "test_loader" # ''
]
# setuptools `python setup.py` Extra commands (python setup.py --help):
setuptools_args=[
  "saveopts",          # save supplied options to setup.cfg or other config file
  "testr",             # Run unit tests using testr
  "develop",           # install package in 'development mode'
  "upload_docs",       # Upload documentation to PyPI
  "test",              # run unit tests after in-place build
  "setopt",            # set an option in setup.cfg or another config file
  "nosetests",         # Run unit tests using nosetests
  "install_egg_info",  # Install an .egg-info directory for the package
  "rotate",            # delete older distributions, keeping N newest files
  "bdist_mpkg",        # create a Mac OS X mpkg distribution for Installer.app
  "egg_info",          # create a distribution's .egg-info directory
  "py2app",            # create a Mac OS X application or plugin from Python scripts
  "alias",             # define a shortcut to invoke one or more commands
  "easy_install",      # Find/get/install Python packages
  "bdist_egg"          # create an "egg" distribution
]

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
        if k not in sys.modules["__main__"].__all__:
            sys.modules["__main__"].__all__.append(k)
        setattr(sys.modules["__main__"],k,v)

def main():
    sys.modules["__main__"].__all__ = []
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

    kwargs = module_kwargs(sys.modules["__main__"])
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

    setuptools=False # check for setuptools
    # `python setup.py` args
    for arg in setuptools_args:
        if arg in sys.argv:
            setuptools=True
    # setup(name,**kwargs) kwargs
    for arg in setuptools_kwargs:
        if arg in kwargs and kwargs[arg] is not None:
            v = kwargs[arg]
            if v!=[] and v!="" and v!={} and v!=False:
                setuptools=True

    if sys.argv[-1]=="--manifest-only": # distutils only
        setuptools=False

    from distutils.core import setup # default
    if setuptools:
        try:
            from setuptools import setup
        except ImportError:
            print("setuptools not installed") # use distutils
    if len(sys.argv)==1: return
    setup(name=name,**kwargs)

#if __name__=="__main__":
main()
