# spotify_top_tracks.py
import requests
import pandas as pd
import time
import base64
import yaml
from sklearn.cluster import KMeans
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET in .env")

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

regions = config["regions"]

def get_access_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}

    response = requests.post(auth_url, headers=headers, data=data)
    response.raise_for_status()

    return response.json()['access_token']

def get_playlist_tracks(token, playlist_id, market='US'):
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    params = {'market': market, 'limit': 100}

    items = []

    while url:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        items.extend(data.get('items', []))
        url = data.get('next')
        params = None

    return items

def get_artist_genres(token, artist_id):
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('genres', [])
    return []

def get_audio_features(token, track_id):
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api.spotify.com/v1/audio-features/{track_id}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {}

# Example Top 50 playlists
top_playlists = {
    'US': '37i9dQZEVXbLRQDuF5jeBp',
    'JP': '37i9dQZEVXbKqiTGXuCOsB',
    'MX': '37i9dQZEVXbO3qyFxbkOE1L',
    'UK': '37i9dQZEVXbLnolsZ8PSrjR',
    'DE': '37i9dQZEVXbJiZcmkrIHGU'
}

# Run
token = get_access_token()
all_tracks = []

for region in regions:
    playlist_id = top_playlists.get(region, None)
    if not playlist_id:
        print(f"Skipping region {region} — no playlist ID defined")
        continue

    print(f"Fetching Spotify: Region={region}")
    items = get_playlist_tracks(token, playlist_id, market=region)

    for item in items:
        track = item.get('track')
        if not track:
            continue

        title = track.get('name')
        artists = [a['name'] for a in track.get('artists', [])]
        artist_id = track['artists'][0]['id'] if track['artists'] else None
        genres = get_artist_genres(token, artist_id) if artist_id else []
        url = track.get('external_urls', {}).get('spotify', '')

        audio = get_audio_features(token, track['id']) if track.get('id') else {}

        all_tracks.append({
            'Platform': 'Spotify',
            'Region': region,
            'Song Name': title,
            'Artist': ', '.join(artists),
            'Genre': ', '.join(genres) if genres else 'Unknown',
            'Streams': 'N/A',
            'URL': url,
            'Danceability': audio.get('danceability'),
            'Energy': audio.get('energy'),
            'Valence': audio.get('valence'),
            'Tempo': audio.get('tempo'),
            'Acousticness': audio.get('acousticness'),
            'Instrumentalness': audio.get('instrumentalness')
        })

        time.sleep(0.2)

df = pd.DataFrame(all_tracks)

# CLUSTERING — KMeans
audio_features = df[[
    "Danceability", "Energy", "Valence", "Tempo", "Acousticness", "Instrumentalness"
]].dropna()

if len(audio_features) >= 4:
    kmeans = KMeans(n_clusters=4, random_state=42)
    df.loc[audio_features.index, "Cluster"] = kmeans.fit_predict(audio_features)
else:
    df["Cluster"] = "N/A"

# Save
df.to_csv("spotify_top_tracks.csv", index=False)
print("spotify_top_tracks.csv saved")