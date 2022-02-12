import datetime
import hashlib
import time
import urllib.request
from threading import Thread
from bs4 import BeautifulSoup
import requests
import webbrowser

domains = ['https://vod-secure.twitch.tv',
           'https://vod-metro.twitch.tv',
           'https://vod-pop-secure.twitch.tv',
           'https://d2e2de1etea730.cloudfront.net',
           'https://dqrpb9wgowsf5.cloudfront.net',
           'https://ds0h3roq6wcgc.cloudfront.net',
           'https://d2nvs31859zcd8.cloudfront.net',
           'https://d2aba1wr3818hz.cloudfront.net',
           'https://d3c27h4odz752x.cloudfront.net',
           'https://dgeft87wbj63p.cloudfront.net',
           'https://d1m7jfoe9zdc1j.cloudfront.net']

find1c = 0


def linkChecker(link):  # twitchtracker ve streamscharts destekli
    global streamername
    global vodID
    link = link.split('/')
    if link[2] == 'twitchtracker.com':
        streamername = link[3]
        vodID = link[5]
        return 1
    elif link[2] == 'streamscharts.com':
        streamername = link[4]
        vodID = link[6]
        return 2
    elif link[0] == 'twitchtracker.com':
        streamername = link[1]
        vodID = link[3]
        return 3
    elif link[0] == 'streamscharts.com':
        streamername = link[2]
        vodID = link[4]
        return 4
    else:
        print('Check the link again. (An unsupported link has been entered or the link has an error.)')
        return 0


def linkTimeCheck(link):
    # global timestamp
    if linkChecker(link) == 2 or linkChecker(link) == 4:  # sadece 2 ve 4 dönerse girsin
        print('Date and Time are checking..')
        r = requests.get(link)

        soup = BeautifulSoup(r.content, 'html.parser')

        gelenveri = soup.find_all('time', 'ml-2 font-bold')

        time = gelenveri[0].text

        if '\n' in time:
            time = time.replace('\n', '')

        if ',' in time:
            time = time.replace(',', '')

        print(f'Clock data: {time}')
        print(f'Streamer name: {streamername} \nvodID: {vodID}')

        time = time.split(' ')

        hoursandminut = time[3]

        hoursandminut = hoursandminut.split(':')

        day = int(time[0])

        month = time[1]

        year = int(time[2])

        hour = int(hoursandminut[0])

        minute = int(hoursandminut[1])

        def months(month):
            if month == 'Jan':
                return 1
            if month == 'Feb':
                return 2
            if month == 'Mar':
                return 3
            if month == 'Apr':
                return 4
            if month == 'May':
                return 5
            if month == 'Jun':
                return 6
            if month == 'Jul':
                return 7
            if month == 'Aug':
                return 8
            if month == 'Sep':
                return 9
            if month == 'Oct':
                return 10
            if month == 'Nov':
                return 11
            if month == 'Dec':
                return 12
            else:
                return 0

        month = months(month)

        second = 60

        timestamp = str(year) + '-' + str(month) + '-' + str(day) + '-' + str(hour) + '-' + str(minute) + '-' + str(
            second)

        print(f'timestamp', timestamp)
        return timestamp

    elif linkChecker(link) == 1 or linkChecker(link) == 3:
        print('Date and Time are checking...')

        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
        }

        r = requests.get(link, headers=header)

        soup = BeautifulSoup(r.content, 'html.parser')

        gelenveri = soup.find_all('div', 'stream-timestamp-dt')

        print(f'Clock data:  {gelenveri[0].text}')
        print(f'Streamer name: {streamername} \nvodID: {vodID}')

        firstandsecond_time = gelenveri[0].text.split(' ')

        first_time = firstandsecond_time[0].split('-')
        second_time = firstandsecond_time[1].split(':')

        day = int(first_time[2])

        month = int(first_time[1])

        year = int(first_time[0])

        hour = int(second_time[0])

        minute = int(second_time[1])

        second = int(second_time[2])

        timestamp = str(year) + '-' + str(month) + '-' + str(day) + '-' + str(hour) + '-' + str(minute) + '-' + str(
            second)

        print(f'timestamp', timestamp)

        return timestamp

    elif linkChecker(link) == 0:
        print('You entered an unsupported link.')
        return 0
    else:
        print('An unknown error has occurred.')
        return None


def totimestamp(dt, epoch=datetime.datetime(1970, 1, 1)):
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6) / 10 ** 6


def find(timestamp, domain):
    timestamp = timestamp.split('-')
    year = int(timestamp[0])
    month = int(timestamp[1])
    day = int(timestamp[2])
    hour = int(timestamp[3])
    minute = int(timestamp[4])
    second = int(timestamp[5])

    def check(url):
        global find1c
        try:
            urllib.request.urlopen(url)
        except urllib.error.HTTPError:
            pass
        else:
            print(url)
            #webbrowser.open(url)
            find1c = 1

    threads = []

    if second == 60:
        for i in range(60):
            seconds = i

            td = datetime.datetime(year, month, day, hour, minute, seconds)

            converted_timestamp = totimestamp(td)

            formattedstring = streamername + "_" + vodID + "_" + str(int(converted_timestamp))

            hash = str(hashlib.sha1(formattedstring.encode('utf-8')).hexdigest())

            requiredhash = hash[:20]

            finalformattedstring = requiredhash + '_' + formattedstring

            url = f"{domain}/{finalformattedstring}/chunked/index-dvr.m3u8"

            threads.append(Thread(target=check, args=(url,)))

        for i in threads:
            i.start()
        for i in threads:
            i.join()
    else:
        td = datetime.datetime(year, month, day, hour, minute, second)

        converted_timestamp = totimestamp(td)

        formattedstring = streamername + "_" + vodID + "_" + str(int(converted_timestamp))

        hash = str(hashlib.sha1(formattedstring.encode('utf-8')).hexdigest())

        requiredhash = hash[:20]

        finalformattedstring = requiredhash + '_' + formattedstring

        url = f"{domain}/{finalformattedstring}/chunked/index-dvr.m3u8"

        threads.append(Thread(target=check, args=(url,)))

        for i in threads:
            i.start()
        for i in threads:
            i.join()


print('Find the broadcast link you want from Twitchtracker or Streamscharts site.')
link = str(input('Enter the link:'))

timestamp = linkTimeCheck(link)

for domain in domains:
    if find1c == 0:
        find(timestamp, domain)
    else:
        pass

if find1c == 0:
    print('No File Found on Twitch Servers.')

if find1c == 1:
    time.sleep(10)


