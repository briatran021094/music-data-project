# soundcloud_top_tracks.py
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import yaml

# Load .env
load_dotenv()
CLIENT_ID = os.getenv("SOUNDCLOUD_CLIENT_ID")

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

regions = config["regions"]
genres = config["genres"]

# Base URL
base_url = "https://api.soundcloud.com/"

def get_soundcloud_tracks(query, region, max_results=50):
    search_url = f"{base_url}tracks?client_id={CLIENT_ID}&q={query}&limit={max_results}"
    response = requests.get(search_url)
    tracks_data = response.json()

    track_details = []

    for track in tracks_data:
        title = track['title']
        artist = track['user']['username']
        genre = track.get('genre', 'Unknown')
        play_count = track.get('playback_count', 0)
        url = track['permalink_url']

        track_details.append({
            'Platform': 'SoundCloud',
            'Region': region,
            'Song Name': title,
            'Artist': artist,
            'Genre': genre,
            'Streams': play_count,
            'URL': url
        })

    return pd.DataFrame(track_details)

# Run for all regions & genres
all_dfs = []

for region in regions:
    for genre_query in genres:
        print(f"Fetching SoundCloud: Region={region}, Genre={genre_query}")
        df = get_soundcloud_tracks(genre_query, region, max_results=50)
        all_dfs.append(df)

# Combine
final_df = pd.concat(all_dfs, ignore_index=True)
final_df.to_csv("soundcloud_top_tracks.csv", index=False)
print("soundcloud_top_tracks.csv saved")