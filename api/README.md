# LINE ボットバックエンド API

# 開発手順

- API を起動

```shell
uv run uvicorn main:app --reload
```

- ngrok で API を公開

```shell
ngrok http 8000
```

- LINE Webhook URL に登録
  - Messaging API > Webhook URL から設定

## Docker コンテナで開発する場合

```shell
# ビルド
docker compose build
# 起動
docker compose up
# 削除
docker rm api
```

# デプロイ

- 依存関係を更新

```shell
cd api
uv pip freeze > requirements.txt
```

# メモ

- Python SDK
  - https://github.com/line/line-bot-sdk-python
- fast api
  - https://fastapi.tiangolo.com/
- Messaging API
  - コンテンツ
    - 画像などはメッセージ ID からコンテンツを取得
    - rest api: https://developers.line.biz/ja/reference/messaging-api/#get-content
    - python sdk: https://github.com/line/line-bot-sdk-python/blob/master/linebot/v3/messaging/docs/MessagingApiBlob.md#get_message_content
