import os
from datetime import datetime
import audiomath as am


class Audio():
    """
    WIP

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
        time_start = str(datetime.now().timestamp()).replace(".", "").ljust(18,'0')

        audio_dir = os.path.join(self.global_conf['raw_datasets_dir'], str(self.global_conf['task']),
                                 self.recorder_starting_time, self.sense)
        os.makedirs(audio_dir, exist_ok=True)

        am.Record(3, loop=True,
                  filename=os.path.join(audio_dir, f'{time_start}.mp3'),
                  device=am.FindDevice(mode='oo'))
