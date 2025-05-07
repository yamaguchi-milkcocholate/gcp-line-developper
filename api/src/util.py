from pathlib import Path

from linebot.v3.messaging import ApiClient, MessagingApiBlob


class TmpImageDownLoader:
    def __init__(self, api_client: ApiClient, content_id: str, tmp_dir: Path) -> None:
        self.api_client = api_client
        self.content_id = content_id
        self.tmp_path = tmp_dir / f"{content_id}.jpg"

    def __enter__(self) -> "TmpImageDownLoader":
        print("前処理")
        api_instance = MessagingApiBlob(self.api_client)
        api_response = api_instance.get_message_content(self.content_id)
        with open(self.tmp_path, "wb") as f:
            f.write(api_response)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        print("後処理")
        self.tmp_path.unlink(missing_ok=True)
