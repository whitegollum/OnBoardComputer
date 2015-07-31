
############################################## IMPORTS ##############################################
from config import *
from pygame import time
import threading

import netifaces
import pythonwifi.flags
from pythonwifi.iwlibs import Wireless, WirelessInfo, Iwrange, getNICnames, getWNICnames

import urllib2
from urllib2 import  URLError
import socket

from wifi import Cell, Scheme
import re
import textwrap

import wifi.subprocess_compat as subprocess
from wifi.utils import db2dbm
from wifi.exceptions import InterfaceError, ConnectionError





############################################## UI CALLBACKS ##############################################
#https://github.com/raphdg/netifaces

class network:
    def __init__(self, **kwargs):
        global continue_reading, config, dataMessage, wifilist
        
        self.continue_reading = True
        self.dataMessage = None #inputDataMessage
        self.config      = None #inputConfig
        self.wifilist    = None #inputWifiList
        self.interface   = "" #self.dataMessage['iface']
        self.ESSID       = ""
        self.ifaceUp     = False
        self.ip          = ""
        self.internet_on = False
        self.availableNetworks = None
        self.timeToScanNetworks = 100000
        self.timeToConnectNetworks = 10000
        self.lastUpdateScan  = time.get_ticks() - self.timeToScanNetworks
        self.lastUpdateConnect  = time.get_ticks() - self.timeToConnectNetworks
        self.testInternetConnection1 = "http://www.google.es"
        
        
        for key, value in kwargs.iteritems():
            if   key == 'continueReading': self.continue_reading = value
            if   key == 'interface': self.interface = value
            if   key == 'configVar': 
                self.config = value
                self.interface = self.config['net_iface']
                self.timeToScanNetworks = self.config['net_TimeToScanNetworks']
                self.timeToConnectNetworks = self.config['net_TimeToConnectNetworks']
                self.testInternetConnection1 = self.config['net_testInternetConnection1']
            if   key == 'wifilistVar': self.wifilist = value            
            if   key == 'dataMessageVar': self.dataMessage = value

        #init Network Manager thread
        if config['NetworkManagerThread'] == 1 :
            print "Launching NetworkManager Thread"
            threading.Thread(target=self.ThreadNetworkManager, args=()).start()



###########################################################################################################################
    def ThreadNetworkManager(self):
        while self.config['continueReading']:
            self.connectToNetworks()
            self.scanNetworks()
            #print ("-----network continue reading: " + str(config['continueReading']))
            #print ("-----network continue reading2: " + str(self.config['continueReading']))

    def scanNetworks(self):
        #solo actualizo cada x segundos
        if time.get_ticks() - self.lastUpdateScan > self.timeToScanNetworks:
            print "Scanning for Networks..."
            self.availableNetworks = Cell.all(self.interface)
            for cell in self.availableNetworks:
                print "-" + str(cell.ssid) + " " + str(cell.signal) + "/" + str(cell.quality) + ":" + str(cell.frequency) + " " + str(cell.channel) + " " + str(cell.address) + " " + str(cell.mode) + " ! " + ('protected' if cell.encrypted else 'unprotected') + ":" +  str(cell.encryption_type)
        
            self.lastUpdateScan = time.get_ticks()
        
    def connectToNetworks(self):
        #global dataMessage
        file = '/etc/network/interfaces'
        
        #solo actualizo cada x segundos
        if time.get_ticks() - self.lastUpdateConnect > self.timeToConnectNetworks:
            
             
            if self.getIP():
                self.dataMessage['ip'] = self.getIP()
                self.testInternetConnection()
            
            elif self.availableNetworks != None and len (self.availableNetworks) >0:
        
                # Primero miramos las Wifis que tenemos guardadas
                for cell in self.availableNetworks:
                    for wifi in self.wifilist:
                        if cell.ssid in self.wifilist.keys():
                            #compruebo que no tenga conexion ya
                            if self.dataMessage['ip'] == "":
                                scheme_class = Scheme.for_file(file)
                                # ensure that we have the adhoc utility scheme
                                try:
                                    adhoc_scheme = scheme_class(self.interface, 'adhoc')
                                    adhoc_scheme.save()
                                except AssertionError:
                                    pass
                                except IOError:
                                    assert False, "Can't write on {0!r}, do you have required privileges?".format(file)
                                
                                
                                scheme = scheme_class.for_cell(self.interface, 'adhoc', cell, passkey=self.wifilist[cell.ssid])
                                
                                try:
                                    print ("asociandose a:" + cell.ssid )
                                    scheme.activate()
                                    self.dataMessage['ssid'] = cell.ssid
                                    print ("ok asociado a " + self.dataMessage['ssid'])
                                    if self.getIP():
                                        self.testInternetConnection()

            
                                except ConnectionError:
                                    assert False, "Failed to connect to %s." % scheme.namescheme.activate()
                                    self.ifaceUp = False
                                    self.dataMessage['ssid'] = ""
                                    self.dataMessage['ip'] = ""
                                    self.dataMessage['internetReachable'] = 0
                                    self.dataMessage['iface'] = self.interface
                                    print ("fallo asocianodse a " + cell.ssid)
                            
                #si ya tengo conexion ni intento buscar
                if self.dataMessage['ip'] == "":
                    print ("Buscando redes open") 
                    for cell in self.availableNetworks:   
                        if cell.encrypted == False:
                            #si ya tengo conexion no me intento conectar
                            if self.dataMessage['ip'] == "":
                    
                                scheme_class = Scheme.for_file(file)
                                # ensure that we have the adhoc utility scheme
                                try:
                                    adhoc_scheme = scheme_class(self.interface, 'adhoc')
                                    adhoc_scheme.save()
                                except AssertionError:
                                    pass
                                except IOError:
                                    assert False, "Can't write on {0!r}, do you have required privileges?".format(file)
                                    
                                scheme = scheme_class.for_cell(self.interface, 'adhoc', cell)
                                
                                try:
                                    print ("asociandose a:" + cell.ssid )
                                    scheme.activate()
                                    self.dataMessage['ssid'] = cell.ssid
                                    print ("ok asociado a " + self.dataMessage['ssid'])
                                    if self.getIP():
                                        self.testInternetConnection()

            
                                except ConnectionError:
                                    assert False, "Failed to connect to %s." % scheme.namescheme.activate()
                                    self.ifaceUp = False
                                    self.dataMessage['ssid'] = ""
                                    self.dataMessage['ip'] = ""
                                    self.dataMessage['internetReachable'] = 0
                                    self.dataMessage['iface'] = self.interface
                                    print ("fallo asocianodse a " + cell.ssid)

            self.lastUpdateConnect  = time.get_ticks()
            

    def getIP(self):
        
        print ("identificando ips en interfaz:" + self.interface)
        if len(netifaces.ifaddresses (self.interface)) > 1:
            for link in netifaces.ifaddresses(self.interface)[netifaces.AF_INET]:
                self.ifaceUp = True
                self.ip = link['addr']
                self.dataMessage['ip'] = link['addr']
                print ("ip detectada " + self.dataMessage['ip'])
                return self.ip
                
        return None
    
    def testInternetConnection(self):
    
        try:
            response=urllib2.urlopen(self.testInternetConnection1,timeout=1)
            self.internet_on = True
            self.dataMessage['internetReachable'] = 1
            print ("ok conexion con internet ok")
            return True
        except URLError,e:
            self.internet_on = False
            self.dataMessage['internetReachable'] = 0
            print ("Nack conexion con internet falllida")
            return False


##############################################################


    def refreshNetwork2(self):
        """ Print the access points detected nearby.
    
        """
        # "Check if the interface could support scanning"
        try:
            wifi = Wireless(wifi.ifname)
            iwrange = Iwrange(self.interface)
        except IOError, (error_number, error_string):
            sys.stderr.write("%-8.16s  Interface doesn't support scanning.\n\n" % (
                                wifi.ifname))
        else:
            # "Check for Active Scan (scan with specific essid)"
            # "Check for last scan result (do not trigger scan)"
            # "Initiate Scanning"
            try:
                results = wifi.scan()
            except IOError, (error_number, error_string):
                if error_number != errno.EPERM:
                    sys.stderr.write(
                        "%-8.16s  Interface doesn't support scanning : %s\n\n" %
                        (wifi.ifname, error_string))
            else:
                if (len(results) == 0):
                    print "%-8.16s  No scan results" % (wifi.ifname, )
                else:
                    (num_channels, frequencies) = wifi.getChannelInfo()
                    print "%-8.16s  Scan completed :" % (wifi.ifname, )
                    index = 1
                    for ap in results:
                        print "          Cell %02d - Address: %s" % (index, ap.bssid)
                        print "                    ESSID:\"%s\"" % (ap.essid, )
                        print "                    Mode:%s" % (ap.mode, )
                        print "                    Frequency:%s (Channel %d)" % \
                            (wifi._formatFrequency(ap.frequency.getFrequency()),
                            frequencies.index(wifi._formatFrequency(
                                ap.frequency.getFrequency())) + 1)
                        if (ap.quality.updated & \
                                    pythonwifi.flags.IW_QUAL_QUAL_UPDATED):
                            quality_updated = "="
                        else:
                            quality_updated = ":"
                        if (ap.quality.updated & \
                                    pythonwifi.flags.IW_QUAL_LEVEL_UPDATED):
                            signal_updated = "="
                        else:
                            signal_updated = ":"
                        if (ap.quality.updated & \
                                    pythonwifi.flags.IW_QUAL_NOISE_UPDATED):
                            noise_updated = "="
                        else:
                            noise_updated = ":"
                        print "                    " + \
                            "Quality%c%s/%s  Signal level%c%s/%s  Noise level%c%s/%s" % \
                            (quality_updated,
                            ap.quality.quality,
                            wifi.getQualityMax().quality,
                            signal_updated,
                            ap.quality.getSignallevel(),
                            "100",
                            noise_updated,
                            ap.quality.getNoiselevel(),
                            "100")
                        # This code on encryption keys is very fragile
                        if (ap.encode.flags & pythonwifi.flags.IW_ENCODE_DISABLED):
                            key_status = "off"
                        else:
                            if (ap.encode.flags & pythonwifi.flags.IW_ENCODE_NOKEY):
                                if (ap.encode.length <= 0):
                                    key_status = "on"
                        print "                    Encryption key:%s" % (key_status, )
                        #compruebo que este en mi lista de ESSIDs y passwords
                        
                        #si encuentro me conecto
                        
                        index = index + 1
                    
                    ################# ahora busco APS sin cifrado ######################
                    for ap in results:
                        if (ap.encode.flags & pythonwifi.flags.IW_ENCODE_DISABLED):
                            key_status = "off"
                            #si encuentro alguno sin cifrado, me conecto
                            #codigo para conectarse
                            wifi.setAPaddr(ap)
                            
                            break
                        
                print


    def refreshNetwork(self):
        try:
            #solo actualizo cada 5 segundos
            if time.get_ticks() - self.lastUpdate > TimeToRefreshNetworks:
                #primero reseteo
                self.ESSID      = ""
                self.ifaceUp    = False
                self.ip         = ""
                self.internet_on = False
        
                #print "actualizo la red. " + self.interface
                self.lastUpdate = time.get_ticks()

                  
                #self.ip = netifaces.AF_INET in addr
                #print ("len interfaces = " + str(len(netifaces.ifaddresses (self.interface))))
                if len(netifaces.ifaddresses (self.interface)) > 1:
                    for link in netifaces.ifaddresses(self.interface)[netifaces.AF_INET]:
                        self.ifaceUp = True
                        self.ip = link['addr']
                        self.ESSID = Wireless(self.interface).getEssid()
                        #print "net:" + self.ESSID + self.ip
                        
                        #TODO: esto no funciona
                        response=urllib2.urlopen('http://74.125.228.100',timeout=1)
                        self.internet_on = True
                    
                
        except urllib2.URLError as err: 
            self.internet_on = False
        except socket.timeout as err: 
            self.internet_on = False
        except ValueError:
            self.internet_on = False
        
    def getESSID(self):
        return self.ESSID
    
    def getIfaceUp(self):
        return self.ifaceUp
    
    def getIp(self):
        return self.ip
    
    def getInterface(self):
        return self.interface
    
    def getInternet_on(self):
        return self.internet_on
       
