from flask import Flask, request, send_from_directory
from line_handler import LineMessageHandler
from camera_controller import CameraController
from config import Config
import os

app = Flask(__name__)
camera_controller = CameraController()
line_handler = LineMessageHandler(camera_controller)

@app.route("/")
def index():
    return "Pet Camera Server Running"

@app.route("/callback", methods=['POST'])
def webhook():

    signature = request.headers['X-Line-Signature']
    if not signature:
        return "Missing signature", 400
    body = request.get_data(as_text=True)

    try:
        line_handler.handler.handle(body, signature)
    except InvalidSignatureError:
        return 'Invalid signature', 400
    except Exception as e:
        print(f"Error handling webhook: {str(e)}")
        return "Internal server error", 500

    return 'OK', 200

@app.route("/images/<path:fliename>")
def serve_image(filename):
    return send_from_directory(Config.IMAGE_SAVE_PATH, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.FLASK_PORT)
