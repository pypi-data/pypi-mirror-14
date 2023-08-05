""" Spotify Tracker - Save every song you play from OS X to a playlist

Usage:
  spotifytracker setup
  spotifytracker watch

"""
from docopt import docopt

from .spotify_client import SpotifyClient


def main():
    arguments = docopt(__doc__)
    spotify_client = SpotifyClient()

    if arguments['setup']:
        spotify_client.setup()
    if arguments['watch']:
        spotify_client.watch()

if __name__ == "__main__":
    main()
