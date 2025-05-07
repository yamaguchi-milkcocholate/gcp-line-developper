import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ImageMessage,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks import ImageMessageContent
from src.gemini import GeminiException, LineDrawGenerationLifecycle
from src.opencv import cv_line_draw
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
app.mount("/images", StaticFiles(directory=str(tmp_dir)), name="tmp")
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

            reply_messages = []
            with TmpImageDownLoader(
                api_client=sync_api_client, content_id=image_content_id, tmp_dir=tmp_dir
            ) as tmp_dl:
                # 1.OpenCVの線画
                cv_line_draw(
                    from_filepath=tmp_dl.tmp_path,
                    to_filepath=tmp_dir / f"{image_content_id}_cv2.jpg",
                    num_dilate_iter=1,
                )
                reply_messages += [
                    TextMessage(text="✅ 画像1枚目の作成に成功しました"),
                    ImageMessage(
                        original_content_url=f"{request.base_url}images/{image_content_id}_cv2.jpg",
                        preview_image_url=f"{request.base_url}images/{image_content_id}_cv2.jpg",
                    ),
                ]
                # 2.Geminiの線画
                try:
                    LineDrawGenerationLifecycle(target_filepath=tmp_dl.tmp_path).run(
                        output_line_draw_filepath=tmp_dir
                        / f"{image_content_id}_gemini.jpg",
                        output_color_filepath=tmp_dir
                        / f"{image_content_id}_gemini_color.jpg",
                    )
                    reply_messages += [
                        TextMessage(text="✅ 画像2、3枚目の作成に成功しました"),
                        ImageMessage(
                            original_content_url=f"{request.base_url}images/{image_content_id}_gemini.jpg",
                            preview_image_url=f"{request.base_url}images/{image_content_id}_gemini.jpg",
                        ),
                        ImageMessage(
                            original_content_url=f"{request.base_url}images/{image_content_id}_gemini_color.jpg",
                            preview_image_url=f"{request.base_url}images/{image_content_id}_gemini_color.jpg",
                        ),
                    ]
                except GeminiException as e:
                    print(e)
                    reply_messages += [
                        TextMessage(
                            text="❌ 画像2,3枚目の生成に失敗しました。もう一度お試しください。"
                        ),
                    ]

            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token, messages=reply_messages
                )
            )
        else:
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="画像1枚を送信してください")],
                )
            )

    return "OK"
