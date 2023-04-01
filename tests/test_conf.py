import time
from multiprocessing import Process
from unittest.mock import patch

from pynput.keyboard import Key

from experience_recorder.configuration.configuration import Configuration
import yaml
import os

import multiprocessing
import os

from experience_recorder.recorder.recorder import Recorder


def click_proccess():
    import pyautogui
    while True:
        time.sleep(1)
        pyautogui.click(400, 100)

def keypress_proccess():
    import pyautogui
    while True:
        time.sleep(1)
        pyautogui.keyUp('a')

def keypress_exit_proccess():
    import pyautogui
    while True:
        pyautogui.keyUp(Key.backspace)
        time.sleep()



def delete_task_configuration(global_configuration):
    task_configuration_filedir = os.path.join(global_configuration['tasks_configuration_dir'],
                                              global_configuration['task'] + '.yaml')

    if os.path.exists(task_configuration_filedir):
        os.remove(task_configuration_filedir)


def new_global_configuration():
    with open("tests/conf/global.yaml", 'r', encoding='utf-8') as global_configuration:
        global_configuration = yaml.safe_load(global_configuration)
        return global_configuration


@patch('builtins.input')
def test_create_succesful_configuration(inputs):
    global_configuration = new_global_configuration()
    delete_task_configuration(global_configuration)
    inputs.side_effect = ['1', '1', '2', "test_sense_1", '1', '1', "test_sense_2", "1", "2"]

    new_process = Process(target=click_proccess)
    new_process.start()

    task_configuration = Configuration(global_configuration)
    task_configuration.save_configuration()
    new_process.kill()


@patch('builtins.input')
def test_fail_at_configuration(inputs):
    global_configuration = new_global_configuration()
    delete_task_configuration(global_configuration)
    inputs.side_effect = ['dfg', '1', 'dgf', '1', 'sdfg', '3', "test_sense_1", '1', '1', "test_sense_2", "dfg", "2",
                          "2",
                          "test_sense_3", "dfg", "2", "sfg", "2"]

    new_process = Process(target= click_proccess)
    new_process.start()

    task_configuration = Configuration(global_configuration)
    task_configuration.save_configuration()
    new_process.kill()


def test_load_configuration():
    global_configuration = new_global_configuration()

    task_configuration = Configuration(global_configuration)
    task_configuration.save_configuration()

    assert global_configuration['task'] == task_configuration.conf['task']


def test_recorder():
    global_configuration = new_global_configuration()
    task_configuration = Configuration(global_configuration)
    recorder = Recorder(global_configuration, task_configuration.conf)
    recorder.empty_buffer()
    recorder.start_senses()
    recorder.start()
    click_process = Process(target=click_proccess)
    keyboard_process = Process(target=click_proccess)
    exit_process = Process(target=click_proccess)
    click_process.start()
    keyboard_process.start()
    exit_process.start()
