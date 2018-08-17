#!/usr/bin/python3
import os
import sys
# Change working directory of this scripts directory, if it is run from somewhere else
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

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
# iMirror Controller
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
	except KeyError:	# Payload different than expected, possibly not own skill.
		subtitle = ""
		mainTitle = ""
		textField =  ""
	if mainTitle == "BuzzBox Command Centre":				# Call came to the BuzzBox
		thread = Thread(target = mirror.UpdateAlexaFrame,
			args = (mainTitle, textField, ))
		thread.start()
		thread.join()
		print (str(buzzbox.Command(mainTitle, textField)))	# Sends the command to the buzzbox
	elif mainTitle == "BuzzBox Information Centre":
		thread = Thread(target = mirror.ShowReading, 
			args = (buzzbox, mainTitle, textField, ))
		thread.start()
		thread.join()
	elif mainTitle == "iMirror Command Centre":				# Call came to the iMirror
		mirror.HandleCommand(mainTitle, textField)
	elif mainTitle == "": 									# Json wasn't parsed
		pass
	else:													# Json parsed but sender skill unknown
		mirror.UpdateAlexaFrame(mainTitle, textField)

#test = Tests()
#test.BuzzboxControlTest(buzzbox)


@app.route('/command', methods=['POST'])
def hello():
	# Format raw json data
	content = str(request.get_data())
	content = content[2:-5]
	content = content.replace("\\", "")
	# start up a CommandRouter
	thread = Thread(target = CommandRouter, args = (content, ))
	thread.start()
	thread.join()
	return jsonify({'response': 'received'})


app.run('localhost', 50000, threaded=True, debug=False)
# Nothing runs below this line
