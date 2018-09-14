import urllib.request as req
import pprint
import json
# import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

api_key = "b42093d17fb4129561f860377096a44a"


def main():

    search_type = input('What do you want to use to search for weather("zip", "city"): ')
    url = get_html(search_type, api_key)
    temperature_units = input("Enter what units you want the temperature in: ")
    data = get_data(url)

    # pprint.pprint(data)
    # method used to reach the temperature
    # pprint.pprint(data["list"][0]["main"]["temp"])

    # gets a whole list of temperatures for use
    temperature_list = []

    # receives all the temperatures and puts it into a list
    for index_count in range(40):
        # print(data["list"][index_count]["main"]["temp"])
        #  gets the temperature
        temperature = data["list"][index_count]["main"]["temp"]
        temperature_list.append(temperature)
        index_count += 1
    pprint.pprint(temperature_list)
    print("REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")

    # if temperature_units.lower() == "fahrenheit" or temperature_units == "f":
    #     for temperature in range(len(temperature_list)):
    #         temp_list = []
    #         temp.list.append[]
    if temperature_units.lower() == "celsius" or temperature_units == "c":
        for temperature in temperature_list:
            temp_list = []
            temp_list.append(temperature - 273)
            # temperature_list.remove(temperature)
        # temp_list = temperature_list
    else:
        print("----- Invalid response -----")
        print("")
        temperature_units = input("Enter what units you want the temperature in: ")
# # converts the given temperature(kelvin) and converts to celsius

# celsius_temperature = round(kelvin_temperature - 273, 2)

    pprint.pprint(temp_list)

# goes to the url and sends back the data for use
def get_data(url):
    response = req.Request(url)
    json_object = req.urlopen(response)
    json_data = json.load(json_object)
    return json_data


# receives a search type and returns the respective url
def get_html(search_type, api_key):
    if search_type.lower() == "city":
        city = input("Enter the city you want weather for: ")
        url = "http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}".format(city, api_key)
        # print(url)
        return url
    elif search_type.lower() == "zip":
        zip_code = int(input("Enter zip code you want weather for: "))
        url = "http://api.openweathermap.org/data/2.5/forecast?zip={}&appid={}".format(zip_code, api_key)
        # print(url)
        return url
    else:
        print("----- Invalid response -----")
        print("")
        search_type = input('What do you want to use to search for weather("zip", "city"): ')
        return get_html(search_type, api_key)


if __name__ == "__main__":
    main()
