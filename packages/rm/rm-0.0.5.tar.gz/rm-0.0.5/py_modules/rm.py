#!/usr/bin/env python
import os
import shutil
# me
from fullpath import *
from public import *


@public
def rm(path):
    """os.unlink and shutil.rmtree replacement"""
    if not path:
        return
    if isinstance(path, list):
        map(rm, path)
        return
    path = fullpath(path)
    if not os.path.exists(path):
        return
    if os.path.isfile(path) or os.path.islink(path):
        os.unlink(path)
        return
    if os.path.isdir(path):
        shutil.rmtree(path)


if __name__ == "__main__":
    import tempfile
    file = tempfile.mkstemp()[1]
    rm(file)  # file
    dir = tempfile.mkdtemp()
    rm(dir)  # dir
    from touch import *
    touch("~/testtest")
    rm("~/testtest")  # fullpath

    rm(None)  # nothing
    rm("not-existing")  # nothing
