import itertools
import os
import time
from datetime import datetime

import pyautogui


class Senses():
    """
    Class that contains the different possibilities of senses in the form of methods.
    At the moment only sight is contemplated.

    Parameters
    ----------
    tasks_configuration:  :class:`dict`
        Previously loaded .yaml file for tasks configuration.
    """

    def __init__(self, global_configuration, tasks_configuration):
        self.global_conf = global_configuration
        self.task_conf = tasks_configuration

    def see(self, sense):
        """
        Screenshot the desired location and buffering it for later consumption through skills.

        Parameters
        ----------
        sense:  :class:`str`
            name of the sense
        """
        location = self.task_conf[sense]['location']
        if not os.path.exists(self.global_conf['buffer_dir']):
            os.makedirs(self.global_conf['buffer_dir'])
        for _ in itertools.count():
            time.sleep(0.5)
            left = location['left']
            top = location['top']
            width = location['width']
            height = location['height']
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            ts = datetime.now().timestamp()
            screenshot.save(os.path.join(self.global_conf['buffer_dir'], f"{str(ts)}-{sense}.png"))

    def ear(self, sense):
        pass
