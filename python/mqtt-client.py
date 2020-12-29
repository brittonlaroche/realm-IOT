import Adafruit_DHT
import time
import requests
import datetime
import paho.mqtt.client as paho
import sys
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4


client = paho.Client()

# Python is host, port, timeout in seconds
if client.connect("localhost",1883,10) != 0:
    print("Could not connect to MQTT Broker")
    sys.exit(-1)

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        sensorDate = datetime.datetime.now()
        ftemp = (temperature * 9/5)+32
        #data = "{\"sensorId\":\"T89176\", \"temperature\":" +str(ftemp) +", \"humidity\":" + str(humidity) +", \"sensorDate\":\"" + str(sensorDate) + "\"}"
        now = int(datetime.datetime.utcnow().timestamp())
        message = "{\"sensorType\":\"temperature\",\"sensorId\":\"af4ff76b-009b-4cc4-8dfe-c058d1d030c9\",\"tempCelsius\":"+ str(temperature) +",\"tempFahrenheit\":"+ str(ftemp) +",\"timestamp\":" + str(now) +"}"
        print(message)
        client.publish("dht/temperature", message)
    else:
        print("Sensor failure. Check wiring.")
    time.sleep(3)