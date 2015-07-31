# Created by Javier Espasa
#import getpass
#import network
import pygame


##########################################################################################################
############################################## VARIABLES ##############################################
##########################################################################################################
# Loop condition
continue_reading = True




##########################################################################################################
############################################## CONFIG ##############################################
##########################################################################################################
config = {
	'net_iface':"wlan0",
	'net_testInternetConnection1':'http://www.google.com',
	'net_testInternetConnection2':"https://github.com/whitegollum/onboard-bike-computer/blob/master/README.md",
	'net_TimeToScanNetworks': 10000,
	'net_TimeToConnectNetworks':10000,
	'deviceid':"onboardcomputer1",
	'allowedGPSmodes':2,
	'api-retry':5,
	'APIversion':1,
	'AutoConfigRPM':1,
	'MaxRPM':3500,
	'MinRPM':500,
	'AutoConfigSPD':0,
	'MaxSPD':250,
	'MinSPD':0,
	'AutoConfigTHR':1,
	'MaxTHR':1,
	'MinTHR':0,
	'AutoConfigLOAD':1,
	'MaxLOAD':1,
	'MinLOAD':0,
	'AutoConfigFUEL':1,
	'MaxFUEL':1,
	'MinFUEL':0,
	'DataLoggerThread':1,						# activa o desactiva el logging a fichero
	'dataLoggingFilename':'datalogger.txt', # nombre del fichero de log
	'GPSThread':1,							# activa la obtencion de datos via GPSD
	'OBDThread':1,							# activa la obtencion de datos via OBD2
	'PrintScreenThread':0,					# activa el refresco de pantalla
	'NetworkManagerThread':1,
	'ReadInputButtons':1,
	'LedThread':1,							# activa la rutina de pintar Leds en el panel
	'OBD2AutoDetect':1,							# Autodetecta los sensores disponibles en el bus CANBUS OBD2
	'continueReading':True
}

wifiList = {
	'Matematica':"Logaritmo de pi",
	'Nada':"nada"							# Autodetecta los sensores disponibles en el bus CANBUS OBD2
}


# Global stuff -------------------------------------------------------------

RED = 2
OFF = 0
YELLOW = 3
GREEN = 1


#cuidado me he cargado la clase timelapse
#t = threading.Thread(target=timeLapse)

backlightpin		= 252

###### variables para poder calcular la inclinacion de la moto + o -
inclinacion         = 0
offsetInclinacion   = 0
maxInclinacion      = 10


clock = pygame.time.Clock()
lastTime = 0.0



# Receive buffer
last_received = ''
lat2 = 0
lon2 = 0


#dataMessage = {'localTime':"0",
#'gpsFix':0, 'gpsCoordLat':NaN,'gpsCoordLon':NaN,'gpsTimeUTC':0,'gpsSpd':0,'gpsAltitude':"0",'gpsSats':"0",
#'gpsEPS':NaN,'gpsEPX':NaN,'gpsEPV':NaN,'gpsEPT':"0",'gpsTrack':"0",'gpsMode':"0", 'gpsClimb':"0", 
#'obdRpm':NaN, 'obdSpeed':NaN, 'obdThrottle_pos':NaN, 'obdLoad':"0", 'obdFuel_status':"0", 'gear':"0"}
dataMessage = {
'localTime':"0",
'gpsFix':0, 
'gpsCoordLat':0.0,
'gpsCoordLon':0.0,
'gpsTimeUTC':0.0,
'gpsSpd':0.0,
'gpsAltitude':0.0,
'gpsSats':0,
'gpsEPS':0.0,
'gpsEPX':0.0,
'gpsEPV':0.0,
'gpsEPT':0.0,
'gpsTrack':0.0,
'gpsMode':0,
'gpsClimb':0.0, 
'gear':0,
'iface':"wlan0",
'ssid':"",
'internetReachable':0,
'ip':""
}
dataLoggingFilename = "datalogger.txt"  
lastTimeLog = 0



switch_1 = 1 # GPIO pin 18 - left to right with switches on the top
switch_2 = 2 # GPIO pin 21/27
switch_3 = 3 # GPIO pin 22
switch_4 = 4 # GPIO pin 23

backlightpin = 252



##########################################################################################################
############################################## FUNCTIONS ##############################################
##########################################################################################################


def getDataMessage(item):
	global dataMessage
	
	return dataMessage.get (item,0)

def saveSettings():
	global config
	try:
	  outfile = open('config.pkl', 'wb')
	  # Use a dictionary (rather than pickling 'raw' values) so
	  # the number & order of things can change without breaking.
	  pickle.dump(config, outfile)
	  outfile.close()
	except:
	  pass

def loadSettings():
	global config
	try:
		print"Load Settings"
		
		infile = open('config.pkl', 'rb')
		config = pickle.load(infile)
		infile.close()
	except:
		pass
