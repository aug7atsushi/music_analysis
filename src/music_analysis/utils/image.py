import base64
from io import BytesIO
from pathlib import Path
from typing import Union

from PIL import Image


def img_to_b64jpg(img):
    # 新しいBytesIOオブジェクトを作成し、そこにJPGとして画像を保存
    jpg_image_buffer = BytesIO()
    img.save(jpg_image_buffer, format="JPEG")

    # BytesIOオブジェクトをBase64エンコードされた文字列に変換
    base64_jpg = base64.b64encode(jpg_image_buffer.getvalue()).decode("utf-8")
    return base64_jpg


def convert_b64png_to_b64jpg(base64_png: str) -> str:
    # Base64データをデコードしてPillowイメージに変換
    png_image = Image.open(BytesIO(base64.b64decode(base64_png)))
    base64_jpg = img_to_b64jpg(png_image)
    return base64_jpg


def read_image_as_b64jpg(file_path: Union[Path, str]):
    img = Image.open(file_path)
    base64_jpg = img_to_b64jpg(img)
    return base64_jpg
