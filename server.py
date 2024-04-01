from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

# app is a Flask application
app = Flask(__name__)

# handle route for index.html
@app.route('/')
@app.route('/index')    # home_pages
def index():
    return render_template("index.html")

# handle route for weather.html
@app.route('/weather')
def get_weather():
    city = request.args.get('city')         # getting the city name passed from the form on index.html

     # Check for empty strings or string with only spaces, strip() strips away the empty spaces
    if not bool(city.strip()):
        # You could render "City Not Found" instead like we do below
        city = "Sahiwal"

    weather_data = get_current_weather(city)     # sendng city name to func() working with API for weather

    # City is not found by API
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')
 
    return render_template(
        "weather.html",
        # title,status,temp,feels_like are vaiables on weather.html
        # weather_data is json object made from the response of API => get_current_weather(), whose inside elements we are redering as weather data
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)