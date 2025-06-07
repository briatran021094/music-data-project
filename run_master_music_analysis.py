# run_master_music_analysis.py
import subprocess
import pandas as pd
import sqlite3
import datetime
import yaml
from textblob import TextBlob

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

regions = config["regions"]
genres = config["genres"]

# Run platform scripts
print("Running SoundCloud script...")
subprocess.run(["python", "soundcloud_top_tracks.py"], check=True)

print("Running Spotify script...")
subprocess.run(["python", "spotify_top_tracks.py"], check=True)

print("Running YouTube script...")
subprocess.run(["python", "youtube_top_tracks.py"], check=True)

# Load CSVs
soundcloud_df = pd.read_csv("soundcloud_top_tracks.csv")
soundcloud_df["Section"] = "SoundCloud Section"

spotify_df = pd.read_csv("spotify_top_tracks.csv")
spotify_df["Section"] = "Spotify Section"

youtube_df = pd.read_csv("youtube_top_tracks.csv")
youtube_df["Section"] = "YouTube Section"

# Add Date Pulled
date_pulled = datetime.date.today().isoformat()
for df in [soundcloud_df, spotify_df, youtube_df]:
    df["Date Pulled"] = date_pulled

# Add Popularity Score
for df in [soundcloud_df, youtube_df]:
    df["Popularity Score"] = pd.to_numeric(df["Streams"], errors="coerce").fillna(0)

spotify_df["Popularity Score"] = "N/A"

# Add Sentiment Score
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

for df in [soundcloud_df, spotify_df, youtube_df]:
    df["Sentiment Score"] = df["Song Name"].apply(get_sentiment)

# Combine
combined_df = pd.concat([soundcloud_df, spotify_df, youtube_df], ignore_index=True)

# Reorder
combined_df = combined_df[[
    "Section", "Platform", "Region", "Song Name", "Artist", "Genre",
    "Streams", "Popularity Score", "Sentiment Score", "URL", "Date Pulled"
]]

# Save to CSV
combined_df.to_csv("combined_music_data.csv", index=False)
print("combined_music_data.csv saved")

# Save to SQLite
conn = sqlite3.connect("music_data.db")
combined_df.to_sql("combined_music_data", conn, if_exists="replace", index=False)
conn.close()
print("music_data.db saved")

# Save BI-ready versions
combined_df.to_csv("tableau_ready_music_data.csv", index=False)
combined_df.to_csv("powerbi_ready_music_data.csv", index=False)

print("Tableau and Power BI CSVs saved")

print("All done! Ready for analysis")