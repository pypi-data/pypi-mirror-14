#!/usr/bin/env python

"""
Utility to adjust the EXIF timestamps in JPEG files by a constant offset.

Requires Benno's pexif library: http://code.google.com/p/pexif/

-- Andrew Baumann <andrewb@inf.ethz.ch>, 20080716
"""

import sys
from rmap.pexif import JpegFile
from datetime import timedelta, datetime
from optparse import OptionParser

DATETIME_EMBEDDED_TAGS = ["DateTimeOriginal", "DateTimeDigitized"]
TIME_FORMAT = '%Y:%m:%d %H:%M:%S'

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
        try:
            jf = JpegFile.fromFile(fname,mode="rw")
        except (IOError, JpegFile.InvalidFile):
            type, value, traceback = sys.exc_info()
            print >> sys.stderr, "Error reading %s:" % fname, value
            return 1

        exif = jf.get_exif()
        if exif:
            primary = exif.get_primary()
        if exif is None or primary is None:
            print >> sys.stderr, "%s has no EXIF tag, skipping" % fname
            continue

        try:
            print primary.DateTime
        except:
            print "DateTime not present"

        primary.DateTime = datetime.utcnow().strftime("%Y:%m:%d %H:%M:%S")
        print primary.DateTime
        primary.ImageDescription ="ciao ciao"
        primary.ExtendedEXIF.UserComment = chr(0x55)+chr(0x4E)+chr(0x49)+chr(0x43)+chr(0x4F)+chr(0x44)+chr(0x45)+chr(0x00)+"ciao bello come stai"
        #embedded = img.exif.primary.__getattr__("ExtendedEXIF")
        #embedded["UserComment"] = chr(0x55)+chr(0x4E)+chr(0x49)+chr(0x43)+chr(0x4F)+chr(0x44)+chr(0x45)+chr(0x00)+"ciao bello come te la passi"
        try:
            jf.writeFile(fname)
        except IOError:
            type, value, traceback = sys.exc_info()
            print >> sys.stderr, "Error saving %s:" % fname, value
            return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
