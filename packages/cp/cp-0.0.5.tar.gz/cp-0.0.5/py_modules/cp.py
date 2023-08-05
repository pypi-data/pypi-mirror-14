#!/usr/bin/env python
from distutils import dir_util
import os
from os.path import *
import shutil
# me
from assert_exists import *
from public import *

@public
def cp(source,target,force=True):
    if isinstance(source,list): # list
        # copy files to dir
        targets = []
        for s in source:
            t = cp(s,target,force)
            targets.append(t)
        return targets
    assert_exists(source) # assert exists
    if not force and exists(target): return
    if source==target:
        return target
    if isfile(source) and isdir(target):
        # target is DIR
        target = join(target,basename(source))
    if isfile(source) or islink(source):
        if (exists(target) or lexists(target)) and isfile(source)!=isfile(target):
            os.unlink(target)
        shutil.copy(source,target)
    if isdir(source):
        # first create dirs
        if not exists(target):
            os.makedirs(target)
        dir_util.copy_tree(source,target)
    return target

if __name__=="__main__":
    dst = join(os.environ["HOME"],".cp_test")
    cp(__file__,dst)
    os.unlink(dst)
    import shutil
    cp(dirname(__file__),dst)
    shutil.rmtree(dst)
    try:
        cp("not-existing","dst") # IOError
    except IOError:
        pass


