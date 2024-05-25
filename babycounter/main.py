import lyricsgenius

# Replace 'YOUR_GENIUS_API_KEY' with your actual Genius API key
genius = lyricsgenius.Genius("YOUR_GENIUS_API_KEY")

# List of Janet Jackson's top songs
songs = [
    "All For You", "Together Again", "That's the Way Love Goes", 
    "Nasty", "Rhythm Nation", "Escapade", "If", "Again", 
    "Love Will Never Do (Without You)", "Feedback"
]

# Function to count occurrences of "baby"
def count_babies(song_title):
    song = genius.search_song(song_title, "Janet Jackson")
    if song:
        lyrics = song.lyrics.lower()
        return lyrics.count("baby")
    return 0

# Count "baby" in each song
baby_counts = {song: count_babies(song) for song in songs}
baby_counts_sorted = sorted(baby_counts.items(), key=lambda item: item[1], reverse=True)

for song, count in baby_counts_sorted:
    print(f"{song}: {count} times")
