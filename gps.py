#!/usr/bin/env python

"""gps.py: Handles GPS Serial Protocol."""

__author__ = "Javier Espasa"
__copyright__ = "Copyright 2015 ManglerBikes"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Javier Espasa"
__email__ = "whitegollum@gmail.com"
__status__ = "Development"


import serial, time, struct


class Gps:

    """Class initialization"""
    def __init__(self, serPort):

        """Global variables of data"""
        self.message = {'gpsTime':0,'gpsCoordLat':0,'gpsCoordLon':0,'dist':0,'gpsSpd':0,'gpsSats':0,'gpsAltitude':0}

        #self.temp = ()
        #self.temp2 = ()
        #self.elapsed = 0
        self.PRINT = True;

        self.ser = serial.Serial()
        self.ser.port = serPort
        self.ser.baudrate = 38400
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 0
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = False
        self.ser.writeTimeout = 2
        try:
            self.ser.open()
            if self.PRINT:
                print "Connecting GPS on "+self.ser.port
            
        except Exception, error:
            print "\n\nError opening "+self.ser.port+" port.\n"+str(error)+"\n\n"
            quit()


    """Function to receive a data packet from the board"""
    def closeSerial(self):
            self.ser.close()
            print "GPS port closed."



    """Function to....Parses GPS time and returns the time in seconds."""    
    def parse_time(time):
            return (float(time[:2])*3600)+(float(time[2:4])*60)+float(time[4:])
    



    """Function to receive a data packet from the board"""
    def getData(self):
        global last_coord
        line = ''
   
        start = time.time()
        buffer = ''
        while True:
          buffer += self.ser.read(self.ser.inWaiting())
          if '\n' in buffer:
            lines = buffer.split('\n')
            last_received = lines[-2]
            buffer = lines[-1]
            line = last_received.strip()
            break
        elapsed = time.time() - start
        
        self.ser.flushInput()
        self.ser.flushOutput()
        
        #parse_nmea
        gpsdata = line.split(',')
        if self.PRINT:
          #if gpsdata[0] == '$GPGGA':
            print line

        # Parse time
        curr_time = self.parse_time(gpsdata[1])
        message['gpsTime']=gpsdata[1]

        # Parse latitude
        lat = float(gpsdata[2][:2])+(float(gpsdata[2][2:])/60)
        if gpsdata[3] == 'S':
          lat = lat*-1
        message['gpsCoordLat']=lat

        # Parse longitude
        lon = float(gpsdata[4][:3])+(float(gpsdata[4][3:])/60)
        if gpsdata[5] == 'W':
          lon = lon*-1
        message['gpsCoordLon']=lon

        # Calculate distance
        curr_coord = (lat,lon)
        dist = calc_distance(curr_coord,last_coord)
        message['dist']=dist
         
        # Calculate speed
        spd = (dist/time_diff(curr_time,last_time))*3600
        last_time = curr_time
        message['gpsSpd']=spd
        last_coord = curr_coord

        # Print satellites
        sats = int(gpsdata[7])
        message['gpsSats']=sats

        # Print altitude
        altitude = float(gpsdata[9])
        message['gpsAltitude']=altitude


    
    
    
    """Function to...."""    
    def time_diff(now,before):
        try:
            print now
            print before
            if now < before:
              return (now+(24*60*60))-before
            else:
              return now-before
        except Exception, error:
            print error

