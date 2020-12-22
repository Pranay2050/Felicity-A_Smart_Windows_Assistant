from googleapiclient.discovery import build
from os import system
import webbrowser  

#song = "despacito"
def play_on_youtube(song):
    DEVELOPER_KEY = "AIzaSyC_qBIFbJSXSNK-AEQCGw2Ld1XyIZ6xdbY" 
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, 
                                           developerKey = DEVELOPER_KEY)
    search_keyword = youtube.search().list(q=song, part="id,snippet",           maxResults = 1).execute()
    URLS = f"https://www.youtube.com/watch?v={search_keyword['items'][0]['id']['videoId']}"

    webbrowser.open(URLS, new=2, autoraise=False)