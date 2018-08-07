#!/usr/bin/python3
import socket    # used for TCP/IP communication 
import smtplib   # used to send email report
import time      # used to insert current date in email report
import threading


class Buzzbox():
	# Constructor, saving constants
	def main(self, _ip, _port, _light, _led):
		self.BUZZBOX_IP = _ip
		self.BUZZBOX_PORT = int(_port)
		self.LEDNUM = int(_led)
		self.LIGHTNUM = int(_light)
		
	def TextCleanup(self, _text):
		''' Text formatting and cleanup
		'''
		text = _text.lower()
		text = text.replace(":", "")
		text = text.replace(".", "")
		text = text.split()
		return set(text)
		
	def Command(self, _title, _text):
		""" Decision tree sends commands
			to the BuzzBox based on the
			input text. Returns string
			feedback if command went
			to the Box,
			returns None if command was
			not valid.
		"""
		text = self.TextCleanup(_text)
		# Preventin guide text to get through
		# by limiting length
		if not len(text) > 5:
			# Decisions based on Alexa textfield
			# containing words
			if "turning" in text:
				if "heater" in text:
					command = "HEATER_"
					if "on" in text:
						command += "ON"
					elif "off" in text:
						command += "OFF"
					else:
						return
					return self.__ContactBuzzBox((command))
					
				elif "fan" in text:
					command = "FAN_"
					if "on" in text:
						command += "ON"
					elif "off" in text:
						command += "OFF"
					else:
						return
					return self.__ContactBuzzBox((command))
					
				elif "light" in text:
					for item in text:
						if item.isdigit():
							lightNum = int(item)
					if lightNum <= self.LIGHTNUM and lightNum > 0:
						return self.__ContactBuzzBox((self.__LightCommandBuilder(lightNum, text)))
						
				elif "led" in text:
					for item in text:
						if item.isdigit():
							ledNum = int(item)                       
					if ledNum <= self.LEDNUM and ledNum > 0:
						return self.__ContactBuzzBox(self.__LedCommandBuilder(ledNum, text))
								
				elif "lights" in text:
					messages = []
					for x in range(1 , (self.LIGHTNUM + 1)):
						messages.append(str(self.__ContactBuzzBox(self.__LightCommandBuilder(x, text))))
					return messages
						
				elif "leds" in text:
					command = "LEDS_ALL"
					if "off" in _text:
						command += "OFF"
					elif "red" in _text or "on" in _text:
						command += "R"
					elif "yellow" in _text:
						command += "Y"
					elif "green" in _text:
						command += "G"
					
					return self.__ContactBuzzBox(command)
						
				elif "all" in text or "everything" in text:
					if "on" in text:
						state = "ON"
					elif "off" in text:
						state = "OFF"
					else:
						return
					messages = []
					# LEDs
					if state == "ON":				
						messages.append(self.__ContactBuzzBox(("LEDS_ALLR")))
					else:
						messages.append(self.__ContactBuzzBox(("LEDS_ALLOFF")))
					# Lights
					for x in range(1 , (self.LIGHTNUM + 1)):
						messages.append(str(self.__ContactBuzzBox(self.__LightCommandBuilder(x, text))))
					# Heater and Fan
					messages.append(self.__ContactBuzzBox(("HEATER_" + state)))
					messages.append(self.__ContactBuzzBox(("FAN_" + state)))
					return messages
				elif "reading" in text and ("display" in text or
											"interface" in text):
					if "on" in text:
						state = "ON"
					elif "off" in text:
						state = "OFF"
					else:
						return
					# TODO iMirror connection
					return "Reading display turned " + state
				else:
					return
		   
	def GetReadings(self, _title, _text):
		text = self.TextCleanup(_text)
		if not len(text) > 5:
			if "displaying" in text:
				command = "GET_"
				if "motion" in text and "sensor ":
					command += "MOTION"
					return self.__ContactBuzzBox((command))                     
				elif "heater" in text:
					command += "HEATER"
					return self.__ContactBuzzBox((command))
				elif "fan" in text:
					command += "FAN"
					return self.__ContactBuzzBox((command))
				elif "light" in text and "level" in text:
					command += "LUX"
					return self.__ContactBuzzBox((command))
				elif "light" in text:
					command += "LIGHT"
					for item in text:
						if item.isdigit():
							lightNum = int(item)
					if lightNum <= self.LIGHTNUM and lightNum > 0:
						command += str(lightNum)
						return self.__ContactBuzzBox(command)
				elif "led" in text:
					command += "LED"
					for item in text:
						if item.isdigit():
							ledNum = int(item)
					if ledNum <= self.LEDNUM and ledNum > 0:
						command += str(ledNum)
						return self.__ContactBuzzBox(command)
				elif "temperature" in text:
					command += "TEMPERATURE"
					return self.__ContactBuzzBox((command))
				else:
					return
			else:
				return
	#-----------------------------------------------
	# SUPPORT METHODS
	#-----------------------------------------------
		
	def __ContactBuzzBox(self, _command):
		# Prepare 3-byte control message for transmission
		TCP_IP = self.BUZZBOX_IP
		TCP_PORT = self.BUZZBOX_PORT
		BUFFER_SIZE = 80
		command = _command + "\n"
		command = command.encode('UTF-8')
		## possible commands: HELLO\n , 
		MESSAGE = command # Relays 1 permanent off     
		# Open socket, send message, close socket
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(0.75)
		try:
			s.connect((TCP_IP, TCP_PORT))
			s.send(MESSAGE)
			data = s.recv(BUFFER_SIZE)
			s.close()
			return (_command + ": " + str(data))
		except socket.error:
			return "Connection to box not available"
		
	def SendCommand(self, _command):
		return self.__ContactBuzzBox(_command)

	def __LedCommandBuilder(self, _ledNum, _text):
		''' Builds command for the leds
			according their number and the
			asked state. Returns the complete
			command.
		'''
		command = "LED" + str(_ledNum) + "_"
		if "off" in _text:
			command += "OFF"
		elif "red" in _text or "on" in _text:
			command += "R"
		elif "yellow" in _text:
			command += "Y"
		elif "green" in _text:
			command += "G"
		return command

	def __LightCommandBuilder(self, _lightNum, _text):
		''' Builds command for the lights
			according their number and the
			asked state. Returns the complete
			command.
		'''
		command = "LIGHT" + str(_lightNum) + "_"
		if "on" in _text:
			command += "ON"
		elif "off" in _text:
			command += "OFF"
		elif "blink" in _text:
			command += "BLINK"
		else:
			return
		return command
	
	def __init__(self, _ip, _port, _light, _led):
		self.main(_ip, _port, _light, _led)
