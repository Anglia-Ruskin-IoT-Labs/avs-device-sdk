#!/usr/bin/python3
from flask import Flask, request, jsonify
import json
from threading import Thread
from config import Config
from buzzcommander import Buzzbox
from tests import Tests
from iMirror import IMirror

# Loading configs from file into an object
config = Config()
# Fire up buzzbox controller
buzzbox = Buzzbox(config.BuzzboxIP, config.BuzzboxPORT,
				  config.BuzzboxLIGHTS, config.BuzzboxLEDS)
mirror = IMirror(config.iMirrorIP, config.iMirrorPORT, config.iMirrorENDPOINT)
# Fire up the Flask webserver
app = Flask(__name__)

def CommandRouter(_json):
	payload = json.loads(_json)
	try:
		# Extraction from desired cards
		subtitle = payload["directive"]["payload"]["title"]["subTitle"]
		mainTitle = payload["directive"]["payload"]["title"]["mainTitle"]
		textField = payload["directive"]["payload"]["textField"]
	except KeyError:
		# Payload different than expected,
		# Possibly not own skill
		subtitle = ""
		mainTitle = ""
		textField =  ""
	# Call came from the right skill 
	if mainTitle == "BuzzBox Command Centre":
		thread = Thread(target = mirror.UpdateAlexaFrame, args = (mainTitle, textField, ))
		thread.start()
		thread.join()
		# Sends the command to the buzzbox
		print (str(buzzbox.Command(mainTitle, textField)))		
	elif mainTitle == "BuzzBox Information Centre":
		thread = Thread(target = mirror.PrintReading, args = (buzzbox, mainTitle, textField, ))
		thread.start()
		thread.join()
	elif mainTitle == "iMirror Command Centre":
		mirror.HandleCommand(mainTitle, textField)
	# Json wasn't parsed
	elif mainTitle == "":
		pass
	# Json was parsed but it is not a special or implemented skill,
	# just print
	else:
		mirror.UpdateAlexaFrame(mainTitle, textField)

#test = Tests()
#test.BuzzboxControlTest(buzzbox)


@app.route('/command', methods=['POST'])
def hello():
	#Format raw json data
	content = str(request.get_data())
	content = content[2:-5]
	content = content.replace("\\", "")
	#start up a CommandRouter
	thread = Thread(target = CommandRouter, args = (content, ))
	thread.start()
	thread.join()
	#print(content)
	return 'Hello, World!'


# Running webserver
app.run('localhost', 50000, threaded=True, debug=False)
# Nothing runs below this line
