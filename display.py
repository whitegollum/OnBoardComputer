
from config import *
import os
import pygame
from pygame.locals import *
import fnmatch


#import network




##########################################################################################################
############################################## CLASS ICON ##############################################
##########################################################################################################
# Icon is a very simple bitmap class, just associates a name and a pygame
# image (PNG loaded from icons directory) for each.
# There isn't a globally-declared fixed list of Icons.  Instead, the list
# is populated at runtime from the contents of the 'icons' directory.

class Icon:

	def __init__(self, name):
	  self.name = name
	  try:
	    self.bitmap = pygame.image.load(iconPath + '/' + name + '.png').convert()
	  except:
	    pass

##########################################################################################################
############################################## CLASS BUTTON ##############################################
##########################################################################################################
# Button is a simple tappable screen region.  Each has:
#  - bounding rect ((X,Y,W,H) in pixels)
#  - optional background color and/or Icon (or None), always centered
#  - optional foreground Icon, always centered
#  - optional single callback function
#  - optional single value passed to callback
# Occasionally Buttons are used as a convenience for positioning Icons
# but the taps are ignored.  Stacking order is important; when Buttons
# overlap, lowest/first Button in list takes precedence when processing
# input, and highest/last Button is drawn atop prior Button(s).  This is
# used, for example, to center an Icon by creating a passive Button the
# width of the full screen, but with other buttons left or right that
# may take input precedence (e.g. the Effect labels & buttons).
# After Icons are loaded at runtime, a pass is made through the global
# buttons[] list to assign the Icon objects (from names) to each Button.

class Button:

	def __init__(self, rect, **kwargs):
	  self.rect     = rect # Bounds
	  self.color    = None # Background fill color, if any
	  self.iconBg   = None # Background Icon (atop color fill)
	  self.iconFg   = None # Foreground Icon (atop background)
	  self.bg       = None # Background Icon name
	  self.fg       = None # Foreground Icon name
	  self.callback = None # Callback function
	  self.value    = None # Value passed to callback
	  for key, value in kwargs.iteritems():
	    if   key == 'color': self.color    = value
	    elif key == 'bg'   : self.bg       = value
	    elif key == 'fg'   : self.fg       = value
	    elif key == 'cb'   : self.callback = value
	    elif key == 'value': self.value    = value

	def selected(self, pos):
	  x1 = self.rect[0]
	  y1 = self.rect[1]
	  x2 = x1 + self.rect[2] - 1
	  y2 = y1 + self.rect[3] - 1
	  if ((pos[0] >= x1) and (pos[0] <= x2) and
	      (pos[1] >= y1) and (pos[1] <= y2)):
	    if self.callback:
	      if self.value is None: self.callback()
	      else:                  self.callback(self.value)
	    return True
	  return False

	def draw(self, screen, dirtyrects):
	  if self.color:
	    screen.fill(self.color, self.rect)
	  if self.iconBg:
	    screen.blit(self.iconBg.bitmap,
	      (self.rect[0]+(self.rect[2]-self.iconBg.bitmap.get_width())/2,
	       self.rect[1]+(self.rect[3]-self.iconBg.bitmap.get_height())/2))
	  if self.iconFg:
	    screen.blit(self.iconFg.bitmap,
	      (self.rect[0]+(self.rect[2]-self.iconFg.bitmap.get_width())/2,
	       self.rect[1]+(self.rect[3]-self.iconFg.bitmap.get_height())/2))

	def setBg(self, name):
	  if name is None:
	    self.iconBg = None
	  else:
	    for i in icons:
	      if name == i.name:
	        self.iconBg = i
	        break


##########################################################################################################
############################################## UI CALLBACKS ##############################################
##########################################################################################################
# UI callbacks -------------------------------------------------------------
# These are defined before globals because they're referenced by items in
# the global buttons[] list.

def ChangeDatafeedCallback(n): # Pass 1 (next setting) or -1 (prev setting)
    global data1Mode
    global data2Mode
    global maxData1Mode
    global maxData2Mode
    global UpdateFullScreen
    
    if ( n == 0 ):
	  data1Mode += 1
	  if ( data1Mode > maxData1Mode ): data1Mode = 0
    if ( n == 1 ):
	  data2Mode += 1
	  if ( data2Mode > maxData2Mode ): data2Mode = 0
	
    UpdateFullScreen = True
        

def doneCallback(): # Exit settings
        global screenMode
        if screenMode > 0:
          saveSettings()
        screenMode = 0 # Switch back to main window
        
        
def startCallback(n): # start/Stop the timelapse thread
        global t, busy, threadExited
        global currentframe

#def signal_handler(signal, frame):
#	print 'got SIGTERM'
#	pygame.quit()
#	sys.exit()

def ledCallback(signal):
	global led
	
	led.demoStart()

def segmCallback(signal):
        print '7Segment demo'

def goToScreenCallback(menu):
        print 'Showing Menu ' + str(menu)
	global screenMode
        screenMode = menu
        


##########################################################################################################
############################################# globals ####################################################
##########################################################################################################
iconPath        	= 'icons' # Subdirectory containing UI bitmaps (PNG format)

icons = [] # This list gets populated at startup


# buttons[] is a list of lists; each top-level list element corresponds
# to one screen mode (e.g. viewfinder, image playback, storage settings),
# and each element within those lists corresponds to one UI button.
# There's a little bit of repetition (e.g. prev/next buttons are
# declared for each settings screen, rather than a single reusable
# set); trying to reuse those few elements just made for an ugly
# tangle of code elsewhere.

buttons = [

  # Screen mode 0 is main view screen of current status
  [Button((  8, 0,102, 33), bg='boton1', cb=goToScreenCallback, value=1),
   Button((110, 0,102, 33), bg='boton1', cb=ledCallback, value=0),
   Button((212, 0,102, 33), bg='boton1', cb=ledCallback, value=1),
   Button((  0,33,160,120), bg='',       cb=ChangeDatafeedCallback, value=0),
   Button((160,33,160,120), bg='',       cb=ChangeDatafeedCallback, value=1)],


  # Screen 1: Configurar View1 Izq
  [Button((  8, 0,102, 33), bg='boton1', cb=goToScreenCallback, value=1),
   Button((110, 0,102, 33), bg='boton1', cb=goToScreenCallback, value=1),
   Button((212, 0,102, 33), bg='boton1', cb=goToScreenCallback, value=1)],

  # Screen 2: Configurar View1 Der
  [Button((  8, 0,102, 33), bg='boton1', cb=goToScreenCallback, value=1),
   Button((110, 0,102, 33), bg='boton1', cb=goToScreenCallback, value=1),
   Button((212, 0,102, 33), bg='boton1', cb=goToScreenCallback, value=1)]
]


busy           		= False
screenMode      	=  0      # Current screen mode; default = viewfinder
screenModePrior 	= -1      # Prior screen mode (for detecting changes)
numeric         	= 0       # number from numeric keypad      
numberstring		= "0"
returnScreen		= 0
###### variables que definen la informacion de la mitad derecha y la mitad izquierda de la pantalla.
###### es ciclico hasta el valor max, donde vuelven a 0
data1Mode			= 0
data2Mode			= 0
maxData1Mode 		= 2
maxData2Mode 		= 0

waitingForNewFrame  = False
dirtyrects = [] # list of update_rects
UpdateFullScreen 	= False
screen				= False





def ThreadPrintScreen():
	global config
	
	while config['continueReading']:
		printScreen()
		
def printScreen():
	global buttons
	global dirtyrects, UpdateFullScreen, clock, lastTime
	global led
	global data1Mode
	global data2Mode
	global screenMode, screenModePrior
	global maxData1Mode
	global maxData2Mode
	global last_coord,spd,altitude,sats
	global screen, config
	global Data1_0
	global Data1_1
	global Data2_1
	global Data2_0
	global iconGps0
	global iconGps1
	global iconGps2
	global iconGps3
	global iconGps4
	global iconWifi0
	global iconWifi1
	global iconWifi2
	global dataMessage
	#global net

	
	 
   	# Overlay buttons on display and update
   	#for i,b in enumerate(buttons[screenMode]):
   		#b.draw(screen,dirtyrects)

	################ Screen mode 2
	if screenMode == 2:
		myfont = pygame.font.SysFont("Arial", 20)
		label = myfont.render(numberstring, 1, (255,255,255))
		dirtyrects.append(screen.blit(label, (10, 2)))
		
		################ Screen mode 1 es el display de config de parametros
		if screenMode == 1:
			myfont = pygame.font.SysFont("Arial", 20)
  		label = myfont.render("Pulse:" , 1, (255,255,255))
		dirtyrects.append(screen.blit(label, (10, 10)))
		label = myfont.render("Interval:" , 1, (255,255,255))
		dirtyrects.append(screen.blit(label, (10, 70)))
		label = myfont.render("Frames:" , 1, (255,255,255))
		dirtyrects.append(screen.blit(label, (10,130)))


	################ Screen mode 0 es el dsiplay principal de datos
	if screenMode == 0:
    	
		#################################### Display1 Mode 0: Barra de RPM ##############################
		if ( data1Mode == 0 ):    
		    screen.fill((0,0,0))
		    #dibujo las barras de velocidad
		    #porcentaje = variable *100/(maximo posible-minimo posible)
		    porcentaje = float(getDataMessage('obdRpm')/6000.0)
		    coordx = 6 + int( (259.0-12.0) * porcentaje )
		    color = (0,220,0)
		    rect = (12,54,coordx,261)
		    pygame.draw.rect(screen, color, rect, 0)
		    
		    # Draw speed
		    myfont = pygame.font.Font("fonts/digital7.ttf",90)
		    spdText = myfont.render("{:04d}".format(int(getDataMessage('rpm'))), 1, (0,255,0))
		    dirtyrects.append(screen.blit(spdText, (26,136)))
		    # Draw "Km/h" encima de las barras de velocidad
		    labelFont = pygame.font.Font("fonts/digital7.ttf",40)
		    lblText = labelFont.render("rpm", 1, (255,255,0))
		    screen.blit(lblText, (190,176))
		    
		    # imprimimos el grafico sobre las barras
		    screen.blit(Data1_1,(0, 0))
		    
		    # Draw number of satellites
		    subFont = pygame.font.Font("fonts/digital7.ttf",40)
		    altText = subFont.render("{:02d}".format(getDataMessage('gpsSats')), 1, (0,0,255))
		    dirtyrects.append(screen.blit(altText, (238,33)))#120
	
	        # Draw "SAT FIXED"
	        if (dataMessage['gpsFix']):
		       labelFont = pygame.font.Font("fonts/digital7.ttf",18)
		       lblText = labelFont.render("FIX", 1, (255,255,0))
		       dirtyrects.append(screen.blit(lblText, (244,18)))#140
	        else:
	           labelFont = pygame.font.Font("fonts/digital7.ttf",18)
	           lblText = labelFont.render("NoFIX", 1, (255,255,0))
	           dirtyrects.append(screen.blit(lblText, (235,18)))#140
	        
	        # config para que no se imprima nada en la segunda mitad de la pantalla
	        data2Mode = 99
	
	    
	    #################################### Display1 Mode 2: Velocidad ##############################333
		if ( data1Mode == 1 ):
		    screen.fill((0,0,0))
		    #dibujo las barras de velocidad
		    #porcentaje = variable *100/(maximo posible-minimo posible)
		    porcentaje = float(dataMessage['obdSpeed']/250.0)
		    coordx = 6 + int( (259.0-12.0) * porcentaje )
		    color = (0,220,0)
		    rect = (12,54,coordx,261)
		    pygame.draw.rect(screen, color, rect, 0)
		    
		    # Draw speed
		    myfont = pygame.font.Font("fonts/digital7.ttf",90)
		    spdText = myfont.render("{:03d}".format(int(getDataMessage('speed'))), 1, (0,255,0))
		    dirtyrects.append(screen.blit(spdText, (26,136)))
		    # Draw "Km/h" encima de las barras de velocidad
		    labelFont = pygame.font.Font("fonts/digital7.ttf",40)
		    lblText = labelFont.render("km/h", 1, (255,255,0))
		    screen.blit(lblText, (190,176))
		    
		    # imprimimos el grafico sobre las barras
		    screen.blit(Data1_1,(0, 0))
		    
		    # Draw number of satellites
		    subFont = pygame.font.Font("fonts/digital7.ttf",40)
		    altText = subFont.render("{:02d}".format(getDataMessage('gpsSats')), 1, (0,0,255))
		    dirtyrects.append(screen.blit(altText, (238,33)))#120
	
	        # Draw "SAT FIXED"
	        if (dataMessage['gpsFix']):
		       labelFont = pygame.font.Font("fonts/digital7.ttf",18)
		       lblText = labelFont.render("FIX", 1, (255,255,0))
		       dirtyrects.append(screen.blit(lblText, (244,18)))#140
	        else:
	           labelFont = pygame.font.Font("fonts/digital7.ttf",18)
	           lblText = labelFont.render("NoFIX", 1, (255,255,0))
	           dirtyrects.append(screen.blit(lblText, (235,18)))#140
	        
	        # config para que no se imprima nada en la segunda mitad de la pantalla
	        data2Mode = 99
	    		
	    #################################### Display1 Mode 3: Detalle completo ##############################333
		if ( data1Mode == 2 ):
			screen.fill((0,0,0))
			myfont = pygame.font.SysFont("Arial", 10)
			x = 20
			for key in dataMessage.keys():
				label = myfont.render(key + ": " + str(dataMessage[key]), 1, (255,255,255))
				dirtyrects.append(screen.blit(label, (1, x)))
				x = x+10
					
				
				
				
				
# 				label = myfont.render("localTime:       " + str(getDataMessage('localTime')), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 20)))
# 				label = myfont.render("GPS Latitude:    " + str(getDataMessage('gpsCoordLat')), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 40)))
# 				label = myfont.render("GPS Longitud:    " + str(getDataMessage('gpsCoordLon')), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 50)))
# 				label = myfont.render("GPS Sats:        " + str(getDataMessage('gpsSats')), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 60)))
# 				label = myfont.render("GPS Time UTC:    " + str(getDataMessage('gpsTimeUTC') ), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 70)))
# 				label = myfont.render("GPS Speed:       " + str(getDataMessage('gpsSpd']), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 80)))
# 				label = myfont.render("GPS Altitude:    " + str(getDataMessage('gpsAltitude'] ), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 90)))
# 				label = myfont.render("GPS Track:       " + str(getDataMessage('gpsTrack'] ), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 100)))
# 				label = myfont.render("GPS Mode:        " + str(getDataMessage('gpsMode'] ), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 110)))
# 				label = myfont.render("GPS Climb:       " + str(getDataMessage('gpsClimb'] ), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 120)))
# 				label = myfont.render("GPS EPS:         " + str(dataMessage['gpsEPS'] ), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 130)))
# 				label = myfont.render("GPS EPX:         " + str(dataMessage['gpsEPX'] ), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 140)))
# 				label = myfont.render("GPS EPV:         " + str(dataMessage['gpsEPV'] ), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 150)))
# 				label = myfont.render("GPS EPT:         " + str(dataMessage['gpsEPT'] ), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 160)))
# 		
# 				label = myfont.render("OBD rpm:       " + str(dataMessage['obdRpm']), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 180)))
# 				label = myfont.render("OBD speed:     " + str(dataMessage['obdSpeed']), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 190)))
# 				label = myfont.render("OBD throttle:  " + str(dataMessage['obdThrottle_pos']), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 200)))
# 				label = myfont.render("OBD load:      " + str(dataMessage['obdLoad']), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 210)))
# 				label = myfont.render("OBD fuel:      " + str(dataMessage['obdFuel_status']), 1, (255,255,255))
# 				dirtyrects.append(screen.blit(label, (1, 220)))
		
	        # config para que no se imprima nada en la segunda mitad de la pantalla
	        data2Mode = 99
	
		#################################### Display1 Mode 1: Resumen informacion grafica ##############################333
		if ( data1Mode == 3 ):
		    screen.fill((0,0,0))
		    # Draw "altitude"
		    subFont = pygame.font.Font("fonts/digital7.ttf",40)
		    altText = subFont.render("{:04f}".format(getDataMessage('gpsAltitude')), 1, (0,255,0))
		    dirtyrects.append(screen.blit(altText, (2,2)))#120
	
		    # Draw "msnm"
		    labelFont = pygame.font.Font("fonts/digital7.ttf",20)
		    lblText = labelFont.render("msnm", 1, (255,255,0))
		    screen.blit(lblText, (60,22))#140
	
	        # Draw latitude
		    subFont = pygame.font.Font("fonts/digital7.ttf",30)
		    altText = subFont.render("{:07.4f}".format(math.fabs(getDataMessage('gpsCoordLat'))), 1, (0,255,0))
		    dirtyrects.append(screen.blit(altText, (2,82)))#200
	
	        # Draw N or S depending on value
		    labelFont = pygame.font.Font("fonts/digital7.ttf",20)
		    lat_lbl = "N"
		    if dataMessage['gpsCoordLat'] < 0:
		      lat_lbl = "S"
		    lblText = labelFont.render(lat_lbl, 1, (255,255,0))
		    dirtyrects.append(screen.blit(lblText, (140,102)))#220
	
	        # Draw longitude
		    subFont = pygame.font.Font("fonts/digital7.ttf",30)
		    altText = subFont.render("{:08.4f}".format(math.fabs(getDataMessage('gpsCoordLon'))), 1, (0,255,0))
		    dirtyrects.append(screen.blit(altText, (2,102)))
	
	        # Draw E or W depending on value
		    labelFont = pygame.font.Font("fonts/digital7.ttf",20)
		    lat_lbl = "E"
		    if dataMessage['gpsCoordLon'] < 0:
		      lat_lbl = "W"
		    lblText = labelFont.render(lat_lbl, 1, (255,255,0))
		    dirtyrects.append(screen.blit(lblText, (140,102)))#200
	
	        # Draw number of satellites
		    subFont = pygame.font.Font("fonts/digital7.ttf",40)
		    altText = subFont.render("{:02d}".format(getDataMessage('gpsSats')), 1, (0,0,255))
		    dirtyrects.append(screen.blit(altText, (2,132)))#120
	
	        # Draw "SAT FIXED"
		    labelFont = pygame.font.Font("fonts/digital7.ttf",20)
		    lblText = labelFont.render("SAT FIXED", 1, (255,255,0))
		    dirtyrects.append(screen.blit(lblText, (240,152)))#140
	
		    # config para que no se imprima nada en la segunda mitad de la pantalla
		    data2Mode = 99
	
	    #################################### Display2 Mode 0 ##############################333
		if ( data2Mode == 0 ):
			screen.fill((0,0,0))
			dirtyrects.append(screen.blit(Data2_0,(160, 32)))
	




	################################### Iconos universales en todas pantallas ##########################
	dirtyrects.append(screen.blit(iconGps0,(0,240-iconGps0.get_height())))
	if (dataMessage['gpsMode'] > 0):
		dirtyrects.append(screen.blit(iconGps1,(0,240-iconGps1.get_height())))
	if (dataMessage['gpsSats'] > 3):
		dirtyrects.append(screen.blit(iconGps2,(0,240-iconGps2.get_height())))
	if (dataMessage['gpsMode'] == 2):
		dirtyrects.append(screen.blit(iconGps3,(0,240-iconGps3.get_height())))
	if (dataMessage['gpsMode'] == 3):
		dirtyrects.append(screen.blit(iconGps4,(0,240-iconGps4.get_height())))




	
	if (dataMessage['iface'] != ""):
		myfont = pygame.font.SysFont("Arial", 10)
		label = myfont.render(dataMessage['ip'] + " : " + dataMessage['ssid'], 1, (255,255,255))
		dirtyrects.append(screen.blit(label, (320-25-label.get_width(), 240-label.get_height())))
		
		if ( dataMessage['internetReachable'] != 0 ):
			dirtyrects.append(screen.blit(iconWifi2,(320-25,240-25)))
		else:
			dirtyrects.append(screen.blit(iconWifi1,(320-25,240-25))	)
	else:
		dirtyrects.append(screen.blit(iconWifi0,(320-25,240-25)))



	#### cuento tiempo para las rutinas de espera y calculo el FPS
	#clock.tick(50)
    #print ("fps: " + str(clock.get_fps()) + " ClockTicks: " + str(lastTime - pygame.time.get_ticks()))
    #print ("fps: " + str(clock.get_fps()))

	################ Fin
	pygame.display.update()
    #if UpdateFullScreen == True:
    #  pygame.display.update()
    #  UpdateFullScreen = False
    #else:
    #  pygame.display.update(dirtyrects)
    #dirtyrects = []




	screenModePrior = screenMode
    #waitingForNewFrame = False

  	#print "Screen thread stopped" 
  	
  	#screen.fill((0,70,40))
	#dirtyrects.append(screen.blit(iconGps4,(0,240-iconGps4.get_height())))
	#pygame.display.update()
	
	
	# Process touchscreen input
	for event in pygame.event.get():
		print ("event")
		if(event.type is MOUSEBUTTONDOWN):
			print ("click")
			pos = pygame.mouse.get_pos()
			for b in buttons[screenMode]:
				if b.selected(pos): break
  
  
def initScreenSDL():
	global screen
	global buttons
	global Data1_0
	global Data1_1
	global Data2_1
	global Data2_0
	global iconGps0
	global iconGps1
	global iconGps2
	global iconGps3
	global iconGps4
	global iconWifi0
	global iconWifi1
	global iconWifi2
	global iconPath
	
	
	
	# Init framebuffer/touchscreen environment variables
	os.putenv('SDL_VIDEODRIVER', 'fbcon')
	os.putenv('SDL_FBDEV'      , '/dev/fb1')
	os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
	os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')
	
	
	# Init pygame and screen
	print "Initting..."
	pygame.init()
	print "Setting Mouse invisible..."
	pygame.mouse.set_visible(False)
	print "Setting fullscreen..."
	modes = pygame.display.list_modes(16)
	screen = pygame.display.set_mode(modes[0], FULLSCREEN, 16)

	print "Loading Icons..."
	# Load all icons at startup.
	for file in os.listdir(iconPath):
	  if fnmatch.fnmatch(file, '*.png'):
	    icons.append(Icon(file.split('.')[0]))
	# Assign Icons to Buttons, now that they're loaded
	print"Assigning Buttons"
	for s in buttons:        # For each screenful of buttons...
	  for b in s:            #  For each button on screen...
	    for i in icons:      #   For each icon...
	      if b.bg == i.name: #    Compare names; match?
	        b.iconBg = i     #     Assign Icon to Button
	        b.bg     = None  #     Name no longer used; allow garbage collection
	      if b.fg == i.name:
	        b.iconFg = i
	        b.fg     = None
	
	print "loading background.."
	Data1_0    = pygame.image.load("icons/Data1_0.png").convert_alpha()
	Data1_1    = pygame.image.load("icons/Data1_1.png").convert_alpha()
	Data2_0    = pygame.image.load("icons/Data2_0.png").convert_alpha()
	Data2_1    = pygame.image.load("icons/Data2_1.png").convert_alpha()
	
	
	print "loading icons..."
	iconGps0    = pygame.image.load("icons/gps_0.png").convert_alpha()
	iconGps1    = pygame.image.load("icons/gps_1.png").convert_alpha()
	iconGps2    = pygame.image.load("icons/gps_2.png").convert_alpha()
	iconGps3    = pygame.image.load("icons/gps_3.png").convert_alpha()
	iconGps4    = pygame.image.load("icons/gps_4.png").convert_alpha()
	iconWifi0	= pygame.image.load("icons/wifi_0.png").convert_alpha()
	iconWifi1	= pygame.image.load("icons/wifi_1.png").convert_alpha()
	iconWifi2	= pygame.image.load("icons/wifi_2.png").convert_alpha()


	


