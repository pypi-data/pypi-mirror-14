
#!/usr/bin/env python

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'rmap.settings'
import django
django.setup()

import rmap.rmap_core

if __name__ == '__main__':

    #rmap.rmap_core.configdb()

    rmap.rmap_core.receivejsonfromamqp(user=u"pat1",password="1password",host="rmap.cc",queue="configuration")


