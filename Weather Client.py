'''
This program scraps the web for data and uses it to graph the data for analysis by the user
'''


import urllib.request
# import pprint
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import tz


API_KEY = "b42093d17fb4129561f860377096a44a"


def main():

    # asks user for units of measurement, unit will default to fahrenheit if any other answer is given
    units = input("Enter what units you want the temperature in (type either the letter symbol or the word): ")
    if units.lower() == "celsius" or units.lower() == "c":
        print("Temperature units has been set to Celsius (°C)")
        units = "metric"
        units_symbol = "°C"
    elif units.lower() == "kelvin" or units.lower() == "k":
        print("Temperature units has been set to Kelvin (K)")
        units = "default"
        units_symbol = "K"
    else:
        print("Temperature units has been set to Fahrenheit (°F)")
        units = "imperial"
        units_symbol = "°F"

    url = get_html(units, API_KEY)

    data = get_data(url)
    # pprint.pprint(data)

    # method used to reach the temperature/date time/wind speed
    # pprint.pprint(data["list"][0]["main"]["temp"])
    # pprint.pprint(data["list"][0]["dt_txt"]
    # pprint.pprint(data["list"][0]["wind"]["speed"])

    # receives the temperature/date time/wind speed from the data
    weather_data = {"Time": [],
                    "Temperature": [],
                    "Wind Speed": [],
                    "Wind Direction": [],
                    "Average Temperature": []}
    datetime_list = []

    for index in range(len(data["list"])):
        # gets the time
        datetime_list.append(data["list"][index]["dt_txt"])
        # gets the temperature
        weather_data["Temperature"].append(data["list"][index]["main"]["temp"])
        # gets the wind speed
        weather_data["Wind Speed"].append(data["list"][index]["wind"]["speed"])
        # gets the wind direction
        weather_data["Wind Direction"].append(data["list"][index]["wind"]["deg"])

    total = 0
    for number in weather_data["Temperature"]:
        total += number
    average = total / int(len(weather_data["Temperature"]))
    for count in range(40):
        weather_data["Average Temperature"].append(average)

    # pprint.pprint(datetime_list)
    # pprint.pprint(weather_data["Temperature"])
    # pprint.pprint(weather_data["Wind Speed"])
    # pprint.pprint(weather_data["Average Temperature"]

    # Auto-detect zones
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # utc = datetime.utcnow()
    for index in datetime_list:
        # print(index)
        utc = datetime.strptime(index, '%Y-%m-%d %H:%M:%S')
        # print(utc)

        # Tell the datetime object that it's in UTC time zone since
        # datetime objects are 'naive' by default
        utc = utc.replace(tzinfo=from_zone)
        # print(utc)

        # Convert time zone
        local = utc.astimezone(to_zone)
        # print(local)
        weather_data["Time"].append(local)

    dataframe = pd.DataFrame(weather_data)
    dataframe.set_index("Time", inplace=True)
    # print(dataframe)

    # time/temp plot
    plt.subplot(2, 1, 1)
    plt.plot(dataframe.index.values, dataframe["Temperature"], color="blue", linewidth=2.5, linestyle="-")
    plt.plot(dataframe.index.values, dataframe["Average Temperature"], color="black", linewidth=2.5, linestyle="-")
    plt.legend(None, ("Temperature", "Average Temperature"))
    plt.ylabel("Temperature({})".format(units_symbol))

    # time/wind speed plot
    plt.subplot(2, 1, 2)
    plt.plot(dataframe.index.values, dataframe["Wind Speed"], color="green", linewidth=2.5, linestyle="-")
    plt.xlabel("Date(Y-M-D)")
    plt.ylabel("Wind Speed(m/s)")

    while True:
        plt.show()


# receives a search type and returns the respective url
def get_html(units, key):
    search = input('What do you want to use to search for weather ("zip", "city"): ')
    if search.lower() == "city":
        city = input("Enter the city you want the weather for: ")
        url = "http://api.openweathermap.org/data/2.5/forecast?q={}&units={}&appid={}".format(city, units, key)
        # print(url)
        return url
    elif search.lower() == "zip":
        zip_code = int(input("Enter zip code you want the weather for: "))
        url = "http://api.openweathermap.org/data/2.5/forecast?zip={}&units={}&appid={}".format(zip_code, units, key)
        # print(url)
        return url
    else:
        print("----- Received Invalid Response -----")
        print('----- Search has now defaulted to "city" -----')
        city = input("Enter the city you want the weather for: ")
        url = "http://api.openweathermap.org/data/2.5/forecast?q={}&units={}&appid={}".format(city, units, key)
        # print(url)
        return url


# goes to the url and sends back the data for use
def get_data(url):
    response = urllib.request.Request(url)
    json_object = urllib.request.urlopen(response)
    json_data = json.load(json_object)
    return json_data


if __name__ == "__main__":
    main()
