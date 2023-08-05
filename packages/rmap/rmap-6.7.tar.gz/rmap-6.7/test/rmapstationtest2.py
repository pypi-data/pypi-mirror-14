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

from rmap.rmapstation import station
import time
from datetime import datetime, timedelta
import time

def main():

    django.utils.translation.activate("it")

    mystation=station(slug="rmap-app",boardslug="rmap_pc")

    #mystation.configurestation(transport="tcpip")

    mystation.starttransport()
    time.sleep(3)
    
    mystation.sensorssetup()
    mystation.getdata()
    print mystation.anavarlist
    print mystation.datavarlist

    mystation.anavarlist=[]
    mystation.datavarlist=[]

    mystation.on_stop()

if __name__ == '__main__':
    main()  # (this code was run as script)

