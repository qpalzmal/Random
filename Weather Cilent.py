'''
This program scraps the web for data and uses it to graph the data for analysis by the user
Section cut off with line of commented "-" is code from someone else modified to work here
'''


import urllib.request
import pprint
import json
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
    elif units.lower() == "kelvin" or units.lower() == "k":
        print("Temperature units has been set to Kelvin (K)")
        units = "default"
    else:
        print("Temperature units has been set to Fahrenheit (°F)")
        units = "imperial"

    search = input("\n"'What do you want to use to search for weather ("zip", "city"): ')
    url = get_html(search, units, API_KEY)

    data = get_data(url)
    # pprint.pprint(data)

    # method used to reach the temperature and time
    # pprint.pprint(data["list"][0]["main"]["temp"])
    # pprint.pprint(data["list"][0]["dt_txt"]

    # receives the temperature and date+time from the data
    temperature_list = []
    datetime_list = []
    for index in range(len(data["list"])):
        # gets the temperature
        temperature = data["list"][index]["main"]["temp"]
        temperature_list.append(temperature)
        # gets the time
        date_time = data["list"][index]["dt_txt"]
        datetime_list.append(date_time)
        index += 1

    # pprint.pprint(temperature_list)
    # pprint.pprint(datetime_list)

    # (----NOT USED----)  DELETE LATER
    # gets the only the "time" from the return "date + time" value
    # time_list = []
    # for i in datetime_list:
    #     time_list.append(i[11:])
    # pprint.pprint(time_list)

    # ------------------------------------------------------------------------------------------------------------------
    local_time_list = []
    # METHOD 2: Auto-detect zones:
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
    # ------------------------------------------------------------------------------------------------------------------

    # (----NOT USED----)  DELETE LATER
    # shows temperature that is equal to the time
    # temperature_time_list = []
    # for i in range(40):
    #     temp = temperature_list[i]
    #     time = time_list[i]
    #     temperature_time_list.append(str(temp) + " = " + time)
    # pprint.pprint(temperature_time_list)

    # plt.scatter(local_time_list, temperature_list)
    plt.plot(local_time_list, temperature_list)
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
