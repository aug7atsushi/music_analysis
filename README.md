# music_analysis

楽曲分析のためのリポジトリ

## 開始する前に

Python3.10がインストールされていることを前提としています。インストールが完了した方は以下を実行してインストールされていることを確認してください。

また、本プロジェクトではパッケージ管理に、[poetry](https://python-poetry.org/docs/)を使用します。事前にインストールしてください。

## インストール方法

### 1. リポジトリのクローン

以下の手順に沿って、リポジトリをクローンします。

```bash
git clone https://github.com/aug7atsushi/music_analysis.git
cd music_analysis
poetry install
```


### 2. APIキーの取得

本プロジェクトでは、PythonからSpotify Web API を操作する Spotipy というライブラリを使用します。その際、 Spotify Web API のAPIキーを取得する必要がありますので、以下に沿って取得をお願いします。

[公式ドキュメント](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)や[以前私がSpotipyの利用方法についてまとめた記事](https://qiita.com/toxic_apple/items/20a0fce60e337bbe8716#2-%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E6%96%B9%E6%B3%95)をもとに、Spotify Web APIのクライアントID、クライアントシークレット、リダイレクトURIの3つを取得してください。リダイレクトURIは自分で任意に設定します。

### 3. 依存パッケージのインストール

```bash
poetry install
```



## 各機能説明

TBD

プロジェクトの使用方法や例をここに記述します。

```python
import yourpackage

yourpackage.do_something()
```
