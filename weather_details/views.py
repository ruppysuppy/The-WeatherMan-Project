from django.shortcuts import render
import datetime

# Create your views here.

def home(request):
    return render(request, 'core/home.html', {"page": "Home"})

def details(request):
    location = request.GET['search_input']
    today = datetime.date.today()
    days = [(today - datetime.timedelta(days=i)).strftime('%d/%m') for i in range(1, 5)]
    
    try:
        lat = request.GET["lat"]
        lng = request.GET["lng"]

    except:
        return render(request, 'weather/weatherdetail.html', {
                            "curr_max_temp": "-",
                            "curr_min_temp": "-",
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
                            "location": location
                        })

    curr_max_temp = 30
    curr_min_temp = 20
    curr_precipitation = 50
    curr_humidity = 40
    
    forecast_data = [(5, 2), (5, 3), (6, 3), (7, 1)]
    forecast = list(zip(forecast_data, [(today + datetime.timedelta(days=i)).strftime('%d/%m') for i in range(1, 5)]))

    temp_high = [5, 5, 6, 7, 4, 6, 4.2]
    temp_low = [2, 1, 2, 3, 2, 1, 1.2]
    precipitation = [0, 0, 0, 0, 0, 0, 0.5]
    humidity = [50, 60, 55, 40, 43.2, 30, 50]

    return render(request, 'weather/weatherdetail.html', {
                            "curr_max_temp": curr_max_temp,
                            "curr_min_temp": curr_min_temp,
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