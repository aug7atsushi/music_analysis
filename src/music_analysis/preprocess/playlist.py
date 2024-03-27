from pathlib import Path
from typing import Dict, List

import spotipy

from music_analysis.consts import PROMPT_COVER_IMG_TEMPLATE
from music_analysis.preprocess.base import SpotifyClientBase
from music_analysis.preprocess.dalle import DalleImageGenerator
from music_analysis.utils.image import convert_b64png_to_b64jpg, read_image_as_b64jpg


class PlaylistCreator(SpotifyClientBase):
    def __init__(
        self,
        sp: spotipy.client.Spotify,
        user_id: str,
        name: str,
        cover_image_path: str,
        public: bool = False,
        collaborative: bool = False,
        description: str = None,
    ) -> None:
        super().__init__(sp=sp)
        self.cover_image_path = Path(cover_image_path)
        self.image_generator = DalleImageGenerator()

        new_playlist = self.create_empty_playlist(
            user_id=user_id,
            name=name,
            public=public,
            collaborative=collaborative,
            description=description,
        )
        self.playlist_id = new_playlist["id"]

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

    def add_tracks(self, track_ids=List[str]) -> None:
        self.sp.playlist_add_items(playlist_id=self.playlist_id, items=track_ids)

    def _create_cover_image(self, prompt: str) -> str:
        b64png_img = self.image_generator.get_generated_images_as_b64(
            prompt=prompt,
            n=1,
        )[0]

        # 戻り値の画像が、base64png形式の画像であるため、base64jpg形式に変更する
        b64jpg_img = convert_b64png_to_b64jpg(b64png_img)
        return b64jpg_img

    def _upload_cover_image(self, playlist_id, b64jpg_img: str):
        self.sp.playlist_upload_cover_image(
            playlist_id=playlist_id, image_b64=b64jpg_img
        )

    def create_upload_cover_image(self) -> None:
        b64jpg_img = self._create_cover_image(prompt=PROMPT_COVER_IMG_TEMPLATE)
        self._upload_cover_image(playlist_id=self.playlist_id, b64jpg_img=b64jpg_img)

    def upload_cover_image_from_local(self) -> None:
        b64jpg_img = read_image_as_b64jpg(self.cover_image_path)
        self._upload_cover_image(playlist_id=self.playlist_id, b64jpg_img=b64jpg_img)
