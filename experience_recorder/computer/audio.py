import os
from datetime import datetime
import audiomath as am

class Audio:
    """
    This class is responsible for capturing audio data.

    The purpose is to record audio for a specified duration and store the captured audio in an appropriate directory
    for further processing or analysis.

    Attributes:
    - global_conf: Contains global configurations used throughout the system.
    - task_conf: Contains configurations specific to a task.
    - sense: Represents the type of sense, in this context, it's audio.
    - recorder_starting_time: The time the recorder was started, useful for uniquely identifying sessions.
    """

    def __init__(self, global_configuration, tasks_configuration, sense, recorder_starting_time):
        """
        Initialize the Audio object with the necessary configurations.

        Parameters:
        - global_configuration: Dict containing global system configurations.
        - tasks_configuration: Dict containing task-specific configurations.
        - sense: The sense associated with this class, expected to be 'audio'.
        - recorder_starting_time: A unique timestamp indicating the start time of the recording session.
        """
        self.global_conf = global_configuration
        self.task_conf = tasks_configuration
        self.sense = sense
        self.recorder_starting_time = recorder_starting_time

    def start(self):
        """
        Record audio continuously, saving chunks in an MP3 format.

        This function captures audio in segments, where each segment is saved with a unique timestamp.
        The audiomath library is used to facilitate the audio recording process.

        Parameters:
        - sense: String indicating the type of sense. In this context, it's expected to be 'audio'.
        """
        # Generate a unique timestamp for this specific audio segment.
        time_start = str(datetime.now().timestamp()).replace(".", "").ljust(18, '0')

        # Define the directory where the audio files will be saved.
        audio_dir = os.path.join(self.global_conf['raw_datasets_dir'], str(self.global_conf['task']),
                                 self.recorder_starting_time, self.sense)

        # Ensure the directory exists or create it.
        os.makedirs(audio_dir, exist_ok=True)

        # Use the audiomath library to record audio.
        # The audio is captured in continuous 3-second segments (looped), saved as MP3 files.
        am.Record(3, loop=True,
                  filename=os.path.join(audio_dir, f'{time_start}.mp3'),
                  device=am.FindDevice(mode='oo'))
