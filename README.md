# Realm IOT

```py
import Adafruit_DHT
import time
import requests




DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        # print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
        # print("temperature:" +str(temperature))
        # print("humidity:" + str(humidity))
        ftemp = (temperature * 9/5)+32
        data = "{sensorId:\"T89176\", temperature:" +str(ftemp) +", humidity:" + str(humidity) +"}"
        print(data)
        headers = {
            'Content-type': 'application/json',
        }
        response = requests.post('https://webhooks.mongodb-realm.com/api/client/v2.0/app/inventory-hhsot/service/Receive-IOT-Data/incoming_webhook/IOT-WH', headers=headers, data=data)
        for x in response:
            print(x)

    else:
        print("Sensor failure. Check wiring.");
    time.sleep(3);
    ```   
    
