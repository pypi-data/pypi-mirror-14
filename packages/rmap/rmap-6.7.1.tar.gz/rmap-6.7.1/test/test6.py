from datetime import datetime

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'rmap.settings'
import django
django.setup()

from rmap.rmapmqtt import rmapmqtt

ident="test"
lon=10.0
lat=44.0
value=100
dt=datetime.utcnow().replace(microsecond=0)

datavar={"B20003":{"t": dt,"v": str(value)}}

mqtt=rmapmqtt(ident=ident,lon=lon,lat=lat,network="rmap",host="rmap.cc",port=1883,prefix="test",maintprefix="test")
mqtt.data(timerange="254,0,0",level="1,-,-,-",datavar=datavar)
mqtt.disconnect()

