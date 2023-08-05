#!/usr/bin/python

# Copyright (c) 2013 Paolo Patruno <p.patruno@iperbole.bologna.it>
#                    Emanuele Di Giacomo <edigiacomo@arpa.emr.it>
# This program is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation; either version 2 of the License, or 
# (at your option) any later version. 
# 
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details. 
# 
# You should have received a copy of the GNU General Public License 
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA 

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'rmap.settings'
import django
django.setup()

from rmap.rmapmqtt import rmapmqtt
import time
from datetime import datetime, timedelta

def main():

    django.utils.translation.activate("it")

    import random

    lon=11.36992
    lat=44.48906
    host="rmap.cc"

    anavar={
        "B07030":{"v": "400"}
    }

    try:
        rmap=rmapmqtt(lon=lon,lat=lat,host=host)
        rmap.loop_start()

        rmap.ana(anavar)
        time.sleep(5)
        #rmap.loop()

        reptime=datetime.now()
        endtime=reptime+timedelta(days=1)
    
        while reptime <= endtime:

            print "connect status: ",rmap.connected
            timerange="254,0,0"               # dati istantanei
            level="103,2000,-,-"              # 2m dal suolo
            value=random.randint(25315,30000) # tempertaure in cent K
            datavar={"B12101":
            {
                "t": reptime,
                "v": str(value),
                "a": {
                    "B33194": "90",           # attributi di qualita' del dato
                    "B33195": "85"
                }   
            }}

            rmap.data(timerange,level,datavar)
            time.sleep(5)
            #rmap.loop()
            reptime=datetime.now()

        rmap.disconnect()
        rmap.loop_stop()
        print "work is done OK"

    except:
        print "terminated with error"
        raise

if __name__ == '__main__':
    main()  # (this code was run as script)

