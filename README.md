# Audio Transcription Agent

このアプリケーションは、Google Cloud Speech-to-Text API と **Local OpenAI Whisper** を使用して音声の書き起こしを行い、結果を比較（Diff表示）できるサンプルアプリケーションです。

## 特長

*   **Dual Transcription**: Google Cloud STT と Local Whisper の両方で同時に書き起こしを実行します。
*   **Diff Analysis**: 2つの書き起こし結果の差分を視覚的に表示し、精度の比較が容易です。
*   **Local Whisper**: ローカル環境（Dockerコンテナ内）で Whisper モデルを動作させます。モデルサイズ（tiny, base, small, medium, large）を選択可能です。

## 前提条件

- **Docker** および **Docker Compose** がインストールされていること。
- 課金が有効になっている **Google Cloud Platform (GCP) プロジェクト** があること。
- **Google Cloud SDK (`gcloud` CLI)** がインストールされ、設定されていること。

## セットアップ手順

### 1. Google Cloud の設定

1.  **Google Cloud プロジェクトの作成または選択**を行います。
2.  プロジェクトで **Speech-to-Text API を有効化**します:
    [Speech-to-Text API を有効にする](https://console.cloud.google.com/apis/library/speech.googleapis.com)
3.  **ローカル認証**を行い、Application Default Credentials (ADC) を作成します:
    ```bash
    gcloud auth application-default login
    ```
4.  **クォータプロジェクトの設定**（必要な場合）:
    ```bash
    gcloud auth application-default set-quota-project <YOUR_PROJECT_ID>
    ```

### 2. Docker の設定

`docker-compose.yml` でローカルの gcloud 認証情報をマウントしています。
パスが正しいか確認してください: `volumes: - ${HOME}/.config/gcloud/application_default_credentials.json:/app/credentials/key.json`

## アプリケーションの実行

1.  **コンテナのビルドと起動**:
    WhisperやPyTorchなどのライブラリをインストールするため、初回ビルドには時間がかかります。
    ```bash
    docker compose up --build
    ```

2.  **アプリケーションへのアクセス**:
    ブラウザで [http://localhost:8501](http://localhost:8501) にアクセスしてください。

## 使い方

1.  **"Browse files"** で音声ファイルをアップロードします。
2.  **"Whisper Model Size"** で Whisper のモデルサイズを選択します（デフォルト: small）。
    *   大きなモデルほど精度は高いですが、処理時間が長くなります（CPU実行のため）。
3.  **"Transcribe"** ボタンをクリックします。
4.  以下の順で処理が行われます:
    *   Google Cloud STT で書き起こし
    *   Local Whisper で書き起こし
    *   **Results Comparison**: 両方の結果を左右に並べて表示
    *   **Diff Analysis**: 差異をハイライト表示

## トラブルシューティング

- **Dockerのメモリ不足**: WhisperのLargeモデルを使用する場合、Dockerに割り当てられたメモリが不足するとクラッシュする可能性があります。Docker Desktopの設定でメモリ割り当てを増やしてください。
- **処理が遅い**: ローカルでのWhisper実行はCPUに依存するため、長い音声データの処理には時間がかかります。

---
**Note**: `credentials/` ディレクトリは gitignore されています。
