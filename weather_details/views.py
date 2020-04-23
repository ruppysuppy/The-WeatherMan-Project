# 3rd party packages

from django.shortcuts import render
from geopy.geocoders import Nominatim

# python packages
import datetime
import requests as rq
from time import mktime

# api end points
API_END_PT_CURR_FORCAST = "https://api.openweathermap.org/data/2.5/onecall?lat={:.1f}&lon={:.1f}&appid={}&units=metric"
API_END_PT_HISTORIC_DATA = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={:.1f}&lon={:.1f}&dt={}&appid={}&units=metric"

# open weather maps api key
API_KEY = "d496fded6f52e05a233d961633e95207"

# open weather maps image location
IMAGE_URL = "http://openweathermap.org/img/wn/{}@2x.png"

# locator to convert location name to latitude and longitude
locator = Nominatim(user_agent="weatherManGeoCoder")

# home page rendering
def home(request):
    return render(request, 'core/home.html', {"page": "Home"})

# about page rendering
def about(request):
    return render(request, 'core/about.html', {"page": "About"})
    
# error page rendering
def error(request, data):
    # Handles Location not found
    if (data == "Location"):
        error_data = "Seems Like You have entered a wrong location"
    # Handles Server did not respond
    elif (data == "Server"):
        error_data = "Seems like the server is not responding."

    return render(request, 'core/error.html', {"page": "Error", "cause": data, "error": error_data})

# weather details page rendering
def details(request):
    # getting the user's chosen location
    location = request.GET['search_input']
    # getting today's date
    today = datetime.date.today()
    
    # checking if the input is valid
    try:
        location_details = locator.geocode(location)
        latitude = location_details.latitude
        longitude = location_details.longitude
    except:
        return error(request, "Location")
    
    # getting the response from open weather maps api
    try:
        url = API_END_PT_CURR_FORCAST.format(latitude, longitude, API_KEY)
        response = rq.get(url=url).json()
    except:
        return error(request, "Server")
    
    # getting current data
    curr_temp = response["current"]["temp"]
    curr_humidity = response["current"]["humidity"]
    curr_icon = IMAGE_URL.format(response["daily"][0]["weather"][0]["icon"])
    curr_status = response["daily"][0]["weather"][0]["main"]

    try:
        curr_precipitation = response["daily"][0]["rain"]
    except KeyError:
        curr_precipitation = 0
    
    # creating forecast data
    forecast_data = []
    
    # getting the forecast
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

    # data dict stores the past data
    data_dict = {(today - datetime.timedelta(days=i)): [0, 9999, 0, 0] for i in range(1, 7)}
    days = [key.strftime("%d/%m") for key in data_dict][:-2]

    # iterating through the days
    for key in data_dict:
        # creating the api
        url = API_END_PT_HISTORIC_DATA.format(latitude, longitude, int(mktime(key.timetuple())), API_KEY)

        # getting the response for past data
        response_temp = rq.get(url=url)
        response = response_temp.json()
        response_code = response_temp.status_code

        rain = 0
        humidity_temp = []
        
        # synthesising the data from the response
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

    # breaking the generated result in the data_dict into the required variables
    temp_high = [data_dict[key][0] for key in data_dict][:-2]
    temp_low = [data_dict[key][1] for key in data_dict][:-2]
    precipitation = [data_dict[key][2] for key in data_dict][:-2]
    humidity = [data_dict[key][3] for key in data_dict][:-2]

    # rendering the page
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
                            "curr_icon": curr_icon, 
                            "curr_status": curr_status
                        })