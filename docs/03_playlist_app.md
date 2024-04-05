# 【Python】Spotifyのプレイリスト作成をAWS Lambdaで自動化する

## TL;DR

- この記事では、PythonからSpotify Web APIを操作できるライブラリである**Spotipy**を使用して、プレイリスト作成を自動化する方法を紹介します。スクリプトの自動実行には**AWS Lambda**を使用します。

- プレイリストに入れるトラックの選定は、Spotify Web APIで提供されているレコメンド機能に基づき行っている(=使用するのみ)ので、推薦アルゴリズムの実装や工夫は特にありません。

- 自分の音楽好みに合わせたプレイリストを効率的に作成したい方や、SpotifyのAPIを使ったプロジェクトに興味がある方の一助となれば幸いです。

- 使用ツール、サービスは、以下の通りです。

  - Python
  - Python依存パッケージ (pandasなど)
  - Spotify Web API (APIキーの発行に必要)
  - Spotipy
  - AWS Lambda、その他AWSのサービス (無料枠で対応できる範囲だと思います)

全体の処理のイメージは以下の通りです。


## 1. はじめに

まず、筆者が本機能を実装しようと思った経緯ですが、作業中に作業用BGMをよく活用しています。

多くの方によって、YoutubeやSpotifyにまとめられおり、これまでそれを利用していました。

そうしてまとめてくださった音楽を聴いている中で、だんだんと自分の好みのアーティストや曲調などが自分なりに分かってきて、自分の好みの曲を中心に収集したいと思ったのが、本機能を実装しようと思ったきっかけです。

本記事が目指すようなプレイリスト自動化については、他の方がすでにまとめてくださっていますが、楽曲取得、プレイリスト作成から自動化手順まで詳しく述べられている記事については、調べた限りなさそうでしたので、筆者のアウトプットの練習も兼ねてこちらに記載します。


### 1-1. 前提

- Pythonの基本的な構文について、ある程度、見識があるという前提で書かれています。

- 本記事では自動プレイリスト作成のため、AWS Lambdaを使用します。そのため、AWS LambdaやAWS S3の操作方法について、必要に応じてご自身でフォローいただかないといけないかも知れません。LambdaやS3については、無料枠で収まる規模の想定ですが、環境によっては課金が発生する可能性があります。

### 1-2. 本記事で扱わないこと

- Pythonやパッケージのインストール方法

- Spotify Web APIの使い方

- Spotipy の使い方

- AWSアカウントの発行方法、AWS S3やAWS Lambdaの基本操作

- 推薦アルゴリズムの実装(本記事では、Spotify Web APIのRecommend機能)


### 1-3. ゴール

AWS Lambdaでプレイリスト作成を自動化すること

### 1-4. 大まかな流れ

また、本記事では以下の手順で説明を進めます。

1. 環境構築

2. レコメンド取得〜プレイリスト作成を行うスクリプトを実装
   1. レコメンドを取得するためのSeedとなるアーティストやトラック等をYAMLファイルへ記述

   2. 2-1で設定したSeedに基づき、Spotify Web APIにより推薦されたトラックのIDを取得

   3. プレイリストを新規作成し、2-2で取得したトラックを追加

3. 作成したスクリプトをAWS Lambda & EventBridgeを用いて自動実行


## 2. 環境構築

### 2-0. 事前知識

実装面の工夫として、拡張性や可読性を考慮して自作パッケージを作ってその中から、Spotipyなどのメソッドを呼び出すようにしています。ついては、以降の説明において自作パッケージを呼び出す処理が出てきますので、Spotify Web APIやSpotipyのメソッドの動きがある程度、頭に入っていた方が理解しやすいかもしれません。


その観点で、事前に目を通していただいた方が良さそうな情報を以下にまとめています。以下、必要に応じてご参照ください。

- [Spotipyに関する基本操作](https://qiita.com/toxic_apple/items/20a0fce60e337bbe8716)

- [Spotify Web APIからデータを取得する上での権限のスコープ](https://developer.spotify.com/documentation/web-api/concepts/scopes)

### 2-1. APIキーの取得

[公式ドキュメント](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)や[以前私がSpotipyの利用方法についてまとめた記事](https://qiita.com/toxic_apple/items/20a0fce60e337bbe8716#2-%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E6%96%B9%E6%B3%95)をもとに、Spotify Web APIのクライアントID、クライアントシークレット、リダイレクトURIの3つを取得してください。リダイレクトURIは自分で任意に設定します。

### 2-2 Python のインストール

筆者環境では、Python 3.10を使用しています。適宜、インストールをお願いします。

パッケージ管理にvenv等の仮想環境等を使用される場合は、そちらも適宜設定し、アクティベーションまでお願いします。

なお、筆者環境では、Pythonのバージョン管理には、[pyenv](https://github.com/pyenv/pyenv)を、パッケージ管理には、[Poetry](https://python-poetry.org/)を使用しており、Poetryを使ったインストール方法についても以下で触れます。

インストールが完了した方は以下を実行してインストールされていることを確認してください。

```bash
python -V
```

```text
Python 3.10.XX
```

### 2-3. リポジトリのインストール

次に、プレイリスト作成に用いるリポジトリをクローンします。

```bash
git clone https://github.com/aug7atsushi/music_analysis.git
cd music_analysis
```

### 2-4. 依存パッケージのインストール

`music_analysis/`以下で実行。

#### pipを使用される方

```bash
pip install -e .
```

#### poetryを使用される方

```bash
poetry install
```

## 3. レコメンド取得〜プレイリスト作成の実装

はじめに、本章で実装するスクリプトは[こちら](https://github.com/aug7atsushi/music_analysis/blob/main/scripts/create_playlist_based_on_user_input.py)になります。以降の説明は、こちらのスクリプトから処理を切り出して説明します。
最終的に、AWS Lambdaにて自動化する際に、数行変更を行いますが本質は変りません。

```python
from datetime import date
from pathlib import Path

import fire
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from music_analysis import REPO_ROOT
from music_analysis.preprocess.playlist import PlaylistCreator
from music_analysis.preprocess.recommend import TrackRecommender
from music_analysis.utils.config import Config

load_dotenv(REPO_ROOT / ".env")


def main(cfg_path: str):
    today = date.today().strftime("%Y%m%d")
    cfg = Config(Path(cfg_path))
    print(cfg)

    # spotipy clientの作成
    scope = "playlist-modify-public,playlist-modify-private,ugc-image-upload"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # レコメンドを取得
    track_recommender = TrackRecommender(sp=sp)
    track_ids = track_recommender.get_recommended_track_ids(
        seed_artists=cfg.seed_artists,
        seed_tracks=cfg.seed_tracks,
        seed_genres=cfg.seed_genres,
        limit=cfg.limit,
        country=cfg.country,
        **cfg.audio_features,
    )

    # プレイリストを作成しトラックを追加
    playlist_creator = PlaylistCreator(
        sp=sp,
        user_id=sp.me()["id"],
        name=f"{cfg.name} #{today}",
        cover_image_path=cfg.cover_image_path,
        public=cfg.public,
        collaborative=cfg.collaborative,
        description=cfg.description,
    )
    playlist_creator.add_tracks(track_ids=track_ids)
    # playlist_creator.create_upload_cover_image()
    playlist_creator.upload_cover_image_from_local()


if __name__ == "__main__":
    fire.Fire(main)
```



### 3-1. 環境変数の設定
2-1節で取得したAPIキーを環境変数に設定していきます。環境変数を`export`コマンド等で設定していただいても良いですが、筆者環境では、[python-dotenv](https://pypi.org/project/python-dotenv/)というライブラリを使用して環境変数をスクリプトの冒頭で読み込みます。

`python-dotenv`を使用するには、リポジトリルート(`music_analysis/`)に、`.env`というファイルを作成し、そこへ環境変数を記入します。[こちら](https://github.com/aug7atsushi/music_analysis/blob/main/sample.env)にサンプルを用意していますので、クライアントID、クライアントシークレット、リダイレクトURIの3つを設定してください。

### 3-2. プレイリスト作成のためのYAMLファイルを作成

YAMLファイルを作成し、以下の項目を記述します。YAMLファイルの例については、[`configs/`](https://github.com/aug7atsushi/music_analysis/tree/main/configs)以下に格納してありますので、参考にしてください。

```yaml
name:             # プレイリストの名前
public:           # プレイリストの公開設定。公開の場合、true
collaborative:    # プレイリストの共同編集設定。共同編集OKの場合、true
description:      # プレイリストの説明
cover_image_path: # プレイリストのカバー画像(ジャケ写)に使用する画像ファイル

seed_artists:     # レコメンドの際にSeedとなるアーティストのID (最大5個まで)
seed_tracks:      # レコメンドの際にSeedとなるトラックのID (最大5個まで)
seed_genres:      # レコメンドの際にSeedとなるジャンル (最大5個まで)
limit:            # プレイリストの総トラック数 (最大100個まで)
country:          # トラックの利用可能な国コード
audio_features:   # 目標となる音響特徴量
```

### 3-3. 処理の実行

```
python scripts/create_playlist_based_on_user_input.py --cfg_path=./configs/YOUR_PLAYLIST.yaml
```

ここで、`cfg_path`には3-2で作成したYAMLを設定してください。

### 3-4. 処理の解説

ここまで、スクリプト(`create_playlist_based_on_user_input.py`)を実行する手順についてのみ説明してきました。この節では、スクリプトの処理内容に関して説明したいと思います。

#### 3-4-1. YAMLファイルの読み込み

`cfg_path`に指定されたYAMLファイルを読み込み、アトリビュート変数に格納します。

```python
cfg = Config(Path(cfg_path))
print(cfg)
```

#### 3-4-2. Spotipy Clientの作成

Spotipyを使用する際に、利用するクライアントを作成します。
また、クラアントを作成する際に、`auth_manager`に権限管理をサポートする`SpotifyOAuth(scope=scope)`を渡しています。
`scope`には今回の実装に必要となる、

- 自分の公開プレイリストへのアクセス権
- 自分の非公開プレイリストへのアクセス権
- 画像をアップロードするための権利

を設定しています。

```python
# spotipy clientの作成
scope = "playlist-modify-public,playlist-modify-private,ugc-image-upload"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
```

#### 3-4-3. レコメンドを取得

YAMLファイルで指定したアーティストやトラック等を元に、Spotifyによって推薦されたトラックのIDを取得します。
`track_ids`には、`limit`で指定された数を要素数とする、トラックIDのリストです。

```python
# レコメンドを取得
track_recommender = TrackRecommender(sp=sp)
track_ids = track_recommender.get_recommended_track_ids(
    seed_artists=cfg.seed_artists,
    seed_tracks=cfg.seed_tracks,
    seed_genres=cfg.seed_genres,
    limit=cfg.limit,
    country=cfg.country,
    **cfg.audio_features,
)
```

#### 3-4-4. プレイリスト作成

空のプレイリストを新規作成し、そこへレコメンドされたトラックを追加します。
また、プレイリストのカバー画像を追加します。

```python
# プレイリストを作成しトラックを追加
playlist_creator = PlaylistCreator(
    sp=sp,
    user_id=sp.me()["id"],
    name=f"{cfg.name} #{today}",
    cover_image_path=cfg.cover_image_path,
    public=cfg.public,
    collaborative=cfg.collaborative,
    description=cfg.description,
)
playlist_creator.add_tracks(track_ids=track_ids)
playlist_creator.upload_cover_image_from_local()
```

## 4. AWS Lambdaを用いて自動実行

### 4-1. デプロイ用パッケージの準備

AWS Lambdaでスクリプトを実行するために、一つのディレクトリにスクリプト群をまとめる必要があります。
また、spotipy等の依存パッケージ等も、同ディレクトリに含める必要があります。

AWS LambdaでPythonスクリプトをデプロイする方法については、[こちら](https://qiita.com/takuma-1234/items/3f23af1994acfb1c0d00)の記事を参考にさせていただきました。

主にデプロイする方法は、以下3つがあり、ここでは、パッケージ容量の観点からzipデプロイする方法を採用します。

1. Lambda レイヤーを使用する方法。
2. zip デブロイを用いる方法。
3. コンテナイメージデブロイを用いる方法。

#### 4-1-1. Lambdaへアップロードするためのディレクトリを用意

はじめに、任意の名前でディレクトリを作成し、作成したディレクトリへ移動します。

```bash
mkdir zip_lambda_deploy
cd zip_lambda_deploy
```

#### 4-1-2. 外部ライブラリの準備

zipデプロイする場合、外部ライブラリも合わせてzip化する必要があります。そのため、`packages/`というディレクトリを作成し、そこへ外部ライブラリをコピーします。

はじめに、必要な外部ライブラリのリストを示した`requirements.txt`作成します。以下をコピペして保存してください。
ここで、`pip freeze > requirements.txt`とせずに、以下のライブラリのみコピペしている理由は、zipをLambdaへアップロードする際に、圧縮済みの容量が50MB以下、展開後の容量が250MB以下という制約を満たすためです。

```text
async-timeout==4.0.3
certifi==2024.2.2
charset-normalizer==3.3.2
colorlog==6.8.2
idna==3.6
pillow==10.3.0
python-dotenv==1.0.1
PyYAML==6.0.1
redis==5.0.3
requests==2.31.0
six==1.16.0
spotipy==2.23.0
urllib3==2.2.1
```

次に、`packages/`というディレクトリを作成し、そこへ`requirements.txt`に記載された外部ライブラリをインストールします。

```bash
mkdir packages
pip install --target ./packages -r requirements.txt
```

#### 4-1-3. 設定ファイル(.yaml)の準備 & カバー画像の準備

次に、3-2節で説明したYAMLファイルを作成し、`config.yaml`という名前で保存します。

また、プレイリストのカバー画像を用意し、`cover_imgs/`ディレクトリを作成し、その直下に格納します。

#### 4-1-4. メインスクリプトの準備

次に、先ほど示した`create_playlist_based_on_user_input.py`を一部改変し、`lambda_function.py`というファイル名で保存します。

ファイル名は、AWS Lambdaへスクリプトを登録する際に変更可能ですが、`lambda_function.py`の方が、後で変更する手間がなくて済みます。

改変後のコードは以下の通りです。

```python
import os
import sys
from datetime import date
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), "./packages"))

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

REPO_ROOT = Path(__file__).parents[0]
load_dotenv(REPO_ROOT / ".env")

from music_analysis.utils import log

log.REPO_ROOT = REPO_ROOT

from music_analysis.preprocess.playlist import PlaylistCreator
from music_analysis.preprocess.recommend import TrackRecommender
from music_analysis.utils.config import Config


def main(
    cfg_path: str = Path(__file__).parents[0] / "config.yaml",
):
    today = date.today().strftime("%Y%m%d")
    cfg = Config(Path(cfg_path))
    print(cfg)

    # spotipy clientの作成
    scope = "playlist-modify-public,playlist-modify-private,ugc-image-upload"
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            open_browser=True,
        )
    )

    # レコメンドを取得
    track_recommender = TrackRecommender(sp=sp)
    track_ids = track_recommender.get_recommended_track_ids(
        seed_artists=cfg.seed_artists,
        seed_tracks=cfg.seed_tracks,
        seed_genres=cfg.seed_genres,
        limit=cfg.limit,
        country=cfg.country,
        **cfg.audio_features,
    )

    # プレイリストを作成しトラックを追加
    playlist_creator = PlaylistCreator(
        sp=sp,
        user_id=sp.me()["id"],
        name=f"{cfg.name} #{today}",
        cover_image_path=cfg.cover_image_path,
        public=cfg.public,
        collaborative=cfg.collaborative,
        description=cfg.description,
    )
    playlist_creator.add_tracks(track_ids=track_ids)
    playlist_creator.upload_cover_image_from_local()


def lambda_handler(event, context):
    main()


if __name__ == "__main__":
    main()
```


#### 4-1-5. テスト実行 & `.cache`の作成

次に、ローカル環境でスクリプトが正しく動作するか確認を行います。

これにより、ディレクトリ内に`.cache`というファイルが自動作成されます。このファイルは、spotipyにより実行時に作成されるファイルで、アクセストークン等の情報が記録されています。**この`.cache`がないとLambdaで実行時にエラーとなる**ので、必ず実行して生成するようにしてください。（筆者が調べた限りでは解決法が見当たらず、場当たり的なやり方なので、ご存知の方いらっしゃいましたら教えていただけますと幸いです。）

```bash
python lambda_function.py
```


#### 4-1-6. Zip圧縮

最後に、ディレクトリ内のファイル、ディレクトリ群一式をzip圧縮します。
この際、**`zip-deploy/`をディレクトリごと圧縮するのではなく、`zip-deploy/`内のファイル、ディレクトリ群を圧縮する必要がある**ことにご注意ください。

```bash
zip -r ../zip-deploy/ .
```

圧縮前のディレクトリ構成は以下の通りです。

```text
.
├── config.yaml           # プレイリスト作成のための設定ファイル
├── cover_imgs/           # プレイリストのカバー画像を格納するディレクトリ
├── lambda_function.py    # Lambdaを動かす際のメインスクリプト
├── music_analysis/       # 自作パッケージ
├── packages/             # 外部ライブラリ
├── requirements.txt      # 必要な外部ライブラリを記述したファイル
├── .cache                # spotipyにより実行時に作成されるファイル
└── .env                  # 環境変数を保持したファイル
```

### 4-2. AWS Lambdaの設定

[こちら](https://qiita.com/takuma-1234/items/3f23af1994acfb1c0d00)の記事を参考にさせていただきました。
記載いただいている手順で筆者環境では問題なく動作しました。

S3経由でzipファイルをアップロードし、読み込みます。Pythonバージョンは3.10に設定してください。

一点、補足させていただくとセッション時間がデフォルトでは3sになっているので、これを30s程度に変更しておいてください。
(プロセスの開始から終了まで10s程度要するため。)

### 4-3. 定期実行

AWS Lambda を定期実行するためには、トリガーが必要となります。
Amazon EventBridge を使用することで、トリガーイベントのルールを作成することができます。

[こちら](https://www.benjamin.co.jp/blog/technologies/lambda-2-eventbridge/)の記事を参考にさせていただきました。



## 5. まとめと今後

- まとめ
  - Spotipy と AWS Lambda を使用して、Spotifyのプレイリスト作成を自動化する方法を紹介しました。

  - 自作パッケージをAWS Lambdaでデプロイするために、アドホックにディレクトリ構造や工夫をしないといけないので、その手順を説明しました。

- 今後

  - 今回は、楽曲推薦にはSpotifyが提供しているAPIを活用しただけなので、推薦アルゴリズムを自作してみたいです。特に、MP3形式で30s程度の音源を取得できるようなので、特徴量作成からやってみたいです。

  - 設定ファイルを少しいじるだけで、狙ったBPMでトラックをフィルタリングしてプレイリストを作成するということもできるので、例えば、自分好みかつランニングに適したプレイリストを作成することもできそうです。


最後まで、お読みいただきありがとうございました。

## 6. 参考文献

- 公式ドキュメント
  - [Spotipy](https://spotipy.readthedocs.io/en/)
  - [Spotipyの実装例](https://github.com/spotipy-dev/spotipy/tree/2.22.1/examples)
  - [Spotify Web API](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)
- Spotipy、Spotify Web APIについて参考にさせていただいた技術記事
  - [Python用 Spotify Web API "spotipy" の楽曲・アーティストを検索（インストール方法，サンプルコード，API仕様）](https://www.wizard-notes.com/entry/python/spotipy)
  - [【Python】Spotify Web APIで楽曲データを分析してみる](https://note.com/bunsekiya_tech/n/n2e3151a6b8fa)
- AWS Lambda
  - [【AWS】AWS Lambdaで外部モジュール（ライブラリ）を含むPythonをzipデブロイする方法](https://qiita.com/takuma-1234/items/3f23af1994acfb1c0d00)
  -  [AWS Lambdaで遊ぼう #2 Lambda関数を定期実行する](https://www.benjamin.co.jp/blog/technologies/lambda-2-eventbridge/)
