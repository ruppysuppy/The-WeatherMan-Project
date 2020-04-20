from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'core/home.html', {"page": "Home", "arr": [1, 5, 1, 5, 1, 5, 1]})

def details(request):
    return render(request, 'weather/weatherdetail.html', {"page": "Detail"})
    
def about(request):
    return render(request, 'core/about.html', {"page": "About"})