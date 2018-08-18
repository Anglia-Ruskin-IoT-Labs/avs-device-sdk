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
	card_title = "Welcome"
	speech_output = ("Welcome to iMirror Controler. You can show, hide or move " + \
					"modules of the mirror, like time, weather, news, " + \
					"sensors and guide. You can also command the mirror without " + \
					"opening the skills, like this: ask imirror from anglia ruskin to " + \
					"show the sensors.")
	# If the user either does not reply to the welcome message or says something
	# that is not understood, they will be prompted again with this text.
	reprompt_text = "Please say a command."
	should_end_session = False
	output = ""
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, output, reprompt_text, should_end_session))


def handle_session_end_request():
	card_title = "Session Ended"
	speech_output = "Bye!"
	# Setting this to true ends the session and exits the skill.
	should_end_session = True
	return build_response({}, build_speechlet_response(
		card_title, speech_output, speech_output, None, should_end_session))

states = ["hide", "show", "on", "off"]
items = ["news", "time", "clock", "weather", "sensors", "guide", "everything", 
	"notifications", "conversation"]
positions = ["top left", "top middle", "top right",
			 "middle left", "middle", "middle right",
			 "bottom left", "bottom middle", "bottom right"]

def ShowingResponse(_item):
	return "Showing " + _item + "."

def Hidingesponse(_item):
	return "Hiding " + _item + "."



def CommandMirror(intent, session):
	""" Interpret the command for the BuzzBox
	"""

	card_title = 'iMirror Command Centre'
	session_attributes = {}

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

	#Check if commands are correct
	if not item in items or not state in states:
		ErrorMsg = True, "", ""
	# ------------------------------------------------
	# Command interpretation
	# ------------------------------------------------

	if item in items:
		if item == items[7] or item == items[8]:
			speech_output = "Please select a valid widget for this command."	
		else:
			# off
			if state == states[0] or state == states[3]:
				speech_output = Hidingesponse(item)
			# on
			elif state == states[1] or state == states[2]:
				speech_output = ShowingResponse(item)
			else: speech_output = "This is not a valid state for the widget."	
	else:
		speech_output = "Please select a valid widget for this command."	

	if ErrorMsg[0] == True:
		speech_output = "This is not a valid command."
	
	reprompt_text = "Is there shomething else you want to do?"

	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, speech_output, reprompt_text, should_end_session))

def MoveWidget(intent, session):
	card_title = 'iMirror Command Centre'
	session_attributes = {}
	should_end_session = False

	# Get slots from intent
	try:
		item = intent['slots']['item']['value']
		item = item.lower()
		if item == items[1]: #change time to clock
			item = items[2]
	except KeyError:
		item = "None"
	try:
		position = intent['slots']['position']['value']
		position = position.lower()
	except KeyError:
		position = "None"

	if item in items:
		if item == items[6]: #everything
			speech_output = "Not a valid widget."
		else:
			if position in positions:
				speech_output = "Moving " + item + " to the " + position + " position."
			else:
				speech_output = "Not valid position."
	else:
		speech_output = "Not a valid widget."

	reprompt_text = "Is there shomething else you want to do?"

	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, speech_output, reprompt_text, should_end_session))

def Fallback(intent, session):


	card_title = 'iMirror Command Centre'
	session_attributes = {}
	should_end_session = False

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
	if intent_name == "CommandMirror":
		return CommandMirror(intent, session)
	elif intent_name == "GetState":
		return GetState(intent, session)
	elif intent_name == "Security":
		return Security(intent, session)
	elif intent_name == "MoveWidget":
		return MoveWidget(intent, session)
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
