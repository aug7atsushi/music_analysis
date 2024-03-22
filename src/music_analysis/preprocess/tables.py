from typing import Dict, List

import pandas as pd
import spotipy

from music_analysis.consts import (
    CATEGORICAL_COLS_KEYS,
    DATETIME_COLS_KEYS,
    NUMERIC_COLS_KEYS,
    USED_AUDIO_FEATURES_KEYS,
    USED_COLS_DICT,
)
from music_analysis.preprocess.base import SpotifyClientBase
from music_analysis.utils.dataframe import convert_msec2sec, get_key, get_mode
from music_analysis.utils.log import get_module_logger

logger = get_module_logger(__name__)


class TrackInfoTable(SpotifyClientBase):
    def __init__(self, sp: spotipy.client.Spotify, tracks: List[Dict]) -> None:
        super().__init__(sp)
        self.tracks = tracks
        self.track_ids = [track["id"] for track in self.tracks]
        self.track_info_df = None

    def _filter_track_info(self, track: List[Dict], features: List[Dict]) -> Dict:
        filtered_track = self._filter_track_dict(track)
        filtered_features = self._filter_features_dict(features)
        return filtered_track | filtered_features

    def _filter_track_dict(self, track_dict: dict):
        d = dict(
            track_id=track_dict["id"],
            artist_id=track_dict["artists"][0]["id"],
            album_id=track_dict["album"]["id"],
            track_name=track_dict["name"],
            artist_name=track_dict["artists"][0]["name"],
            album_name=track_dict["album"]["name"],
            album_type=track_dict["album"]["album_type"],
            release_date=track_dict["album"]["release_date"],
            release_date_precision=track_dict["album"]["release_date_precision"],
            popularity=track_dict["popularity"],
        )
        return d

    def _filter_features_dict(self, features_dict: dict):
        # 特定のキーのみを抽出して新しい辞書を作成
        new_d = {
            key: features_dict[key]
            for key in USED_AUDIO_FEATURES_KEYS
            if key in features_dict
        }
        return new_d

    def _post_process(self) -> None:
        # 値の置換
        self.track_info_df["duration"] = self.track_info_df["duration_ms"].apply(
            convert_msec2sec
        )
        self.track_info_df.drop(columns=["duration_ms"], inplace=True)
        self.track_info_df["key"] = self.track_info_df["key"].apply(get_key)
        self.track_info_df["mode"] = self.track_info_df["mode"].apply(get_mode)

        # 型変換
        self._convert_dtypes()

        # カラム名変更
        self.track_info_df = self.track_info_df.rename(columns=USED_COLS_DICT)

    def audio_features(self, n_max_track=100) -> List[Dict]:

        # 1回に抽出できる量が最大100件のため部分集合へ分割
        subset_track_ids = [
            self.track_ids[i : i + n_max_track]
            for i in range(0, len(self.track_ids), n_max_track)
        ]

        audio_features = []
        for track_ids in subset_track_ids:
            audio_features.extend(self.sp.audio_features(track_ids))
        return audio_features

    def get_track_info_df(self) -> pd.DataFrame:
        df = []
        for track, features in zip(self.tracks, self.audio_features()):
            _track_info = self._filter_track_info(track, features)
            df.append(_track_info)

        self.track_info_df = pd.DataFrame(df)
        self._post_process()
        return self.track_info_df

    def _convert_dtypes(self) -> None:
        # Numeric
        self.track_info_df[NUMERIC_COLS_KEYS] = self.track_info_df[
            NUMERIC_COLS_KEYS
        ].astype(pd.Float32Dtype())

        # Categorical
        self.track_info_df[CATEGORICAL_COLS_KEYS] = self.track_info_df[
            CATEGORICAL_COLS_KEYS
        ].astype("category")

        # Datetime
        for datetime_col in DATETIME_COLS_KEYS:
            self.track_info_df[datetime_col] = pd.to_datetime(
                self.track_info_df[datetime_col], format="mixed"
            )
