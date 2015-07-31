# http://www.adafruit.com/products/998  (Raspberry Pi Model B)
# http://www.adafruit.com/products/1601 (PiTFT Mini Kit)
#
# onboardBikeComputer.py by WhiteGollum (whitegollum@gmail.com)
# BSD license, all text above must be included in any redistribution.
#

#Diseno general. Part List:
#- RaspBerry Pi B+
#- Adafruit PiTFT
#- 2 x Metal PushButtons - Momentary (http://www.amazon.es/gp/product/B00O30FBLQ?psc=1&redirect=true&ref_=oh_aui_detailpage_o00_s00) 9,90 Eur
#- 1 x Metal Pushbutton - Latching (16mm, Red) (http://www.amazon.es/gp/product/B00LHOGMD2?psc=1&redirect=true&ref_=oh_aui_detailpage_o00_s03) 9,90 Eur
#- 1 x Adafruit 0.56 4-Digit 7-Segment Display w/I2C Backpack - Blue (http://www.amazon.es/gp/product/B00DHK1E1O?psc=1&redirect=true&ref_=oh_aui_detailpage_o00_s01) 15,90 Eur
#- 2 x Adafruit Bicolor LED Square Pixel Matrix with I2C Backpack (http://www.adafruit.com/product/902) 15,95 $
#- 1 x Cable GPIO (http://www.amazon.es/GPIO-Ribbon-Cable-Raspberry-Model/dp/B00MIM358C/ref=sr_1_19?s=electronics&ie=UTF8&qid=1422180533&sr=1-19) 9,90 Eur
#- GPIO Ribbon Cable for Raspberry Pi (http://www.amazon.es/GPIO-Ribbon-Cable-Raspberry-Pi/dp/B00MIM2UXI/ref=sr_1_26?ie=UTF8&qid=1422181644&sr=8-26&keywords=gpio+raspberry+pi) 9,90 Eur
#- 1 x NeoPixel Ring - 16 x WS2812 5050 RGB LED with Integrated Drivers (http://www.amazon.es/NeoPixel-Ring-WS2812-Integrated-Drivers/dp/B00KT4H3MK/ref=sr_1_40?s=electronics&ie=UTF8&qid=1422180634&sr=1-40) 12 Eur
#- 1 x PiTFT Mini Kit - 320x240 2.8 TFT+ Capacitive Touchscreen (http://www.amazon.es/PiTFT-Mini-Kit-Capacitive-Touchscreen/dp/B00MUJ2IAY/ref=sr_1_44?s=electronics&ie=UTF8&qid=1422180634&sr=1-44) 59 Eur
#- 1 x PowerBoost 500 Charger - Rechargeable 5V Lipo USB (http://www.amazon.es/PowerBoost-500-Charger-Rechargeable-Boost/dp/B00PY2YTVU/ref=lh_ni_t?ie=UTF8&psc=1&smid=A3VZWH9QVI2V2M) 14,90 Eur
#- 1 x Cargador USB de telefonos apto para motocicletas(http://www.amazon.es/gp/product/B00AMDI34U/ref=ox_sc_act_title_2?ie=UTF8&psc=1&smid=A19RHJWCKQI8PY) 19,99 Eur

#obd2: para bmw: http://www.carsets.co.uk/wholesale/bmw-10pin-icom-d-cable.html
# http://www.cardiag.co.uk/bmw-10pin-cable-for-icom.html
# http://www.f650gs.crossroadz.com.au/Diagnostics/DiagsCable.pdf

#- play audio: os.system('mpg321 --quiet /home/pi/GPSLogger/MP3/logging_started.mp3 &')

#inicializacion automatica
#http://www.megaleecher.net/Raspberry_Pi_Autostart#axzz3QXscsgSz

# gps:
# https://github.com/laf/GPSLogger/blob/master/README.md


# ToDo.Investigar:
# http://www.amazon.es/Waterproof-DS18B20-Digital-temperature-sensor/dp/B00LB76KSM/ref=sr_1_32?s=electronics&ie=UTF8&qid=1422180634&sr=1-32
# http://en.wikipedia.org/wiki/OBD-II_PIDs


#
# Nota a tener en cuenta: la alimentacion debe de tener algun tipo de BEC y recarga de bateria de emergencia
#			http://www.repairhub.co.uk/content/resources/raspberry-pi-battery-backup
#			http://www.ebay.ie/itm/191133345539
#			http://raspberrypi.stackexchange.com/questions/1360/how-do-i-build-a-ups-like-battery-backup-system
#			http://www.mini-box.com/picoUPS-100-12V-DC-micro-UPS-system-battery-backup-system
#	-->		http://www.batterymart.com/p-6v-0_5ah-sealed-lead-acid-power-sonic-battery.html
#           http://www.adafruit.com/product/2078 pero para Arduino
#			
#			http://www.adafruit.com/product/1944 para USB normal. Faltaria el estabilizador de tension a salida USB.
#			http://www.ebay.com/bhp/motorcycle-usb-charger
#			PowerBoost 500 Charger - Rechargeable 5V Lipo USB
#
# Bucle principal:
#  recopila datos de ODB2: http://www.cowfishstudios.com/blog/obd-pi-raspberry-pi-displaying-car-diagnostics-obd-ii-data-on-an-aftermarket-head-unit
#  recopila datos de wii nunchuck: http://computers.tutsplus.com/tutorials/using-a-wii-nunchuck-to-control-python-turtle--cms-20984  
#  recopila datos de GPS: http://community.wolfram.com/groups/-/m/t/157461
#                         http://fuenteabierta.teubi.co/2013/05/velocimetro-digital-con-raspberry-pi-y.html
#  Calcula alertas
#  guarda log a fichero
#  comprueba si hay conexion a internet y en caso contrario, envia log cada hora
#  Imprime el screen actual
#
# Menu principal:
#  Dos ventanas informativas customizables y tres botones superiores
#  si se pulsa sobre una ventana de datos, esta pasa a la siguiente opcion
#   
#  3D: http://nccastaff.bournemouth.ac.uk/jmacey/GraphicsLib/piNGL/index.html
#  

############################################## IMPORTS ##############################################
from config import *

import atexit
import cPickle as pickle
import errno

import io
import pygame
import threading
import signal
import sys
import time
import Image
import ImageDraw
import serial
import math




from pygame.locals import *
from subprocess import call  
from time import sleep
from datetime import datetime, timedelta

import wiringpi2 as wiringpi
#to install: http://raspi.tv/how-to-install-wiringpi2-for-python-on-the-raspberry-pi#install

#from obd_interface import OBD_Interface
import obd_sensors
import obd_io
from gps import *
from gisFunctions import haversine
from led import ledArrayThread
from Adafruit_LED_Backpack import BicolorMatrix8x8





import display
from display import *

import network





############################################## UI CALLBACKS ##############################################
def getAllData():
	# get OBD Data
	# http://www.cowfishstudios.com/blog/obd-pi-raspberry-pi-displaying-car-diagnostics-obd-ii-data-on-an-aftermarket-head-unit
	demotest = ""	




def calc_inclinacion(offsetInclinacion):
  #global inclinacion
  #global offsetInclinacion
  global dataMessage
  
  return 0

def calc_distance(lat1, lon1):
	# la funcion haversine esta en gisFunctions. hacer import
	global lon2, lat2
	if lon1 <> 0 and lat1 <> 0 and lon2 <> 0 and lat2 <> 0 :
		distance = haversine(lon1, lat1, lon2, lat2)
		if distance < 3 :
			distance = 0
	else :
		distance = 0
	lat2 = lat1
	lon2 = lon1

	return distance


################################### array de leds ##########################
def Prepare_ledDrawing():
	global led
	
	#init Led Array
	led = ledArrayThread()

def ThreadLedDrawing():
	global continue_reading, config
	
	while config['continueReading']:
		ledDrawing()

def ledDrawing():
	global dataMessage, led
	
	
	led.resetLeds()
	gauge = dataMessage['gpsSats']
	if gauge > 8: gauge = 8
	led.drawGauge(1,gauge,BicolorMatrix8x8.YELLOW,1) 							# Satellites: array de leds
	led.drawGauge(2,gauge,BicolorMatrix8x8.YELLOW,1) 							# Satellites: array de leds
		
	if ( getDataMessage('rpm') == 0 ): rate = 0.0
	else: rate = getDataMessage('rpm')/6000.0
	gauge = int(float(7)*rate)
	led.drawGauge(3,gauge,BicolorMatrix8x8.GREEN,1)							# RPM: array de leds 
	led.drawGauge(4,gauge,BicolorMatrix8x8.GREEN,1)
	#print ("array led RPM: " + str(dataMessage['obdRpm']) + "/6000.0 = " + str(rate) + " : " + str(gauge))
	
	if ( getDataMessage('speed') == 0 ): rate = 0.0
	else: rate = getDataMessage('speed')/250.0
	gauge = int(float(7)*rate)
	led.drawGauge(1,gauge,BicolorMatrix8x8.RED,2)							# SPD: array de leds 
	led.drawGauge(2,gauge,BicolorMatrix8x8.RED,2)							# RPM: array de leds 
	#print ("array led SPD: " + str(dataMessage['obdSpeed']) + "/250.0 = " + str(rate) + " : " + str(gauge))
	
	if ( getDataMessage('throttle_pos') == 0 ): rate = 0.0
	else: rate = getDataMessage('throttle_pos')/100.0
	gauge = int(float(7)*rate)
	led.drawGauge(3,gauge,BicolorMatrix8x8.GREEN,2)							# THR: array de leds 
	led.drawGauge(4,gauge,BicolorMatrix8x8.GREEN,2)							# THR: array de leds 
	
	led.drawDisplays()
	#  print "Led thread stopped"  



def Prepare_GpsRead():
  global gpsd

  gpsd = gps()
  #gpsd = Gps("localhost", "2947")
  #gpsd.stream(WATCH_ENABLE)
  #gpsd = gps(mode=WATCH_ENABLE) 
  #gpsd = gps(mode=WATCH_NEWSTYLE)
  #gpsd.stream(WATCH_NMEA)
  gpsd.stream(WATCH_ENABLE | WATCH_NEWSTYLE)
  #gpsd = gps(mode=WATCH_ENABLE)

def ThreadGpsRead():
	global continue_reading, config
	
	while config['continueReading']:
		GpsRead()
		
def GpsRead():
	global dataMessage, gpsd
  
	#time.sleep(0.2)
	gpsd.next()						#this will continue to loop and grab EACH set of gpsd info to clear the buffer
	#print gpsd

	if gpsd.fix:
		dataMessage['gpsFix']=    	gpsd.status
	else:
		dataMessage['gpsFix']=    	"0"
		dataMessage['gpsCoordLat']=		gpsd.fix.latitude
		dataMessage['gpsCoordLon']=		gpsd.fix.longitude
		dataMessage['gpsEPS']=			gpsd.fix.eps
		dataMessage['gpsEPX']=			gpsd.fix.epx
		dataMessage['gpsEPV']=			gpsd.fix.epv
		dataMessage['gpsEPT']=			gpsd.fix.ept
		dataMessage['gpsTrack']=		gpsd.fix.track
		dataMessage['gpsMode']=			gpsd.fix.mode
		dataMessage['gpsClimb']=		gpsd.fix.climb
		dataMessage['gpsAltitude']=		gpsd.fix.altitude
		dataMessage['dist']=	   		calc_distance(gpsd.fix.latitude, gpsd.fix.longitude)
		dataMessage['gpsSpd']=	 		gpsd.fix.speed
		
	dataMessage['gpsTimeUTC']=    	gpsd.utc
	dataMessage['gpsSats']=    		gpsd.satellites_used #len(gpsd.satellites)
	#print dataMessage['gpsTimeUTC']
	#print dataMessage['gpsSats']
	#print "GPS: " + str(gpsd.satellites_used) + "/" + str(len(gpsd.satellites))

	# tiempo local
	localtime = datetime.now()  
	current_time = str(localtime.hour)+":"+str(localtime.minute)+":"+str(localtime.second)
	dataMessage['localTime'] = localtime	
    
    
	#print "GPS thread iteration... Sats:" + str(len(gpsd.satellites)) + " Mode:" + str(gpsd.fix.mode)
	#print "GPS thread stopped"  


def Prepare_ObdRead():
	global OBD_port, sensorlist

  	OBD_port = None
  	sensorlist = []
  	serialPort = '/dev/ttyUSB0'
  	log_items = ["rpm", "speed", "throttle_pos", "load", "fuel_status"]

	#conecto el interfaz
	OBD_port = obd_io.OBDPort(serialPort, None, 2, 2)
	if(OBD_port.State == 0):
		OBD_port.close()
		OBD_port = None 
		print "OBD Not connected"

 	#anado los elementos a monitorizar
 	print "HardCoded Sensor List: "
  	for item in log_items:
		addSensor(item)
	if config['OBD2AutoDetect'] == 1 :
		rescanSensorlist()   

def addSensor(item):
	global sensorlist, dataMessage

	sensorIsIdentified = False
	for index, e in enumerate(obd_sensors.SENSORS):
		if(item == e.shortname):
			sensorlist.append(index)
			#anado la entrada a cero ya que aun no la he leido
			dataMessage[item] = 0
			sensorIsIdentified = True
			print "   Logging item: "+e.name
			break
	if sensorIsIdentified == False:
		print "Sensor not identified in Database: "+e.name

	            
def rescanSensorlist():
	global OBD_port, sensorlist
	
	print "Rescanning Sensor List: "
	if OBD_port and OBD_port.State:
		supp = OBD_port.sensor(0)[1]
      
		# loop through PIDs binary
		for i in range(0, len(supp)):
			if supp[i] == "1":
				#detectedSensor =  obd_sensors.SENSORS[i+1].shortname
				addSensor(obd_sensors.SENSORS[i+1].shortname)
				   

def ThreadObdRead():
	global continue_reading, config
	
	while config['continueReading']:
		ObdRead()

def ObdRead():
  global continue_reading, dataMessage, OBD_port, sensorlist

  #while continue_reading:
  if OBD_port and OBD_port.State:
  
      #time.sleep(0.5)
      # Adquisicion de datos
      #results = {}
      for index in sensorlist:
         (name, value, unit) = OBD_port.sensor(index)
         if value == 'NODATA': value = 0
         #results[obd_sensors.SENSORS[index].shortname] = value
         dataMessage[obd_sensors.SENSORS[index].shortname] = value
   
#    print "OBD Port closed."

# https://github.com/arcoslab/python-multiwii/blob/master/docs/multiwii_serial_protocol
# https://github.com/martinohanlon/pyobd/blob/master/obd_recorder.py


def Prepare_dataLogging():
  # sustituir esto por SQLData y Upload to website
  # https://github.com/laf/GPSLogger/blob/master/checkData.py
  global continue_reading, dataMessage, dataLoggingFilename, log_file
  
  log_file = open(dataLoggingFilename, "a", 128)
  log_string = "# Logging:"
  for index in dataMessage:
        log_string = log_string + str(index) + ";"
  log_file.write(log_string+"\n")
  print log_string
  

def ThreadDataLogging():
	global continue_reading, config
	
	while config['continueReading']:
		dataLogging()
		
def dataLogging():
  global dataMessage, log_file, buttons, log_string, lastTimeLog

  if (pygame.time.get_ticks() - lastTimeLog > 5000):
     log_string = ""
     for index in dataMessage:
        log_string = log_string + ";" + str(dataMessage[index])
     log_file.write(log_string+"\n") 
     log_file.flush() # make sure it actually gets written out
     #time.sleep(10)  
     lastTimeLog = pygame.time.get_ticks()
     
     print log_string
  #print "Logging thread stoped"

def ThreadReadInputButtons():
	global continue_reading, config
	
	while config['continueReading']:
		ReadInputButtons()
		
def ReadInputButtons():
  global waitingForNewFrame, dataMessage, lastTime
  
  # Process all inputs- Comportamiento programado de los botones fisicos
  if checkButtons() == 4 and waitingForNewFrame == False:
    print 'switch 4'
    ChangeDatafeedCallback(0)
    dataMessage['obdSpeed']=0.0
    dataMessage['obdRpm']=0.0
    waitingForNewFrame = True
    lastTime = pygame.time.get_ticks()

  if checkButtons() == 3 and waitingForNewFrame == False:
    print 'switch 3'
    ChangeDatafeedCallback(1)
    waitingForNewFrame = True
    lastTime = pygame.time.get_ticks()
    
  
  if checkButtons() == 2 and waitingForNewFrame == False:
    print 'switch 2'
    #shutdown()
    dataMessage['obdRpm']=3000.0
    dataMessage['obdSpeed']=110.0
    #ChangeDatafeedCallback(0)
    #ChangeDatafeedCallback(1)
    waitingForNewFrame = True
    lastTime = pygame.time.get_ticks()

  # Process touchscreen input
  for event in pygame.event.get():
      if(event.type is MOUSEBUTTONDOWN):
        pos = pygame.mouse.get_pos()
        for b in buttons[screenMode]:
          if b.selected(pos): break

  #determinar si ha pasado el tiempo suficiente para considerar nuesvos eventos de pulsacion como validos
  if waitingForNewFrame == True:
    if pygame.time.get_ticks() - lastTime > 1000:
  	  print "restauro waiting forNewFrame"
  	  waitingForNewFrame = False


  

		


  
# ---------------------------------------------------------------------

def checkButtons():
    global switch_1,switch_2, switch_3, switch_4

    sw1 = not wiringpi.digitalRead(switch_1) # Read switch
    if sw1: 
      return 1
    sw2 = not wiringpi.digitalRead(switch_2) # Read switch
    if sw2: 
      return 2
    sw3 = not wiringpi.digitalRead(switch_3) # Read switch
    if sw3: 
      return 3
    sw4 = not wiringpi.digitalRead(switch_4) # Read switch
    if sw4: 
      return 4

    return 0

# ---------------------------------------------------------------------

def shutdown():
    command = "/sbin/shutdown -f now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output






# Set up GPIO pins
def initGPIOPins():

	print "Init GPIO pins..."
	# Set up GPIO pins
	wiringpi.wiringPiSetup() # use wiringpi pin numbers
	
	wiringpi.pinMode(switch_1,0) # input
	wiringpi.pullUpDnControl(switch_1, 2)
	wiringpi.pinMode(switch_2,0) # input
	wiringpi.pullUpDnControl(switch_2, 2)
	wiringpi.pinMode(switch_3,0) # input
	wiringpi.pullUpDnControl(switch_3, 2)
	wiringpi.pinMode(switch_4,0) # input
	wiringpi.pullUpDnControl(switch_4, 2)
	
	# I couldnt seem to get at pin 252 for the backlight using the usual method above, 
	# but this seems to work
	os.system("echo 252 > /sys/class/gpio/export")
	os.system("echo 'out' > /sys/class/gpio/gpio252/direction")
	os.system("echo '1' > /sys/class/gpio/gpio252/value")



def launchThreads():
	global config
	
	#init GPS. Start serial monitor thread
	if config['GPSThread'] == 1 :
		print "Launching GPS Thread"
		t1 = threading.Thread(target=ThreadGpsRead,    args=()).start()
	
	#init LEd drawing thread
	if config['LedThread'] == 1 :
		print "Launching Led Drawing Thread"
		t1 = threading.Thread(target=ThreadLedDrawing,    args=()).start()
	
	#init OBD
	if config['OBDThread'] == 1 :
		print "Launching OBD Thread"
		t2 = threading.Thread(target=ThreadObdRead,args=()).start()
	
	#init Data Logging
	if config['DataLoggerThread'] == 1 :
		print "Launching DataLogger Thread"
		t4 = threading.Thread(target=ThreadDataLogging, args=()).start()
	
	#init Screen refreashing thread
	if config['PrintScreenThread'] == 1 :
		print "Launching Screen Updating Thread"
		t5 = threading.Thread(target=ThreadPrintScreen, args=()).start()

	#init Network Manager thread
	#if config['NetworkManagerThread'] == 1 :
	#	print "Launching NetworkManager Thread"
	#	t5 = threading.Thread(target=ThreadNetworkManager, args=()).start()




#############################################################################################
# Initialization -----------------------------------------------------------
#############################################################################################

# Init framebuffer/touchscreen environment variables
initScreenSDL()

initGPIOPins()

loadSettings() 

Prepare_GpsRead()
Prepare_ledDrawing()
Prepare_ObdRead()
Prepare_dataLogging()
#Prepare_networkManager()
net = network.network(configVar=config, wifilistVar=wifiList,dataMessageVar=dataMessage)

launchThreads()

# Capture SIGINT
def end_read(signal,frame):
  global continue_reading, config
  print "Ctrl+C captured, ending read."
  #continue_reading = False
  config['continueReading'] = False
  sys.exit(0)
signal.signal(signal.SIGINT, end_read)










#############################################################################################
# Main loop -----------------------------------------------------------
#############################################################################################
lastUpdateScan = pygame.time.get_ticks()
while(config['continueReading']):
	#if pygame.time.get_ticks() - lastUpdateScan > 1000:
	#	print ("-----global continue reading: " + str(config['continueReading']))
	#	lastUpdateScan = pygame.time.get_ticks()
            
	if config['GPSThread'] == 0 :
		GpsRead()
	if config['LedThread'] == 0 :
		ledDrawing()
	if config['OBDThread'] == 0 :
		ObdRead()
	if config['DataLoggerThread'] == 0 :
		dataLogging()
	if config['PrintScreenThread'] == 0 :
		printScreen()
	if config['NetworkManagerThread'] == 0 :
		net.connectToNetworks()
		

	
	
  
  
  
	ReadInputButtons()

  


