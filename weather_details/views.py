from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'core/home.html', {"page": "Home", "arr": [1, 5, 1, 5, 1, 5, 1]})

def details(request):
    location = request.GET['search_input'].split(',')

    temp_high = [5, 5, 6, 7, 4, 6, 4.2]
    temp_low = [2, 1, 2, 3, 2, 1, 1.2]
    precipitation = [0, 0, 0, 0, 0, 0, 0.5]
    humidity = [50, 60, 55, 40, 43.2, 30, 50]
    print(location[0])

    return render(request, 'weather/weatherdetail.html', {"page": "Detail", 
                            "temp_high": temp_high,
                            "temp_low": temp_low, 
                            "precipitation": precipitation,
                            "humidity": humidity
                        })
    
def about(request):
    return render(request, 'core/about.html', {"page": "About"})