from datetime import date
from pathlib import Path

import fire
import spotipy
import yaml
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from music_analysis import REPO_ROOT
from music_analysis.preprocess.playlist import PlaylistCreator
from music_analysis.preprocess.recommend import TrackRecommender

load_dotenv(REPO_ROOT / ".env")


class Config:
    def __init__(self, config_path: str) -> None:
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        for k, v in self.config.items():
            setattr(self, k, v)

    def __str__(self):
        attributes = [f"{k}: {v}" for k, v in self.config.items()]
        return "\n".join(attributes)


def main(cfg_path: str):
    today = date.today().strftime("%Y%m%d")
    cfg = Config(Path(cfg_path))
    print(cfg)

    # spotipy clientの作成
    scope = "playlist-modify-public,playlist-modify-private,ugc-image-upload"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # レコメンドを取得
    track_recommender = TrackRecommender(sp=sp)
    track_ids = track_recommender.get_recommended_track_ids(
        seed_artists=cfg.seed_artists,
        seed_tracks=cfg.seed_tracks,
        seed_genres=cfg.seed_genres,
        limit=cfg.limit,
        country=cfg.country,
        **cfg.audio_features,
    )

    # プレイリストを作成しトラックを追加
    playlist_creator = PlaylistCreator(
        sp=sp,
        user_id=sp.me()["id"],
        name=f"{cfg.name} #{today}",
        public=cfg.public,
        collaborative=cfg.collaborative,
        description=cfg.description,
    )
    playlist_creator.add_tracks(track_ids=track_ids)
    playlist_creator.create_upload_cover_image()


if __name__ == "__main__":
    fire.Fire(main)
