"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


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
    session_attributes.update({ "state" : "beginning" })
    card_title = "Welcome to Zork"
    speech_output = "Welcome to Zork. " \
                    "You are standing in an open field west of a white house, with a boarded front door. " \
                    "A secret path leads southwest into the forest. There is a Small Mailbox."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "What do you do?"
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

LOCATIONS = ["beginning", "southwest", "east", "grating", "cave"]








def GiveCommand(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = 'Buzzbox Command Centre'
    session_attributes = {}
    try:
        session_attributes.update({"state" : session["attributes"]["state"]})
        currentLocation = session["attributes"]["state"]
    # Imposssible as we set it to true in the welcome message, this case only happens in testing
    # Thats why we assign it to False for the tests to go through
    except KeyError:
        session_attributes.update({"state" : "beginning"})
    should_end_session = False

    command = intent['slots']['Replies']['value']


    # Beginning
    if LOCATIONS[0] == currentLocation:
        FIRST_LOOP = ["take mailbox", "open mailbox", "go east", "open door", 
                      "take boards", "look at house", 
                      "read leaflet", "go southwest"]
        # take mailbox
        if command == FIRST_LOOP[0]:
            speech_output = ("You cannot be serious.")
        # open mailbox
        elif command == FIRST_LOOP[1]:
            speech_output = ("Opening the small mailbox reveals a leaflet.")
        # go east
        elif command == FIRST_LOOP[2]:
            speech_output = ("The door is boarded and you cannot remove the boards.")
        # open door
        elif command == FIRST_LOOP[3]:
            speech_output = ("The door cannot be opened.")
        # take boards
        elif command == FIRST_LOOP[4]:
            speech_output = ("The boards are securely fastened.")
        # look at house
        elif command == FIRST_LOOP[5]:
            speech_output = ("The house is a beautiful colonial house which is painted white. It is clear that the owners must have been extremely wealthy.")
        # read leaflet
        elif command == FIRST_LOOP[6]:
            speech_output = ("Welcome to the Unofficial Version of Zork. Your mission is to find a Jade Statue.")
        # go southwest
        elif command == FIRST_LOOP[7]:
            speech_output = ("You are going southwest. This is a forest, with trees in all directions. " + 
                             "To the east, there appears to be sunlight.")
            session_attributes.update({"state" : LOCATIONS[1]})
        else:
            speech_output = "You can't do that."
    # SouthWest
    elif LOCATIONS[1] == currentLocation:
        SOUTHWEST = ["go west", "go north", "go south", "go east"]
        # go west
        if command == SOUTHWEST[0]:
            speech_output = ("You would need a machete to go further west.")
        # go north
        elif command == SOUTHWEST[1]:
            speech_output = ("The forest becomes impenetrable to the North.")
        # go south
        elif command == SOUTHWEST[2]:
            speech_output = ("Storm-tossed trees block your way.")
        # go east
        elif command == SOUTHWEST[3]:
            speech_output = ("You are going east. You are in a clearing, with a " + 
                             "forest surrounding you on all sides. A path leads south. " 
                              + "There is an open grating, descending into darkness.")
            session_attributes.update({"state" : LOCATIONS[2]})
        else:
            speech_output = "You can't do that."
    # East
    elif LOCATIONS[2] == currentLocation:
        EAST = ["go south", "descend grating"]
        # go south
        if command == EAST[0]:
            speech_output = ("You see a large ogre and turn around.")
        # descend grating
        elif command == EAST[1]:
            speech_output = ("You are descending into the grating. " + 
                             "You are in a tiny cave with a dark, forbidding staircase leading down." + 
                             " There is a skeleton of a human male in one corner.")
            session_attributes.update({"state" : LOCATIONS[3]})
        else:
            speech_output = "You can't do that."
    # Grating
    elif LOCATIONS[3] == currentLocation:
        GRATING = ["descend staircase", "take skeleton", "smash skeleton",
                   "light up room", "break skeleton", 
                   "go down staircase", "scale staircase", "suicide"]
        # descend staircase
        if command == GRATING[0]:
            speech_output = ("You descend on the staircase. You have entered a mud-floored room."
                             + "Lying half buried in the mud is an old trunk, bulging with jewels.")
            session_attributes.update({"state" : LOCATIONS[4]})
        # take skeleton
        elif command == GRATING[1]:
            speech_output = ("Why would you do that? Are you some sort of sicko?")
        # smash skeleton
        elif command == GRATING[2]:
            speech_output = ("Sick person. Have some respect.")
        # light up room
        elif command == GRATING[3]:
            speech_output = ("You would need a torch or lamp to do that.")
        # break skeleton
        elif command == GRATING[4]:
            speech_output = ("I have two questions: Why and With What?")
        # go down staircase
        elif command == GRATING[5]:
            speech_output = ("You go down on the staircase. You have entered a mud-floored room."
                             + "Lying half buried in the mud is an old trunk, bulging with jewels.")
            session_attributes.update({"state" : LOCATIONS[4]})
        # scale staircasse
        elif command == GRATING[6]:
            speech_output = ("You scale the staircase. You have entered a mud-floored room. "
                             + "Lying half buried in the mud is an old trunk, bulging with jewels.")
            session_attributes.update({"state" : LOCATIONS[4]})
        # suicide
        elif command == GRATING[7]:
            speech_output = ("You throw yourself down the staircase as an attempt at suicide. You die.")
            should_end_session = True
        else:
            speech_output = "You can't do that."
    # Cave
    elif LOCATIONS[4] == currentLocation:
        CAVE = ["open trunk"]
        # take mailbox
        if command == CAVE[0]:
            speech_output = ("You have found the Jade Statue and have completed your quest!")
            should_end_session = True
        else:
            speech_output = "You can't do that."
    # Should be impossible
    else:
        speech_output = "Error, wrong location"




    reprompt_text = "What do you do?"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, speech_output, reprompt_text, should_end_session))

def DescribeLocation(intent, session):

    card_title = 'What you see'
    session_attributes = {}
    should_end_session = False
    try:
        session_attributes.update({"state" : session["attributes"]["state"]})
        currentLocation = session["attributes"]["state"]
    # Imposssible as we set it to true in the welcome message, this case only happens in testing
    # Thats why we assign it to False for the tests to go through
    except KeyError:
        session_attributes.update({"state" : "beginning"})

    if LOCATIONS[0] == currentLocation:
        speech_output = ("You are standing in an open field west of a white house, " +  
                         "with a boarded front door. A secret path leads southwest into the forest. " + 
                         "There is a Small Mailbox.")
        session_attributes.update({"state" : LOCATIONS[0]})
    # SouthWest
    elif LOCATIONS[1] == currentLocation:
        speech_output = ("This is a forest, with trees in all directions. " 
             + "To the east, there appears to be sunlight.")
        session_attributes.update({"state" : LOCATIONS[1]})
    # East
    elif LOCATIONS[2] == currentLocation:
        speech_output = ("You are in a clearing, with a forest surrounding you on all sides. " + 
                        "A path leads south. There is an open grating, descending into darkness.")
        session_attributes.update({"state" : LOCATIONS[2]})
    # Grating
    elif LOCATIONS[3] == currentLocation:
        speech_output = ("You are in a tiny cave with a dark, forbidding staircase leading down. " + 
                         "There is a skeleton of a human male in one corner.")
        session_attributes.update({"state" : LOCATIONS[3]})
    # Cave
    elif LOCATIONS[4] == currentLocation:
        speech_output = ("You have entered a mud-floored room. " + 
                         "Lying half buried in the mud is an old trunk, bulging with jewels.")
        session_attributes.update({"state" : LOCATIONS[4]})
    # Should be impossible
    else:
        speech_output = "Error, wrong location"


    reprompt_text = "What do you do?"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, speech_output, reprompt_text, should_end_session))

def Fallback(intent, session):
    card_title = 'Error'
    session_attributes = {}
    should_end_session = False

    speech_output = "You can't do that."

    reprompt_text = "What do you do?"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, speech_output, reprompt_text, should_end_session))



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
    if intent_name == "GiveCommand":
        return GiveCommand(intent, session)
    if intent_name == "DescribeLocation":
        return DescribeLocation(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.FallbackIntent":
        return get_welcome_response()
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
