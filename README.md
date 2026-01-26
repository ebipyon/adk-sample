# Audio Transcription Agent

このアプリケーションは、Google Cloud Speech-to-Text API を Streamlit で使用するサンプルアプリケーションです。ユーザーがアップロードした音声ファイルを適切な形式に変換し、文字起こし結果を表示します。

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
    このコマンドを実行するとブラウザが開き、ログインを求められます。認証が完了すると、認証用JSONファイルがローカルマシン（通常は `~/.config/gcloud/application_default_credentials.json`）に保存されます。

4.  **クォータプロジェクトの設定**（プロンプトが表示された場合や、クォータエラーが発生した場合）:
    ```bash
    gcloud auth application-default set-quota-project <YOUR_PROJECT_ID>
    ```

### 2. Docker の設定

`docker-compose.yml` は、ローカルの gcloud 認証情報をコンテナ内にマウントするように設定されています。

`docker-compose.yml` の9行目が、あなたの ADC ファイルのパスを正しく指していることを確認してください（デフォルト設定では標準的なパスを使用しています）:

```yaml
    volumes:
      - ${HOME}/.config/gcloud/application_default_credentials.json:/app/credentials/key.json
```

## アプリケーションの実行

1.  **コンテナのビルドと起動**:
    ```bash
    docker compose up --build
    ```

2.  **アプリケーションへのアクセス**:
    ブラウザで [http://localhost:8501](http://localhost:8501) にアクセスしてください。

## 使い方

1.  **"Browse files"** をクリックして音声ファイルをアップロードします（対応フォーマット: wav, mp3, m4a, ogg）。
2.  **"Transcribe"** ボタンをクリックします。
3.  アプリケーションは以下の処理を行います:
    - 音声を Google Cloud STT で必要な形式（Linear16, 16kHz, モノラル）に変換します。
    - 音声データを Speech-to-Text API に送信します。
    - 文字起こしされたテキストを画面下部のテキストエリアに表示します。

## トラブルシューティング

- **`403 Cloud Speech-to-Text API has not been used...`**:
    - Google Cloud Console で API が有効になっているか確認してください。
    - 有効化してから変更が反映されるまで数分かかる場合があります。
- **`File /app/credentials/key.json was not found`**:
    - `gcloud auth application-default login` を実行したか確認してください。
    - `docker-compose.yml` のボリュームマウント設定が、実際の認証ファイルの場所と一致しているか確認してください。
