import yaml
import os
from multiprocessing import Process
from unittest.mock import patch

from tests.hci_interaction_processes import click_proccess

from experience_recorder.configuration.configuration import Configuration
import Xlib.threaded


# Filesystem auxiliar functions
def delete_task_configuration(global_configuration,):
    task_configuration_filedir = os.path.join(global_configuration['tasks_configuration_dir'],
                                              global_configuration['task'] + '.yaml')

    if os.path.exists(task_configuration_filedir):
        os.remove(task_configuration_filedir)


def load_configuration():
    with open("tests/conf/global.yaml", 'r', encoding='utf-8') as global_configuration:
        global_configuration = yaml.safe_load(global_configuration)
        return global_configuration


@patch('builtins.input')
def test_fail_at_configuration(inputs):
    # Load the global configuration file
    global_configuration = load_configuration()

    # Remove any existing task configuration
    delete_task_configuration(global_configuration)

    # Simulate wrong user inputs during configuration
    inputs.side_effect = ['dfg', '1', 'dgf', '1', 'sdfg', '3', "test_sense_1", '1', '1', "test_sense_2", "dfg", "2",
                          "2",
                          "test_sense_3", "dfg", "2", "sfg", "2"]

    # Start a new process to simulate clicking on arbitrary coordinates
    clickp = Process(target=click_proccess, args=([200, 400], 100000, 0.01,))

    clickp.start()

    task_configuration = Configuration(global_configuration)
    task_configuration.save_configuration()

    delete_task_configuration(global_configuration)

    # Simulate correct user input for a testing use case

    inputs.side_effect = ['1', '1', '2', "test_sense_1", '1', '1', "test_sense_2", "1", "2"]
    task_configuration = Configuration(global_configuration)
    task_configuration.save_configuration()

    # Stop the process for clicking on coordinates
    clickp.terminate()




