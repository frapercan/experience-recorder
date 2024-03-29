import os
import shutil
import time
from unittest.mock import patch, MagicMock
from multiprocessing import Process
from PIL import Image

from experience_recorder.configuration.configuration import Configuration
from experience_recorder.recorder.recorder import Recorder
from tests.hci_interaction_processes import click_proccess, keypress_proccess
from tests.test_configuration import load_configuration


@patch('paddleocr.PaddleOCR.__new__')
@patch('pyautogui.screenshot')
def test_recorder(screenshot, ocr):
    global_configuration = load_configuration()
    task_configuration = Configuration(global_configuration)

    dataset_dir = os.path.join(global_configuration['datasets_dir'],
                               str(global_configuration['task']))
    if os.path.exists(dataset_dir):
        shutil.rmtree(dataset_dir, ignore_errors=True)

    buffer_dir = global_configuration['buffer_dir']
    if os.path.exists(buffer_dir):
        shutil.rmtree(buffer_dir)

    recorder = Recorder(global_configuration, task_configuration.conf)

    screenshot.return_value = Image.open(r"./tests/mock_data/mock_read.png")
    ocr.return_value = MagicMock()
    ocr.return_value.ocr.return_value = [[[[[19.0, 3.0], [70.0, 3.0], [70.0, 27.0], [19.0, 27.0]], ('276', 0.9999577403068542)]]]

    recorder.empty_buffer()
    recorder.start_senses()

    clickp = Process(target=click_proccess, args=([200, 400], 10, 1,))
    keyboardp = Process(target=keypress_proccess, args=["KP_Enter", 10, 2])
    exitp = Process(target=keypress_proccess, args=["BackSpace", 10, 5])

    clickp.start()
    keyboardp.start()
    exitp.start()

    recorder.start()

    time.sleep(5)

    recorder.empty_buffer()
