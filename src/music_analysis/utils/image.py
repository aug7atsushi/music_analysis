import base64
from io import BytesIO

from PIL import Image


def convert_b64png_to_b64jpg(base64_png: str) -> str:
    # Base64データをデコードしてPillowイメージに変換
    png_image = Image.open(BytesIO(base64.b64decode(base64_png)))

    # 新しいBytesIOオブジェクトを作成し、そこにJPGとして画像を保存
    jpg_image_buffer = BytesIO()
    png_image.save(jpg_image_buffer, format="JPEG")

    # BytesIOオブジェクトをBase64エンコードされた文字列に変換
    base64_jpg = base64.b64encode(jpg_image_buffer.getvalue()).decode("utf-8")
    return base64_jpg
