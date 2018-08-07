#!/usr/bin/python3
import time

class Tests:
    def BuzzboxControlTest(self, _buzzbox):
        title = "Buzzbox Command Centre"
        textfields = ["turning heater on", 
                    "turning heater off",
                    "turning fan on",
                    "turning fan off",
                    "turning light 1 on",
                    "turning light 1 blink",
                    "turning light 1 off",
                    "turning light 2 on",
                    "turning light 2 blink",
                    "turning light 2 off",
                    "turning led 1 on",
                    "turning led 2 on",
                    "turning led 3 on",
                    "turning led 4 on",
                    "turning led 5 on",
                    "turning led 6 on",
                    "turning led 7 on",
                    "turning led 8 on",
                    "turning led 1 yellow",
                    "turning led 2 yellow",
                    "turning led 3 yellow",
                    "turning led 4 yellow",
                    "turning led 5 yellow",
                    "turning led 6 yellow",
                    "turning led 7 yellow",
                    "turning led 8 yellow",
                    "turning led 1 red",
                    "turning led 2 red",
                    "turning led 3 red",
                    "turning led 4 red",
                    "turning led 5 red",
                    "turning led 6 red",
                    "turning led 7 red",
                    "turning led 8 red",
                    "turning led 1 green",
                    "turning led 2 green",
                    "turning led 3 green",
                    "turning led 4 green",
                    "turning led 5 green",
                    "turning led 6 green",
                    "turning led 7 green",
                    "turning led 8 green",
                    "turning led 1 off",
                    "turning led 2 off",
                    "turning led 3 off",
                    "turning led 4 off",
                    "turning led 5 off",
                    "turning led 6 off",
                    "turning led 7 off",
                    "turning led 8 off",
                    "turning lights on",
                    "turning lights blink",
                    "turning lights off",                   
                    "turning leds on",
                    "turning leds red",                   
                    "turning leds green",
                    "turning leds off",
                    "turning all on",
                    "turning all off",
                    "turning everything on",
                    "turning everything off",
                    "turning reading display on",
                    "turning reading display off",
                    "turning reading interface on",
                    "turning reading interface off",
                    "displaying heater state:",
                    "displaying fan state:",
                    "displaying motion sensor reading:",
                    "displaying led 1 state:",
                    "displaying led 2 state:",
                    "displaying led 3 state:",
                    "displaying led 4 state:",
                    "displaying led 5 state:",
                    "displaying led 6 state:",
                    "displaying led 7 state:",
                    "displaying led 8 state:",
                    "displaying light 1 state:",
                    "displaying light 2 state:",
                    "displaying temperature:",
                    "displaying light level:"
                      ]
        for item in textfields:
            print("Test: " + item + ", Result: " + str(_buzzbox.Command(title, item)))
            time.sleep(0.5)
            
    def SendACommand(self, _command, _buzzbox):
        return _buzzbox.SendCommand(_command)
        