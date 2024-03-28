# Spotify Web API 日本語ドキュメント

## 1. はじめに

Spotify Web APIを利用するにあたり、取得可能なデータや形式についてまとめる。
個人用メモ程度なので、詳細は[公式ドキュメント](https://developer.spotify.com/documentation/web-api)を参照ください。

## 2. 取得可能なデータ
Spotify Web APIにリクエストを投げると、要求したリクエストに応じてレスポンス(オブジェクト)が返される。
その代表的なオブジェクトついて以下にまとめる。本記事では以下のオブジェクトについて取り扱う。


| オブジェクト名 | 説明 |
| -------------- | ---- |
| ArtistObject   | アーティストに関する情報    |
| AlbumObject    | アルバムに関する情報     |
| TrackObject    | トラックに関する情報     |
| PlaylistObject | プレイリストに関する情報    |
| EpisodeObject  | エピソード(トラックとトークを合わせたラジオ形式のやつ)に関する情報     |



### ArtistObject

| 属性          | 型                   | 説明                                                                        |
| ------------- | -------------------- | --------------------------------------------------------------------------- |
| external_urls | object               | アーティストページへのリンク。                                              |
| followers     | object               | フォローワーに関する情報。                                                  |
| genres        | array of strings     | 音楽ジャンルのリスト。                                                      |
| href          | string               | ArtistObjectへのURL。ArtistObject全情報へのアクセスするために使用する。     |
| id            | string               | アーティストID。                                                            |
| images        | array of ImageObject | アーティストのカバー画像情報(ImageObject)のリスト。                         |
| name          | string               | アーティスト名。                                                            |
| popularity    | integer              | 人気度。0-100の値をとる。そのアーティストの全トラックの人気から計算される。 |
| type          | string               | オブジェクトの型。"artist"が格納される。                                    |
| uri           | string               | Spotify URI。                                                               |


### AlbumObject

| 属性                   | 型                       | 説明                                                                                                                                                                                                                                                                                           |
| ---------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| album_type             | string                   | アルバム種別。 ["album", "single", "compilation"] を取り得る。                                                                                                                                                                                                                                 |
| artists                | array of ArtistObject(*) | ArtistObjectのリスト。                                                                                                                                                                                                                                                                         |
| available_markets      | array of strings         | 取得可能な国のリスト。アルバムのトラックのうち1曲でも取得可能であれば、取得可能とみなされる。                                                                                                                                                                                                  |
| copyrights             | array of CopyrightObject | 著作権表示と種別。                                                                                                                                                                                                                                                                             |
| external_ids           | object                   | 外部ID。ISRCコード等。                                                                                                                                                                                                                                                                         |
| external_urls          | object                   | アルバムページへのリンク。                                                                                                                                                                                                                                                                     |
| genres                 | array of strings         | アルバムに紐づく音楽ジャンルのリスト。紐付けられていない場合は、空になる。                                                                                                                                                                                                                     |
| href                   | string                   | AlbumObjectへのURL。TrackObject全情報へのアクセスするために使用する。                                                                                                                                                                                                                          |
| id                     | string                   | アルバムID                                                                                                                                                                                                                                                                                     |
| images                 | array of ImageObject     | アルバムのカバー画像情報(ImageObject)のリスト。様々な解像度の画像を提供している。                                                                                                                                                                                                              |
| label                  | string                   | 出版レーベル名。                                                                                                                                                                                                                                                                               |
| name                   | string                   | アルバム名。                                                                                                                                                                                                                                                                                   |
| popularity             | integer                  | アルバムの人気度。0−100の値をとる。                                                                                                                                                                                                                                                            |
| release_date           | string                   | リリース日。                                                                                                                                                                                                                                                                                   |
| release_date_precision | string                   | リリース日の精度。                                                                                                                                                                                                                                                                             |
| total_tracks           | integer                  | 合計トラック数。                                                                                                                                                                                                                                                                               |
| tracks                 | object                   | アルバムに収録されているトラックを格納したオブジェクト。<br>`items`属性に各トラックのTrackObject(*)が格納されている。トラックの人気度などは、このTrackObjectには含まれない。<br>またページネーションをサポートしており、トラック数が多い場合などは、`next`や`previous`属性を利用して取得する。 |
| type                   | string                   | オブジェクトの型。"album"が格納される。                                                                                                                                                                                                                                                        |
| uri                    | string                   | Spotify URI。                                                                                                                                                                                                                                                                                  |

### TrackObject

| 属性              | 型                    | 説明                                                                  |
| ----------------- | --------------------- | --------------------------------------------------------------------- |
| album             | object                | AlbumObject(*)。                                                      |
| artists           | array of ArtistObject | ArtistObjectのリスト。                                                |
| available_markets | array of strings      | トラック再生可能な国のリスト。                                        |
| disc_number       | integer               | ディスク番号。(複数のディスクで構成されている場合以外1)               |
| duration_ms       | integer               | 曲の長さ。単位はmsec                                                  |
| explicit          | boolean               | 歌詞の有無。 true: 有。false: = 無or不明。                            |
| external_ids      | object                | 外部ID。ISRCコード等。                                                |
| external_urls     | object                | トラックページへのリンク。                                            |
| href              | string                | TrackObjectへのURL。TrackObject全情報へのアクセスするために使用する。 |
| id                | string                | トラックID。                                                          |
| is_local          | boolean               | トラックがローカル保存されているか。                                  |
| name              | string                | トラック名。                                                          |
| popularity        | integer               | 人気度。                                                              |
| preview_url       | string                | 試聴用オーディオ(30s, mp3)へのURL。                                   |
| track_number      | integer               | トラック番号。                                                        |
| type              | string                | オブジェクトの型。"track"が格納される。                               |
| uri               | string                | Spotify URI。                                                         |

(*)がついているものは、オブジェクトの属性の一部が省略されています。全情報へのアクセスするためには、`href`属性使用する。

### PlaylistObject

| 属性          | 型                   | 説明                                                                                                                                                                                                                                                                            |
| ------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| collaborative | boolean              | 編集権限の有無。オーナーが他ユーザに編集を許可している場合はtrue。                                                                                                                                                                                                              |
| description   | string               | プレイリストの説明。                                                                                                                                                                                                                                                            |
| external_urls | object               | プレイリストページへのリンク。                                                                                                                                                                                                                                                  |
| followers     | object               | プレイリストのフォローワー情報。フォローワー数等。                                                                                                                                                                                                                              |
| href          | string               | PlaylistObjectへのURL。TrackObject全情報へのアクセスするために使用する。                                                                                                                                                                                                        |
| id            | string               | プレイリストID。                                                                                                                                                                                                                                                                |
| images        | array of ImageObject | アルバムのカバー画像情報(ImageObject)のリスト。                                                                                                                                                                                                                                 |
| name          | string               | プレイリスト名。                                                                                                                                                                                                                                                                |
| owner         | object               | プレイリストのオーナの情報。ユーザ名、ID等。                                                                                                                                                                                                                                    |
| primary_color |                      |                                                                                                                                                                                                                                                                                 |
| public        | boolean              | プレイリストの公開/非公開。                                                                                                                                                                                                                                                     |
| snapshot_id   | string               | 現在のプレイリストのバージョン識別子。バージョン管理に使用する。                                                                                                                                                                                                                |
| tracks        | object               | プレイリストに含まれているトラックを格納したオブジェクト。それぞれのトラックは、PlaylistTrackObjectという形で格納されている。これは、トラック情報の他に、トラックの追加日や追加したユーザなどの情報を格納している。なお、プレイリストには、エピソード or トラックを追加できる。 |
| type          | string               | オブジェクトの型。"playlist"が格納される。                                                                                                                                                                                                                                      |
| uri           | string               | Spotify URI。                                                                                                                                                                                                                                                                   |

### AudiobookObject
オーディオオブジェクトは、2024/3現在、日本では利用できない。

### EpisodeObject
TBD

## 3. HTTP ステータスコード

リクエストを送信した際に、返却される代表的なHTTPステータスコードを以下の表にまとめる。

| HTTP ステータスコード | 説明                                       | 対応策                                           |
| --------------------- | ------------------------------------------ | ------------------------------------------------ |
| 200 OK                | リクエストが成功したことを示す。           | -                                                |
| 400 Bad Request       | 不正なリクエストを示す。                   | 指定したパラメーターが正しいかなど確認してみる。 |
| 401 Unauthorized      | トークンの誤りや期限切れを示す。           | 再度、認証を行なってみる。                       |
| 403 Forbidden         | アクセス権がないため拒否されたことを示す。 | アクセスキーやスコープ設定など再度、見直す。     |
| 429 Too Many Requests | アクセスが上限回数に到達したことを示す。   | 時間をおいて再度試してみる。                     |
