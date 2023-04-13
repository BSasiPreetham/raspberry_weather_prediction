from sklearn import linear_model
import pandas as pd
import openpyxl
import Adafruit_DHT
from bmp280 import BMP280
import time


DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
    
# Initialise the BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)


#----------------------creating dataframe-------------------------
df = pd.DataFrame(columns=['TEMPERATURE','HUMIDITY','PRESSURE','RESULT'])
wb = openpyxl.load_workbook("weatherPrediction.xlsx")
ws = wb['Sheet1']

value_range = ws['B2':'E367']
for a,b,c,d in value_range:
    if(d.value == "Sunny"):
        r=1
    else:
        r=0
    df = df.append({'TEMPERATURE':a.value, 'HUMIDITY':b.value, 'PRESSURE':c.value, 'RESULT':r},ignore_index=True)


#---------------------Training model----------------------
reg = linear_model.LinearRegression()
reg.fit(df.drop('RESULT',axis='columns'),df.RESULT)
reg.coef_
reg.intercept_

#----------------------loop---------------------------
#time.sleep(1)
while True:
    #input data from DHT
    hum, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    
        
    #input data from BMP
    dum = bmp280.get_temperature()
    pressure = bmp280.get_pressure()
    pressure = pressure * 0.02952
    
    
    if hum is not None and temp is not None and pressure is not None:
        print("T:{0:0.1f}C  H:{1:0.1f}%".format(temp,hum))
        print('P:{:05.2f}hg'.format(pressure))
        print('Prediction')
        x = reg.predict([[temp,hum,pressure]])
        print('{0:0.2f}% chance of sunny'.format(x[0]*100))
        print()
    else:
        print("Fail")
    time.sleep(4)
        