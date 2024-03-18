def get_mode(mode: int) -> str:
    return "Major" if mode == 1 else "Minor"


def get_key(key: int) -> str:
    # ピッチクラス表記に基づくキーのマッピング
    key_class = {
        0: "C",
        1: "C♯/D♭",
        2: "D",
        3: "D♯/E♭",
        4: "E",
        5: "F",
        6: "F♯/G♭",
        7: "G",
        8: "G♯/A♭",
        9: "A",
        10: "A♯/B♭",
        11: "B",
    }
    if key == -1:
        return "Unknown"

    return key_class.get(key, "Invalid key")


def convert_msec2sec(value: int) -> float:
    return value / 1000
