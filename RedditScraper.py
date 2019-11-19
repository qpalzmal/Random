import urllib.request
import json
import time
# import pprint  # used to print json data formatted

print("\nThis program shows the title of the newest thread on a subreddit every 10 seconds\n")
subreddit = input("Enter the name of any valid subreddit (e.g. todayilearned, showerthoughts, jokes, etc): ")
see_text = input("Type (Y) if you want to see the thread text in the post otherwise type anything else: ")
if see_text == "Y" or see_text == "y":
    see_text_bool = True
else:
    see_text_bool = False  # boolean used to decide whether to show the thread text


def get_data():
    url = "https://www.reddit.com/r/{}/new/.json".format(subreddit)
    json_req = urllib.request.Request(url, data=None, headers={"User-Agent": "Windows:Working with Reddit API:v1"})
    json_obj = urllib.request.urlopen(json_req)
    data = json.load(json_obj)
    return data


data = get_data()
# pprint.pprint(data)  # prints the api data formatted

title_text = (data["data"]["children"][0]["data"]["title"])  # goes through dictionary/lists and returns the title
thread_text = (data["data"]["children"][0]["data"]["selftext"])  # returns the text in each thread
print("\n" + title_text)
if see_text_bool:
    print(thread_text)
time.sleep(10)

while True:  # loops every 10s to check/print any new posts
    data = get_data()
    new_title_text = (data["data"]["children"][0]["data"]["title"])
    new_thread_text = (data["data"]["children"][0]["data"]["selftext"])
    if new_title_text != title_text:
        print(new_title_text)
        if see_text_bool:
            print("\n" + new_thread_text)
        title_text = new_title_text
        thread_text = new_thread_text
    else:
        print("\n---No new post found, checking again in 10 seconds---")
    time.sleep(10)
