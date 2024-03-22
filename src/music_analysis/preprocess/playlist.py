from typing import Dict, List

import spotipy

from music_analysis.preprocess.base import SpotifyClientBase


class PlaylistCreator(SpotifyClientBase):
    def __init__(self, sp: spotipy.client.Spotify) -> None:
        super().__init__(sp=sp)

    def create_empty_playlist(
        self,
        user_id: str,
        name: str,
        public: bool = False,
        collaborative: bool = False,
        description: str = None,
    ) -> Dict:
        new_playlist = self.sp.user_playlist_create(
            user=user_id,
            name=name,
            public=public,
            collaborative=collaborative,
            description=description,
        )
        return new_playlist

    def add_tracks(self, playlist_id: str, track_ids=List[str]) -> None:
        self.sp.playlist_add_items(playlist_id=playlist_id, items=track_ids)
