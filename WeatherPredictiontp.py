from sklearn import linear_model
import pandas as pd
import openpyxl
from bmp280 import BMP280
import time
import requests


api_key = '085TV6N8ZHG1RUKO'

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
    
# Initialise the BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)


def send_data_to_thingspeak(temp, humidity, pressure, result):
    # Construct the API endpoint URL
    url = 'https://api.thingspeak.com/update'
    payload = {'api_key': api_key, 'field1': temp, 'field2': humidity, 'field3':pressure, 'field4':result}
    # Send the HTTP request to ThingSpeak
    response = requests.get(url, params=payload)

    # Print the server's response
    print(response.text)

#----------------------creating dataframe-------------------------
df = pd.DataFrame(columns=['TEMPERATURE','PRESSURE','RESULT'])
wb = openpyxl.load_workbook("weatherPredictiontp.xlsx")
ws = wb['Sheet1']

value_range = ws['A2':'C115']
for a,b,c in value_range:
    if(c.value == "Sunny"):
        r=1
    else:
        r=0
    df = df.append({'TEMPERATURE':a.value, 'PRESSURE':b.value, 'RESULT':r},ignore_index=True)


#---------------------Training model----------------------
reg = linear_model.LinearRegression()
reg.fit(df.drop('RESULT',axis='columns'),df.RESULT)
reg.coef_
reg.intercept_

#----------------------loop---------------------------
#time.sleep(1)
while True:
    
        
    #input data from BMP
    temp = bmp280.get_temperature()
    pressure = bmp280.get_pressure()
    pressure = pressure * 0.02952
    
    
    if temp is not None and pressure is not None:
        print("T:{0:0.1f}C".format(temp))
        print('P:{:05.2f}hg'.format(pressure))
        print('Prediction')
        x = reg.predict([[temp,pressure]])
        print('{0:0.2f}% chance of sunny'.format(x[0]*100))
        send_data_to_thingspeak(temp, humidity, pressure, result)
        print()
    else:
        print("Fail")
    time.sleep(4)
        