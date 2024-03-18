ORIGINAL_KEYS = [
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

NUMERIC_FEATURES_DICT = {
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

CATEGORICAL_FEATURES_DICT = {
    "track_id": "トラックID",
    "artist_id": "アーティストID",
    "track_name": "トラック名",
    "artist_name": "アーティスト名",
    "time_signature": "拍子",
    "key": "キー",
    "mode": "長短長",
}


NUMERIC_FEATURES_KEYS = list(NUMERIC_FEATURES_DICT.keys())
CATEGORICAL_FEATURES_KEYS = list(CATEGORICAL_FEATURES_DICT.keys())

FEATURES_DICT = NUMERIC_FEATURES_DICT | CATEGORICAL_FEATURES_DICT
