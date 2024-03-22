USED_AUDIO_FEATURES_KEYS = [
    "duration_ms",
    "loudness",
    "tempo",
    "danceability",
    "energy",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "time_signature",
    "key",
    "mode",
]

NUMERIC_COLS_DICT = {
    "duration": "曲長[s]",
    "loudness": "平均ラウドネス[dB]",
    "tempo": "テンポ(BPM)",
    "danceability": "danceability",
    "energy": "energy",
    "speechiness": "speechiness",
    "acousticness": "acousticness",
    "instrumentalness": "instrumentalness",
    "liveness": "liveness",
    "valence": "valence",
}

CATEGORICAL_COLS_DICT = {
    "track_id": "トラックID",
    "artist_id": "アーティストID",
    "album_id": "アルバムID",
    "track_name": "トラック名",
    "artist_name": "アーティスト名",
    "album_name": "アルバム名",
    "album_type": "アルバム種別",
    "release_date_precision": "リリース日の精度",
    "popularity": "人気度",
    "time_signature": "拍子",
    "key": "キー",
    "mode": "長短長",
}

DATETIME_COLS_DICT = {
    "release_date": "リリース日",
}

NUMERIC_COLS_KEYS = list(NUMERIC_COLS_DICT.keys())
CATEGORICAL_COLS_KEYS = list(CATEGORICAL_COLS_DICT.keys())
DATETIME_COLS_KEYS = list(DATETIME_COLS_DICT.keys())

USED_COLS_DICT = NUMERIC_COLS_DICT | CATEGORICAL_COLS_DICT | DATETIME_COLS_DICT


PROMPT_COVER_IMG_TEMPLATE = """
プレイリストのカバー画像を作成してください。
プレイリストのジャンルは、Lofi-Hiphopです。
"""
