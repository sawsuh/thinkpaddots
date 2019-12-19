from bs4 import BeautifulSoup
import threading
import requests
import dateparser

pitchfork = requests.get("https://pitchfork.com/best/")
pitchfork.raise_for_status()
p4ksoup = BeautifulSoup(pitchfork.text, "lxml")
print("pitchfork downloaded")
needledrop = requests.get("https://www.theneedledrop.com/loved-list/")
needledrop.raise_for_status()
ndsoup = BeautifulSoup(needledrop.text, "lxml")
print("needledrop downloaded")
outputdict = {}
timelist = []


def bigp4k():
    bigauth = p4ksoup.select(".bnm-hero__artist .artist-list li")[0].getText()
    bigalbum = p4ksoup.select(".bnm-hero__title")[0].getText()
    imglink = "https://pitchfork.com" + p4ksoup.select(".bnm-hero__link-block")[0].get(
        "href"
    )
    try:
        reviewpage = requests.get(imglink)
    except requests.exceptions.RequestException:
        print('download failed')
        return False
    reviewpage.raise_for_status()
    reviewsoup = BeautifulSoup(reviewpage.text, "lxml")
    bigtime = reviewsoup.select(".article-meta .pub-date")[0].getText()
    date = dateparser.parse(bigtime)
    #    print(f"{bigauth} - {bigalbum} ({bigtime})")
    entry = f'{bigauth} - {bigalbum} ({date.strftime("%d %b %Y")})'
    global outputdict
    outputdict[date] = entry
    global timelist
    timelist.append(date)


def downloadp4ksoup(index):
    author = p4ksoup.select(".bnm-small .artist-list li")[index].getText()
    album = p4ksoup.select(".bnm-small .title")[index].getText()
    imglink = "https://pitchfork.com" + p4ksoup.select(".bnm-small .link-block")[
        index
    ].get("href")
    try:
        reviewpage = requests.get(imglink)
    except requests.exceptions.RequestException:
        print('download failed')
        return False
    reviewpage.raise_for_status()
    reviewsoup = BeautifulSoup(reviewpage.text, "lxml")
    time = reviewsoup.select(".article-meta .pub-date")[0].getText()
    date = dateparser.parse(time)
    entry = f"{author} - {album} ({date.strftime('%d %b %Y')})"
    global outputdict
    outputdict[date] = entry
    global timelist
    timelist.append(date)


def dlnd(index):
    albumline = ndsoup.select(
        ".sqs-block .sqs-block-content a")[index].getText()
    reviewlink = ndsoup.select(
        ".sqs-block .sqs-block-content a")[index].get("href")
    try:
        reviewpage = requests.get(reviewlink)
    except requests.exceptions.RequestException:
        print('download failed')
        return False
    reviewpage.raise_for_status()
    reviewsoup = BeautifulSoup(reviewpage.text, "lxml")
    time = reviewsoup.select(".entry-header-date-link")[0].getText()
    date = dateparser.parse(time)
    entry = f"{albumline} ({date.strftime('%d %b %Y')})"
    global outputdict
    outputdict[date] = entry
    global timelist
    timelist.append(date)


threads = []
bigdthread = threading.Thread(target=bigp4k)
threads.append(bigdthread)
bigdthread.start()
for i in range(0, 6):
    downloadthread = threading.Thread(target=downloadp4ksoup, args=[i])
    threads.append(downloadthread)
    downloadthread.start()
for i in range(0, 7):
    downloadthread = threading.Thread(target=dlnd, args=[i])
    threads.append(downloadthread)
    downloadthread.start()
[item.join() for item in threads]
print('')
for date in sorted(timelist, reverse=1):
    print(outputdict[date])
