import urllib.request
import json
import pprint
import time


def main():

    url = get_html()
    json_data = get_data(url)
    pprint.pprint(json_data)
    print(json_data["list"][0]["main"]["temp"])


def get_data(url):
    json_req = urllib.request.Request(url)
    json_obj = urllib.request.urlopen(json_req)
    data = json.load(json_obj)
    return data


def get_html():
    search_type = input("What do you want to use to search for weather('zip' or 'city'): ")
    api_key = "b42093d17fb4129561f860377096a44a"
    if search_type.lower() == "city":
        city = input("Enter the city you want weather for: ")
        url = "http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}".format(city, api_key)
        print(url)
        return url
    elif search_type.lower() == "zip":
        zip_code = input("Enter zip code you want weather for: ")
        url = "http://api.openweathermap.org/data/2.5/forecast?zip={}&appid={}".format(zip_code, api_key)
        print(url)
        return url


if __name__ == "__main__":
    main()
