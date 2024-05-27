import os
import argparse
import lyricsgenius
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress
from rich import box
from rich.table import Table
import asyncio
import time


def initialize_genius(verbose):
    load_dotenv()
    genius = lyricsgenius.Genius(os.getenv("GENIUS_API_KEY"), verbose=verbose)
    # Set a default encoding if not provided by the API response
    if not genius.response.encoding:
        genius.response.encoding = 'utf-8'
    return genius


async def fetch_top_songs(genius, artist_name, max_songs=10):
    try:
        artist = await asyncio.to_thread(genius.search_artist, artist_name, max_songs=max_songs, get_full_info=False)
        if artist:
            return [song.title for song in artist.songs]
        else:
            return []
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
    return song_title, 0


def parse_args():
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
        "--max-songs",
        type=int,
        default=10,
        help="Number of top songs to fetch (default: 10)",
    )
    parser.add_argument(
        "--search-term",
        type=str,
        default="baby",
        help="Word to search for in lyrics (default: baby)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    return parser.parse_args()

async def main(args):

    console = Console()
    genius = initialize_genius(args.verbose)
    console.print(
        f"[bold green]Fetching top {args.max_songs} songs for {args.artist}...[/bold green]"
    )
    start_time = time.time()
    songs = await fetch_top_songs(genius, args.artist, max_songs=args.max_songs)
    if not songs:
        console.print(f"[bold red]Error: No songs fetched for {args.artist}. Exiting...[/bold red]")
        return 1
    end_time = time.time()
    if args.verbose:
        console.print(f"[bold green]Fetched {len(songs)} songs in {end_time - start_time:.2f} seconds.[/bold green]")
    console.print(f"[bold green]Fetched {len(songs)} songs.[/bold green]")
    start_time = time.time()

    async def count_all_babies():
        baby_counts = {}
        with Progress() as progress:
            task = progress.add_task("[cyan]Counting occurrences...", total=len(songs))
            tasks = [count_babies(genius, song, args.artist) for song in songs]
            for coro in asyncio.as_completed(tasks):
                song, count = await coro
                baby_counts[song] = count
                progress.advance(task)
        end_time = time.time()
        if args.verbose:
            console.print(f"[bold green]Counted occurrences in {end_time - start_time:.2f} seconds.[/bold green]")
        return baby_counts

    baby_counts = await count_all_babies()
    baby_counts_sorted = sorted(
        baby_counts.items(), key=lambda item: item[1], reverse=True
    )

    table = Table(title="Occurrences of 'baby' in Songs", box=box.ROUNDED)
    table.add_column("Song", style="cyan", no_wrap=True)
    table.add_column("Count", style="magenta")

    for song, count in baby_counts_sorted:
        table.add_row(song, str(count))

    console.print(table)


if __name__ == "__main__":
    try:
        args = parse_args()
        exit_code = asyncio.run(main(args))
        if exit_code is not None:
            exit(exit_code)
    except KeyboardInterrupt:
        print("\nProcess interrupted. Exiting gracefully...")
