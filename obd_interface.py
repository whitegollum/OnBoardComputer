#!/usr/bin/env python

import obd_io
import serial
import platform
import obd_sensors
from datetime import datetime
import time
import getpass


from obd_utils import scanSerial



class OBD_Interface():


    def __init__(self, log_items):

        self.path = "/home/pi/onboardComp/logs/"
        self.port = None
        self.sensorlist = []
        self.gear_ratios = [34/13, 39/21, 36/23, 27/20, 26/21, 25/22]
        self.results = {}
        
        #localtime = time.localtime(time.time())
        for item in log_items:
            self.add_log_item(item)
            
            
        #filename = self.path+"obd-"+str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2])+"-"+str(localtime[3])+"-"+str(localtime[4])+"-"+str(localtime[5])+".log"
        #self.log_file = open(filename, "w", 128)
        #self.log_file.write("Time,RPM,MPH,Throttle,Load,Fuel Status\n");

    def connect(self):
        self.port = obd_io.OBDPortr('/dev/ttyUSB0', None, 2, 2)
        if(self.port.State == 0):
            self.port.close()
            self.port = None    
    
        #portnames = scanSerial()
        #print portnames
        #for port in portnames:
        #    self.port = obd_io.OBDPort(port, None, 2, 2)
        #    if(self.port.State == 0):
        #        self.port.close()
        #        self.port = None
        #    else:
        #        break

        if(self.port):
            print "Connected to "+self.port.port.name
            
    def is_connected(self):
        return self.port
        
    def add_log_item(self, item):
        for index, e in enumerate(obd_sensors.SENSORS):
            #print "trying item: "+e.name
            if(item == e.shortname):
                self.sensorlist.append(index)
                print "Logging item: "+e.name
                break
    
    def get_value(self, item):
    	if(self.port is None):
            return None
        for index in self.sensorlist:
            (name, value, unit) = self.port.sensor(index)
            if (name == item):
                return value
                break

            
    def get_data(self):
        localtime = datetime.now()
        #current_time = str(localtime.hour)+":"+str(localtime.minute)+":"+str(localtime.second)
        #log_string = current_time +  " - "

    	if(self.port is None):
            return None
        
        for index in self.sensorlist:
            (name, value, unit) = self.port.sensor(index)
            #log_string = log_string + ","+str(name)+"="+str(value)+str(unit)
            self.results[obd_sensors.SENSORS[index].shortname] = value;

        #gear = self.calculate_gear(self.results["rpm"], self.results["speed"])
        
        #log_string = log_string + "," + str(gear)
        #self.log_file.write(log_string+"\n")
        #print log_stringh


            
    def calculate_gear(self, rpm, speed):
        if speed == "" or speed == 0 or speed == "NODATA":
            return 0
        if rpm == "" or rpm == 0 or rpm == "NODATA":
            return 0

        rps = rpm/60
        mps = (speed*1.609*1000)/3600
        
        primary_gear = 85/46 #street triple
        final_drive  = 47/16
        
        tyre_circumference = 1.978 #meters

        current_gear_ratio = (rps*tyre_circumference)/(mps*primary_gear*final_drive)
        
        #print current_gear_ratio
        gear = min((abs(current_gear_ratio - i), i) for i in self.gear_ratios)[1] 
        return gear
        


