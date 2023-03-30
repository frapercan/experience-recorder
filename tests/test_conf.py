from multiprocessing import Process
from unittest.mock import patch

from experience_recorder.configuration.configuration import Configuration
import yaml
import os

import multiprocessing


def new_global_configuration():
    with open("tests/conf/global.yaml", 'r', encoding='utf-8') as global_configuration:
        global_configuration = yaml.safe_load(global_configuration)
        return global_configuration

@patch('builtins.input')
def test_create_configuration(inputs):
    global_configuration = new_global_configuration()
    inputs.side_effect = ['1', '1', '1', "test_task",'1','1']

    def example_function():
        import pyautogui
        while True:
            pyautogui.click(100, 100)

    new_process = Process(target=example_function)
    new_process.start()


    task_configuration = Configuration(global_configuration)
    task_configuration.save_configuration()
    print(task_configuration)

