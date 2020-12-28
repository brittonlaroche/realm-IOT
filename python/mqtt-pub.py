# A simple example for an MQTT Publisher

import paho.mqtt.client as paho
import sys
import datetime

client = paho.Client()
# The way we do it in node.js
# const client = mqtt.connect('mqtt://localhost:9000');

# Python is host, port, timeout in seconds
if client.connect("localhost",1883,10) != 0:
    print("Could not connect to MQTT Broker")
    sys.exit(-1)

now = int(datetime.datetime.utcnow().timestamp())
print("now: "+ str(now)) 
message = "{'sensorType':'temperature','sensorId':'S1989','tempCelsius':26.66,'tempFahrenheit':80.00,'timestamp':" + str(now) +"}"
# topic, message, quality of service.
client.publish("dht/temperature", )

# Disconnect
client.disconnect()