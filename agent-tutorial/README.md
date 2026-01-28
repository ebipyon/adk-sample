# Agent Tutorial

Google ADK (Agent Development Kit) を使用したシンプルなエージェントのサンプルプロジェクトです。
ユーザーの質問に応じて、指定された都市の天気や現在時刻を回答する機能を持っています。

## 前提条件

- Python 3.10 以上
- Google Cloud プロジェクト (Gemini API が有効になっていること)
- Google Cloud API Key

## セットアップ

1. **ディレクトリへの移動**

   ```bash
   cd agent-tutorial
   ```

2. **仮想環境の作成と有効化**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **依存パッケージのインストール**

   ```bash
   pip install -r requirements.txt
   ```

4. **環境変数の設定**

   プロジェクトルートに `.env` ファイルを作成し、`GOOGLE_API_KEY` を設定してください。

   ```bash
   echo 'GOOGLE_API_KEY="your-api-key-here"' > .env
   ```

   ※ `.gitignore` により `.env` はコミットされません。

## エージェントの構成

このプロジェクトのエージェントは `my_agent/agent.py` で定義されています。

- **名前**: `weather_time_agent`
- **モデル**: `gemini-2.5-flash`
- **主な機能**:
    - `get_weather(city: str)`: 指定された都市の天気情報を返します。（サンプル実装: "New York" のみ対応）
    - `get_current_time(city: str)`: 指定された都市の現在時刻を返します。（サンプル実装: "New York" のみ対応）

## 使用方法

本エージェントは Python コード内でインポートして使用することを想定しています。

```python
import os
from my_agent.agent import root_agent

# 注意: 実際にエージェントを実行するには、ADKのランタイムや適切な呼び出しコードが必要です。
# ここではエージェント定義のロード確認のみを行えます。
print(f"Agent Name: {root_agent.name}")
print(f"Description: {root_agent.description}")
```