# babycounter

babycounter is a command-line tool that fetches the top songs of an artist from the Genius API and counts the occurrences of a specified word in the lyrics.

## Usage

```sh
python -m babycounter.main [--artist ARTIST_NAME] [--max_songs MAX_SONGS] [--search_term SEARCH_TERM] [--verbose]
```

### Options

- `--artist`: Artist name (default: Janet Jackson)
- `--max_songs`: Number of top songs to fetch (default: 10)
- `--search_term`: Word to search for in lyrics (default: baby)
- `--verbose`: Enable verbose output

### Example

```sh
python -m babycounter.main --artist "So Inagawa" --max_songs 20 --search_term "deep" --verbose
```
