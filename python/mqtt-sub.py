# A simple example for an MQTT Subscriber

import paho.mqtt.client as paho
import sys
import datetime

def onMessage(client, userdata, msg):
    print(msg.topic + ": " + msg.payload.decode())

client = paho.Client()
client.on_message = onMessage

# The way we do it in node.js
# const client = mqtt.connect('mqtt://localhost:9000');

# Python is host, port, timeout in seconds
if client.connect("localhost",1883,10) != 0:
    print("Could not connect to MQTT Broker")
    sys.exit(-1)

client.subscribe("dht/temperature")

try:
    print("Press CTLRL+C to exit...")
    client.loop_forever()
except:
    print("Disconnecting from broker")


# Disconnect
client.disconnect()