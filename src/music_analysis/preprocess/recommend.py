from typing import Dict, List, Union

import spotipy

from music_analysis.preprocess.base import SpotifyClientBase
from music_analysis.utils.log import get_module_logger

logger = get_module_logger(__name__)


class TrackRecommender(SpotifyClientBase):
    def __init__(self, sp: spotipy.client.Spotify) -> None:
        super().__init__(sp=sp)
        self.available_genres = sp.recommendation_genre_seeds()["genres"]

    def _recommend(
        self,
        seed_artists: List[str] | None = None,
        seed_tracks: List[str] | None = None,
        seed_genres: List[str] | None = None,
        limit: int = 20,
        country: str | None = None,
        **kwargs,
    ) -> Union[List, Dict]:
        results = self.sp.recommendations(
            seed_artists=seed_artists,
            seed_tracks=seed_tracks,
            seed_genres=seed_genres,
            limit=limit,
            country=country,
            **kwargs,
        )

        return results["tracks"], results["seeds"][0]

    def get_recommended_track_ids(
        self,
        seed_artists: List[str] | None = None,
        seed_tracks: List[str] | None = None,
        seed_genres: List[str] | None = None,
        limit: int = 20,
        country: str | None = None,
        **kwargs,
    ) -> List[str]:
        tracks, _ = self._recommend(
            seed_artists=seed_artists,
            seed_tracks=seed_tracks,
            seed_genres=seed_genres,
            limit=limit,
            country=country,
            **kwargs,
        )
        for track in tracks:
            logger.info(
                "Artist: {}, Track: {}".format(
                    track["artists"][0]["name"], track["name"]
                )
            )

        return [track["id"] for track in tracks]
