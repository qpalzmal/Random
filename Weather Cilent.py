import urllib.request
import pprint
import json
# import time
import pandas

api_key = "b42093d17fb4129561f860377096a44a"


def main():

    search_type = input("What do you want to use to search for weather('zip' or 'city'): ")
    url = get_html(search_type, api_key)
    data = get_data(url)
    # pprint.pprint(data)
    # method used to reach the temperature
    # pprint.pprint(data["list"][0]["main"]["temp"])

    # gets a whole list of temperatures for use
    temperature_list = []

    for index_count in range(40):
        # print(data["list"][index_count]["main"]["temp"])
        #  gets the temperature
        kelvin_temperature = data["list"][index_count]["main"]["temp"]
        # converts the given temperature(kelvin) and converts to celsius
        celsius_temperature = round(kelvin_temperature - 273, 2)
        temperature_list.append(celsius_temperature)
        index_count += 1

    print(temperature_list)


# goes to the url and sends back the data for use
def get_data(url):
    response = urllib.request.Request(url)
    json_object = urllib.request.urlopen(response)
    json_data = json.load(json_object)
    return json_data


# receives a search type and returns the respective url
def get_html(search_type, api_key):
    if search_type.lower() == "city":
        city = input("Enter the city you want weather for: ")
        url = "http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}".format(city, api_key)
        print(url)
        return url
    elif search_type.lower() == "zip":
        zip_code = int(input("Enter zip code you want weather for: "))
        url = "http://api.openweathermap.org/data/2.5/forecast?zip={}&appid={}".format(zip_code, api_key)
        print(url)
        return url
    else:
        print("----- Invalid response -----""\n")
        search_type = input("What do you want to use to search for weather('zip' or 'city'): ")
        return get_html(search_type, api_key)


if __name__ == "__main__":
    main()
