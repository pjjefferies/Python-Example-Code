# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 21:58:45 2015

"""

import os
from stat import *

def walktree(top, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname).st_mode
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            print("DIR:", pathname)
            walktree(pathname, callback)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print('Skipping %s' % pathname)

def visitfile(file):
    pass
    #print('visiting', file)

if __name__ == '__main__':
    rootFile = "C:\\Users\PaulJ\Data"
    walktree(rootFile, visitfile)