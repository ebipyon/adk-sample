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

### 2. 環境変数の設定

`.env.example` をコピーして `.env` ファイルを作成し、必要な環境変数を設定します:

```bash
cp .env.example .env
```

`.env` ファイルを編集して、以下の値を設定してください:

```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GCS_BUCKET_NAME=your-bucket-name
```

- `GOOGLE_CLOUD_PROJECT`: Google Cloud のプロジェクトID
- `GCS_BUCKET_NAME`: 長い音声ファイル用の一時ストレージとして使用するGCSバケット名

### 3. Docker の設定

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

## Cloud Run へのデプロイ

### 前提条件
- `gcloud` CLI がインストール・認証済みであること
- プロジェクトIDを設定済みであること

### デプロイ手順

```bash
# 1. 必要なAPIを有効化
gcloud services enable artifactregistry.googleapis.com run.googleapis.com speech.googleapis.com

# 2. サービスアカウントの作成
gcloud iam service-accounts create adk-transcription-sa --display-name="ADK Transcription SA"

# 3. 権限付与
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:adk-transcription-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/speech.client"

## アーキテクチャ構成 (Nginx + Streamlit)

Cloud Run での大きなファイルアップロード (32MB以上) と HTTP/2 通信をサポートするため、以下のような構成をとっています。

*   **Nginx (Port 8501)**:
    *   **役割**: エントリーポイント。Cloud Run からの **HTTP/2** リクエストを受け付けます。
    *   **理由**: Cloud Run の 32MB 制限を回避するには HTTP/2 が必須ですが、Streamlit はネイティブで HTTP/2 をサポートしていないため、Nginx が前段でこれを受け持ちます。
*   **Streamlit (Port 8502)**:
    *   **役割**: アプリケーションロジックとUI。Nginx から HTTP/1.1 で転送されたリクエストを処理します。
    *   **理由**: Whisper による書き起こし処理や画面描画に専念します。

**データの流れ**:
`[User] --(HTTP/2)--> [Cloud Run] --(HTTP/2)--> [Nginx] --(HTTP/1.1)--> [Streamlit]`

## セットアップ手順

### 1. Google Cloud の設定
(変更なし: 省略)

### 2. 環境変数の設定
(変更なし: 省略)

### 3. Google Cloud 認証キー (ローカル実行用)
ローカルで Docker を実行する場合、サービスアカウントキーが必要です。
1. GCP コンソールからサービスアカウントキー (JSON) をダウンロードします。
2. プロジェクトルートの `credentials/` ディレクトリに配置します。
   `credentials/key.json`

## アプリケーションの実行

1.  **コンテナのビルドと起動**:
    (初回はGPU対応のベースイメージをプルするため時間がかかります)
    ```bash
    docker compose up --build
    ```

2.  **アプリケーションへのアクセス**:
    [http://localhost:8501](http://localhost:8501)

## Cloud Run へのデプロイ (GPU有効化済み)

GPU (NVIDIA L4) を利用して Whisper を高速化するためのデプロイ用スクリプト `deploy.sh` を用意しています。

### 手順

1.  `deploy.sh` を実行します:
    ```bash
    ./deploy.sh
    ```
    (注意: 初回デプロイ時はイメージサイズが大きいため時間がかかります)

2.  デプロイ完了後、表示された URL にアクセスします。

### GPU の確認
書き起こし実行時、ログに `Using device: cuda` と表示されていれば GPU が使用されています。

---
**Note**: 手動でデプロイする場合は、`--use-http2` (32MB制限回避) と `--gpu 1` (GPU有効化) のフラグが必須です。詳細は `deploy.sh` を参照してください。
```

> **Note**: `YOUR_PROJECT_ID` と `YOUR_BUCKET_NAME` は実際の値に置き換えてください。

---
**Note**: `credentials/` ディレクトリは gitignore されています。

