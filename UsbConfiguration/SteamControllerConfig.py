#!/usr/bin/env python

import usb.core
import usb.util

from datetime import datetime

import sys, getopt

class SteamControllerConfig:
	'Class for configuring of a Steam Controller'

	# TODO: Need to add __ for private members
	usbDev = None
	firmwareRev = 0
	bootloaderRev = 0	

	def __init__(self):
		# TODO: only searches for wired controller 
		self.usbDev = usb.core.find(idVendor=0x28DE, idProduct=0x1102)

		if self.usbDev is None:
		    raise ValueError('Wired Steam Controller not found')

		print "Found Wired Steam Controller"

		# TODO: what about reattaching controller on exit?
		if (self.usbDev.is_kernel_driver_active(interface=2)):
			self.usbDev.detach_kernel_driver(interface=2)

		# TODO: need to claim interface?
		#self.usbDev.claim_interface(

		payload = [0x83, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ,0x00, 0x00, 
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
		
		# Send request for revision info
		self.usbDev.ctrl_transfer(bmRequestType=0x21, bRequest=9, wValue=0x0300, wIndex=2, 
			data_or_wLength=payload)

		# Get revision info
		payload = self.usbDev.ctrl_transfer(bmRequestType=0xa1, bRequest=1, wValue=0x0300, wIndex=2, 
			data_or_wLength=64)

		for index in range(26, 22, -1):
			self.firmwareRev *= 256 
			self.firmwareRev += payload[index]

		print 'Firmware Revision: 0x', format(self.firmwareRev, '08X'), datetime.fromtimestamp(self.firmwareRev)

		# TODO: what else can we pull from revision info payload? Bootloader revision?

	def __enterPersonalize(self):
		"""
		USB command sent when "Personalize" is clicked in Steam
		"""

		payload = [0xc1, 0x10, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 
			0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x00, 0x00 ,0x00, 0x00, 
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

		self.usbDev.ctrl_transfer(bmRequestType=0x21, bRequest=9, wValue=0x0300, wIndex=2, 
			data_or_wLength=payload)

	def playSong(self, index):
		"""
		Play song that could be set to boot up or power off

		Keyword arguments:
		index -- Index of song to play:
			 0 = Warm and Happy
			 1 = Invader
			 2 = Controller Confirmed
			 3 = Victory!
			 4 = Rise and Shine:
			 5 = Shorty
			 6 = Warm Boot
			 7 = Next Level
			 8 = Shake It Off
			 9 = Access Denied
			10 = Deactivate
			11 = Discovery
			12 = Triumph
			13 = The Mann
		"""
		# TODO: Make index into enums

		# Put controller into Personalize mode
		self.__enterPersonalize()

		# Play demo song at given index
		payload = [0xb6, 0x04, index, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ,0x00, 0x00, 
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

		self.usbDev.ctrl_transfer(bmRequestType=0x21, bRequest=9, wValue=0x0300, wIndex=2, 
			data_or_wLength=payload)

	def setBrightness(self, brightness):
		"""
		Set current the brightness level of the Steam Button. If this is to be saved
		 make sure to call confirmPersonalize()

		Keyword arguments:
		brightness -- Corresponds to brightness level. 
		"""

		# Put controller into Personalize mode
		self.__enterPersonalize()

		# This is the maximum steam lets the brightness be set to
		#  Keeping limitation in case going higher could damage hw
		if brightness > 0x64:
			brightness = 0x64

		# Play demo song at given index
		payload = [0x87, 0x03, 0x2d, brightness, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ,0x00, 0x00, 
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

		self.usbDev.ctrl_transfer(bmRequestType=0x21, bRequest=9, wValue=0x0300, wIndex=2, 
			data_or_wLength=payload)

	# TODO
	#def personalize(self, pwrUpSong, pwrDwnSong, brightness)
	# Save config = c1 10 pwrUpSong pwrDwnSong ffff0309 05ffffff ffffffff ffff0000 00000000 00000000 00000000


def main(argv):
	songIndex = 0

	try:
		opts, args = getopt.getopt(argv,"hp:",["playsong="])
	except getopt.GetoptError:
		print 'SteamControllerConfig.py -p <songIndex>'
	for opt, arg in opts:
		if opt == '-h':
			print 'SteamControllerConfig.py -p <songIndex>'
		elif opt in ("-p", "--playsong"):
			songIndex = int(arg)

	controller = SteamControllerConfig()

	controller.playSong(songIndex)

if __name__ == "__main__":
	main(sys.argv[1:])
