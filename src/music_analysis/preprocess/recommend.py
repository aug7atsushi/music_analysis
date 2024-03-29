import random
from typing import Dict, List, Optional, Union

import spotipy
from pydantic import BaseModel, Field

from music_analysis.preprocess.base import SpotifyClientBase
from music_analysis.utils.log import get_module_logger

logger = get_module_logger(__name__)


class RecommendSeed(BaseModel):
    seed_artists: List[str] = Field(..., min_items=0, max_items=5)
    seed_tracks: List[str] = Field(..., min_items=0, max_items=5)
    seed_genres: List[str] = Field(..., min_items=0, max_items=5)
    limit: int = Field(..., ge=1, le=100)
    country: Optional[str] = None
    kwargs: dict = {}


class TrackRecommender(SpotifyClientBase):
    def __init__(self, sp: spotipy.client.Spotify) -> None:
        super().__init__(sp=sp)
        self.available_genres = sp.recommendation_genre_seeds()["genres"]

    def _recommend(self, recommend_seed: RecommendSeed) -> Union[List, Dict]:
        results = self.sp.recommendations(
            seed_artists=recommend_seed.seed_artists,
            seed_tracks=recommend_seed.seed_tracks,
            seed_genres=recommend_seed.seed_genres,
            limit=recommend_seed.limit,
            country=recommend_seed.country,
            **recommend_seed.kwargs,
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

        # Sampling
        seed_artists = TrackRecommender.sample(seed_artists, n_max=5)
        seed_tracks = TrackRecommender.sample(seed_tracks, n_max=5)
        seed_genres = TrackRecommender.sample(seed_genres, n_max=5)

        print(type(seed_artists), type(seed_tracks), type(seed_genres))

        # Validation
        recommend_seed = RecommendSeed(
            seed_artists=seed_artists,
            seed_tracks=seed_tracks,
            seed_genres=seed_genres,
            limit=limit,
            country=country,
            **kwargs,
        )

        # Recommendation
        tracks, _ = self._recommend(recommend_seed)
        for track in tracks:
            logger.info(
                "Artist: {}, Track: {}".format(
                    track["artists"][0]["name"], track["name"]
                )
            )

        return [track["id"] for track in tracks]

    @staticmethod
    def sample(list: List | None, n_max: int = 5):
        if list is None:
            list = []

        if len(list) <= n_max:
            return list
        else:
            return random.sample(list, n_max)
