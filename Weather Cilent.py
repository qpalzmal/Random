# import urllib
# import pprint
# import json
# import time


def main():

    code = input("What zip code do you want to search for: ")
    print(code)
    get_html(code)


def get_html(zip_code):
    url = "api.openweathermap.org/data/2.5/weather?zip={}".format(zip_code)


if __name__ == "__main__":
    main()
