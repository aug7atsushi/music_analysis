from typing import Dict, List

import spotipy

from music_analysis.preprocess.base import SpotifyClientBase
from music_analysis.utils.log import get_module_logger

logger = get_module_logger(__name__)


class TrackRetriever(SpotifyClientBase):
    def __init__(self, sp: spotipy.Spotify) -> None:
        super().__init__(sp)

    def glob_artist_all_album_tracks(
        self,
        artist_id: str,
        album_types: List[str] = ["album", "single", "appears_on", "compilation"],
    ) -> List[Dict]:
        """アーティストの全アルバムの全トラックを取得"""
        album_ids = self._get_artist_album_ids(artist_id, album_types=album_types)

        tracks = []
        for album_id in album_ids:
            tracks_ = self.glob_album_tracks(album_id)
            tracks.extend(tracks_)
        return tracks

    def glob_album_tracks(self, album_id: str) -> List[Dict]:
        """アルバムのトラックを取得"""
        track_ids = self._get_album_track_ids(album_id)
        tracks = self.get_track_infos(track_ids)
        return tracks

    def glob_playlist_tracks(self, pl_id: str) -> List[Dict]:
        """プレイリストのトラックを取得"""
        track_ids = self._get_playlist_track_ids(pl_id)
        tracks = self.get_track_infos(track_ids)
        return tracks

    def _get_artist_album_ids(
        self,
        artist_id: str,
        album_types: List[str] | None,
    ) -> List[str]:
        """アーティストのアルバムIDを取得"""
        if album_types is not None:
            album_types = ",".join(album_types)

        results = self.sp.artist_albums(artist_id, album_type=album_types)

        album_ids = [result["id"] for result in results["items"]]
        while results["next"]:
            results = self.sp.next(results)
            for result in results["items"]:
                album_ids.append(result["id"])
        logger.info(f"Total albums: {len(album_ids)}")
        return album_ids

    def _get_album_track_ids(self, album_id: str) -> List[str]:
        """アルバム内に含まれるトラックIDを取得"""
        results = self.sp.album_tracks(album_id)

        track_ids = [result["id"] for result in results["items"]]
        while results["next"]:
            results = self.sp.next(results)
            for result in results["items"]:
                track_ids.append(result["id"])

        logger.info(f"This album inclues {len(track_ids)} tracks")
        return track_ids

    def _get_playlist_track_ids(self, pl_id: str):
        """プレイリスト内に含まれるトラックIDを取得"""
        results = self.sp.playlist_tracks(pl_id)

        # print(tracks)
        track_ids = [
            result["track"]["id"]
            for result in results["items"]
            if result["track"] is not None
        ]
        while results["next"]:
            results = self.sp.next(results)
            for result in results["items"]:
                track_id = result["track"]["id"]
                track_ids.append(track_id)
        logger.info(f"This playlist inclues {len(track_ids)} tracks")
        return track_ids

    def get_track_infos(self, track_ids: List[str], n_max_track: int = 50):
        """指定されたIDのトラックを取得"""
        # 1回に抽出できる量が最大50件のため部分集合へ分割
        subset_track_ids = [
            track_ids[i : i + n_max_track]
            for i in range(0, len(track_ids), n_max_track)
        ]

        track_infos = []
        for track_ids in subset_track_ids:
            track_infos.extend(self.sp.tracks(track_ids)["tracks"])
            # print(track_infos)
        return track_infos


class ArtistRetriver(SpotifyClientBase):
    def __init__(self, sp: spotipy.Spotify) -> None:
        super().__init__(sp)

    def get_artist_id_with_name(self, artist_name: str) -> dict:
        """アーティスト名で検索を行い、最上位のアーティストIDを返す"""
        results = self.sp.search(
            q=f"artist: {artist_name}", type="artist", limit=10, market=None
        )
        items = results["artists"]["items"]
        if len(items) > 0:
            return items[0]["id"]
        else:
            return None

    def get_artist_infos(self, artist_ids: List[str]) -> List[Dict]:
        """アーティストIDで検索し、アーティストのメタ情報を返す"""
        return self.sp.artists(artist_ids)
