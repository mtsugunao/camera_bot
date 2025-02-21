from flask import Flask, request, send_from_directory
from line_handler import LineMessageHandler
from camera_controller import CameraController
from config import Config
import os
from logger import logger
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)
camera_controller = CameraController()
line_handler = LineMessageHandler(camera_controller)

processed_tokens = set()

@app.route("/")
def index():
    logger.info("Accessed index page")
    return "Pet Camera Server Running"

@app.route("/callback", methods=['POST'])
def webhook():
    try:
        signature = request.headers.get('X-Line-Signature')
        body = request.get_data(as_text=True)
        logger.info(f"Received webhook with signature: {signature}")

        if not signature:
            logger.error("Missing signature", 400)
            return "Missing signature", 400
        logger.info(f"Request body: {body}")

        events = request.json.get('events', [])
        if not events:
            logger.error("No events found in the request")
            logger.info(f"Request JSON: {request.json}")
            return 'No events', 400

        reply_token = events[0]['replyToken']

        if reply_token in processed_tokens:
            logger.info("Duplicate request detected, ignoring...")
            return 'OK', 200

        processed_tokens.add(reply_token)

        line_handler.handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signarture error")
        return 'Invalid signature', 400
    except Exception as e:
        logger.error(f"Error handling webhook: {str(e)}", exc_info=True)
        return "Internal server error", 500


    logger.info("Webhook processed successfully")
    return 'OK', 200

@app.route("/images/<path:fliename>")
def serve_image(filename):
    return send_from_directory(Config.IMAGE_SAVE_PATH, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.FLASK_PORT)
