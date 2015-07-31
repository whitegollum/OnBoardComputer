#!/usr/bin/env python

import obd_io
import serial
import platform
import obd_sensors
from datetime import datetime
import time

from obd_utils import scanSerial

class OBD_Scanner():
    def __init__(self, path, log_items):
        self.port = None
        self.sensorlist = []
        
        
        
    def connect(self):
        portnames = scanSerial()
        #portnames = ['COM10']
        print portnames
        for port in portnames:
            self.port = obd_io.OBDPort(port, None, 2, 2)
            if(self.port.State == 0):
                self.port.close()
                self.port = None
            else:
                break

        if(self.port):
            print "Connected to "+self.port.port.name
            
    def is_connected(self):
        return self.port
        
    def add_log_item(self, item):
        for index, e in enumerate(obd_sensors.SENSORS):
            if(item == e.shortname):
                self.sensorlist.append(index)
                print "Logging item: "+e.name
                break
            
            
    def scan_PID(self, command):
        if(self.port is None):
            return None
        self.port.send_command(command)
        ready = self.port.get_result()
        print command + ": " + ready
        
            
            
o = OBD_Scanner('/home/pi/onboardComp/logs/', logitems)
o.connect()
if not o.is_connected():
    print "Not connected"
print "Scanning started"
        
o.scan_PID("0100")
o.scan_PID("0101")
o.scan_PID("0102")
o.scan_PID("0103")
o.scan_PID("0104")
o.scan_PID("0105")
o.scan_PID("0106")
o.scan_PID("0107")
o.scan_PID("0108")
o.scan_PID("0109")
o.scan_PID("010A")
o.scan_PID("010B")
o.scan_PID("010C")
o.scan_PID("010D")
o.scan_PID("010E")
o.scan_PID("010F")
o.scan_PID("0110")
o.scan_PID("0111")

