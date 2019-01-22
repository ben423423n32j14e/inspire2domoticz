# Smart Temp SMT-775 Thermostat Plugin
#
# Author: ben53252642
#
"""
<plugin key="smt775" name="Smart Temp SMT-775 Thermostat" author="ben53252642" version="1.0.0" externallink="https://github.com/ben423423n32j14e/inspire2domoticz">
<params>
        <param field="Mode1" label="Domoticz LAN IP" width="200px" required="true" default="192.168.0.5"/>
        <param field="Mode2" label="SMT-775 LAN IP" width="200px" required="true" default="192.168.0.77"/>
        <param field="Mode3" label="Number of Zones" width="200px" required="true" default="2"/>
        <param field="Mode4" label="Temperature Drift" width="200px" required="true" default="1"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true"/>
            </options>
        </param>
</params>
</plugin>
"""
import Domoticz
import sys
#import socket

class BasePlugin:
    enabled = False
    def __init__(self):
        #self.var = 123
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging( 1 )
        else:
            Domoticz.Debugging( 0 )

        if (len(Devices) == 0):
        # Create devices in Domoticz
            # Thermostat Mode
            Options = {"LevelActions": "||||", "LevelNames": "Off|Cool|Heat|Auto", "LevelOffHidden": "false", "SelectorStyle": "0"}
            Domoticz.Device(Name="Thermostat Mode", Used=1, Unit=1, Type=244, Subtype=73, Switchtype=18, Options=Options, Image=9).Create()

            # Thermostat Zones
            zonenum = 10
            w = 1
            while w<=int((Parameters["Mode3"])):
                Domoticz.Device(Name="Thermostat Zone {}".format(w), Used=1, Unit=zonenum, Type=244, Subtype=73, Switchtype=0, Image=9).Create()
                zonenum=zonenum+1
                w=w+1

            # Thermostat Fan Speed
            Options = {"LevelActions": "||||", "LevelNames": "Low|Medium|High|Auto", "LevelOffHidden": "false", "SelectorStyle": "0"}
            Domoticz.Device(Name="Thermostat Fan Speed", Used=1, Unit=3, Type=244, Subtype=73, Switchtype=18, Options=Options, Image=7).Create()
            Devices[3].Update(nValue=1, sValue=str("0"))

            # Thermostat Fan Mode
            Options = {"LevelActions": "||", "LevelNames": "Continuous|Auto", "LevelOffHidden": "false", "SelectorStyle": "0"}
            Domoticz.Device(Name="Thermostat Fan Mode", Used=1, Unit=4, Type=244, Subtype=73, Switchtype=18, Options=Options, Image=7).Create()
            Devices[4].Update(nValue=1, sValue=str("0"))

            # Thermostat Temperature Set Point (and set initial default value to 20)
            Domoticz.Device(Name="Thermostat", Used=1, Unit=5, Type=242, Subtype=1).Create()
            Devices[5].Update(nValue=0, sValue=str("20"))

            Domoticz.Log("Devices created.")

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

        Command = Command.strip()
        action, sep, params = Command.partition(' ')
        action = action.capitalize()
        params = params.capitalize()

        # Send via UDP function
        def udpsend8899():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
            sock.sendto(bytes(msg, "utf-8"), ((Parameters["Mode2"]), 8899))

        # Control: Thermostat Mode
        if Unit == 1:
            if Level == 0:
                Domoticz.Log("Setting thermostat mode: off")
                msg = '{"equip_mode":"0"}'
                Devices[1].Update(nValue=0, sValue=str("0"), Image=9)
            elif Level == 10:
                Domoticz.Log("Setting thermostat mode: cool")
                msg = '{"equip_mode":"2"}'
                Devices[1].Update(nValue=1, sValue=str("10"), Image=16)
            elif Level == 20:
                Domoticz.Log("Setting thermostat mode: heat")
                msg = '{"equip_mode":"1"}'
                Devices[1].Update(nValue=1, sValue=str("20"), Image=15)
            elif Level == 30:
                Domoticz.Log("Setting thermostat mode: auto")
                msg = '{"equip_mode":"3"}'
                Devices[1].Update(nValue=1, sValue=str("30"), Image=9)
            udpsend8899()
            # Set thermostat temperature after changing mode
            if Level != 0:
                cooltemp = (float(Devices[5].sValue) + int(Parameters["Mode4"]))
                heattemp = (float(Devices[5].sValue) - int(Parameters["Mode4"]))
                msg = '{"prog_hold_value":"2","temp_cool":' + '"' + str(cooltemp) + '"' + ',"temp_heat":' + '"' + str(heattemp) + '"' + '}'
                udpsend8899()

        # Control: Thermostat Zones
        zonenum = 10
        w = 1
        while w<=int((Parameters["Mode3"])):
            if (Unit == zonenum):
                if (action == 'On'):
                    Devices[zonenum].Update(nValue=1, sValue=str("On"))
                if (action == 'Off'):
                    Devices[zonenum].Update(nValue=0, sValue=str("On"))
                zonesum = 0
                if (int(Parameters["Mode3"]) >= 1):
                    if (Devices[10].nValue == 1):
                        zonesum = (zonesum + 1)
                if (int(Parameters["Mode3"]) >= 2):
                    if (Devices[11].nValue == 1):
                        zonesum = (zonesum + 2)
                if (int(Parameters["Mode3"]) >= 3):
                    if (Devices[12].nValue == 1):
                        zonesum = (zonesum + 4)
                if (int(Parameters["Mode3"]) >= 4):
                    if (Devices[13].nValue == 1):
                        zonesum = (zonesum + 8)
                if (int(Parameters["Mode3"]) >= 5):
                    if (Devices[14].nValue == 1):
                        zonesum = (zonesum + 16)
                if (int(Parameters["Mode3"]) >= 6):
                    if (Devices[15].nValue == 1):
                        zonesum = (zonesum + 32)
                msg = '{"zone_pilot":' + '"' + str(zonesum) + '"' + ',"zone_partion":' + '"' + str(zonesum) + '"' + '}'
                if (zonesum >= 1):
                    udpsend8899()
            w=w+1
            zonenum=zonenum+1

        # Control: Thermostat Fan Speed
        if Unit == 3:
            if Level == 0:
                Domoticz.Log("Setting thermostat fan speed to: low")
                msg = '{"fan_speed":"1"}'
                Devices[3].Update(nValue=1, sValue=str("0"), Image=7)
            elif Level == 10:
                Domoticz.Log("Setting thermostat fan speed to: medium")
                msg = '{"fan_speed":"2"}'
                Devices[3].Update(nValue=1, sValue=str("10"), Image=7)
            elif Level == 20:
                Domoticz.Log("Setting thermostat fan speed to: high")
                msg = '{"fan_speed":"3"}'
                Devices[3].Update(nValue=1, sValue=str("20"), Image=7)
            elif Level == 30:
                Domoticz.Log("Setting thermostat fan speed to: auto")
                msg = '{"fan_speed":"4"}'
                Devices[3].Update(nValue=1, sValue=str("30"), Image=7)
            udpsend8899()

        # Control: Thermostat Fan Mode
        if Unit == 4:
            if Level == 0:
                Domoticz.Log("Setting thermostat mode to: continuous")
                msg = '{"fan_mod":"1"}'
                Devices[4].Update(nValue=1, sValue=str("0"), Image=7)
            elif Level == 10:
                Domoticz.Log("Setting thermostat mode to: auto")
                msg = '{"fan_mod":"0"}'
                Devices[4].Update(nValue=1, sValue=str("10"), Image=7)
            udpsend8899()

        # Control: Thermostat Temperature
        if Unit == 5:
            Devices[5].Update(nValue=0, sValue=str(Level))
            cooltemp = (float(Devices[5].sValue) + int(Parameters["Mode4"]))
            heattemp = (float(Devices[5].sValue) - int(Parameters["Mode4"]))
            msg = '{"prog_hold_value":"2","temp_cool":' + '"' + str(cooltemp) + '"' + ',"temp_heat":' + '"' + str(heattemp) + '"' + '}'
            udpsend8899()

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
