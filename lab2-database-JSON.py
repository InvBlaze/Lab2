'''
Script to access weather data from openweathermap.org using a REST API
Data are returned as a JSON string
The JSON string is then deserialized/parsed into a Python dictionary
Sample data fields are printed.

See http://openweathermap.org/current#current for the API

Originally written by Cheryl Schramm ~2015
Updated by James Green Jan-2023
'''

from urllib.request import urlopen 
from urllib.parse import urlencode
import json
import sqlite3

# The URL that is formatted: http://api.openweathermap.org/data/2.5/weather?APPID=a808bbf30202728efca23e099a4eecc7&units=imperial&q=ottawa
# As of October 2015, you need an API key.
# Prof Schramm created this API key several years ago. If it doesn?t work, get your own.
apiKey = "a808bbf30202728efca23e099a4eecc7"   
# Query the user for a city
city = input("Enter the name of a city whose weather you want: ")

# Build the URL parameters
params = {"q":city, "units":"metric", "APPID":apiKey }
arguments = urlencode(params)

# Get the weather information
address = "http://api.openweathermap.org/data/2.5/weather"
url = address + "?" + arguments

print(f"Requesting data from URL: {url}")
webData = urlopen(url)
results = webData.read().decode('utf-8')  # results is a JSON string
webData.close()

print("The raw JSON string returned by the query is")
print(results)

# Deserialize/parse the JSON string into a Python Dictionary data structure
# See https://www.geeksforgeeks.org/json-loads-in-python/ for loads details
data = json.loads(results)  

# Use the Dictionary to print specific fields from the data
print ("Temperature: %d%sC" % (data["main"]["temp"], chr(176) ))
print ("Humidity: %d%%" % data["main"]["humidity"])
print ("Pressure: %d" % data["main"]["pressure"] )
print ("Wind : %d" % data["wind"]["speed"])

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('weather_data.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS wind_speed
             (city TEXT, speed REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

# Insert the current wind speed into the database
c.execute("INSERT INTO wind_speed (city, speed) VALUES (?, ?)", (city, data["wind"]["speed"]))
conn.commit()

# Retrieve the second most recent wind speed for the city
c.execute('''SELECT speed FROM wind_speed 
             WHERE city = ? 
             ORDER BY timestamp DESC 
             LIMIT 1 OFFSET 1''', (city,))
second_most_recent = c.fetchone()

if second_most_recent:
    second_most_recent_speed = second_most_recent[0]
    current_speed = data["wind"]["speed"]
    if current_speed > second_most_recent_speed:
        print("The most recent wind speed is larger than the second most recent entry.")
    elif current_speed < second_most_recent_speed:
        print("The most recent wind speed is smaller than the second most recent entry.")
    else:
        print("The most recent wind speed is the same as the second most recent entry.")
else:
    print("Not enough data to compare wind speeds.")

# Close the database connection
conn.close()