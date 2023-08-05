#!/usr/bin/env python

import os
from optparse import OptionParser

os.environ['DJANGO_SETTINGS_MODULE'] = 'rmap.settings'
import django
django.setup()

import rmap.rmap_core

def parse_args():
    p = OptionParser(usage='%prog file.jpg...',
           description='adjusts timestamps in EXIF metadata')
    options, args = p.parse_args()
    if len(args) < 1:
        p.error('not enough arguments')
    return  args


if __name__ == '__main__':

    files = parse_args()

    for file in files:

        photo_file = open(file,"r")
        body = photo_file.read()
        photo_file.close()

        rmap.rmap_core.send2amqp(body=body,user=u"pat1",password="1password",host="rmap.cc",exchange="photo",routing_key="photo")

