# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 21:58:45 2015

"""

import os, string
from stat import *
from jsonReadWriteFile import *


def walktree(top):
    listOfDirectoriesFound = {}
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        try:
            mode = os.stat(pathname).st_mode
            if S_ISDIR(mode):
                # It's a directory, recurse into it
                #print("DIR:", pathname)
                dirListReturned = walktree(pathname)
                if dirListReturned == None:
                    listOfDirectoriesFound[f] = "No Subdirectories"
                else:
                    listOfDirectoriesFound[f] = dirListReturned
            elif S_ISREG(mode):
                #It's a file, ignore for now
                #callback(pathname)
                #listOfDirectoriesFound.append(pathname)     #Use if saving filenames too
                #print("File", f + ". Ignore for now")
                pass
            else:
                # Unknown file type, print a message
                print('Skipping %s' % pathname)
        except(FileNotFoundError):
            print("File not found:", pathname + ". Skipping")
    if len(listOfDirectoriesFound) == 0:
        return None
    else:
        return listOfDirectoriesFound

def visitfile(file):
    pass
    #print('visiting', file)

if __name__ == '__main__':
    rootFile = "C:\\Users\\PaulJ\\Data\\tmp"
    tempSaveFile = "C:\\Users\\PaulJ\\Data\\Computers & Internet\\Python\\Example Code\\tempListOfDirs.json"
    structuredListOfDirectories = walktree(rootFile)
    try:
        write_json(tempSaveFile, structuredListOfDirectories)
    except OSError:
        print("Unable to write local databasefile")
