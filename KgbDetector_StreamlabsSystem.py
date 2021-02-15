#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
import time
import colorsys
import random
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from KGBSettings_Module import MyKGBSettings
from time import sleep
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "KGB Detector"
Website = "https://www.twitch.tv/redjohn260"
Description = "Detects if the user is part of KGB"
Creator = "RedJohn260"
Version = "1.0.0"

#---------------------------
#   Define Global Variables
#---------------------------
global KGBSettingsFile
KGBSettingsFile = os.path.join(os.path.dirname(__file__), "Settings\kgb_settings.json")
global KGBScriptSettings
KGBScriptSettings = MyKGBSettings(KGBSettingsFile)

global KGBSecretFiles 
KGBSecretFiles = os.path.join(os.path.dirname(__file__), "Settings\kgb_secrets.txt")

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #KGBSecretFiles = os.path.join(os.path.dirname(__file__), "Settings\kgb_secrets.txt")
    #f = open(KGBSecretFiles, 'w')
    #with open('kgb_secrets.txt', 'w') as f:
     #   f.write('Create a new text file!')

    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):


    if not data.IsChatMessage() and not data.IsFromTwitch():
        return

    if data.IsChatMessage():
        if data.GetParam(0).lower() == KGBScriptSettings.DetectKgbCommand and not Parent.IsOnCooldown(ScriptName, KGBScriptSettings.DetectKgbCommand.lower()):
            if Parent.HasPermission(data.User,KGBScriptSettings.Permission,""):
                number = Parent.GetRandom(0, 100)

                KgbWords = KGBScriptSettings.SecretKeywords.split(',')
                color = data.RawData.lower().split('color=')[1].split(';')[0]
                #Log("Color=" + str(color))

                if any(word in data.UserName.lower() for word in KgbWords) or IsColorRed(color):
                    lines = open(KGBSecretFiles).read().splitlines()
                    myline = random.choice(lines)

                    SendMessage(KGBScriptSettings.Message1 + data.UserName)
                    SendMessage(data.UserName + KGBScriptSettings.Message2)
                    SendMessage(data.UserName + KGBScriptSettings.Message3 + myline)

                else:
                    SendMessage("Unauthorized use of secret keyword!")
                    SendMessage("Sending agents to: " + data.UserName + " location.")


                Parent.AddCooldown(ScriptName, KGBScriptSettings.DetectKgbCommand, KGBScriptSettings.Cooldown)
            else:
                SendMessage("Unauthorized access!")
                SendMessage("Spy agent detected... " + data.UserName)

        else:
            SendMessage("System overloaded... Please wait for cooldown." )

    
    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

def IsColorRed(hex):
    # Hue abouve 345 or below 30
    Log(hex)
    (red, green, blue) = hexToRgb(hex)
    Log((red, green, blue))
    (hue, sat, light) = colorsys.rgb_to_hls(red/255.0, green/255.0, blue/255.0)
    Log(hue)
    hue *= 360
    return hue >= 345 or hue <= 30 #red hues

def ReloadSettings(jsonData):
    # Execute json reloading here
    KGBScriptSettings.__dict__ = json.loads(jsonData)
    KGBScriptSettings.Save(KGBSettingsFile)
    return

def hexToRgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def Log(message):
    Parent.Log("KGB Detector Script: ", str(message))
    return

def SendMessage(message):
    Parent.SendStreamMessage(message)
    return