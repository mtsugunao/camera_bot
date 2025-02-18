import subprocess
import os
import signal
from datetime import datetime
from config import Config

class CameraController:
    def __init__(self):
        self.camera_process = None
        os.makedirs(Config.IMAGE_SAVE_PATH, exist_ok=True)

    def start_camera(self):
        if not self.camera_process:
            self.camera_process = subprocess.Popen(['python3', 'camera_script.py'])
            return True
        return False

    def stop_camera(self):
        if self.camera_process:
            os.kill(self.camera_process.pid, signal.SIGTERM)
            self.camera_process = None
            return True
        return False

    def is_running(self):
        return self.camera_process is not None

    def get_latest_image_path(self):
        if os.path.exists(Config.LATEST_IMAGE_PATH):
            return Config.LATEST_IMAGE_PATH
        return None
