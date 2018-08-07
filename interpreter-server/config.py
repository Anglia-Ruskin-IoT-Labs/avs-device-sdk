#!/usr/bin/python3
import configparser
from inputparser import ParseYorN

class Config:
    #Constructor method
    def main(self):
        self.config = configparser.ConfigParser()
        self.configPath = "server_settings.cfg"
        self.LoadConfig()
        
    # Runs on init
    def LoadConfig(self):
        try:
            self.config.readfp(open(self.configPath))
            self.LoadVariables()
        except (FileNotFoundError, KeyError) as e:
            print("Error: Config file doesn't exist or not in the correct format! "
                  + "It is required to run the program!")
            if ParseYorN(input("Would you like to create one now? Y/N: ")):
                self.CreateConfig()
                self.LoadVariables()
            else:
                print("Program now exits.")
                exit()
                
    def LoadVariables(self):
        self.BuzzboxIP = self.config['BUZZBOX']['ip']
        self.BuzzboxPORT = self.config['BUZZBOX']['port']
        self.BuzzboxLEDS = self.config['BUZZBOX']['led number']
        self.BuzzboxLIGHTS = self.config['BUZZBOX']['light number']
        self.iMirrorIP = self.config['iMirror']['ip']
        self.iMirrorPORT = self.config['iMirror']['port']
        self.iMirrorENDPOINT = self.config['iMirror']['alexa_endpoint']
    
    def CreateConfig(self):
        if ParseYorN(input("Do you have BuzzBox? Y/N: ")):
            ip = input("IP address of the Buzzbox: ")
            port = input("Port number of the BuzzBox: ")
            lednum = input("Number of controllable leds on the Buzzbox: ")
            lightnum = input("Number of controllable light sets on the Buzzbox: ")
        else:
            ip = ""
            port = ""
            lednum = ""
            lightnum = ""
        
        self.config['BUZZBOX'] = {'IP': ip,
                             'Port': port,
                             'LED Number': lednum,
                             'Light Number' : lightnum}
        
        if ParseYorN(input("Do you have iMirror? Y/N: ")):
            ip = input("IP address of the iMirror: ")
            port = input("Port number of the iMirror: ")
            endpoint = input("POST endpoint on the iMirror (if address is " +
                             "'http://localhost:5555/sendhere', you need to type " +
                             "in 'endpoint'")
        else:
            ip = ""
            port = ""
            endpoint = ""
            
        self.config['iMirror'] = {'IP': ip,
                                  'Port': port,
                                  'alexa_endpoint' : endpoint
                                  }
        with open(self.configPath, 'w') as configfile:
            self.config.write(configfile)
        print("config is written to " + self.configPath)             
        
    #Constructor calling main
    def __init__(self):
        self.main()
        