#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
"""
Utility to adjust the EXIF
"""

import sys
sys.path.insert(0, "..")
from datetime import timedelta, datetime
from optparse import OptionParser
import io
import rmap.exifutils

def parse_args():
    p = OptionParser(usage='%prog file.jpg...',
           description='adjusts timestamps in EXIF metadata')
    options, args = p.parse_args()
    if len(args) < 1:
        p.error('not enough arguments')
    return  args

def main():
    files = parse_args()

    for fname in files:

        with open(fname) as file:
            data = file.read()

            new_data=rmap.exifutils.setgeoimage(data,lat=44.,lon=11.,imagedescription="pat1",usercomment="prova")

            with open(fname+"new","w") as file:
                file.write(new_data)

    return 0

if __name__ == "__main__":
    sys.exit(main())
