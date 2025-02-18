from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from config import Config
import os

class LineMessageHandler:
    def __init__(self, camera_controller):
        self.line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)
        self.camera_controller = camera_controller

    def handler_message(self, event):
        text = event.message.text.lower()

        if text == 'start':
            if self.camera.controller.start_camera():
                self._senf_reply(event, 'camera activated!')
            else:
                self._send_reply(event, 'camera already activated!')
        elif text == 'stop':
            if self.camera_controller.stop_camera():
                self._send_reply(event, 'camera terminated.')
            else:
                self._send_reply(event, 'camera already terminated.')
        elif text == 'photo':
            self_.send_photo(event)
        else:
            return "I do not understand you"

    def _send_reply(self, event, message):
        self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )

    def _send_photo(self, event):
        image_path = self.camera_controller.get_latest_image_path()
        if image_path and os.path.exists(image_path):
            public_url = f"{Config.NGROK_URL}/latest_image.jpg"

            self.line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text='Chai desu!'),
                    ImageSendMessage(
                        original_content_url=public_url,
                        preview_image_url=public_url
                    )
                ]
            )
        else:
            self._send_reply(event, 'Either camera not activated or failed to save a photo')
