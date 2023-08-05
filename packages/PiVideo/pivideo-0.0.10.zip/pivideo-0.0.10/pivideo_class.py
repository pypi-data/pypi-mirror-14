#!/usr/bin/python
######################################################################
#
#  PiVideo interface class
#  Copyright(c) 2015 by Lintest Systems LLC
#
######################################################################
#
#  Revision History
#	0.1	Initial Version
#
#  PiVideo Class:
#	open			Open a PiVideo object
#	pivideo_port		Specify the communications port - must match jumper settings
#	pivideo_i2c_address	Specfiy the PiVideo I2C address = must match jumper settings
#	ready			PiVideo processor is ready for the Raspberry Pi
#	running			Raspberry Pi camera interface is active
#	source			Video Source selection
#	active_source		Video source currently active
#	effect			Various video effects
#	led			Control status LEDs
#	lock			Active video status and type
#	config 			Set or restore current configuration
#	version			Report the software version
#	id			Report the PiConfig hardware ID
#	update			Update the PiVideo processor software
#	command			Modify internal processing - use only with approved Lintest scripts

try:
        import smbus
        _i2c_available = True
except:
        _i2c_available = False

import serial
import time

if __name__ == "__main__":
	print("pivideo_class.py contains the PiVideo class for use with pivideo.py or your program")

sources=['auto','video1','video2','video3','svideo','component']
ports=['i2c0','i2c1','serial']
effects=['none','bw','colorbar','nomsg']
config_actions=['none','restore','save','reset']
led_settings=['normal','min','off']

class PiVideo(object):
    	"""
    	Provides a Python interface to the Lintest Systems video module
    	"""

	
	status = None				# Changes to open port if successful
	port = "serial"				# Default communication port
	serial_address = "/dev/ttyAMA0"
	i2c_address = 0x40   			# 7 bit address (will be left shifted)
	serial_baudrate = 9600
	serport = None

#----------------------------------------------------------------------
# open

	def _get_open(self):
		if self.port in ports:
			self.status=self.port
			if (self.port=="serial"):
				self.serport=serial.Serial(self.serial_address,baudrate=self.serial_baudrate,timeout=0.1)
			else:
                                if (_i2c_available==True):
                                        self._open_i2c_port(ports.index(self.port))
                                else:
                                        raise PiVideoException("Python smbus module must be installed for I2C communication")
			if not self.status:
				raise PiVideoException("Unable to communicate with video processor")
		else:
			raise PiVideoException("Bad communication port specified")
			self.status=None
		return self.status

	def _set_open(self,value):
		self._set_port(value)
		_get_open()


	open = property(_get_open, _set_open, doc="""
		Opens the communication port to the video processor.
		""" )

#----------------------------------------------------------------------
# version

    	def _get_version(self):
        	self._check_video_open()
        	return format(self._read_video_register(4),'02X')+format(self._read_video_register(3),'02X')+format(self._read_video_register(5),'02X')

	def _set_version(self):
		raise PiVideoException("Version is read-only")

    	version = property(_get_version,_set_version, doc="""
        	Software version of the video processor
        	""" )

#----------------------------------------------------------------------
# id

    	def _get_id(self):
        	self._check_video_open()
		idstring=""
		for r in range(30,38):
			idstring=format(self._read_video_register(r),'02X')+idstring
        	return idstring

	def _set_id(self):
		raise PiVideoException("ID is read-only")

    	id = property(_get_id,_set_id, doc="""
        	Hardware ID of the video processor
        	""" )

#----------------------------------------------------------------------
# update

	def _prepare_for_update(self):
        	self._check_video_open()
		self._write_serial_video_register(4,238)
		return 0

	update = property(_prepare_for_update,_prepare_for_update, doc="""
        	Place processor in firmware update mode
        	""" )

#----------------------------------------------------------------------
# pivideo_port

	def _get_port(self):
		return self.port

	def _set_port(self, value):
		if value in ports:
			self.port=value
		else:
			raise PiVideoException("Bad communication port specified")
			self.port=None

	pivideo_port = property(_get_port, _set_port, doc="""
		Retrieves or sets the communication port used for the video processor.
		""" )

#----------------------------------------------------------------------
# pivideo_i2c_address

	def _get_i2caddr(self):
		return self.i2c_address

	def _set_i2caddr(self, value):
		i2c_address=value

	pivideo_i2c_address = property(_get_i2caddr, _set_i2caddr, doc="""
		Retrieves or sets the i2c address used for the video processor.
		""" )

#----------------------------------------------------------------------
# source

    	def _get_source(self):
        	self._check_video_open()
        	return sources[self._read_video_register(6)]
    	def _set_source(self, value):
        	self._check_video_open()
		if value in sources:
			source=value
			self._write_video_register(6,sources.index(source))
		else:
			raise PiVideoException("Bad source specified")

    	source = property(_get_source, _set_source, doc="""
        	Retrieves or sets the desired video source.
        	""" )

#----------------------------------------------------------------------
# active_source

    	def _get_actsource(self):
        	self._check_video_open()
        	return sources[self._read_video_register(11)]
    	def _set_actsource(self, value):
		_set_source(self,value)

    	active_source = property(_get_actsource, _set_actsource, doc="""
        	Retrieves or sets the desired video source.
        	""" )


#----------------------------------------------------------------------
# effect

    	def _get_effect(self):
        	self._check_video_open()
        	return effects[self._read_video_register(7)]
    	def _set_effect(self, value):
        	self._check_video_open()
		if value in effects:
			self._write_video_register(7,effects.index(value))
		else:
			raise PiVideoException("Bad effect specified")

    	effect = property(_get_effect, _set_effect, doc="""
        	Test modes and special effects.
        	""" )

#----------------------------------------------------------------------
# ready

    	def _get_ready(self):
        	self._check_video_open()
		return self._read_video_register(8);

	def _set_ready(self):
		raise PiVideoException("Ready is read-only")

    	ready = property(_get_ready,_set_ready, doc="""
        	Video processor is ready
        	""" )

#----------------------------------------------------------------------
# running

    	def _get_running(self):
        	self._check_video_open()
		return self._read_video_register(12);

	def _set_running(self):
		raise PiVideoException("Running is read-only")

    	running = property(_get_running,_set_running, doc="""
        	Raspberry Pi is accessing the camera port
        	""" )

#----------------------------------------------------------------------
# lock

    	def _get_lock(self):
        	self._check_video_open()
		if (self._read_video_register(9)):
			return self._read_video_register(10)
		else:
			return 0;

	def _set_lock(self):
		raise PiVideoException("Lock is read-only")

    	lock = property(_get_lock,_set_lock, doc="""
       		Video lock status:  0 = No video, 1 = NTSC, 2 = PAL
        	""" )

#----------------------------------------------------------------------
# config

    	def _get_config(self):
        	self._check_video_open()
		return self._read_video_register(6)

	def _set_config(self, value):
         	self._check_video_open()
		if value in config_actions:
			action=value
			self._write_video_register(15,config_actions.index(action))
		else:
			raise PiVideoException("Bad configuration action specified")

    	config = property(_get_config,_set_config, doc="""
       		Configuration action:  1 = Restore, 2 = Save, 3 = Reset; Read returns source
        	""" )

#----------------------------------------------------------------------
# led

    	def _get_led(self):
        	self._check_video_open()
        	return led_settings[self._read_video_register(14)]
    	def _set_led(self, value):
        	self._check_video_open()
		if value in led_settings:
			self._write_video_register(14,led_settings.index(value))
		else:
			raise PiVideoException("Bad LED setting specified")

    	led = property(_get_led, _set_led, doc="""
        	LED Control.
        	""" )
#----------------------------------------------------------------------
# command

    	def _get_command(self):
        	self._check_video_open()
		result=self._read_video_register(25)
		result=(result<<8)+self._read_video_register(24)
		result=(result<<8)+self._read_video_register(23)
		result=(result<<8)+self._read_video_register(22)
		return hex(result)

	def _set_command(self, value):
         	self._check_video_open()
		if (self._read_video_register(16)==0):
			try:
				self._write_video_register(18,int(value[0:2],16))
				self._write_video_register(19,int(value[2:4],16))
				self._write_video_register(20,int(value[6:8],16))
				self._write_video_register(21,int(value[4:6],16))
				if (len(value)==16):
					self._write_video_register(22,int(value[14:16],16))
					self._write_video_register(23,int(value[12:14],16))
					self._write_video_register(24,int(value[10:12],16))
					self._write_video_register(25,int(value[8:10],16))
			except:
				raise PiVideoException("Invalid command string")
			else:
				if (len(value)==8):
					self._write_video_register(16,1)
				elif (len(value)==16):
					self._write_video_register(16,2)
				else:
					raise PiVideoException("Command must be 8 or 16 hex characters")
				result=1;
				while (result):
					result=self._read_video_register(16)
				result=self._read_video_register(17)
				return result
		else:
			raise PiVideoException("Video processor is busy - command not processed")

    	command = property(_get_command,_set_command, doc="""
       		Process command:  RESERVED
        	""" )

#----------------------------------------------------------------------
# _open_i2c_port

	def _open_i2c_port(self,port_number):
		global video_i2c
		if port_number < 2:
			try:
				video_i2c = smbus.SMBus(port_number)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
			except:
				raise PiVideoException("Port not available - make sure it is enabled")
			else:
				retrycount = 0
				self.status=None
				while (retrycount < 4):		
					if  not self.status:
						try:
							video_i2c.write_quick(self.i2c_address)
						except IOError:
							self.status=None
						else:
							self.status=self.port
					retrycount+=1
				if not self.status:		
					raise PiVideoException("Video processor not found")
		else:
			# Serial
			print("Serial not supported yet")

#----------------------------------------------------------------------
	def _check_video_open(self):
		if not self.status:
			raise PiVideoException("Cannot communicate with video processor")
		
#----------------------------------------------------------------------
	def _write_i2c_video_register(self,address,value):
		retrycount = 0
		while (retrycount < 4):
			try:
				video_i2c.write_byte_data(self.i2c_address,address,value)
				retrycount=10
			except IOError:
				retrycount+=1
				time.sleep(.02)
		if (retrycount < 10):
			raise PiVideoException("Video processor communication error")			
		
#----------------------------------------------------------------------
	def _read_i2c_video_register(self,address):
		retrycount = 0
		while (retrycount < 4):
			try:
				video_i2c.write_byte(self.i2c_address,address)
				value=video_i2c.read_byte(self.i2c_address)
				retrycount=10
				return value
			except IOError:
				retrycount+=1
				time.sleep(.02)
		if (retrycount < 10):
				raise PiVideoException("Video processor communication error")		
		
#----------------------------------------------------------------------
	def _clear_serial_buffer(self):
		lastchar=" "
		while (lastchar<>""):
			lastchar=self.serport.read(1)

#----------------------------------------------------------------------
	def _write_serial_video_register(self,address,value):
		self._clear_serial_buffer()
		retrycount = 0
		while (retrycount < 4):
			try:
				self.serport.write("\xDD")
				self.serport.write("\xDF")
				self.serport.write(chr(address))
				self.serport.write(chr(value))
				retrycount=10
			except IOError:
				retrycount+=1
				time.sleep(.02)
		if (retrycount < 10):
			raise PiVideoException("Video processor communication error")			
		
#----------------------------------------------------------------------
	def _read_serial_video_register(self,address):
		self._clear_serial_buffer()
		retrycount = 0
		while (retrycount < 4):
			try:
				self.serport.write("\xDD")
				self.serport.write("\xDE")
				self.serport.write(chr(address))
				value=self.serport.read(1)			
				retrycount=10
				return ord(value)
			except IOError:
				retrycount+=1
				time.sleep(.02)
		if (retrycount < 10):
				raise PiVideoException("Video processor communication error")		

#----------------------------------------------------------------------
	def _write_video_register(self,address,value):
		if self.status:
			if (self.status=="serial"):
				self._write_serial_video_register(address,value)
			else:
				self._write_i2c_video_register(address,value)
		
#----------------------------------------------------------------------
	def _read_video_register(self,address):
		if self.status:
			if (self.status=="serial"):
				return self._read_serial_video_register(address)
			else:
				return self._read_i2c_video_register(address)


#----------------------------------------------------------------------

class PiVideoException(Exception):
	pass
