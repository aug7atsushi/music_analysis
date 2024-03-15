from typing import Dict, List

import pandas as pd

from music_analysis.consts import FEATURES_KEYS, FEATURES_MAPPING_DICT
from music_analysis.utils.dataframe import get_key, get_mode
from music_analysis.utils.log import get_module_logger

logger = get_module_logger(__name__)


class TrackInfoTable:
    def __init__(self, sp, tracks) -> None:
        self.sp = sp
        self.tracks = tracks
        self.track_ids = [track["id"] for track in self.tracks]

    def _filter_track_info(self, track: List[Dict], features: List[Dict]) -> Dict:
        filtered_track = self._filter_track_dict(track)
        filtered_features = self._filter_features_dict(features)
        return filtered_track | filtered_features

    def _filter_track_dict(self, track_dict: dict):
        d = dict(
            track_id=track_dict["id"],
            artist_id=track_dict["artists"][0]["id"],
            track_name=track_dict["name"],
            artist_name=track_dict["artists"][0]["name"],
        )
        return d

    def _filter_features_dict(self, features_dict: dict):
        # NOTE: album, release_date, popularityなどは別から取ってこないといけない

        # 特定のキーのみを抽出して新しい辞書を作成
        new_d = {
            key: features_dict[key] for key in FEATURES_KEYS if key in features_dict
        }
        return new_d

    def _post_process(self, track_info_df: pd.DataFrame) -> pd.DataFrame:
        track_info_df["key"] = track_info_df["key"].apply(get_key)
        track_info_df["mode"] = track_info_df["mode"].apply(get_mode)
        track_info_df = track_info_df.rename(columns=FEATURES_MAPPING_DICT)
        return track_info_df

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
        track_info_df = []
        for track, features in zip(self.tracks, self.audio_features()):
            _track_info = self._filter_track_info(track, features)
            track_info_df.append(_track_info)

        track_info_df = pd.DataFrame(track_info_df)
        track_info_df = self._post_process(track_info_df)
        return track_info_df
