import os
import argparse
import lyricsgenius
from dotenv import load_dotenv

def initialize_genius(verbose):
    load_dotenv()
    return lyricsgenius.Genius(os.getenv("GENIUS_API_KEY"), verbose=verbose)

def fetch_top_songs(genius, artist_name, max_songs=10):
    try:
        artist = genius.search_artist(artist_name, max_songs=max_songs)
        return [song.title for song in artist.songs]
    except Exception as e:
        print(f"Error fetching top songs: {e}")
        return []

def count_babies(genius, song_title, artist_name):
    try:
        song = genius.search_song(song_title, artist_name)
        if song:
            lyrics = song.lyrics.lower()
            return lyrics.count("baby")
    except Exception as e:
        print(f"Error fetching song lyrics: {e}")
    return 0

def main():
    parser = argparse.ArgumentParser(
        description="Count occurrences of a word in an artist's songs."
    )
    parser.add_argument(
        "--artist",
        type=str,
        default="Janet Jackson",
        help="Artist name (default: Janet Jackson)",
    )
    parser.add_argument(
        "--max_songs",
        type=int,
        default=10,
        help="Number of top songs to fetch (default: 10)",
    )
    parser.add_argument(
        "--search_term",
        type=str,
        default="baby",
        help="Word to search for in lyrics (default: baby)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    args = parser.parse_args()

    genius = initialize_genius(args.verbose)
    songs = fetch_top_songs(genius, args.artist, max_songs=args.max_songs)

    baby_counts = {song: count_babies(genius, song, args.artist) for song in songs}
    baby_counts_sorted = sorted(baby_counts.items(), key=lambda item: item[1], reverse=True)

    for song, count in baby_counts_sorted:
        print(f"{song}: {count} times")

if __name__ == "__main__":
    main()
