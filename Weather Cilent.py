# import urllib
# import pprint
# import json
# import time


def main():

    search_type = input("What do you want to use to search for weather('zip' or 'city'): ")
    print(search_type)
    search_type = search_type.lower
    get_html(search_type)


def get_html(search_type):
    if search_type == "city":
        city = input("Enter the city you want weather for: ")
        url = "api.openweathermap.org/data/2.5/forecast/daily?q={}".format(city)
        print(url)
    elif search_type == "zip":
        zip_code = input("Enter zip code you want weather for: ")
        url = "api.openweathermap.org/data/2.5/forecast/daily?zip={}".format(zip_code)
        print(url)


if __name__ == "__main__":
    main()
