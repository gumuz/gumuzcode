# -*- coding: Cp1252 -*-
"""
Project         :   Dupes

Author          :   Guyon Morée <gumuz@looze.net>
Createdate      :   30 March 2005
Filename        :   dupes.py

Description     :   Find duplicates using MD5 sums.

"""

#--- Standard lib imports
import sys
import os
import md5
from pprint import pprint
from path import path


#--- Custom lib imports


#--- Module functions

def get_hash(filename):
    """ Return md5 hash """
    f = open(filename,'rb')
    hsh = md5.new()
    while 1:
        data = f.read(2048)
        if not data: break
        hsh.update(data)
    f.close()
    return hsh.hexdigest()



#--- MAIN - this only runs if the module was *not* imported
if __name__ == '__main__':
    #--- Check for command line arguments
    try:
        # try commandline arg
        currdir = path(sys.argv[1])
    except IndexError:
        # no args use default
        currdir = path(".")

    # check if dir is valid
    if not currdir.isdir():
        print "ERROR: ", currdir, "is not a valid path"
        sys.exit()

    #--- Loop through files for simple size-check
    sizemap = {}
    for f in currdir.files():
        size = f.size
        if size in sizemap:
            sizemap[size].append(f)
        else:
            sizemap[size] = [f]

    #--- collect size dupes
    sizedupes = {}
    for size, files in sizemap.items():
        if len(files) > 1:
            sizedupes[size] = files

    #--- Check size dupes with MD5 hash
    hashmap = {}
    for size, files in sizedupes.items():
        for f in files:
            md5hash = get_hash(f)
            if md5hash in hashmap:
                hashmap[md5hash].append(f)
            else:
                hashmap[md5hash] = [f]

    #--- Collect real dupes
    realdupes = {}
    for md5hash, files in hashmap.items():
        if len(files) > 1:
            realdupes[md5hash] = files

    #--- show dupes
    print "Duplicates found in:", currdir
    print
    for h, files in realdupes.items():
        print "#", h
        for f in files:
            print " -> %s (%s bytes)" % (f,f.size)
        print

