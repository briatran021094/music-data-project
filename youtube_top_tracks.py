# youtube_top_tracks.py
from googleapiclient.discovery import build
import pandas as pd
import yaml
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
if not API_KEY:
    raise ValueError("Missing YOUTUBE_API_KEY in .env")

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

regions = config["regions"]
genres = config["genres"]

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Build client
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

def get_youtube_music_data(query, region, max_results=50):
    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=max_results,
        type="video",
        videoCategoryId="10"
    ).execute()

    video_details = []

    for item in search_response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        channel = item['snippet']['channelTitle']

        video_stats = youtube.videos().list(
            part="statistics",
            id=video_id
        ).execute()

        views = video_stats['items'][0]['statistics'].get('viewCount', '0')
        url = f"https://www.youtube.com/watch?v={video_id}"

        video_details.append({
            'Platform': 'YouTube',
            'Region': region,
            'Song Name': title,
            'Artist': channel,
            'Genre': 'Unknown',
            'Streams': views,
            'URL': url
        })

    return pd.DataFrame(video_details)

# Run for all regions & genres
all_dfs = []

for region in regions:
    for genre_query in genres:
        print(f"Fetching YouTube: Region={region}, Genre={genre_query}")
        df = get_youtube_music_data(genre_query, region, max_results=50)
        all_dfs.append(df)

# Combine
final_df = pd.concat(all_dfs, ignore_index=True)
final_df.to_csv("youtube_top_tracks.csv", index=False)
print("youtube_top_tracks.csv saved")