import urllib.request as req
import pprint
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

api_key = "b42093d17fb4129561f860377096a44a"
temperature_list = []
time_list = []


def main():

    # asks user for units of measurement, unit will default to fahrenheit if no valid answer given
    units = input("Enter what units you want the temperature in(defaults to Fahrenheit(F) if there are any typos): ")
    if units.lower() == "celsius" or units.lower() == "c":
        print("Temperature units has been set to Celsius")
        units = "metric"
    elif units.lower() == "kelvin" or units.lower() == "k":
        print("Temperature units has been set to Kelvin")
        units = "default"
    else:
        print("Temperature units has been set to Fahrenheit")
        units = "imperial"

    search = input("\n"'What do you want to use to search for weather("zip", "city"): ')
    url = get_html(search, units, api_key)

    data = get_data(url)
    # pprint.pprint(data)

    # method used to reach the temperature and time
    # pprint.pprint(data["list"][0]["main"]["temp"])
    # pprint.pprint(data["list"][0]["dt_txt"]

    # receives all the temperatures and puts it into a list
    for index_count in range(40):
        # print(data["list"][index_count]["main"]["temp"])
        # gets the temperature
        temperature = data["list"][index_count]["main"]["temp"]
        temperature_list.append(temperature)
        index_count += 1

    # receives all the times and puts it into a list
    for index_count in range(40):
        # print(data["list"][index_count]["main"]["temp"])
        # gets the time
        time = data["list"][index_count]["dt_txt"]
        time_list.append(time)
        index_count += 1

    pprint.pprint(temperature_list)
    pprint.pprint(time_list)
    plt.plot(time_list, temperature_list)
    plt.show()


# goes to the url and sends back the data for use
def get_data(url):
    response = req.Request(url)
    json_object = req.urlopen(response)
    json_data = json.load(json_object)
    return json_data


# receives a search type and returns the respective url
def get_html(search, units, key):
    if search.lower() == "city":
        city = input("Enter the city you want weather for: ")
        url = "http://api.openweathermap.org/data/2.5/forecast?q={}&units={}&appid={}".format(city, units, key)
        # print(url)
        return url
    elif search.lower() == "zip":
        zip_code = int(input("Enter zip code you want weather for: "))
        url = "http://api.openweathermap.org/data/2.5/forecast?zip={}&units={}&appid={}".format(zip_code, units, key)
        # print(url)
        return url
    else:
        print("----- Invalid response -----")
        search = input('What do you want to use to search for weather("zip", "city"): ')
        return get_html(search, units, key)


if __name__ == "__main__":
    main()
