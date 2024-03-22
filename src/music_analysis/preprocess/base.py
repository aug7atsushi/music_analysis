import spotipy


class SpotifyClientBase:
    def __init__(self, sp: spotipy.client.Spotify) -> None:
        self.sp = sp
