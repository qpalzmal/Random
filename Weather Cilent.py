'''
This program scraps the web for data and uses it to graph the data for analysis by the user
'''


import urllib.request
import pprint
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
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

    search = input('What do you want to use to search for weather ("zip", "city"): ')
    url = get_html(search, units, API_KEY)

    data = get_data(url)
    # pprint.pprint(data)

    # method used to reach the temperature/date time/wind speed
    # pprint.pprint(data["list"][0]["main"]["temp"])
    # pprint.pprint(data["list"][0]["dt_txt"]
    # pprint.pprint(data["list"][0]["wind"]["speed"])

    # receives the temperature/date time/wind speed from the data
    temperature_list = []
    datetime_list = []
    wind_speed_list = []
    for index in range(len(data["list"])):
        # gets the temperature
        temperature = data["list"][index]["main"]["temp"]
        temperature_list.append(temperature)
        # gets the time
        date_time = data["list"][index]["dt_txt"]
        datetime_list.append(date_time)
        # gets the wind speed
        wind_speed = data["list"][index]["wind"]["speed"]
        wind_speed_list.append(wind_speed)
        index += 1

    # pprint.pprint(temperature_list)
    # pprint.pprint(datetime_list)
    # pprint.pprint(wind_speed_list)

    local_time_list = []
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
        local_time_list.append(local)

    # pprint.pprint(local_time_list)

    # shows temperature that is equal to the time
    # temperature_time_list = []
    # for i in range(40):
    #     temp = temperature_list[i]
    #     time = local_time_list[i]
    #     temperature_time_list.append(str(temp) + " = " + str(time))
    # pprint.pprint(temperature_time_list)

    weather_data = {"Time": [],
                    "Temperature": [],
                    "Wind Speed": []}

    for i in range(len(temperature_list)):
        weather_data["Time"].append(local_time_list[i])
        weather_data["Temperature"].append(temperature_list[i])
        weather_data["Wind Speed"].append(wind_speed_list[i])

    dataframe = pd.DataFrame(weather_data)
    print(dataframe)

    stats1 = linregress(dataframe["Time"], dataframe["Temperature"])
    stats2 = linregress(dataframe["Time"], dataframe["Wind Speed"])

    plt.subplot(2, 1, 1)
    m1 = stats1.slope
    b1 = stats1.intercept
    plt.plot(dataframe["Time"], m1 * dataframe["Time"] + b1, color="red")

    plt.subplot(2, 1, 2)
    m2 = stats2.slope
    b2 = stats2.intercept
    plt.plot(dataframe["Time"], m2 * dataframe["Time"] + b2, color="red")



    # time/temp plot
    plt.subplot(2, 1, 1)
    plt.plot(dataframe["Time"], dataframe["Temperature"], color="blue", linewidth=2.5, linestyle="-")
    plt.ylabel("Temperature({})".format(units_symbol))

    # time/wind speed plot
    plt.subplot(2, 1, 2)
    plt.plot(dataframe["Time"], dataframe["Wind Speed"], color="green", linewidth=2.5, linestyle="-")
    plt.xlabel("Date(Y-M-D)")
    plt.ylabel("Wind Speed(m/s)")

    plt.show()


# receives a search type and returns the respective url
def get_html(search, units, key):
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
        print("----- Invalid response -----")
        search = input('What do you want to use to search for the weather ("zip", "city"): ')
        return get_html(search, units, key)


# goes to the url and sends back the data for use
def get_data(url):
    response = urllib.request.Request(url)
    json_object = urllib.request.urlopen(response)
    json_data = json.load(json_object)
    return json_data


if __name__ == "__main__":
    main()
