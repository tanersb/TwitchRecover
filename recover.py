from datetime import timedelta
import datetime
import time
import hashlib
from concurrent.futures import ThreadPoolExecutor
import requests

domains = ["https://vod-secure.twitch.tv/",
           "https://vod-metro.twitch.tv/",
           "https://vod-pop-secure.twitch.tv/",
           "https://d2e2de1etea730.cloudfront.net/",
           "https://dqrpb9wgowsf5.cloudfront.net/",
           "https://ds0h3roq6wcgc.cloudfront.net/",
           "https://d2nvs31859zcd8.cloudfront.net/",
           "https://d2aba1wr3818hz.cloudfront.net/",
           "https://d3c27h4odz752x.cloudfront.net/",
           "https://dgeft87wbj63p.cloudfront.net/",
           "https://d1m7jfoe9zdc1j.cloudfront.net/",
           "https://d3vd9lfkzbru3h.cloudfront.net/",
           "https://d2vjef5jvl6bfs.cloudfront.net/",
           "https://d1ymi26ma8va5x.cloudfront.net/"]

possible_urls = []
valid_m3u8_list = []

tracker_url = input("Enter the tracker stream url (https://twitchtracker.com/streamer_id/streams/xxxx...): ")

# parsing the tracker url to get the streamer id
streamer_name = tracker_url.split("/")[-3].strip()
vodID = tracker_url.split("/")[-1].strip()


def get_url(url, options=False):
    if options:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        return requests.get(url, headers=headers, timeout=1000)
    else:
        return requests.get(url, timeout=100)


# getting the time from the tracker url
html = get_url(tracker_url, True).text
timestamp = html.split("<div class=\"stream-timestamp-dt to-dowdatetime\">")[1].split("</div>")[0].strip()

# get utc timedelta
utc_timedelta = datetime.datetime.now() - datetime.datetime.utcnow()

formatted_date = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") + utc_timedelta

days_between = datetime.datetime.now() - formatted_date

if days_between > timedelta(days=60):
    print("Vod is " + str(days_between.days) + " days old. Vods typically cannot be recovered when older then 60 days.")
    user_continue = input("Do you want to continue (Y/N): ")
    if user_continue.upper() == "Y":
        pass
    else:
        exit()

print("Wait a minute, please...")
for bf_second in range(60):
    vod_date = datetime.datetime(formatted_date.year, formatted_date.month, formatted_date.day,
                                 formatted_date.hour, formatted_date.minute, bf_second)
    converted_timestamp = round(time.mktime(vod_date.timetuple()) * 1000)
    base_url = streamer_name + "_" + vodID + "_" + str(int(converted_timestamp)).strip("0")
    hashed_base_url = str(hashlib.sha1(base_url.encode('utf-8')).hexdigest())[:20]
    formatted_base_url = hashed_base_url + '_' + base_url
    for domain in domains:
        url = domain + formatted_base_url + "/chunked/index-dvr.m3u8"
        possible_urls.append(url)

with ThreadPoolExecutor(max_workers=100) as pool:
    max_url_list_length = 100
    current_list = possible_urls

    for i in range(0, len(possible_urls), max_url_list_length):
        batch = current_list[i:i + max_url_list_length]
        response_list = list(pool.map(get_url, batch))
        for m3u8_link in response_list:
            if m3u8_link.status_code == 200:
                valid_m3u8_list.append(m3u8_link.url)

if not valid_m3u8_list:
    print("No vods found using current domains.")

for m3u8 in valid_m3u8_list:
    print(m3u8)


input("Press any key to exit...")