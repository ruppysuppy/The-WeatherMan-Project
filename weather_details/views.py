from django.shortcuts import render
import datetime
import requests as rq

from geopy.geocoders import Nominatim

API_END_PT_CURR = "http://api.openweathermap.org/data/2.5/weather?lat={:.1f}&lon={:.1f}&appid={}&units=metric"
API_KEY = "d496fded6f52e05a233d961633e95207"
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
        url = API_END_PT_CURR.format(latitude, longitude, API_KEY)
        response_curr = rq.get(url=url).json()
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
    
    curr_temp = response_curr["main"]["temp"]
    curr_precipitation = response_curr["weather"][0]["main"]
    curr_humidity = response_curr["main"]["humidity"]
    
    forecast_data = [(5, 2), (5, 3), (6, 3), (7, 1)]
    forecast = list(zip(forecast_data, [(today + datetime.timedelta(days=i)).strftime('%d/%m') for i in range(1, 5)]))

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
                            "location": location
                        })
    
def about(request):
    return render(request, 'core/about.html', {"page": "About"})