from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the API key

app = Flask(__name__)

# OpenWeatherMap API key (replace with your actual key)
API_KEY = os.getenv('API_KEY')

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    weather_data = None
    error_message = None

    if request.method == 'POST':
        city = request.form['city']
        # Make the API request
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'  # Use 'metric' for Celsius
        }
        try:
            response = requests.get(BASE_URL, params=params)
            data = response.json()

            if data['cod'] == 200:
                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                }
            else:
                error_message = "City not found or API request failed."
        except Exception as e:
            error_message = f"Error fetching data: {str(e)}"
    
    return render_template('weather.html', weather_data=weather_data, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
