from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from config import Config
import os
from logger import logger

class LineMessageHandler:
    def __init__(self, camera_controller):
        self.line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)
        self.camera_controller = camera_controller
        self.handler.add(MessageEvent, message=TextMessage)(self.handle_message)

    def handle_message(self, event):
        text = event.message.text.lower()
        logger.info(f"Received message: {text}")

        if text == 'start':
            if self.camera_controller.start_camera():
                self._send_reply(event, 'camera activated!')
                logger.info("Camera started successfully")
            else:
                self._send_reply(event, 'camera already activated!')
                logger.warning("Camera start requested, but it was already running")
        elif text == 'stop':
            if self.camera_controller.stop_camera():
                self._send_reply(event, 'camera terminated.')
                logger.info("Camera stopped successfully")
            else:
                self._send_reply(event, 'camera already terminated.')
                logger.warning("Camera stop requested, but it was already stopped")
        elif text == 'photo':
            logger.info("Photo request received")
            self._send_photo(event)
        else:
            logger.warning(f"Unkown command received: {text}")
            return "I do not understand you"

    def _send_reply(self, event, message):
        logger.info(f"Sending reply: {message}")
        self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )

    def _send_photo(self, event):
        image_path = self.camera_controller.get_latest_image_path()
        if image_path and os.path.exists(image_path):
            image_filename = os.path.exists(image_path)
            public_url = f"{Config.NGROK_URL}/images/{image_filename}"

            logger.info(f"Sending image: {public_url}")
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
            logger.error("Failed to send photo: No image found")
            self._send_reply(event, 'Either camera not activated or failed to save a photo')
