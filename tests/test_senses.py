import os
import shutil
import time
from multiprocessing import active_children
from unittest.mock import patch

from PIL import Image

from experience_recorder.configuration.configuration import Configuration
from experience_recorder.senses.senses import Senses
from tests.test_configuration import load_configuration


@patch('itertools.count')
@patch('pyautogui.screenshot')
def test_sense(screenshot,count):
    global_configuration = load_configuration()
    task_configuration = Configuration(global_configuration)
    screenshot.return_value = Image.open(r"./tests/mock_data/mock_read.png")
    senses = Senses(global_configuration, task_configuration.conf['senses'])

    buffer_dir = global_configuration['buffer_dir']
    if os.path.exists(buffer_dir):
        shutil.rmtree(buffer_dir)

    count.return_value = range(5)
    senses.see('test_sense_1')
    senses.ear('test_sense_fake')


test_sense()