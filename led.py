#!/usr/bin/env python

import threading
import time
#import Image
#import ImageDraw
from PIL import Image, ImageSequence, ImageDraw
import sys, os
from Adafruit_LED_Backpack import BicolorMatrix8x8


class ledArrayThread(threading.Thread):
	
	
	def __init__(self):
		threading.Thread.__init__(self)
		
		self.numLedArrayThreads = 0
		self.initLeds()
	
		#self.playSimpleGIF("./gif/test.gif", 1, 1)
		self.playDoubleGIF("./gif/test_doble.gif", 0.1)
		#self.playDoubleGIF("./gif/test_doble.gif", 0.1)
		#self.initLeds()
		#self.demoGaugeStart()
		
		self.initLeds()
		
	def initLeds(self):
		self.display1 = BicolorMatrix8x8.BicolorMatrix8x8(address=0x70, busnum=1)
		self.display2 = BicolorMatrix8x8.BicolorMatrix8x8(address=0x71, busnum=1)
		
		
		self.display1.begin()
		self.display2.begin()
				
		self.image1 = Image.new('RGB', (8, 8))
		self.image2 = Image.new('RGB', (8, 8))
		self.draw1 = ImageDraw.Draw(self.image1)
		self.draw2 = ImageDraw.Draw(self.image2)

	def resetLeds(self):
		self.display1.set_brightness(8) #brillo de 0 a 15
		self.display1.clear()	
		self.display2.set_brightness(8) #brillo de 0 a 15
		self.display2.clear()	

		
		

	def drawDisplays(self):
		
		self.display1.set_image(self.image1.rotate(90, expand=0))
		self.display1.write_display()
		
		self.display2.set_image(self.image2.rotate(90, expand=0))
		self.display2.write_display()

	def drawGauge(self,numGauge, gauge, color, display):
		if numGauge == 1:
			range1 = 0
			range2 = 1
		elif numGauge == 2:
			range1 = 2
			range2 = 3
		elif numGauge == 3:
			range1 = 4
			range2 = 5
		elif numGauge == 4:
			range1 = 6
			range2 = 7
			
		
		if color == BicolorMatrix8x8.RED:
			c = (255,0,0)
		elif color == BicolorMatrix8x8.GREEN:	
			c = (0,255,0)
		elif color == BicolorMatrix8x8.YELLOW:	
			c = (255,255,0)
			
		if display == 1:
			self.draw1.rectangle((range1,7,range1+1,7-gauge), outline=c, fill=c)
			#self.draw1.rectangle((7,range1,7-gauge,range2), outline=c, fill=c)
		if display == 2:
			self.draw2.rectangle((range1,7,range1+1,7-gauge), outline=c, fill=c)
			#self.draw2.rectangle((7,range1,7-gauge,range2), outline=c, fill=c)
			
	def playDoubleGIF(self,fileName, waitTime):
		if ( self.numLedArrayThreads > 0 ):
			# solo permito un thread a la vez, nada mas		
			print 'abort led anim, due to anim in progress'
		else:
			self.numLedArrayThreads += 1
			print 'execute gif anim'
			
			self.resetLeds()

						
			
			im = Image.open(fileName)
			original_duration = im.info['duration']
			frames1 = [frame.crop((0,0,8,8)).copy() for frame in ImageSequence.Iterator(im)]    
			frames2 = [frame.crop((8,0,16,8)).copy() for frame in ImageSequence.Iterator(im)]
			imwidth, imheight = frames2[1].size
			#print str(imwidth) + "x" + str(imheight)
			

			for x in range(0,len(frames1)):
				self.image1 = frames1[x]
				self.image2 = frames2[x]
				self.drawDisplays()
				time.sleep(waitTime)
		
			
			
			self.numLedArrayThreads -= 1
			
	def playSimpleGIF(self, fileName, waitTime, screen):
		if ( self.numLedArrayThreads > 0 ):
			# solo permito un thread a la vez, nada mas		
			print 'abort led anim, due to anim in progress'
		else:
			self.numLedArrayThreads += 1
			print 'execute gif anim'
			
			self.resetLeds()

						

			im = Image.open(fileName)
			original_duration = im.info['duration']
			frames = [frame.copy() for frame in ImageSequence.Iterator(im)]    

			for x in range(0,len(frames)):
				if screen == 1:
					self.image1 = frames[x]
					self.drawDisplays()
					time.sleep(1)
				if screen == 2:
					self.image2 = frames[x]
					self.drawDisplays()
					time.sleep(1)
					
		
			
			
			self.numLedArrayThreads -= 1












			
	def demoGaugeStart(self):
		
		if ( self.numLedArrayThreads > 0 ):
			# solo permito un thread a la vez, nada mas		
			print 'abort led anim, due to anim in progress'
		else:
			self.numLedArrayThreads = self.numLedArrayThreads +1
			print 'execute gauge led anim'
			
			self.resetLeds()
			
			for numGauge in range(1,5):
				for bar in range(0,8):
					self.resetLeds()
					self.drawGauge(numGauge, bar,BicolorMatrix8x8.RED,1)
					self.drawDisplays()
					#time.sleep(0.1)
				for bar in range(7, -1, -1):
					self.resetLeds()
					self.drawGauge(numGauge, bar,BicolorMatrix8x8.GREEN,1)
					self.drawDisplays()
					#time.sleep(0.1)
			for numGauge in range(1,5):
				for bar in range(0,8):
					self.resetLeds()
					self.drawGauge(numGauge, bar,BicolorMatrix8x8.YELLOW,2)
					self.drawDisplays()
					#time.sleep(0.1)
				for bar in range(7, -1, -1):
					self.resetLeds()
					self.drawGauge(numGauge, bar,BicolorMatrix8x8.GREEN,2)
					self.drawDisplays()
					#time.sleep(0.1)
			self.numLedArrayThreads = self.numLedArrayThreads - 1



		
	def demoLed2(self):
		
		if ( self.numLedArrayThreads > 0 ):
			# solo permito un thread a la vez, nada mas		
			print 'abort led anim, due to anim in progress'
		else:
			self.numLedArrayThreads = self.numLedArrayThreads +1
			
			# Clear the display buffer.
			#self.display.clear()
			self.resetLeds()
			
			self.draw1.rectangle((0,0,7,7), outline=(255,255,0), fill=0)

			# Draw an X with two lines.
			self.draw1.line((1,1,6,6), fill=(255,255,0))
			self.draw1.line((1,6,6,1), fill=(255,255,0))

						# Draw the buffer to the display hardware.
			#self.display.write_display()
			self.drawDisplays()
			
			time.sleep(1)
						
			self.numLedArrayThreads -= 1
