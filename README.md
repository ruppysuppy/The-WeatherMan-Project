# THE WEATHER MAN PROJECT
This is a simple Django project which displays the weather details (current + forecast + previous) of any location in the world.

### Resources Used
* Google Places JavaScript API: For the place name auto-completion
* Open Weather Maps API: For getting the weather details
* Chart.js: For plotting the charts of previous data

### How To Use
Follow the steps to start the local server on your machine:
* __Enter Your Google API Key (./templates/core/home.html) and Open Weather Maps API KEY (./weather_details/views.py). You receive the key after you make an account in the Google Cloud Platform (and Activate Google Places JavaScript API) and Open Weather Maps__
* Download and install Python 3.x
* Navigate to the repository folder
* Open the Terminal/CMD/PowerShell at the location (Shift + Right Click => Run Command Prompt/PowerShell for Windows or Right Click => Run Terminal for Linux based system)
* Run the Command 'pip install -r requirements.txt' (to download and install the dependencies)
* Run the Command 'python manage.py runserver'
* Run the website (Navigate to '127.0.0.1:8000' on a web-browser)