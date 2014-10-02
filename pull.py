import gdata.youtube
import gdata.youtube.service
from time import sleep

yt_service = gdata.youtube.service.YouTubeService()
yt_service.ssl = True

baseURL = "http://gdata.youtube.com/feeds/api/playlists/"

list_ids = ['RDrVqAdIMQZlk']

videos = []

#iterates through all playlist ids
for pid in list_ids:
    #fetches the playlist
    videoFeed = yt_service.GetYouTubePlaylistVideoFeed(playlist_id = pid)
    #iterates through each video
    for video in videoFeed.entry:
        if video.link:
            #gets http link and removes gdata tag
            videos.append(video.link[0].href.replace("&feature=youtube_gdata", ""))

#order not preserved but ensures if a video will only be downloaded one time

videos = list(set(videos))

sleep(10)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib

mp3url = "http://www.youtube-mp3.org/"
#Uses firefox browser -- must be installed!
browser = webdriver.Firefox()
links = []

print "Videos attempted: {}".format(len(videos))
count = 0
for video in videos:
    try:
        browser.get(mp3url)
        iput = browser.find_element_by_id('youtube-url')
        iput.clear()
        iput.send_keys(video + Keys.RETURN)
        sleep(5)
        anchors = browser.find_elements_by_xpath('//*[@id="dl_link"]/a')
        for anchor in anchors:
            link = anchor.get_attribute("href")
            if link.split('/')[-1][:7] == "get?ab=":
                links.append(link)
    except:
        print video
        count += 1
browser.close()

print "Failure rate: {}".format( float(count) / len(videos))

for i,link in enumerate(links):
    file_name = "{}.mp3".format(i)
    urllib.urlretrieve(link,file_name)

