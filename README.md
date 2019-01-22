# inspire2domoticz
A Domoticz plugin to control the Smart Temp SMT-775 Inspire Thermostat

<BR>
<B>Instructions:</B>
<BR>
<BR>
1) Install [Domoticz](https://www.domoticz.com/) (if not already installed)
<BR>
<BR>  
2) Install the latest version of [Python](https://www.python.org/downloads/)
<BR>
<BR>
3) Find the Domoticz install files on your system (look in program files if using Windows) and go into the plugins folder.
<BR>
<BR>
4) Create a new folder inside the plugins folder called smt775 then download the plugin.py file and place it inside.
<BR>
<BR>
5) Start or restart Domoticz if you already have it running, go to "Setup > Hardware", you should see "Smart Temp SMT-775 Thermostat" in the "Type:" dropdown box at the bottom of the page. Select it and fill out the fields to configure.
<BR>
<BR>

Configuring the plugin:
* "Domoticz Lan IP" is the static IP address you have given your computer that is running Domoticz
* "SMT-775 Lan IP" is the static IP address you have given the SMT-775 either by setting a static IP on the unit or by using the DHCP settings on your router.
* "Number of Zones" is how many seperate air conditioning zones you have (you can find this out by looking in Zones on the SMT-775 physical screen.
* "Temperature Drift" is how far the thermostat should allow the temperature to vary from your set temperature, the default is 1 degree either above or below your setpoint.


![Screenshot](images/hardwarepagescreenshot.JPG)

It was nessesary to combine the cool and heat setpoints into a single temperature with a "Drift" allownace in order to accomodate home automation appliaces such as Amazon Alexa, eg: "Alexa set the thermostat to 22", the plugin takes care of setting the thermostat to heat at 23 degrees and cool at 21 degrees.

Note that Alexa has been tested and I can confirm that it is working nicely in my environment. Note that a seperate Domoticz plugin is required for Alexa support.
