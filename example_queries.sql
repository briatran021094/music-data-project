-- Top genres by region
SELECT Region, Genre, COUNT(*) AS SongCount
FROM combined_music_data
GROUP BY Region, Genre
ORDER BY SongCount DESC;

-- Top 10 artists overall
SELECT Artist, COUNT(*) AS SongCount
FROM combined_music_data
GROUP BY Artist
ORDER BY SongCount DESC
LIMIT 10;

-- Spotify audio features by region
SELECT Region, AVG("Danceability"), AVG("Energy"), AVG("Valence")
FROM combined_music_data
WHERE Platform = 'Spotify'
GROUP BY Region;

-- Most positive songs (valence or sentiment)
SELECT "Song Name", Artist, "Valence", "Sentiment Score"
FROM combined_music_data
WHERE "Valence" IS NOT NULL
ORDER BY "Valence" DESC
LIMIT 20;