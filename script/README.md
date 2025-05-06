# LINE Messaging API のチャネルアクセストークン v2.1 の設定

チャネルアクセストークン v2.1 とは、任意の有効期限を設定できる認証機能。

c.f. 「長期のチャネルアクセストークン」

- https://developers.line.biz/ja/docs/basics/channel-access-token/#long-lived-channel-access-token
- チャネル設定 > Messaging API 設定 > チャネルアクセストークン(長期)から取得できる

## ドキュメント

- https://developers.line.biz/ja/docs/messaging-api/generate-json-web-token/#use-python

## 手順

- 鍵を作成

```shell
uv run python keygen.py
```

- 標準出力に秘密鍵と公開鍵が表示される

```shell
# 秘密鍵
{
  "alg": "RS256",
  "d": "zKh7iwIIPXXFKYQS...",
  "dp": "u1qKg_43UeuGpZFI...",
  "dq": "69AzYgpcg0ckypUrv...",
  "e": "AQ..",
  "kty": "RSA",
  "n": "_RzHf7cgG_i6Pdo_...",
  "p": "_20iRavoSrMIwWuRPxo...",
  "q": "_a5QodMBbEriAgztXvHi...",
  "qi": "JozdjTtK57IFLeVAB...",
  "use": "sig"
}
# 公開鍵
{
  "alg": "RS256",
  "e": "AQAB",
  "kty": "RSA",
  "n": "_RzHf7cgG_i6Pdo...",
  "use": "sig"
}
```

- 公開鍵を LINE Developer コンソールから登録して、kid を取得

- gettoken.py を実行して JWT トークンを取得
  - .env ファイルに KID と CHANNEL_ID を記載すること
  - チャンネルの基本設定から閲覧できる

```shell
uv run python keygen.py
```

- チャネルアクセストークン v2.1 を発行
  - エンドポイントにリクエストを送り、トークンを取得

```shell
JWT=eyJhbGciOi...

curl -v -X POST https://api.line.me/oauth2/v2.1/token \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=client_credentials' \
--data-urlencode 'client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer' \
--data-urlencode "client_assertion=${JWT}"
```

- レスポンス

```shell
{
  "access_token": "eyJhbGciOiJIUz.....",
  "token_type": "Bearer",
  "expires_in": 2592000,
  "key_id": "sDTO....."
}
```
