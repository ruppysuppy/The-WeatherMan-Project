from django.shortcuts import render
import datetime
import requests as rq

from geopy.geocoders import Nominatim

API_END_PT = "https://api.openweathermap.org/data/2.5/onecall?lat={:.1f}&lon={:.1f}&appid={}&units=metric"
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
                                        [0 for _ in range(4)], 
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
        url = API_END_PT.format(latitude, longitude, API_KEY)
        response = rq.get(url=url).json()
    except:
        return render(request, 'weather/weatherdetail.html', {
                            "curr_temp": "-",
                            "curr_precipitation": "-",
                            "curr_humidity": "-",
                            "forecast": list(
                                    zip(
                                        [0 for _ in range(4)], 
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

    temp_high = [5, 5, 6, 7, 4, 6, 4.2]
    temp_low = [2, 1, 2, 3, 2, 1, 1.2]
    precipitation = [0, 0, 0, 0, 0, 0, 0.5]
    humidity = [50, 60, 55, 40, 43.2, 30, 50]

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