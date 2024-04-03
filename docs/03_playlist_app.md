# 【Python】Spotifyのプレイリスト作成をAWS Lambdaで自動化する

## TL;DR

この記事では、PythonからSpotify Web APIを操作できるライブラリである**Spotipy**を使用して、プレイリスト作成を自動化する方法を紹介します。スクリプトの自動実行にはAWS Lambdaを使用します。

プレイリストに入れるトラックの選定は、Spotify Web APIで提供されているレコメンド機能に基づき行っている(=使用するのみ)ので、推薦アルゴリズムの実装や工夫は特にありません。

自分の音楽好みに合わせたプレイリストを効率的に作成したい方や、SpotifyのAPIを使ったプロジェクトに興味がある方の一助となれば幸いです。

使用ツール、サービスは、以下の通りです。

- Python
- Python依存パッケージ (pandasなど)
- Spotify Web API (APIキーの発行に必要)
- Spotipy
- AWS Lambda、その他AWSのサービス (無料枠で対応できる範囲だと思います)


## 1. はじめに

まず、本機能を実装しようと思った経緯ですが、作業の気晴らし時間などで、私は作業用BGMをよく活用しています。
その作業用BGMも多くの方によって、YoutubeやSpotifyにまとめられおり、これまでそれを利用していました。そうしてまとめてくださった音楽を聴いている中で、だんだんと自分の好みのアーティストや曲調などが自分なりに分かってきて、自分の好みの曲を中心に収集したいと思ったのが、本機能を実装しようと思ったきっかけです。

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

### 1-2. 大まかな流れ

1. 環境構築

2. レコメンド取得〜プレイリスト作成を行うスクリプトを実装
   1. レコメンドを取得するためのSeedとなるアーティストやトラック等をYAMLファイルへ記述
   2. 2-1で設定したSeedに基づき、Spotify Web APIにより推薦されたトラックのIDを取得
   3. プレイリストを新規作成し、2-2で取得したトラックを追加

3. 作成したスクリプトをAWS Lambdaを用いて自動実行

### 1-3. ゴール

- AWS Lambdaで自分好みのプレイリスト作成を自動化


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


### 3-1. 環境変数の設定
2-1節で取得したAPIキーを環境変数に設定していきます。

環境変数を`export`コマンド等で設定していただいても良いですが、筆者環境では、[python-dotenv](https://pypi.org/project/python-dotenv/)というライブラリを使用して環境変数をスクリプトの冒頭で読み込みます。

`python-dotenv`を使用するには、リポジトリルート(`music_analysis/`)に、`.env`というファイルを作成し、そこへ環境変数を記入します。
[こちら](https://github.com/aug7atsushi/music_analysis/blob/main/sample.env)にサンプルを用意していますので、クライアントID、クライアントシークレット、リダイレクトURIの3つを設定してください。

### 3-2. プレイリスト作成のためのYAMLファイルを作成

YAMLファイルを作成し、以下の項目を記述します。
YAMLファイルの例については、[`configs/`](https://github.com/aug7atsushi/music_analysis/tree/main/configs)以下に格納してありますので、参考にしてください。

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

ここまで、スクリプト(`create_playlist_based_on_user_input.py`)を実行する手順についてのみ説明してきました。
この節では、スクリプトの処理内容に関して説明したいと思います。


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



### 4. つまづいたポイント
- zipの圧縮には注意する必要がある
- `.cache`を含める必要がある

## 5. まとめと残課題
- 本記事の要点のまとめ
- Spotify Web APIを使った開発の今後の可能性

## 9. 参考文献
- 公式ドキュメント
  - [Spotipy](https://spotipy.readthedocs.io/en/)
  - [Spotipyの実装例](https://github.com/spotipy-dev/spotipy/tree/2.22.1/examples)
  - [Spotify Web API](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)
- Spotipy、Spotify Web APIについて参考にさせていただいた技術記事
  - https://www.wizard-notes.com/entry/python/spotipy
  - https://note.com/bunsekiya_tech/n/n2e3151a6b8fa
