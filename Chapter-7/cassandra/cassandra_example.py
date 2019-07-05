'''
MIT License

Copyright (c) 2019 Arshdeep Bahga and Vijay Madisetti

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


import pyowm 
import time 
from datetime import date 
import datetime 
import cPickle 
from cassandra.cluster import Cluster 
 
PYOWM_KEY='<enter>' 
owm = pyowm.OWM(PYOWM_KEY) 
 
## create Cassandra instance 
cluster = Cluster() 
 
## establish Cassandra connection, using local default 
session = cluster.connect('weatherkeyspace')  
places=['New York,US','Los Angeles,US','Chicago,US', 
'Houston,US', 'Philadelphia,US', 'Phoenix,US',  
'San Antonio,US','San Diego,US','Dallas,US','San Jose,US'] 
 
for place in places: 
    print place 
    observation = owm.weather_at_place(place) 
    w= observation.get_weather() 
     
    rain= w.get_rain() 
    if rain.has_key('all'): 
        rainVolume = rain['all'] 
    else: 
        rainVolume = 0 
             
             
    statement="INSERT INTO weathernew (city, time, currentTemperature, weatherStatus, cloudCoverage, rainVolume, windSpeed, humidity, pressure) VALUES('" + str(place)+"','"+ str(w.get_reference_time(timeformat='iso'))+ "',"+ str(w.get_temperature(unit='celsius')['temp'])+",'"+ str(w.get_detailed_status())+"','"+ str(w.get_clouds())+"','"+ str(rainVolume) +"',"+ str(w.get_wind()['speed'])+","+ str(w.get_humidity())+","+ str(w.get_pressure()['press'])+")" 
     
    session.execute(statement) 

for place in places: 
    print place 
    fc = owm.daily_forecast(place, limit=7) 
    f = fc.get_forecast() 
    forecast_list=[] 
    for w in f.get_weathers(): 
        forecast_dict={} 
        t=w.get_reference_time() 
        forecast_dict['date'] = 
        datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d') 
        forecast_dict['tempMin']= w.get_temperature(unit='celsius')['min'] 
        forecast_dict['tempMax']= w.get_temperature(unit='celsius')['max'] 
         
        rain= w.get_rain() 
        if rain.has_key('all'): 
            forecast_dict['rain'] = rain['all'] 
        else: 
            forecast_dict['rain'] = 0 
        forecast_dict['status']= w.get_detailed_status() 
        forecast_list.append(forecast_dict) 
 
    statement="INSERT INTO forecast (city, forecastList) VALUES('"+str(place)+"','"+ cPickle.dumps(forecast_list).encode("hex") +"')" 
         
    session.execute(statement)
