import os
import argparse
import lyricsgenius
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress
from rich import box
from rich.table import Table
import asyncio

def initialize_genius(verbose):
    load_dotenv()
    return lyricsgenius.Genius(os.getenv("GENIUS_API_KEY"), verbose=verbose)

async def fetch_top_songs(genius, artist_name, max_songs=10):
    try:
        artist = genius.search_artist(artist_name, max_songs=max_songs)
        return [song.title for song in artist.songs]
    except Exception as e:
        print(f"Error fetching top songs: {e}")
        return []

async def count_babies(genius, song_title, artist_name):
    try:
        song = genius.search_song(song_title, artist_name)
        if song:
            lyrics = song.lyrics.lower()
            return song_title, lyrics.count("baby")
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

    console = Console()
    genius = initialize_genius(args.verbose)
    console.print(f"[bold green]Fetching top {args.max_songs} songs for {args.artist}...[/bold green]")
    songs = await fetch_top_songs(genius, args.artist, max_songs=args.max_songs)
    console.print(f"[bold green]Fetched {len(songs)} songs.[/bold green]")

    async def count_all_babies():
        baby_counts = {}
        with Progress() as progress:
            task = progress.add_task("[cyan]Counting occurrences...", total=len(songs))
            tasks = [count_babies(genius, song, args.artist) for song in songs]
            for coro in asyncio.as_completed(tasks):
                song, count = await coro
                baby_counts[song] = count
                progress.advance(task)
        return baby_counts

    baby_counts = await count_all_babies()
    baby_counts_sorted = sorted(baby_counts.items(), key=lambda item: item[1], reverse=True)

    table = Table(title="Occurrences of 'baby' in Songs", box=box.ROUNDED)
    table.add_column("Song", style="cyan", no_wrap=True)
    table.add_column("Count", style="magenta")

    for song, count in baby_counts_sorted:
        table.add_row(song, str(count))

    console.print(table)

if __name__ == "__main__":
    asyncio.run(main())
