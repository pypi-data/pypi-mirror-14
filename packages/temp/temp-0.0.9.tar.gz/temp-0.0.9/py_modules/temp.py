#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tempfile import *
from public import *

public(gettempdir)

@public
def tempfile():
    """Create temp file"""
    return mkstemp()[1]

@public
def tempdir():
    """create temp dir"""
    return mkdtemp()

if __name__=="__main__":
	print(gettempdir())
	print(tempfile())
	print(tempdir())
