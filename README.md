# Realm IOT

## Overview
MongoDB Realm sync is a poewerful tool that has now been brought to the world of IOT usecases.  In this example we use a DHT11 sensor and a Raspbery Pi to send temperature and humidity data from a delivery truck as part of solution to a cold chain logistics problem.


## Hands On Lab
In this "hands on lab" we will create our own full featured IOT sensor device that will send data from a remote IOT device to MongoDB Atlas. After setting up our Raspberry pi and wiring inthe DHT11 temperature and humidity sensor, we will begin with a simple python script that sends data directly to MongoDB via a REST API webhook.  We will then enhance this simple code to retry sending its data in the event of a local network outage. Finally, we will upgrade our simple script to talk to an MQTT Broker which will send data to the Realm Middleware which will guarantee delivery and bi-directional communication with MongoDB Atlas. The MQTT broker and Realm Middleware opens a whole new world of possibilities where configuration changes and upgrades can be passed down to remote IOT devices rather than a one way sending of sensor data from the IOT device.   
   
![Realm IOT MQTT](./img/RealmIOT-V4-5.png) 

## Getting Started

### Purchase IOT Equipment
You will need a Rasbery Pi 4 and a DHT11 Temperature sensor along with some wiring.  For a little extra you can get a whole kit with multiple sensors a bread board and all the wiring you will need with the purchase of an Elegoo UNO R3 Starter Kit.  I selected the Pi 4 with 4GB, this githib has instructions for the Pi 4 with this configuration.  The details are in the Amazon links provided in the table below.

| Raspberry Pi Cana Kit | Elegoo UNO Starter Kit |
|-----------------------|------------------------|
|[Raspbery Pi with Cana Kit](https://www.amazon.com/CanaKit-Raspberry-4GB-Starter-Kit/dp/B07V5JTMV9/) | [ELEGOO UNO Project Super Starter Kit](https://www.amazon.com/ELEGOO-Project-Tutorial-Controller-Projects/dp/B01D8KOZF4/)|
| <a href="https://www.amazon.com/CanaKit-Raspberry-4GB-Starter-Kit/dp/B07V5JTMV9/" target="pi"><img src="./img/CanaKit.png" width="400px"></a>|<a href="https://www.amazon.com/ELEGOO-Project-Tutorial-Controller-Projects/dp/B01D8KOZF4/" target="pi"><img src="./img/UnoR3.png" width="400px"></a>|

### Configure the IOT Hardware

#### <img src="./img/1.svg" width="32px"> Rasperry Pi Cana Kit Installation Guide
When you first get the cana kit and the Raspbery Pi you will want to set it up.  You need to install the operating system and get the latest updates. I found that the rasbian operating system was pre-installed on the sd card and all I had to do was insert the card and perform an update. Watch the video below for step by step instructions.
|Getting STarted Video|Getting Started Blog & Video|
|--------------|---------------|
|[Video: Setting up the Raspberry Pi 4](https://www.youtube.com/watch?v=BpJCAafw2qE&feature=youtu.be)|[Instructions: Setting up the Rasperry Pi4](https://crosstalksolutions.com/getting-started-with-raspberry-pi-4/)|
|<a href="https://www.youtube.com/watch?v=BpJCAafw2qE&feature=youtu.be" target="video"><img src="./img/CTVideo.png"></a>|<a href="https://crosstalksolutions.com/getting-started-with-raspberry-pi-4/" target="blog"><img src="./img/CTBlog.png"></a>|

After assempling the Raspberry Pi cana Kit, insert the SD card, plug in a monitor, mouse and keyboard and power it on.  Once inside the rasbian operating system open the terminal window and run the following command:   
   
```   
sudo apt-get update && sudo apt-get upgrade -y
```   

It will take serveral minutes to apply all the updates.
   
#### <img src="./img/2.svg" width="32px"> Wiring the DHT11 Sensor to the Raspberry Pi
Open the ELEGOO UNO Project Super Starter Kit with UNO R3 and find the DHT11 sensor and take 3 female to female wiring connections. 
|DHT11 Temperature and humidity Sensor|
|-------------------------------------|
|<img src="./img/DHT11-Sensor.jpg">|


The DHT11 temperature sensor needs to be connected to the Rasperry PI GPIO pin out array.  To get an idea of what to do if this is your first time watch the following video: [DHT11 Raspery Pi Configurtaion](https://www.youtube.com/watch?v=GsG1OClojOk&feature=youtu.be) 

We will need to connect the DHT11 sensor to the right GPIO pins on the Raspberry Pi.  To get a listing of your specific Rasperry pi and its GPIO pin configuration you can type "pinout" from the pi terminal.  You will get a beatifully colored ASCII art map like the following:

|PI Board|GPIO Pins|
|-------------|------------------|
|<img src="./img/PIBoard.png">|<img src="./img/GPIOPins.png">|

|DHT11 GPIO Wiring Diagram|
|-------------------------|
|<img src="./img/DHT11Wiring.png">|

We are not going to use the bread board.  Instead we will wire the DHT11 sensor directly to the Raspbery Pi GPIO board using the female to female conector wires we took from the ELEGOO UNO Project Super Starter Kit as seen below:

|Pi with Cana Kit Open | Pi with Cana Kit Closed|
|----------------------|------------------------|
|<a href="./img/PIKitOpenLarge.jpg" target="large"><img src="./img/PIKitOpen.jpg"></a>|<img src="./img/PIKitLid.jpg">|

The exact wiring for my particluar set up allowed me to include the Cana kit fan.  My wiring is as follows:
|DHT11 Pin| Wire Color|Raspberry Pi GPIO Pin| Pin Number|
|---------|---------|---------|---------|
|[Left] Data Pin| Orange| GPIO4 | (7)|
|[Middle] Power| Red | --- |(2)|
|[Right] Ground| Brown| --- |(9)|

|Cana Kit Fan| Wire Color|Raspberry Pi GPIO Pin| Pin Number|
|---------|---------|---------|---------|
|Power Wire | Red| --- | (4)|
|Ground Wire| Black| --- |(6)|

#### <img src="./img/3.svg" width="32px"> Write a python script to read sensor data
I will summarize the following link [DHT11 Coding](https://www.thegeekpub.com/236867/using-the-dht11-temperature-sensor-with-the-raspberry-pi/) below:

PYTHON CODE FOR RASPBERRY PI DHT11/DHT22
Next thing we need to do is install the DHT python library. This is done by entering  the following command:
```
sudo pip3 install Adafruit_DHT
```
Note: If you run into problems with the above command, you may not have PIP installed on your Pi.  You can fix that by running the following commands.  These will install PIP and other utilities you may need.
   
```
sudo apt-get install python3-dev python3-pip
sudo python3 -m pip install --upgrade pip setuptools wheel
```


## Send IOT Data to Atlas

### First Version

Our first version of the code uses the Realm Serverless capability to create a webhook to receive the sensor data directly from the IOT device using nothing more thana REST API call.

![Realm IOT](./img/RealmIOT.png) 

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

if you get the error: "cannot import name 'Beaglebone_Black_Driver' from 'Adafruit_DHT'" then the following instructions will show how to add the proper entry for the DHT settings.

In "/usr/local/lib/python3.7/dist-packages/Adafruit_DHT/platform_detect.py", you can add the followings at line #112 in the elif ladder, so it should workaround the issue. 

```
elif match.group(1) == 'BCM2711':
    return 3
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
   



## Second Version
A second version of this code that handles errors and has built in retry logic is here.  It also batches the data.  If the sensor data is collected every 3 seconds then with a batch of 20 you can send data once a minute and still maintain the granualarity of each 3 second reading.   

You can access the second version of the code here.
https://github.com/brittonlaroche/realm-IOT/blob/main/python/readTempBatch.py

You can also run the wifi outage script and see that it will store and retry the data.  This is all well and good.  But it is severly lacking as it is only one way communication.  Imagine trying to change the configuration.  Maybe you have an upgrade or maybe you want to save money and batch the data so it sends once every five minutes.  Perhaps you want the sensor to only read once a minute.  How will you apply these changes?  Imagine going to thousands of devices to make the necessary upgrades. This solution is untenable in the long run and will quickly become a maintenance nightmare. Enter the next phase of our lab.  We will now enable an MQTT broker and the Realm Sync capabilities.

## Realm IOT MQTT
![Realm IOT MQTT](./img/RealmIOTMqtt2.png) 


### Learning Journey


| Node.js | MQTT Broker | MQTT Client| Docker |
|---------|-------------|------------|--------|
|<a href="https://www.youtube.com/watch?v=TlB_eWDSMt4" target="video"><img src="./img/nodejs-icon.svg"  width="200px">Intro Video</a>   <a href="https://codewithmosh.com/p/the-complete-node-js-course" target="video"><img src="./img/node-master.png" width="200px">   Complete Course</a>|<a href="https://www.youtube.com/watch?v=eS4nx6tLSLs" target="video"><img src="./img/mqtt.png" width="256px">   What is MQTT?</a>   <a href="https://www.youtube.com/watch?v=WmKAWOVnwjE" target="video"><img src="./img/mqtt-broker.png" width="256px">   MQTT Broker</a>|<a href="https://www.youtube.com/watch?v=c_DPKujOmGw" target="video"><img src="./img/sensorClient2.png" width="256px">   Short Client Video</a>   <a href="https://youtu.be/QAaXNt0oqSI" target="video"><img src="./img/tempSensorClient.png" width="256px">   Detailed Client Video</a>|<a href="https://youtu.be/ASNL27a7sE4" target="video"><img src="./img/DockerHub.png" width="256px">   Short Docker Video</a>   <a href="https://www.youtube.com/watch?v=fqMOX6JJhGo" target="video"><img src="./img/docker-icon_copy.png" width="256px">   Complete Docker Course</a>|The Realm MQTT framework runs on node.js.  If you are not familiar with node.js then I recommend the following video to learn the basics: [Node.js Tutorial for Beginners: Learn Node in 1 Hour](https://www.youtube.com/watch?v=TlB_eWDSMt4) A full course with RESTful APIs with Node, Express, and MongoDB is here: [The Complete Node.js Course](https://codewithmosh.com/p/the-complete-node-js-course)| If you are not familiar with MQTT here is a great getting started videos: [What is MQTT?](https://www.youtube.com/watch?v=eS4nx6tLSLs) [What is the MQTT Broker?](https://www.youtube.com/watch?v=WmKAWOVnwjE)  | In our example we are using python libraries to read the sensor data and node.js to run the MQTT Broker and realm Middleware.  The simpliest solution is to create a python MQTT client.  Short videos here:[MQTT Clients in Python with the paho-mqtt module](https://www.youtube.com/watch?v=c_DPKujOmGw) and here: [How to Use the Paho Python MQTT Client- (Beginners Guide)](https://youtu.be/QAaXNt0oqSI) |  The basic introduction to docker is here [Docker Hub Introduction Tutorial](https://youtu.be/ASNL27a7sE4) |





### Install the real MQTT Broker and middleware   
Note: This section requires the realm mqtt libraries which will be found [here] in the near future.


### Configure the broker to connect to your Realm application
Edit the realm.js file under the broker source utils directory.   
   
```
/IOT/sensor/broker/src/utils $ vi realm.js
```

    
Change the new app function to include the app_id of your realm application.   
   
```js
'use strict';

const Realm = require('realm');

exports.app = new Realm.App('your-realm-app-id');

exports.loginEmailPassword = async (email, password) => {
  const credentials = Realm.Credentials.emailPassword(email, password);
  return this.app.logIn(credentials).catch((error) => {
    console.log(error);
    return false;
  });
};
```   

Now we will do the same to the realm middleware as well, we will replace the 'your-realm-app-id' portion with the realm app you created.  We will update the middleware realm.js file in the following directory:   
   
```
~/IOT/sensor/middleware/aedes-emitter-realm $ vi realm.js
```


```js
'use strict'

const Realm = require('realm')

const app = new Realm.App('your-realm-app-id')

exports.app = app

exports.loginEmailPassword = async (email, password) => {
  const credentials = Realm.Credentials.emailPassword(email, password)
  try {
    const user = await app.logIn(credentials)
    if (user.id !== app.currentUser.id) {
      throw new Error('Current user invalid')
    }
    return user
  } catch (err) {
    console.error('Failed to log in', err)
    return false
  }
}
```   
   
Now lets edit the username and password for the email user we created.  There are two ways to set the password, the proper way is to set up environment variables.  In order to create a quick test we can comment out the use of environment variables and hardcode the userename and password in the index.js.     
   
```
~/IOT/sensor/broker/src $ vi index.js
```
   
```js
const main = async () => {
/*  const user = await utils.realm.loginEmailPassword(
    process.env.AEDES_REALM_EMAIL,
    process.env.AEDES_REALM_PASSWORD
  );
*/

const user = await utils.realm.loginEmailPassword(
    'mqtt@pi.com',
    'Passw0rd'
  );
```

## Creating a Python MQTT client

We begin by installing the python libraries for paho-mqtt on the raspberry pi. We do this by running the following from the command line:   
   
```
sudo pip install paho-mqtt
```


