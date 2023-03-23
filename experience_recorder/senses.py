import os
import time
from datetime import datetime

import pyautogui


class Senses():
    def __init__(self, tasks_configuration):
        self.task_conf = tasks_configuration

    def see(self, sense):
        location = self.task_conf[sense]['location']
        while True:
            time.sleep(0.5)
            left = location['left']
            top = location['top']
            width = location['width']
            height = location['height']

            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            ts = datetime.now().timestamp()
            screenshot.save(os.path.join("./__buffer__", f"{str(ts)}-{sense}.png"))
