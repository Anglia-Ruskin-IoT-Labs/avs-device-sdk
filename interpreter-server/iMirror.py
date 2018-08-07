#!/usr/bin/python3
import requests
import json

class IMirror:
	# -------------------------------------
	# Attributes
	# -------------------------------------
	
	# -------------------------------------
	# Constructor
	# -------------------------------------
	def main(self, _ip, _port, _alexaEndpoint):
		self.IP = _ip
		self.PORT = _port
		self.ENDPOINT = _alexaEndpoint
	
	
	
	# -------------------------------------
	# Public Methods
	# -------------------------------------
	def PrintReading(self, _buzzbox, _title, _text):
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
		url = self.UrlConstructor(self.ENDPOINT)
		payload = { 'title' : _title ,
					'text' : _text }
		headers = {'content-type': 'application/json'}

		response = requests.post(url, data=json.dumps(payload), headers=headers, verify = False)
	

	def HandleCommand(self, _title, _text):
		print ("Command Routed to iMirror")
		url = self.UrlConstructor("toggle?command=")
		text = self.TextCleanup(_text)
		if "clock" in text or "time" in text:			
			url += ("clock-" + str(self.OnOff(text)))
		elif "news" in text:
			url += ("news-" + str(self.OnOff(text)))
		elif "sensors" in text:
			url += ("board-" + str(self.OnOff(text)))
		elif "weather" in text:
			url += ("weather-" + str(self.OnOff(text)))
		elif "guide" in text:
			url += ("guide-" + str(self.OnOff(text)))
		elif "everything" in text:
			url += str(self.OnOff(text))
		else:
			pass
		print (url)
		response = requests.get(url, verify = False)
	
	
	
	
	# -------------------------------------
	# Private Methods
	# -------------------------------------
	
	def OnOff(self, text):
		if "showing" in text:
			return "on"
		elif "hiding" in text:
			return "off"
			
		
	def UrlConstructor(self, _endpoint):
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
