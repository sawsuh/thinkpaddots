from bs4 import BeautifulSoup
import requests

pitchfork = requests.get("https://pitchfork.com/best/")
pitchfork.raise_for_status()
p4ksoup = BeautifulSoup(pitchfork.text, "lxml")

bigauth = p4ksoup.select(".bnm-hero__artist .artist-list li")[0].getText()
bigalbum = p4ksoup.select(".bnm-hero__title")[0].getText()
print(f"{bigauth} - {bigalbum}")

for index in range(0, 6):
    author = p4ksoup.select(".bnm-small .artist-list li")[index].getText()
    album = p4ksoup.select(".bnm-small .title")[index].getText()
    print(f"{author} - {album}")
print('')

needledrop = requests.get("https://www.theneedledrop.com/loved-list/")
needledrop.raise_for_status()
ndsoup = BeautifulSoup(needledrop.text, "lxml")

for index in range(0, 7):
    print ( ndsoup.select(".sqs-block .sqs-block-content a")[index].getText() )
