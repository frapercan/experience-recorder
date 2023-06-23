import itertools
import os
import time
from datetime import datetime

import pyautogui


class Display():
    """
    Class that contains the different possibilities of senses in the form of methods.
    At the moment only sight is contemplated.

    Parameters
    ----------
    tasks_configuration:  :class:`dict`
        Previously loaded .yaml file for tasks configuration.
    """

    def __init__(self, global_configuration, tasks_configuration, sense, recorder_starting_time):
        self.global_conf = global_configuration
        self.task_conf = tasks_configuration
        self.sense = sense
        self.recorder_starting_time = recorder_starting_time

    def start(self):
        """
        Screenshot the desired location and buffering it for later consumption through skills.

        Parameters
        ----------
        sense:  :class:`str`
            name of the sense
        """
        location = self.task_conf[self.sense]['location']
        samples_dir = os.path.join(self.global_conf['raw_datasets_dir'], str(self.global_conf['task']),
                                   self.recorder_starting_time, self.sense, )

        os.makedirs(samples_dir, exist_ok=True)

        for _ in itertools.count():
            time.sleep(self.global_conf['computer_delay'])

            screenshot = pyautogui.screenshot(region=location)
            ts = str(datetime.now().timestamp()).replace(".", "").ljust(18,'0')
            screenshot.save(os.path.join(samples_dir, f"{str(ts)}.png"))
