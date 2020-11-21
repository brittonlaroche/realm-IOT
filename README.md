# Realm IOT


## Overview

In this "hands on lab" we will create our own full featured IOT sensor device that will send data from a remote IOT device to MongoDB Atlas.  We will begin with a simple script that sends data directly to MongoDb via a REST API webhook.  We will then enhance this simple code to retry sending its data in the event of a network outage. Finally we will upgrade our simple script to talk to an MQTT Broker which will send data to the Realm Middleware which will guarantee delivery and bi-directional communication with MongoDB Atlas. The MQTT broker and Realm Middleware opens a whole new world of possibilities where configuration changes and upgrades can be passed down to remote IOT devices rather than a one way sending of sensor data from the IOT device.   
   
![Realm IOT MQTT](./img/RealmIOTMqtt2.png) 

## Getting Started

### Equipment
[Raspbery Pi with Cana Kit](https://www.amazon.com/CanaKit-Raspberry-4GB-Starter-Kit/dp/B07V5JTMV9/ref=sr_1_3?dchild=1&keywords=Raspberry+Pi+Cana+Kit&qid=1605933239&sr=8-3)
[Uno R3 Elegoo](https://www.amazon.com/ELEGOO-Project-Tutorial-Controller-Projects/dp/B01D8KOZF4/)

### Installation Guides



## First Version

Our first version of the code uses the Realm Serverless capability to create a webhook to receive the sensor data directly from the IOT device using nothing more thana REST API call.


```py
import Adafruit_DHT
import time
import requests
import datetime

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        sensorDate = datetime.datetime.now()
        ftemp = (temperature * 9/5)+32
        data = "{\"sensorId\":\"T89176\", \"temperature\":" +str(ftemp) +", \"humidity\":" + str(humidity) +", \"sensorDate\":\"" + str(sensorDate) + "\"}"
        print(data)
        url = 'https://webhooks.mongodb-realm.com/api/client/v2.0/app/inventory-hhsot/service/Receive-IOT-Data/incoming_webhook/IOT-WH'
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        response = requests.post(url, data=data, headers=headers )
        for x in response:
            print(x)

    else:
        print("Sensor failure. Check wiring.");
    time.sleep(3);   
```   
   
It works!  But there are many problems with this code.  There is no error handling, so if the network goes down the code throws an error and stops working on the IOT device.  You have to connect to the IOT device to start again.  Even if there was error handleing there would be data loss for the entire time the network is down.

The network outage can be tested with the following code:   
   
```py
import os
import time

print("Shutting down wifi for 60 seconds")
cmd = 'sudo ifconfig wlan0 down'
os.system(cmd)

time.sleep(60)

cmd = 'sudo ifconfig wlan0 up'
os.system(cmd)
print("wifi back up")
```   
   

![Realm IOT MQTT](./img/RealmIOT.png) 

## Second Version
A second version of this code that handles errors and has built in retry logic is here.  It also batches the data.  If the sensor data is collected every 3 seconds then with a batch of 20 you can send data once a minute and still maintain the granualarity of each 3 second reading.   

You can access the second version of the code here.
https://github.com/brittonlaroche/realm-IOT/blob/main/python/readTempBatch.py

You can also run the wifi outage script and see that it will store and retry the data.  This is all well and good.  But it is severly lacking as it is only one way communication.  Imagine trying to change the configuration.  Maybe you have an upgrade or maybe you want to save money and batch the data so it sends once every five minutes.  Perhaps you want the sensor to only read once a minute.  How will you apply these changes?  Imagine going to thousands of devices to make the necessary upgrades. This solution is untenable in the long run and will quickly become a maintenance nightmare. Enter the next phase of our lab.  We will now enable an MQTT broker and the Realm Sync capabilities.

## Realm IOT MQTT
![Realm IOT MQTT](./img/RealmIOTMqtt2.png) 
