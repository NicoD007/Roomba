## Running MQTT

To run MQTT for this project, make sure the Mosquitto broker is installed and running on your machine. Then start the simulator by running Mainflow.py and keep that window open, because it is the client that listens for commands. In a second PowerShell terminal, publish the `start` message to the `roomba/command` topic using `mosquitto_pub`. If MQTT is not available or fails to connect, you can still start the robot manually by clicking the simulator window and pressing `S` as a fallback.


# Terminal 1: start the simulator
& C:/Users/nicod/AppData/Local/Microsoft/WindowsApps/python3.13.exe "c:/Users/nicod/Downloads/Roomba-main (2)/Roomba-main/Mainflow.py"

# Terminal 2: send the MQTT start command
& "C:\Program Files\mosquitto\mosquitto_pub.exe" -h localhost -p 1883 -t roomba/command -m start
(send this in powershell)
# Optional: check that the broker is running
Get-Service mosquitto

# Optional: start the broker if it is not running
Start-Service mosquitto
```

