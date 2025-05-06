# gcp-line-developper

## メモ

- 認証について
  - LINE プラットフォームの IP は公開されていないため、API 内部処理で署名を認証する必要がある
    - https://developers.line.biz/ja/docs/messaging-api/development-guidelines/#prohibiting-ip-address-restrictions
  - cloud run で構築した API では IP アドレスとリクエストを限定しない
  - 逆に LINE プラットフォームにリクエストする IP は絞り込むことができる
    - https://developers.line.biz/ja/docs/messaging-api/building-bot/#configure-security-settings
