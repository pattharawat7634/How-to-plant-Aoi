
import requests

# Your API key from OpenWeatherMap
API_KEY = '2d2aceb6784907982259211844276aa2'
CITY = 'Thailand'

# OpenWeatherMap URL
BASE_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Sending HTTP request
response = requests.get(BASE_URL)

# Extracting data in JSON format
data = response.json()

# Checking if request was successful
if data["cod"] == 200:
    main = data['main']
    temperature = main['temp']
    humidity = main['humidity']
    weather_desc = data['weather'][0]['description']
    
    # Printing the results
    print(f"Weather in {CITY}:")
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
    print(f"Description: {weather_desc}")
else:
    print("City not found.")
