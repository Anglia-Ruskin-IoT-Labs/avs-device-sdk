#!/usr/bin/python3
import requests
import json

class IMirror:
		
	# -------------------------------------
	# Constructor
	# -------------------------------------
	def main(self, _ip, _port, _alexaEndpoint):
		self.IP = _ip
		self.PORT = _port
		self.ENDPOINT = _alexaEndpoint
		# -------------------------------------
		# Attributes
		# -------------------------------------
		self.toggleWidgetKey = 'widget'
		self.toggleStateKey = 'state'
		self.moveWidgetKey = 'widget'
		self.movePositionKey = 'position'
		self.movePositionValues = [
			'TOPLEFT', 'TOPMID',
			'TOPRIGHT', 'MIDLEFT',
			'MIDMID', 'MIDRIGHT',
			'BOTLEFT', 'BOTMID', 
			'BOTRIGHT']
	
	
	
	# -------------------------------------
	# Public Methods
	# -------------------------------------
	def ShowReading(self, _buzzbox, _title, _text):
		reading = _buzzbox.GetReadings(_title, _text)
		displayedText = _text
		displayedText += " "
		try:
			reading = reading.replace("\\n'", "")
			reading = reading.replace("b'", "")
			reading = reading.split(" ", 1)
			displayedText += reading[1]
		except AttributeError:
			pass
		print(displayedText)
		self.UpdateAlexaFrame(_title, displayedText)
	
	
	def UpdateAlexaFrame(self, _title, _text):
		url = self.__UrlConstructor(self.ENDPOINT)
		payload = { 'title' : _title ,
					'text' : _text }
		headers = {'content-type': 'application/json'}

		response = requests.post(url, data=json.dumps(payload), headers=headers, verify = False)
	

	def HandleCommand(self, _title, _text):		
		print ("Command Routed to iMirror")
		text = self.TextCleanup(_text)
		headers = {'content-type': 'application/json'}	
		jsonPayload = dict()
		if "moving" in text:
			url = self.__UrlConstructor("move")
			jsonPayload[self.moveWidgetKey] = self.__GetWidget(text)
			jsonPayload[self.movePositionKey] = self.__GetPosition(text)			
		elif "showing" in text or "hiding" in text:
			url = self.__UrlConstructor("toggle")
			jsonPayload = dict()
			jsonPayload[self.toggleStateKey] = self.__GetState(text)
			jsonPayload[self.toggleWidgetKey] = self.__GetWidget(text)
		else:
			return
		r = requests.post(url, data=json.dumps(jsonPayload), headers=headers, verify = False)
		print("Payload: " + str(jsonPayload) + "\nResponse: " + str(r.json()))	
	
	# -------------------------------------
	# Private Methods
	# -------------------------------------
	def __GetWidget(self, text: str) -> str:
		if "clock" in text or "time" in text:			
			return 'clock'
		elif "news" in text:
			return 'news'
		elif "sensors" in text:
			return 'sensors'
		elif "weather" in text:
			return 'weather'
		elif "guide" in text:
			return 'guide'
		elif "everything" in text:
			return 'all'
		elif "conversation" in text:
			return "alexa"
		elif "notification" in text:
			return "notif"
		else:
			return ''
				
	def __GetPosition(self, text: str) -> str:
		result = ""
		if "top" in text:
			result += "TOP"	
		elif "bottom" in text:
			result += "BOT"
		elif "middle" in text:
			result += "MID"
		else:
			pass
		
		if "left" in text:
			result += "LEFT"
		elif "right" in text:
			result += "RIGHT"
		elif "middle" in text:
			result += "MID"
		else:
			pass			
		return result
		
	def __GetState(self, text):
		if "showing" in text:
			return "on"
		elif "hiding" in text:
			return "off"
		
			
		
	def __UrlConstructor(self, _endpoint):
		return ("https://" + self.IP + ":" + self.PORT + "/" + _endpoint)
		
	def TextCleanup(self, _text):
		''' Text formatting and cleanup
		'''
		text = _text.lower()
		text = text.replace(":", "")
		text = text.replace(".", "")
		text = text.split()
		return set(text)
		
	
	# -------------------------------------
	# Init
	# -------------------------------------
	def __init__(self, _ip, _port, _endpoint):
		self.main(_ip, _port, _endpoint)
