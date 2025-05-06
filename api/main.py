import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ImageMessage,
    ReplyMessageRequest,
)
from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks import ImageMessageContent
from src.util import TmpImageDownLoader

root_dir = Path(__file__).resolve().parent
tmp_dir = root_dir / "tmp"
tmp_dir.mkdir(exist_ok=True, parents=True)

load_dotenv(root_dir / ".env")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

configuration = Configuration(access_token=channel_access_token)

app = FastAPI()
async_api_client = AsyncApiClient(configuration)
sync_api_client = ApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(channel_secret)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/callback")
async def handle_callback(request: Request):
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if isinstance(event.message, ImageMessageContent):
            image_content_id = event.message.id
            print(image_content_id)

            with TmpImageDownLoader(
                api_client=sync_api_client, content_id=image_content_id, tmp_dir=tmp_dir
            ) as tmp_dl:
                print(tmp_dl.tmp_path, tmp_dl.tmp_path.exists())

                await line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[
                            ImageMessage(
                                original_content_url="https://i.gzn.jp/img/2018/01/15/google-gorilla-ban/00.jpg",
                                preview_image_url="https://i.gzn.jp/img/2018/01/15/google-gorilla-ban/00.jpg",
                            )
                        ],
                    )
                )

    return "OK"
