# dashboard_app.py
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("combined_music_data.csv")

st.title("Multi-Platform Music Trends Dashboard")

# Region selector
region = st.selectbox("Select Region", df["Region"].unique())

# Filter data
df_region = df[df["Region"] == region]

# Top Genres
st.subheader(f"Top Genres in {region}")
genre_count = df_region["Genre"].value_counts().head(10)
st.bar_chart(genre_count)

# Top Artists
st.subheader(f"Top Artists in {region}")
artist_count = df_region["Artist"].value_counts().head(10)
st.bar_chart(artist_count)

# Sentiment distribution
st.subheader(f"Sentiment Distribution in {region}")
sns.histplot(df_region["Sentiment Score"], kde=True)
st.pyplot(plt.gcf())

# Spotify Audio Features (if Spotify)
if st.checkbox("Show Spotify Audio Feature Clusters"):
    spotify_df = df_region[df_region["Platform"] == "Spotify"]
    required_cols = ["Danceability", "Energy", "Valence", "Tempo", "Cluster"]

    if all(col in spotify_df.columns for col in required_cols) and not spotify_df.empty:
        sns.pairplot(spotify_df, vars=[
            "Danceability", "Energy", "Valence", "Tempo"
        ], hue="Cluster")
        st.pyplot(plt.gcf())
    else:
        st.write("No Spotify audio feature data available for this region.")