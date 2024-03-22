# Spotipy: PythonでSpotify Web API を利用する

## 1. はじめに

Spotifyは、楽曲のメタデータの取得、レコメンデーションの取得、プレイリストの作成と管理などを可能にする、[Spotify Web API](https://developer.spotify.com/documentation/web-api)を公開しています。

**Spotipy**は、このSpotify Web APIをPythonから利用するためのライブラリです。
Spotipyを活用することで、Pythonスクリプトから、以下に示すような機能を使用できます。

公式ドキュメントは[こちら](https://spotipy.readthedocs.io/)

#### 主な機能
- **ユーザー認証**: OAuth 2.0をサポートし、ユーザー認証を実行。
- **データアクセス**: アーティスト、アルバム、トラックに関する詳細情報の取得や、ユーザーのプレイリスト操作。
- **検索機能**: 曲名、アーティスト名、アルバム名による検索。
- **プレイリスト管理**: ユーザーのプレイリストの作成、更新、削除。


## 2. インストール方法

### 2-0. Spotify Web APIのクライアントID、クライアントシークレットの取得
Spotipyを使用するには、まずSpotify Developer Dashboardでアプリを登録し、
**クライアントID**と**クライアントシークレット**を取得する必要があります。

取得方法については、[公式ドキュメント](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)などを参考にしてください。
また、日本語の解説記事も多くありますので、ここでの説明は割愛します。

### 2-1. 環境変数への設定
前節のクライアントIDとクライアントシークレットが取得できたら、それらを環境変数へ設定します。
APIのアクセストークン等はスクリプト内にベタ書きするのはよくないので、ここでは環境変数に設定しています。

なお、Spotipyでは以下の変数名で格納しておくと、(後述しますが)認証の際にクライアントIDと
クライアントシークレットを明示的に引数として渡す必要がないため、便利です。

```bash
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
```

### 2-2. Spotipyのインストール
Spotipyはpipを使用して簡単にインストールできます。

```bash
pip install spotipy
```

## 2-3. 基本的な使い方
認証後に、あるトラックの情報を取得する例です。

```python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotifyの認証情報
client_credentials_manager = SpotifyClientCredentials(client_id='Your_Client_ID', client_secret='Your_Client_Secret')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# トラック情報の取得
track = sp.track('spotify:track:4cluDES4hQEUhmXj6TXkSo')
print(track)
```

- 上の例では、`SpotifyClientCredentials()`にクライアントIDとクライアントシークレットを渡していますが、前述の`SPOTIPY_CLIENT_ID`および`SPOTIPY_CLIENT_SECRET`を設定することで、引数にこれらを渡さなくても認証ができます。
- トラックIDとして、`4cluDES4hQEUhmXj6TXkSo` という記号列を渡していますが、これは、Spotify デスクトップアプリのシェアリンクから取得できます。また、`spotify:track:track_id`という形式で渡していますが、以下の形式に対応しています。
  - `Spotify URI` : 例：spotify:track:4cluDES4hQEUhmXj6TXkSo
  - `Spotify URL` : 例：http://open.spotify.com/track/4cluDES4hQEUhmXj6TXkSo
  - `Spotify ID` : 例：4cluDES4hQEUhmXj6TXkSo


## 3. サポートされているモジュール・メソッド
主に以下2つのモジュールが提供されています。

| モジュール名        | 概要                                                                   |
| ------------------- | ---------------------------------------------------------------------- |
| `client` モジュール | 楽曲検索等、データ取得全般をサポートする。メインで使用するのはこっち。 |
| `oauth2` モジュール | ユーザのプレイリスト取得等、認証周りの機能をサポートする。             |

### 3-1. `client`モジュール
`client`モジュールで実装されているメソッドを紹介します。

#### アルバム情報
| メソッド名     | 概要                                                     |
| -------------- | -------------------------------------------------------- |
| `album`        | 指定したアルバムIDに関する情報を取得する。               |
| `album_tracks` | 指定したアルバムIDに含まれるトラックのリストを取得する。 |
| `albums`       | 複数のアルバムIDに基づいて、アルバム情報を取得する。     |
| `new_releases` | 新しくリリースされたアルバムの情報を取得する。           |


#### アーティスト情報
| メソッド名               | 概要                                                     |
| ------------------------ | -------------------------------------------------------- |
| `artist`                 | 指定したアーティストIDに関する情報を取得する。           |
| `artist_albums`          | 指定したアーティストIDのアルバムを取得する。             |
| `artist_top_tracks`      | 指定したアーティストIDのトップトラックを取得する。       |
| `artist_related_artists` | 指定したアーティストIDに関連するアーティストを取得する。 |
| `artists`                | 複数のアーティストIDに関する情報を取得する。             |


#### トラック情報
| メソッド名       | 概要                                                                                                                              |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `audio_analysis` | 指定したトラックIDのオーディオ詳細情報を取得する。1トラックに対してさらに細かい単位で、属性値が決まるイメージ。例: 小節ごとの長さ |
| `audio_features` | 指定したトラックIDのオーディオ属性情報を取得する。1トラックに対して1つ属性値が決まるイメージ。例: 曲の長さ                        |
| `track`          | 指定したトラックIDに関する情報を取得する。                                                                                        |
| `tracks`         | 複数のトラックIDに基づいて、トラック情報を取得する。                                                                              |


#### カテゴリ情報
| メソッド名           | 概要                                           |
| -------------------- | ---------------------------------------------- |
| `categories`         | 利用可能なカテゴリのリストを取得する。         |
| `category_playlists` | 特定のカテゴリに属するプレイリストを取得する。 |

#### プレイリスト情報
| メソッド名                                            | 概要                                                                           |
| ----------------------------------------------------- | ------------------------------------------------------------------------------ |
| `featured_playlists`                                  | Spotifyが提供するプレイリストを取得する。                                      |
| `playlist`                                            | 指定したプレイリストからプレイリストの情報を取得する。                         |
| `playlist_add_items`                                  | 指定したプレイリストにトラック/エピソードを追加する。                          |
| `playlist_change_details`                             | 指定したプレイリストの詳細情報を変更する。                                     |
| `playlist_cover_image`                                | 指定したプレイリストのカバー画像を取得する。                                   |
| `playlist_items`                                      | 指定したプレイリスト内のトラック/エピソードを取得する。                        |
| `playlist_upload_cover_image`                         | 指定したプレイリストのカバー画像を変更する。                                   |
| `user_playlist_create`                                | 新しいプレイリストを作成する。                                                 |
| `user_playlist_remove_all_occurrences_of_tracks`      | 指定したプレイリストから指定したすべてのトラックを削除する。                   |
| `user_playlist_remove_specific_occurrences_of_tracks` | 指定したプレイリストから指定したトラックの特定の出現位置(再生順序)を削除する。 |
| `user_playlist_replace_tracks`                        | 指定したプレイリストのトラックを置き換える。                                   |
| `user_playlist_reorder_tracks`                        | 指定したプレイリストID内のトラックの順序を変更する。                           |
| `user_playlist_tracks`                                | ユーザーのプレイリストに含まれるトラックを取得する。                           |
| `user_playlists`                                      | 特定のユーザーのプレイリストを取得する。                                       |


#### 再生
| メソッド名       | 概要                                           |
| ---------------- | ---------------------------------------------- |
| `device`         | ユーザーの利用可能なデバイスを取得する。       |
| `repeat`         | 再生中のトラックのリピートモードを設定する。   |
| `shuffle`        | 再生中のトラックのシャッフルモードを設定する。 |
| `volume`         | 再生中のデバイスの音量を設定する。             |
| `pause_playback` | 再生中のコンテンツを止める。                   |
| `previous_track` | 再生中のトラックを前のトラックへ戻す。         |
| `queue`          | 再生キューを取得する。                         |
| `next_track`     | 再生中のトラックを次のトラックへ進める。       |


#### ユーザ情報
| メソッド名                       | 概要                                                         |
| -------------------------------- | ------------------------------------------------------------ |
| `current_playback`               | 自分の現在の再生情報を取得する。                             |
| `current_user`                   | 自分のアカウント情報を取得する。`me`メソッドへのエイリアス。 |
| `current_user_follow_playlist`   | プレイリストをフォローする。                                 |
| `current_user_followed_artists`  | 自分がフォローしているアーティストを取得する。               |
| `current_user_unfollow_playlist` | プレイリストをアンフォローする。                             |
| `current_user_playlists`         | 自分ののプレイリスト一覧を取得する。                         |
| `current_user_saved_albums`      | ユーザーが保存したアルバムを取得する。                       |
| `current_user_saved_tracks`      | ユーザーが保存したトラックを取得する。                       |
| `current_user_top_artists`       | ユーザーのトップアーティストを取得する。                     |
| `current_user_top_tracks`        | ユーザーのトップトラックを取得する。                         |
| `me`                             | ユーザーのアカウント情報を取得する。                         |


#### 検索 & レコメンド
| メソッド名        | 概要                                                                          |
| ----------------- | ----------------------------------------------------------------------------- |
| `next`            | ページネーションをサポートするため、次の結果セットを取得する。                |
| `previous`        | ページネーションをサポートするため、前の結果セットを取得する。                |
| `search`          | Spotifyのカタログでトラック、アーティスト、アルバム、プレイリストを検索する。 |
| `recommendations` | 指定した情報に基づくレコメンデーションを取得する。                            |


### 3-2. `oauth`モジュール
`oauth2`モジュールで実装されているクラスを紹介します。主に認証まわりで利用するクラスが実装されています。


| メソッド名                 | 概要                                                                                                                             |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `SpotifyOAuth`             | クライアント認証フローをサポートするクラス。クライアントID、クライアントシークレット、リダイレクトURIなどを引数に取る。          |
| `SpotifyClientCredentials` | 認証コードフローをサポートするクラス。クライアントID、クライアントシークレットなどを引数に取る。                                 |
| `SpotifyImplicitGrant`     | 暗黙的な認証をサポートするクラス。ブラウザベースのアプリケーション向けに設計されており、クライアントシークレットを必要としない。 |


## 4. 認証フローについて
これまで明示的にユーザ認証について扱っていませんでしたが、認証周りについて本節で扱いたいと思います。
はじめに、上記すべてのクラス、メソッドを使用するには、ユーザ認証が必要となります。
Spotipyでは主に二つの認証フローをサポートしています。他にも、"PKCE Authorization Flow" や "Implicit Grant Flow"
という認証についてもサポートされているようですが、筆者がこの辺り詳しくないこともあり、ここでは割愛します。

#### 認証コードフロー
- ユーザーが一度ログインする長期間実行されるようなアプリケーション向き。ユーザーに代わって、プレイリストの操作等行う必要がある場合に使用する。
- `spotipy.oauth2.SpotifyClientCredentials`クラスを使用する。
- リダイレクトURI (`SPOTIPY_REDIRECT_URI`) を設定する必要がある。Spotify Web APIのMy Dashboardから設定できる
- 取得するデータに応じて、適切なスコープを設定して利用する。指定可能なスコープは[こちら](https://developer.spotify.com/documentation/web-api/concepts/scopes)。スコープを適切に定義しないと ERROR 401 Unauthorized, permission missing が発生する可能性がある。

#### クライアント認証フロー
- ユーザ情報の取得を伴わないアプリケーション向き。そのため、認証コードフローに比べ、取得可能なデータの範囲は小さい。
- `spotipy.oauth2.SpotifyOAuth`クラスを使用する。
- リダイレクトURI (`SPOTIPY_REDIRECT_URI`) を設定する必要がない。つまり、ブラウザのサインインページへリダイレクトされることはない。
