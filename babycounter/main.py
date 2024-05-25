import os
import lyricsgenius
from dotenv import load_dotenv

load_dotenv()

# Replace 'YOUR_GENIUS_API_KEY' with your actual Genius API key
genius = lyricsgenius.Genius(
    os.getenv("GENIUS_API_KEY")
)  # , verbose=False, remove_section_headers=True)

# Fetch the top 100 Janet Jackson songs
def fetch_top_songs(artist_name, max_songs=100):
    artist = genius.search_artist(artist_name, max_songs=max_songs)
    return [song.title for song in artist.songs]

songs = fetch_top_songs("Janet Jackson")


# Function to count occurrences of "baby"
def count_babies(song_title):
    song = genius.search_song(song_title, "Janet Jackson")
    if song:
        lyrics = song.lyrics.lower()
        return lyrics.count("baby")
    return 0


if __name__ == "__main__":
    # Count "baby" in each song
    baby_counts = {song: count_babies(song) for song in songs}
    baby_counts_sorted = sorted(baby_counts.items(), key=lambda item: item[1], reverse=True)

    for song, count in baby_counts_sorted:
        print(f"{song}: {count} times")
