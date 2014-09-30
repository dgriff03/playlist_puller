import gdata.youtube
import gdata.youtube.service

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

print videos        
