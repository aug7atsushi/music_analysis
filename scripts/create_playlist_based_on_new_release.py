from datetime import date
from pathlib import Path

import fire
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from music_analysis import REPO_ROOT
from music_analysis.preprocess.playlist import PlaylistCreator
from music_analysis.preprocess.retrieve import TrackRetriever
from music_analysis.preprocess.tables import TrackInfoTable
from music_analysis.utils.config import Config

load_dotenv(REPO_ROOT / ".env")


def main(cfg_path: str):
    today = date.today().strftime("%Y%m%d")
    cfg = Config(Path(cfg_path))
    print(cfg)

    # spotipy clientの作成
    scope = "playlist-modify-public,playlist-modify-private,ugc-image-upload,user-library-modify,user-library-read"  # noqa
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # New releaseのアルバムIDを取得
    track_retriever = TrackRetriever(sp=sp)
    album_ids = track_retriever.get_new_release_album_ids(
        limit=cfg.n_used_album, country=cfg.country
    )

    # アルバムごとにトラックIDを取得
    track_ids = []
    for album_id in album_ids:
        track_ids_ = track_retriever.get_album_track_ids(album_id=album_id)
        track_ids.extend(track_ids_)

    # トラックテーブルを取得
    track_info_table = TrackInfoTable(sp=sp, track_ids=track_ids)
    track_info_df = track_info_table.get_track_info_df()

    # トラックテーブルを人気度順にソート
    track_info_df = track_info_df.sort_values(by="人気度", ascending=False)
    track_info_df = track_info_df.groupby("アルバムID", observed=True).head(
        cfg.n_duplicate_track_in_same_album
    )
    top_track_ids = track_info_df.head(cfg.n_track)["トラックID"].values

    # プレイリストを作成しトラックを追加
    playlist_creator = PlaylistCreator(
        sp=sp,
        user_id=sp.me()["id"],
        name=f"{cfg.name} #{today}",
        public=cfg.public,
        collaborative=cfg.collaborative,
        description=cfg.description,
    )
    playlist_creator.add_tracks(track_ids=top_track_ids)
    # playlist_creator.create_upload_cover_image()


if __name__ == "__main__":
    fire.Fire(main)
