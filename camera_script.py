import cv2
import time
import os
from datetime import datetime
from config import Config
import signal
import sys

running = True

def handle_signal(signal_number, frame):
    global running
    running = False

signal.signal(signal.SIGTERM, handle_signal)

def main():
    camera = cv2.VideoCapture(0)
    os.makedirs(Config.IMAGE_SAVE_PATH, exist_ok=True)

    try:
        while True:
            ret, frame = camera.read()
            if ret:
                # here is something that you want to implement like save the pic or object detection
                cv2.imwrite('Config.LATEST_IMAGE_PATH', frame)
		timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
		archive_path = os.path.join(Config.IMAGE_SAVE_PATH, f'image_{timestamp}.jpg'
                cv2.imwrite(archive_path, frame)
 
            time.sleep(0.1)
    finally:
        camera.release()
        sys.exit(0)

if __name__ == '__main__':
    main()

