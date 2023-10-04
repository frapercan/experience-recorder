import itertools
import os
import time
from datetime import datetime

import pyautogui
import mss.tools


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

        monitor = {
            "top": location[1],
            "left": location[0],
            "width": location[2],
            "height": location[3]
        }

        with mss.mss() as sct:
            for _ in itertools.count():
                time.sleep(self.global_conf['computer_delay'])
                ts = str(datetime.now().timestamp()).replace(".", "").ljust(18, '0')
                sct_img = sct.grab(monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=os.path.join(samples_dir, f"{str(ts)}.png"))
