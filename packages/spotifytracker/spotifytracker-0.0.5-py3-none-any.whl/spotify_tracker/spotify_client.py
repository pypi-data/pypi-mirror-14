import time

import spotipy
import spotipy.util as util

from . import current_track
from . import config


class SpotifyClient:
    def __init__(self):
        self.username = config.get_config_value('username')
        self.client_id = config.get_config_value('client_id')
        self.client_secret = config.get_config_value('client_secret')
        self.callback_url = config.get_config_value('callback_url')
        self.token = config.get_config_value('token')
        self.playlist_id = config.get_config_value('playlist_id')
        self.last_track_id = None

    @property
    def sp(self):
        if not hasattr(self, '_sp'):
            self._sp = spotipy.Spotify(auth=config.get_config_value('token'))
            self._sp.trace = False
        return self._sp

    @property
    def playlist_track_ids(self):
        if not hasattr(self, '_playlist_track_ids'):
            pl = self.sp.user_playlist(self.username, self.playlist_id)
            self._playlist_track_ids = {
                track['track']['id'] for track in pl['tracks']['items']
            }
        return self._playlist_track_ids

    def check_track_in_playlist(self, track_id):
        return track_id in self.playlist_track_ids

    def add_track_to_playlist(self, track_id):
        if not self.check_track_in_playlist(track_id):
            self.sp.user_playlist_add_tracks(
                self.username, self.playlist_id, [track_id]
            )
            self.playlist_track_ids.add(track_id)
            return True
        return False

    def save_token(self):
        token = util.prompt_for_user_token(
            self.username, config.SCOPE, self.client_id,
            self.client_secret, self.callback_url)
        config.save_config_value('token', token)
        self.token = token

    def watch(self):
        if not self.check_config():
            raise Exception("Please run setup")
        while True:
            self.main()

    def get_current_track_id(self):
        try:
            track_id = current_track.get_current_track_id()
        except Exception as exc:
            print("AppleScript Exception")
            print(exc)
            return
        if not track_id or track_id == self.last_track_id:
            return
        self.last_track_id = track_id
        print('Currently listening to {}'.format(track_id))
        return track_id

    def main(self):
        track_id = self.get_current_track_id()
        if not track_id:
            return
        try:
            success = self.add_track_to_playlist(track_id)
            if success:
                print('Added {}'.format(track_id))
            time.sleep(30)
        except spotipy.client.SpotifyException as exc:
            if exc.code == -1:
                self.save_token()
            else:
                print(exc.__dict__)
                raise exc

    def setup_username(self):
        username = input("Please provide your Spotify username: ")
        config.save_config_value('username', username)

    def setup_client_id(self):
        print("You'll need to setup a Spotify Application at "
              "https://developer.spotify.com/my-applications/#!/applications/create")
        client_id = input("Please provide your Spotify application Client ID: ")
        config.save_config_value('client_id', client_id)

    def setup_client_secret(self):
        print("You should have a Spotify Application. "
              "See https://developer.spotify.com/my-applications/#!/applications")
        client_secret = input("Please provide your Spotify application Client Secret: ")
        config.save_config_value('client_secret', client_secret)

    def setup_callback_url(self):
        print("You should have a Spotify Application. "
              "See https://developer.spotify.com/my-applications/#!/applications")
        print("You need to specify a Callback URL. "
              "It can be anything, but must match what you've saved on Spotify.")
        callback_url = input("Please provide your Spotify application Callback URL: ")
        config.save_config_value('callback_url', callback_url)

    def setup_token(self):
        print("You need to authorize your application.")
        self.save_token()
        print('Your token is saved.')

    def setup_playlist_id(self):
        print("You need to add a playlist_id to your config")
        sp_playlists = self.sp.user_playlists(self.username)
        playlists = [p for p in sp_playlists['items']
                     if p['owner']['id'] == self.username]
        for playlist in playlists:
            print('{}: {}'.format(playlist['name'], playlist['id']))
        playlist_id = input("Please input the playlist_id of the Playlist "
                            "you'd like to save your history to.")
        config.save_config_value('playlist_id', playlist_id)

    def setup(self):
        if not self.username:
            self.setup_username()
        if not self.client_id:
            self.setup_client_id()
        if not self.client_secret:
            self.setup_client_secret()
        if not self.callback_url:
            self.setup_callback_url()
        if not self.token:
            self.setup_token()
        if not self.playlist_id:
            self.setup_playlist_id()

    def check_config(self):
        return (self.username and self.client_id and self.client_secret and
                self.callback_url and self.token and self.playlist_id)
