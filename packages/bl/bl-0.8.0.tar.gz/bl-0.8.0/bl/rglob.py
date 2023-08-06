
import os
from glob import glob, escape

def rglob(dirname, pattern, incl_dirs=False, sort=True):
    """recursive glob, gets all files that match the pattern within the directory tree"""
    fns = glob(os.path.join(dirname, pattern))
    dirs = [fn for fn 
            in [escape(os.path.join(dirname, fn)) 
                for fn in os.listdir(dirname)] 
            if os.path.isdir(fn)]
    if incl_dirs==True:
        fns += dirs
    for d in dirs:
        fns += rglob(d, pattern)
    if sort==True:
        fns.sort()
    return fns
