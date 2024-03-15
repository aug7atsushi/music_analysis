from typing import Dict, List

import spotipy

from music_analysis.utils.log import get_module_logger

logger = get_module_logger(__name__)


class TrackRetriever:
    def __init__(self, sp: spotipy.client.Spotify) -> None:
        self.sp = sp

    def get_artist_with_name(self, artist_name: str) -> dict:
        """アーティスト名で検索を行い、最上位のアーティストのメタ情報を返す"""
        results = self.sp.search(
            q=f"artist: {artist_name}", type="artist", limit=10, market=None
        )
        items = results["artists"]["items"]
        if len(items) > 0:
            return items[0]
        else:
            return None

    def get_artist_with_id(self, artist_id: str) -> dict:
        """アーティストIDで検索し、アーティストのメタ情報を返す"""
        return self.sp.artist(artist_id)

    def glob_artist_albums(
        self, artist_meta: dict, album_type: str = "album"
    ) -> List[Dict]:
        """アーティストのアルバムを取得"""
        albums = []
        results = self.sp.artist_albums(artist_meta["id"], album_type=album_type)
        albums.extend(results["items"])
        while results["next"]:
            results = self.sp.next(results)
            albums.extend(results["items"])
        logger.info(f"Total albums: {len(albums)}")
        return albums

    def glob_album_tracks(self, album_meta: dict) -> List[Dict]:
        """アルバムのトラックを取得"""
        tracks = []
        results = self.sp.album_tracks(album_meta["id"])
        tracks.extend(results["items"])
        while results["next"]:
            results = self.sp.next(results)
            tracks.extend(results["items"])

        logger.info("{} inclues {} tracks".format(album_meta["name"], len(tracks)))
        for i, track in enumerate(tracks):
            logger.info("%s. %s", i + 1, track["name"])
        return tracks
