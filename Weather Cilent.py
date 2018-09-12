import requests
import pprint
import json
import time


def main():

    search_type = input("What do you want to use to search for weather('zip' or 'city'): ")
    api_key = "b42093d17fb4129561f860377096a44a"
    get_html(search_type, api_key)


def get_html(search_type, api_key):
    if search_type.lower() == "city":
        city = input("Enter the city you want weather for: ")
        url = "http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}".format(city, api_key)
        print(url)
        response = requests.get(url)
        # print(response.status_code)
        # pprint.pprint(response.text)
        print(response.text)
        print(response.text[1][1][0])
    elif search_type.lower() == "zip":
        zip_code = input("Enter zip code you want weather for: ")
        url = "http://api.openweathermap.org/data/2.5/forecast?zip={}&appid={}".format(zip_code, api_key)
        print(url)
        response = requests.get(url)
        # print(response.status_code)
        # pprint.pprint(response.text)
        print(response.text)
        print(response.text[1][1][0])


if __name__ == "__main__":
    main()
