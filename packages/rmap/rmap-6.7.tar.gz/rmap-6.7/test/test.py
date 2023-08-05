#!/usr/bin/env python

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'rmap.settings'
import django
django.setup()

import rmap.rmap_core

if __name__ == '__main__':

#    rmap.rmap_core.configdb(username="pat1",password="1password",
#             station="home",lat=0,lon=0,constantdata=(),
#             mqttusername="pat1",
#             mqttpassword="1password",
#             mqttserver="rmap.cc",
#             mqttsamplerate=5,
#             bluetoothname="hc05",
#             amqpusername="pat1",
#             amqppassword="1password",
#             amqpserver="rmap.cc",
#             queue="rmap",
#             exchange="rmap")

    rmap.rmap_core.sendjson2amqp(station="passive",user=u"pat1",password="1password",host="rmap.cc",exchange="configuration")
