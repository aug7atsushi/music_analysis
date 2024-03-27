from typing import List


def split_array2subarry(arr: List, n_max_elm: int) -> List[List]:
    """配列を指定された要素数の部分配列に分割する"""
    sub_array = [arr[i : i + n_max_elm] for i in range(0, len(arr), n_max_elm)]
    return sub_array
