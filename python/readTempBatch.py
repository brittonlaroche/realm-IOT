import Adafruit_DHT
import time
import requests
import datetime
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
BATCH_LIST = []
RETRY_LIST = []
BATCH_SIZE = 1
RETRY_LIMIT = 2

def transmitData(inBatchList):
    batchLen = len(inBatchList)
    numRetrys = 0
    listNum = 0
    sResponse = ""
    response = ""
    batchData = ""
    url = 'https://webhooks.mongodb-realm.com/api/client/v2.0/app/inventory-hhsot/service/Receive-IOT-Data/incoming_webhook/IOT-WH'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    while listNum < BATCH_SIZE and listNum < len(inBatchList):
        if listNum == 0:
            batchData = batchData + inBatchList[listNum]
        else:
            batchData = batchData + "," + inBatchList[listNum]
        listNum += 1
    insertData = "[" + batchData + "]"
    while numRetrys < RETRY_LIMIT and sResponse != "<Response [200]>":
        try:
            response = requests.post(url, data=insertData, headers=headers )
            print(response)
            #for x in response:
            #    print(x)
        except:
            response = "E"
            print("Error transmitting sensor data")
        sResponse = str(response)
        numRetrys += 1
        time.sleep(1)
    return sResponse

def addToRetryList(inBatchList, inRetryList):
    #printRetryList(inRetryList);
    batchLen = len(inBatchList)
    print("batchLen:" + str(batchLen))
    listNum = 0
    while listNum < batchLen:
        listItem = str(inBatchList[listNum])
        print("listItem: "+ listItem);
        inRetryList.append(listItem)
        listNum += 1
    return inRetryList

def reTransmitData(inRetryList):
    while len(inRetryList) > 0:
        listNum = 0
        newBatchList =[]
        while listNum < BATCH_SIZE and listNum < len(inRetryList):
            newBatchList.append(inRetryList[listNum])
            listNum += 1
        print("Resending data that failed earlier transmission with a batch of " + str(BATCH_SIZE))
        sResponse = transmitData(newBatchList)
        if sResponse == "<Response [200]>":
            # We succesfully retransmitted the data
            # Remove the succesful transmissions from the RETRY list
            delNum = 0
            while delNum < BATCH_SIZE and delNum < len(inRetryList):
                del inRetryList[0]
                delNum += 1
            #print("reTransmitData After Reseting list")
            #printRetryList(inRetryList)
        else:
            #we are having connectivity issues, try again later
            return inRetryList

def printRetryList(inRetryList):
    print("Retry List:")
    i = 0
    for x in inRetryList:
        print( str(i) + ": " + x)
        i += 1

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        sensorDate = datetime.datetime.now()
        ftemp = (temperature * 9/5)+32
        data = "{\"sensorId\":\"T89176\", \"temperature\":" +str(ftemp) +", \"humidity\":" + str(humidity) +", \"sensorDate\":\"" + str(sensorDate) + "\"}"
        print(data)
        BATCH_LIST.append(data)
        if len(BATCH_LIST) >= BATCH_SIZE:
            sResponse = transmitData(BATCH_LIST)
            if sResponse == "<Response [200]>":
                BATCH_LIST = []
            else:
                print("Error Transmitting data")
                RETRY_LIST = addToRetryList(BATCH_LIST, RETRY_LIST)
                BATCH_LIST = []
        if RETRY_LIST is not None and len(RETRY_LIST) > 0:
            RETRY_LIST = reTransmitData(RETRY_LIST)
    else:
        print("Sensor failure. Check wiring.")
    time.sleep(3)
