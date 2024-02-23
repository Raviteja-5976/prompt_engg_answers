# Use an API to fetch the current weather data for your city and display 
# the temperature and humidity in a human-readable format.  

import requests

def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

def display_weather(data):
    if data["cod"] == 200:
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        city = data["name"]
        country = data["sys"]["country"]
        print(f"Current weather in {city}, {country}:")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
    else:
        print("Failed to fetch weather data. Check your city name or API key.")

# Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
api_key = "8566ae627bf8f3d9f6aa9eea7aebec3d"
city = "hyderabad"
weather_data = get_weather(api_key, city)
display_weather(weather_data)
