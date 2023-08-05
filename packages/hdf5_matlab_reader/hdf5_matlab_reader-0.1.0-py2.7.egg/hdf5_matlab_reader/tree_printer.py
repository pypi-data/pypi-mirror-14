#!/usr/bin/env python

import sys
import h5py

def disp2(n,o):
    print n,o
    print o.attrs.items()

def tree(f):
    h5_file = h5py.File(f, 'r')
    h5_file.visititems(disp2)


if __name__ == '__main__':
    tree(sys.argv[1])
