from django.shortcuts import render
from geopy.geocoders import Nominatim

import datetime
import requests as rq
from time import mktime

API_END_PT_CURR_FORCAST = "https://api.openweathermap.org/data/2.5/onecall?lat={:.1f}&lon={:.1f}&appid={}&units=metric"
API_END_PT_HISTORIC_DATA = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={:.1f}&lon={:.1f}&dt={}&appid={}&units=metric"
API_KEY = "d496fded6f52e05a233d961633e95207"
IMAGE_URL = "http://openweathermap.org/img/wn/{}@2x.png"
locator = Nominatim(user_agent="weatherManGeoCoder")

def home(request):
    return render(request, 'core/home.html', {"page": "Home"})

def details(request):
    location = request.GET['search_input']
    today = datetime.date.today()
    days = [(today - datetime.timedelta(days=i)).strftime('%d/%m') for i in range(1, 5)]
    
    try:
        location_details = locator.geocode(location)
        latitude = location_details.latitude
        longitude = location_details.longitude
    except:
        return render(request, 'weather/weatherdetail.html', {
                            "curr_temp": "-",
                            "curr_precipitation": "-",
                            "curr_humidity": "-",
                            "forecast": list(
                                    zip(
                                        [("-", "-", "-", "-", "-") for _ in range(3)], 
                                        [(today + datetime.timedelta(days=i)).strftime('%d/%m') for i in range(1, 5)]
                                    )
                                ),
                            "page": "Detail", 
                            "temp_high": [0 for _ in range(7)],
                            "temp_low": [0 for _ in range(7)], 
                            "precipitation": [0 for _ in range(7)],
                            "humidity": [0 for _ in range(7)],
                            "days": days, 
                            "location": location,
                            "error": "Location Could Not Be Found!"
                        })
    
    try:
        url = API_END_PT_CURR_FORCAST.format(latitude, longitude, API_KEY)
        response = rq.get(url=url).json()
    except:
        return render(request, 'weather/weatherdetail.html', {
                            "curr_temp": "-",
                            "curr_precipitation": "-",
                            "curr_humidity": "-",
                            "forecast": list(
                                    zip(
                                        [("-", "-", "-", "-", "-") for _ in range(3)], 
                                        [(today + datetime.timedelta(days=i)).strftime('%d/%m') for i in range(1, 5)]
                                    )
                                ),
                            "page": "Detail", 
                            "temp_high": [0 for _ in range(7)],
                            "temp_low": [0 for _ in range(7)], 
                            "precipitation": [0 for _ in range(7)],
                            "humidity": [0 for _ in range(7)],
                            "days": days, 
                            "location": location,
                            "error": "Response not received!"
                        })
    
    curr_temp = response["current"]["temp"]
    curr_humidity = response["current"]["humidity"]
    curr_icon = IMAGE_URL.format(response["daily"][0]["weather"][0]["icon"])

    try:
        curr_precipitation = response["daily"][0]["rain"]
    except KeyError:
        curr_precipitation = 0
    
    forecast_data = []
    
    for data in response["daily"][1:4]:
        try:
	        forecast_data.append((
                data["temp"]["max"], 
                data["temp"]["min"], 
                data["humidity"], 
                data["rain"], 
                IMAGE_URL.format(data["weather"][0]["icon"])
            ))
        except KeyError:
            forecast_data.append((
                data["temp"]["max"], 
                data["temp"]["min"], 
                data["humidity"], 
                0, 
                IMAGE_URL.format(data["weather"][0]["icon"])
            ))

    forecast = list(zip(forecast_data, [(today + datetime.timedelta(days=i)).strftime('%d/%m') for i in range(1, 4)]))

    data_dict = {(today - datetime.timedelta(days=i)): [0, 9999, 0, 0] for i in range(1, 7)}
    days = [key.strftime("%d/%m") for key in data_dict][:-2]

    for key in data_dict:
        url = API_END_PT_HISTORIC_DATA.format(latitude, longitude, int(mktime(key.timetuple())), API_KEY)

        response_temp = rq.get(url=url)
        response = response_temp.json()
        response_code = response_temp.status_code

        rain = 0
        humidity_temp = []
        
        if (response_code != 400):
            for data in response["hourly"]:
                time = datetime.date.fromtimestamp(data["dt"])

                if (data_dict[time][0] < data["temp"]):
                    data_dict[time][0] = data["temp"]
                if (data_dict[time][1] > data["temp"]):
                    data_dict[time][1] = data["temp"]
                
                try:
                    rain += data["rain"]
                except:
                    pass

                humidity_temp.append(data["humidity"])
        else:
            data_dict[key] = [0, 0, 0, 0]
        
        data_dict[key][2] = rain

        try:
            data_dict[key][3] = sum(humidity_temp) / len(humidity_temp)
        except ZeroDivisionError:
            data_dict[key][3] = 0

    temp_high = [data_dict[key][0] for key in data_dict][:-2] # [5, 5, 6, 7, 4, 6, 4.2]
    temp_low = [data_dict[key][1] for key in data_dict][:-2] # [2, 1, 2, 3, 2, 1, 1.2]
    precipitation = [data_dict[key][2] for key in data_dict][:-2] # [0, 0, 0, 0, 0, 0, 0.5]
    humidity = [data_dict[key][3] for key in data_dict][:-2] # [50, 60, 55, 40, 43.2, 30, 50]

    return render(request, 'weather/weatherdetail.html', {
                            "curr_temp": curr_temp,
                            "curr_precipitation": curr_precipitation,
                            "curr_humidity": curr_humidity,
                            "forecast": forecast,
                            "page": "Detail", 
                            "temp_high": temp_high,
                            "temp_low": temp_low, 
                            "precipitation": precipitation,
                            "humidity": humidity,
                            "days": days, 
                            "location": location,
                            "curr_icon": curr_icon
                        })
    
def about(request):
    return render(request, 'core/about.html', {"page": "About"})