#!/usr/bin/python

######################################################################
#
#  PiVideo control program
#  Copyright(c) 2015 by Lintest Systems LLC
#
######################################################################
#
#  Revision History
#	0.1	Initial Version
#
 
import argparse
import serial
import os
import time
import sys
try:
        import smbus
        _i2c_available = True
except:
        _i2c_available = False
import pivideo

#---------------------------------------------------------------------------------
def main():
	queries=['all','ready','running','lock','source','effect','led','version','id','cmd']
	
	parser = argparse.ArgumentParser(description='PiVideo control program version 0.1    Lintest Systems LLC')
	parser.add_argument('--verbose','-v',action='count',help='Trace communications with with video processor')
	parser.add_argument('--port','-p',default='serial',choices=pivideo.ports,help='Specify the communication port for the video processor')
	parser.add_argument('--address','-a',help='Specify the address used for the selected port')
	parser.add_argument('--source','-s',choices=pivideo.sources,help='Select the source input')
	parser.add_argument('--query','-q-',choices=queries,help='Query the status of the video processor')
	parser.add_argument('--effect','-e',choices=pivideo.effects,help='Select special effect or test video')
	parser.add_argument('--led','-l',choices=pivideo.led_settings,help='Control LED status display')
	parser.add_argument('--update','-update',help='Update the PiVideo software')
	parser.add_argument('--force','-force',help='Force update using downlevel PiVideo software')
	parser.add_argument('--config','-c',choices=pivideo.config_actions,help='Save settings as the power-on default')
	parser.add_argument('--command','-cmd',help='RESERVED')
	parser.add_argument('--script','-script',help='Process a Lintest-supplied script file')
	
	args = parser.parse_args()
	
	# Check for OS support installed
	if not _check_os_camera_support():
		print "  Make sure camera support is enabled on your system"

	if args.verbose:
		print "  Port used for video processor is: ",args.port

	# Establish communication with the video processor
	vid=pivideo.PiVideo()
	vid.pivideo_port=args.port
	if not (vid.pivideo_port=="serial"):
		if (_i2c_available==True):
			vid.pivideo_i2c_address=args.address
		else:
			print "  Python smbus module not found - install to use I2C communication"
	try:	
		pivideo_port=vid.open
	except pivideo.PiVideoException, e:
		print "  Video Processor was not found - please check your switches and settings"
                print " ",e
	
	else:	# Process the commands
		if args.source:
			vid.source=args.source
			if args.verbose:
				print "  Source is: ",args.source
	
		if args.effect:
			vid.effect=args.effect
			if args.verbose:
				print "  Effect set: ",args.effect

		if args.led:
			vid.led=args.led
			if args.verbose:
				print "  LED setting is: ",args.led
	
		if args.config:
			vid.config=args.config
			if args.verbose:
				print "  Configuration:  ",args.config
	
		if args.query:
			result=vid.ready
			if (args.query=='all') | (args.query=='ready'):
				if result:
					print "  Video processor is ready"
				else:
					print "  Video processor is NOT READY"
			if (args.query=='all') | (args.query=='lock'):
				result=vid.lock
				if (result==0):
					print "  No active video detected"
				if (result==1):
					print "  Active video:  NTSC"
				if (result==2):
					print "  Active video:  PAL"
			if (args.query=='all'):
				print "  Selected video source is: ",vid.source
			if (args.query=='all') | (args.query=='source'):
				result=vid.active_source
				print "  Active video source is: ",result
			if (args.query=='all') | (args.query=='running'):
				result=vid.running
				if result:
					print "  Raspberry Pi camera port is active"
				else:
					print "  Raspberry Pi camera port is not active"
			if (args.query=='all') | (args.query=='effect'):
				result=vid.effect
				if not result=='none':
					if (result=='colorbar'):
						print "  Effect set to Color Bars"
					if (result=='bw'):
						print "  Effect set to Black & White"
			if (args.query=='all') | (args.query=='led'):
				result=vid.led
				if not result=='normal':
					if (result=='min'):
						print "  Basic LED display"
					if (result=='off'):
						print "  LEDs off"
			if (args.query=='all') | (args.query=='version'):
				result=vid.version
				print "  Video processor software version: ",result
			if ((args.query=='all') & (args.verbose==1)) | (args.query=='id'):
				result=vid.id
				print "  Video processor hardware id: ",result
			if (args.query=='cmd'):
				result=vid.command
				print "  ",result

		if args.update:
			Update_Software(vid,args.update,False)
	
		if args.force:
			Update_Software(vid,args.force,True)
	
		if args.command:
			vid.command=args.command
			if (len(args.command)==8):
				print "  Command result:  ",vid.command
	
		if args.script:
			Process_Script(vid,args.script)

#----------------------------------------------------------------------
# Check for OS camera support installed

def _check_os_camera_support():
	try:
		ossupport = os.popen('vcgencmd get_camera').readline()
	except:
		return False
	else:
		if (ossupport.count("=1")>=1):	# return value should be "supported=1 detected=1"
			return True
		else:
			return False
		
#----------------------------------------------------------------------
# Clear serial buffer

def _clear_serial_buffer(vid):
	lastchar=" "
	while (lastchar<>""):
		lastchar=vid.serport.read(1)

#----------------------------------------------------------------------
# UPDATE SOFTWARE

def Update_Software(vid,filename,force):
	vid._check_video_open()
	if (vid.status!="serial"):
		print "Software update is only supported over serial connection"
	else:
		try:
			updatefile=open(filename);
		except:
			raise PiVideoException("Update file not found")
		else:
			hexfilesize=os.stat(filename).st_size
			fccount=0
			success=True
			print
			print "Updating software from file ",filename
			print
			_clear_serial_buffer(vid)
			for line in updatefile:
				lccount=0
				if (fccount==0):
					if (line[0:2]=="LT"):
						fccount=3
						cversion=vid.version
						cv1=int(cversion[2:4],16)
						cv2=int(cversion[4:6],16) & 192
						cv3=int(cversion[6:8],16)
						uv1=int("0"+line[2:4],16)
						uv2=int("0"+line[4:6],16)
						uv3=int("0"+line[6:8],16)
						if (uv1<=cv1):
							print "Warning: update file version is older than the current version"
							if not force:
								success=False
								break
						elif (uv2!=cv2):
							print "Software update error:  video engine version mismatch"
							if not force:
								success=False
								break
						elif (uv3!=cv3):
							print "Software update error:  incompatible version"
							if not force:
								success=False
								break
						vid.update
						_clear_serial_buffer(vid)
					else:
						print "Not a valid PiVideo update file"
						success=False
						break;
				elif (line[0]=="#"):
					print line[1:]
				elif (line[0]==':'):
					tryagain=True
					while (tryagain):
						for character in line:
							lccount+=1
							if (ord(character)!=10):
								vid.serport.write(character)
						time.sleep(0.05)
						if (vid.serport.inWaiting()>=3):
							a=vid.serport.read(1)
							b=vid.serport.read(1)
							c=vid.serport.read(1)	
							tryagain=(b!=chr(6))					
					_clear_serial_buffer
					fccount+=lccount
					percent=int(fccount*100/hexfilesize)
					sys.stdout.write("\r Software update in progress:  %d%%" % percent)
					sys.stdout.flush()
			if success:
				print "\rUpdate complete - video processor will now restart"
			else:
				print "\rUpdate was not completed                          "
		finally:
			print
			updatefile.close()

#----------------------------------------------------------------------
# PROCESS SCRIPT

def Process_Script(vid,filename):
	vid._check_video_open()
	try:
		scriptfile=open(filename);
	except:
		raise PiVideoException("Script file not found")
	else:
		success=True
		print
		print "Processing script file ",filename
		print
		for line in scriptfile:
			if (line[0]=="#"):
				print line[1:]
			elif (line[0]==","):
				time.sleep(len(line)*0.1)
			elif (len(line)>=16):
				vid.command=line[0:16]
			else:
				print "Invalid script entry:  ",line
	finally:
		print
		scriptfile.close()

#----------------------------------------------------------------------
main()
