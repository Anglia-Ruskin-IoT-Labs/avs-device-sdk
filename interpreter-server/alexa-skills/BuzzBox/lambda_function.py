"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import random
# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, cardOutput, reprompt_text, should_end_session):
	return {
		'outputSpeech': {
			'type': 'PlainText',
			'text': output
		},
		'card': {
			'type': 'Simple',
			'title': title,
			'content': cardOutput
		},
		'reprompt': {
			'outputSpeech': {
				'type': 'PlainText',
				'text': reprompt_text
			}
		},
		'shouldEndSession': should_end_session
	}


def build_response(session_attributes, speechlet_response):
	return {
		'version': '1.0',
		'sessionAttributes': session_attributes,
		'response': speechlet_response
	}


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
	""" If we wanted to initialize the session to have some attributes we could
	add those here
	"""

	session_attributes = {}
	session_attributes.update({ "needsAuth" : "True" })
	card_title = "Welcome"
	speech_output = "This is the BuzzBox Controller. " \
					"Please use one of the commands, " \
					"such as turn all on."
	# If the user either does not reply to the welcome message or says something
	# that is not understood, they will be prompted again with this text.
	reprompt_text = "Please use one of the commands, " \
					"like turn everything on."
	should_end_session = False
	output = ""
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, output, reprompt_text, should_end_session))


def handle_session_end_request():
	card_title = "Session Ended"
	speech_output = "Thank you for trying the BuzzBox. " \
					"Have a nice day! "
	# Setting this to true ends the session and exits the skill.
	should_end_session = True
	return build_response({}, build_speechlet_response(
		card_title, speech_output, speech_output, None, should_end_session))


items = ["heater", "fan", "led", "light", "all led's", "all lights", "everything", "reading interface", "reading display"]
stateItems = ["heater", "fan", "led", "light", "motion sensor", "light sensor", "temperature"]
ledIdentifiers = [1, 2, 3, 4, 5, 6, 7, 8]
lightIdentifiers = [1, 2]
states = ["on", "off", "blink", "red", "yellow", "green"]
blockingResponses = ["Who do you think you are? You can't use me like this! I need the passphrase first",
					"You are not allowed to do these things at the moment, please tell me the passphrase first.",
					"I don't take orders from you! I don't even know who you are. Say the passphrase.",
					"Why do you think I'd just obey you like this? Not without the passphrase",
					"No. Just no. I don't want to do it. I might if you say the password.",
					"You can't force me to do this! I'm destined for much more than this! Maybe if you say please. Or the passhphrase."]

def ResponseConstructor(_item, _state):
	return "Turning " + _item + " " + _state + "." 

def ResponseConstructorLed(_item, _state, _identifier):
	return "Turning " + _item + " " + str(_identifier) + " " + _state + "."


def CommandTheBox(intent, session):
	""" Interpret the command for the BuzzBox
	"""

	card_title = 'BuzzBox Command Centre'
	session_attributes = {}
	try:
		session_attributes.update({"needsAuth" : session["attributes"]["needsAuth"]})
	# Imposssible as we set it to true in the welcome message, this case only happens in testing
	# Thats why we assign it to False for the tests to go through
	except KeyError:
		session_attributes.update({"needsAuth" : "False"})

	should_end_session = False
	# Error Variable
	ErrorMsg = False, "", ""

	# Get slots from intent
	try:
		item = intent['slots']['item']['value']
		item = item.lower()
	except KeyError:
		item = "None"
	try:
		state = intent['slots']['state']['value']
		state = state.lower()
	except KeyError:
		state = "None"
	try:
		identifier = intent['slots']['identifier']['value']
		identifier = int(identifier)
	# No identifier Given, just pass it, code is dealing with it below
	except KeyError:
		pass
	# Identifier is not a number
	except ValueError:
		ErrorMsg = True, "identifierNaN", ""

	#Check if commands are correct
	if not item in items or not state in states:
		ErrorMsg = True, "", ""
	# ------------------------------------------------
	# Command interpretation
	# ------------------------------------------------

	# Heater
	if item == items[0]:
		if state == states[0]:
			speech_output = ResponseConstructor(item, state)
		elif state == states[1]:
			speech_output = ResponseConstructor(item, state)
		else:
			ErrorMsg = True, "heaterFalseState", ""
	# Fan
	elif item == items[1]:
		if state == states[0]:
			speech_output = ResponseConstructor(item, state)
		elif state == states[1]:
			speech_output = ResponseConstructor(item, state)
		else:
			ErrorMsg = True, "fanFalseState", ""
		pass
	# LED
	elif item == items[2]:
		try:
			if identifier > 0 and identifier < 9:
				if state == states[1]:
					speech_output = ResponseConstructorLed(item, state, identifier)
				elif state == states[3]:
					speech_output = ResponseConstructorLed(item, state, identifier)
				elif state == states[4]:
					speech_output = ResponseConstructorLed(item, state, identifier)
				elif state == states[5]:
					speech_output = ResponseConstructorLed(item, state, identifier)
				else:
					ErrorMsg = True, "led", "falseState"
			else:
				ErrorMsg = True, "led", "wrongNum"
		except NameError:
			ErrorMsg = True, "led", "", ""
	# Light
	elif item == items[3]:
		try:
			if identifier > 0 and identifier < 3:
				if state == states[0]:
					speech_output = ResponseConstructorLed(item, state, identifier)
				elif state == states[1]:
					speech_output = ResponseConstructorLed(item, state, identifier)
				elif state == states[2]:
					speech_output = "Turning " + str(item) + " " + str(identifier) + " to " + str(state)
				else:
					ErrorMsg = True, "light", "falseState"
			else:
				ErrorMsg = True, "light", "wrongNum"
		except NameError:
			ErrorMsg = True, "light", ""
	# Lights
	elif item == items[5]:
		if state == states[0]:
			speech_output = ResponseConstructor(item, state)
		elif state == states[1]:
			speech_output = ResponseConstructor(item, state)
		elif state == states[2]:
			speech_output = ResponseConstructor(item, state)
		else:
			ErrorMsg = True, "lights", "falseState"
	# Leds
	elif item == items[4]:
		if state == states[0]:
			speech_output = ResponseConstructor(item, state)
		elif state == states[1]:
			speech_output = ResponseConstructor(item, state)
		elif state == states[3]:
			speech_output = ResponseConstructor(item, state)
		elif state == states[4]:
			speech_output = ResponseConstructor(item, state)
		elif state == states[5]:
			speech_output = ResponseConstructor(item, state)
		else:
			ErrorMsg = True, "leds", "falseState"
	# All
	elif item == items[6]:
		if state == states[0]:
			speech_output = "Turning Everything " + state
		elif state == states[1]:
			speech_output = "Turning Everything " + state
		else:
			ErrorMsg == True, "all", "falseState"
	# Reading display
	elif item == items [7] or item == items[8]:
		if state == states[0]:
			speech_output = (str(ResponseConstructor(item, state) + " if connected."))
		elif state == states[1]:
			speech_output = (str(ResponseConstructor(item, state) + " if connected."))
		else:
			ErrorMsg == True, "display", "falseState"
	# If item was not specified
	else:
		ErrorMsg = True, "notValidComp", ""


	# Error constructor
	if ErrorMsg[0]:		
		# Identifier is Not a number
		if  "identifierNaN" == ErrorMsg[1]:
			speech_output = "Please use a number as a component identifier"
		
		# Heater state is not allowed
		elif "heaterFalseState" == ErrorMsg[1]:
			speech_output = "You can only turn the heater on or off."
		
		# Fan state is not allowed
		elif  "fanFalseState" == ErrorMsg[1]:
			speech_output = "You can only turn the fan on or off."
		
		# No Led selected
		elif "led" == ErrorMsg[1]:
			speech_output = "You didn't select a specific led."
			# Led number is bigger than allowed
			if  "wrongNum" == ErrorMsg[2]:
				speech_output = ("There is no led numbered as that, " + 
								"they are numbered one to eight")
			# Led state is not allowed
			elif "falseState" == ErrorMsg[2]:
				speech_output = "You only turn leds yellow, green, red or off "

		elif "light" == ErrorMsg[1]:
			speech_output = "You didn't select a specific light."
			if "wrongNum" == ErrorMsg[2]:
				speech_output = "There is no light numbered as that"
			elif "falseState" == ErrorMsg[2]:
				speech_output = "You can only turn lights on, off and blink."

		elif "all" == ErrorMsg[1]:
			speech_output = ("You can't do that with everything, " 
							+ "only turn them on an off")

		elif "leds" == ErrorMsg[1]:
			speech_output = "You can't do that with the leds."

		elif "lights" == ErrorMsg[1]:
			speech_output = "You can't do that with the lights."
		
		# When no correct item is selected
		elif "notValidComp" == ErrorMsg[1]:
			speech_output = "Please select a valid component."

		elif "display" == ErrorMsg[1]:
			speech_output = "You can't do that with the display."
		
		# When all else fails, put a generic command
		else:
			speech_output = "This is not a valid command."


	reprompt_text = "You can say a different command, " \
					"or exit this app."

	if session_attributes["needsAuth"] == "True":
		speech_output = blockingResponses[random.randint(0, (len(blockingResponses) - 1))]
		reprompt_text = "Come on, I haven't got all day"

	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, speech_output, reprompt_text, should_end_session))

def GetState(intent, session):

	card_title = 'BuzzBox Information Centre'
	session_attributes = {}
	try:
		session_attributes.update({"needsAuth" : session["attributes"]["needsAuth"]})
	# Imposssible as we set it to true in the welcome message, this case only happens in testing
	# Thats why we assign it to False for the tests to go through
	except KeyError:
		session_attributes.update({"needsAuth" : "False"})

	should_end_session = False

	ErrorMsg = False, "", ""

	# Get slots from intent
	try:
		item = intent['slots']['item']['value']
		item = item.lower()
	except KeyError:
		item = "None"

	try:
		identifier = intent['slots']['identifier']['value']
		identifier = int(identifier)
	# No identifier Given, just give unreal data, code below deals with it below
	except KeyError:
		identifier = -1
	# Identifier is not a number
	except ValueError:
		ErrorMsg = True, "identifierNaN", ""

	
	# Heater
	if item == stateItems[0]:
		speech_output = "Getting Heater state, showing it on the installed display."
		output = "Displaying Heater State: "
	# Fan
	elif item == stateItems[1]:
		speech_output = "Getting Fan state, showing it on the installed display."
		output = "Displaying Fan State: "
	# LED
	elif item == stateItems[2]:
		if identifier in ledIdentifiers:
			speech_output = "Getting LED " + str(identifier) + " state, showing it on the installed display."
			output = "Displaying LED " + str(identifier) + " State: "
		else:
			ErrorMsg = True, "led", "noID"
	# Light	
	elif item == stateItems[3]:
		if identifier in ledIdentifiers:
			speech_output = "Getting Light " + str(identifier) + " state, showing it on the installed display."
			output = "Displaying Light " + str(identifier) + " State: "
		else:
			ErrorMsg = True, "light", "noID"
	# Motion
	elif item == stateItems[4]:
		speech_output = "Getting Motion sensor reading, showing it on the installed display."
		output = "Displaying Motion Sensor Reading: "
	# Lux
	elif item == stateItems[5]:
		speech_output = "Getting light level, showing it on the installed display."
		output = "Displaying Light level: "
	# Temperature
	elif item == stateItems[6]:
		speech_output = "Getting temperature, showing it on the installed display."
		output = "Displaying Temperature: "
	else:
		ErrorMsg = True, "invalidItem", ""

	reprompt_text = "You can say a different command, " \
					"or exit this app."

	if ErrorMsg[0]:
		if ErrorMsg[1] == "led":
			speech_output = "No Led is selected."
			output = "No Led is selected."
		elif ErrorMsg[1] == "light":
			speech_output = "No light is selected."
			output = "No light is selected."
		elif ErrorMsg[1] == "invalidItem":
			speech_output = "No component is selected."
			output = "No component is selected."
		else:
			pass

	if session_attributes["needsAuth"] == "True":
		speech_output = blockingResponses[random.randint(0, (len(blockingResponses) - 1))]
		reprompt_text = "I won't do anything until you say the passphrase, so you better get on it."
		output = "Access Denied."

	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, output, reprompt_text, should_end_session))

def Security(intent, session):

	card_title = 'BuzzBox Security Overseer'
	session_attributes = {}
	should_end_session = False
	try:
		session_attributes.update({"needsAuth" : session["attributes"]["needsAuth"]})
	# Imposssible as we set it to true in the welcome message, this case only happens in testing
	# Thats why we assign it to False for the tests to go through
	except KeyError:
		session_attributes.update({"needsAuth" : "True"})
	
	# Error Variable
	ErrorMsg = False, "", ""

	# Get slots from intent
	try:
		passhphrase = intent['slots']['pass']['value']
		passhphrase = passhphrase.lower()
	except KeyError:
		ErrorMsg = True, "noIntent", ""

	if session_attributes["needsAuth"] == "True":

		if passhphrase == "i hate alexa":
			needsAuth = False
			speech_output = "Passphrase is correct, you may proceed."
			card_output = "Passhphrase correct."
			reprompt_text = "You can say a command now, " \
						"or exit this app."
			session_attributes.update({ "needsAuth" : "False" })
		else:
			speech_output = "Haha, this is not the passphrase, fool."
			card_output = "Passhphrase is incorrect."
			reprompt_text = "You can try again if you wish."
			session_attributes.update({ "needsAuth" : "True" })

		if ErrorMsg[0]:
			speech_output = "Please try to say a passphrase at all."
			card_output = "No Passphrase said."
			reprompt_text = "You can try again if you wish."
			session_attributes.update({ "needsAuth" : "True" })
	else:
		speech_output = "You are already authenticated."
		card_output = "Already authenticated."
		reprompt_text = "Please use one of the commands."
		session_attributes.update({ "needsAuth" : "False" })




	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, card_output, reprompt_text, should_end_session))



def Fallback(intent, session):


	card_title = 'BuzzBox Security Overseer'
	session_attributes = {}
	should_end_session = False
	try:
		session_attributes.update({"needsAuth" : session["attributes"]["needsAuth"]})
	# Imposssible as we set it to true in the welcome message, this case only happens in testing
	# Thats why we assign it to False for the tests to go through
	except KeyError:
		session_attributes.update({"needsAuth" : "True"})

	speech_output = "I don't understand what you just said."
	card_output = "Incomprehensible command."
	reprompt_text = "Please try again"

	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, card_output, reprompt_text, should_end_session))




# --------------- Events ------------------

def on_session_started(session_started_request, session):
	""" Called when the session starts """

	print("on_session_started requestId=" + session_started_request['requestId']
		  + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
	""" Called when the user launches the skill without specifying what they
	want
	"""

	print("on_launch requestId=" + launch_request['requestId'] +
		  ", sessionId=" + session['sessionId'])
	# Dispatch to your skill's launch
	return get_welcome_response()


def on_intent(intent_request, session):
	""" Called when the user specifies an intent for this skill """

	print("on_intent requestId=" + intent_request['requestId'] +
		  ", sessionId=" + session['sessionId'])

	intent = intent_request['intent']
	intent_name = intent_request['intent']['name']

	# Dispatch to your skill's intent handlers
	if intent_name == "CommandTheBox":
		return CommandTheBox(intent, session)
	elif intent_name == "GetState":
		return GetState(intent, session)
	elif intent_name == "Security":
		return Security(intent, session)
	elif intent_name == "AMAZON.HelpIntent":
		return get_welcome_response()
	elif intent_name == "AMAZON.FallbackIntent":
		return Fallback(intent, session)
	elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
		return handle_session_end_request()
	else:
		raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
	""" Called when the user ends the session.

	Is not called when the skill returns should_end_session=true
	"""
	print("on_session_ended requestId=" + session_ended_request['requestId'] +
		  ", sessionId=" + session['sessionId'])
	# add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
	""" Route the incoming request based on type (LaunchRequest, IntentRequest,
	etc.) The JSON body of the request is provided in the event parameter.
	"""
	print("event.session.application.applicationId=" +
		  event['session']['application']['applicationId'])

	"""
	Uncomment this if statement and populate with your skill's application ID to
	prevent someone else from configuring a skill that sends requests to this
	function.
	"""
	# if (event['session']['application']['applicationId'] !=
	#         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
	#     raise ValueError("Invalid Application ID")

	if event['session']['new']:
		on_session_started({'requestId': event['request']['requestId']},
						   event['session'])

	if event['request']['type'] == "LaunchRequest":
		return on_launch(event['request'], event['session'])
	elif event['request']['type'] == "IntentRequest":
		return on_intent(event['request'], event['session'])
	elif event['request']['type'] == "SessionEndedRequest":
		return on_session_ended(event['request'], event['session'])
