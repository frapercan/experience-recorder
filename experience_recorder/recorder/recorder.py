import json
import logging
import os
import sys
from datetime import datetime
import shutil

import time

from multiprocessing import active_children

from pynput import mouse
from pynput.keyboard import Listener as KeyboardListener
from pynput.keyboard import Key

from multiprocessing import Process

import experience_recorder.computer as computer
from experience_recorder.human.human import Human
from experience_recorder.perceptions.perceptions import Perceptions

fmt = '[%(asctime)-15s] [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, stream=sys.stdout)


class Recorder:
    """
    Allows the procceses  to run according to the configured senses, it also handles the keyboard and mouse
    listeners in order to generate the experience dataset.

    Parameters
    ----------
    global_configuration:  :class:`dict`
        Previously loaded .yaml file for system configuration
    task_configuration:  :class:`dict`
        Previously loaded .yaml file for task configuration.
    """

    def __init__(self, global_configuration, task_configuration):
        self.global_conf = global_configuration
        self.task_conf = task_configuration

        self.logger = logging.getLogger(f'{self.__class__.__name__}')
        self.logger.info('Starting recorder...')
        self.starting_time = str(datetime.now().timestamp()).replace(".", "").ljust(18, '0')
        self.logger.info(f"Global Conf:\n {self.global_conf}")
        self.logger.info(f"Task Conf: \n{self.task_conf}")

    def start_computer_recording(self):
        """
        A method that starts sensing processes in parallel.
        """
        for sense in self.task_conf['senses']:
            print(self.task_conf)
            sense_object = getattr(computer, self.task_conf['senses'][sense]['kind'])(self.global_conf,
                                                                                      self.task_conf['senses'], sense,
                                                                                      self.starting_time)
            sense_proccess = Process(target=getattr(sense_object, 'start'))
            sense_proccess.start()

    def start_human_recording(self):
        Human(self.global_conf, self.task_conf, self.starting_time).start()

    def start(self):
        self.start_computer_recording()
        self.start_human_recording()

    def empty_buffer(self):
        raw_datasets_dir = self.global_conf['raw_datasets_dir']
        if os.path.exists(raw_datasets_dir):
            for f in os.listdir(raw_datasets_dir):
                os.remove(os.path.join(raw_datasets_dir, f))

    def percept_on_actions(self):
        self.perceptions = Perceptions(self.global_conf, self.task_conf['senses'], self.starting_time)
        datasets_dir = os.path.join(self.global_conf['datasets_dir'], str(self.global_conf['task']), self.starting_time)

        os.makedirs(datasets_dir, exist_ok=True)

        for sense in self.task_conf['senses']:
            states_dir = os.path.join(self.global_conf['raw_datasets_dir'], self.task_conf['task'], self.starting_time,
                                      sense)
            actions_dir = os.path.join(self.global_conf['raw_datasets_dir'], self.task_conf['task'], self.starting_time,
                                       'actions')

            for action in os.listdir(actions_dir):
                action_file = open(os.path.join(actions_dir, action), "r")
                action_dict = json.load(action_file)
                data_info_file = open(os.path.join(datasets_dir, f"{action_dict['ts']}.json"), "w")

                if self.task_conf['senses'][sense]['perception'] != 'None':
                    perception = getattr(self.perceptions, self.task_conf['senses'][sense]['perception'])(sense,
                                                                                                          action_dict[
                                                                                                              'ts'])
                    action_dict = action_dict | {sense: perception}
                    json.dump(action_dict, data_info_file)

    def post_process(self):
        self.percept_on_actions()
        self.map_states_to_actions()

    def map_states_to_actions(self):
        actions_dir = os.path.join(self.global_conf['raw_datasets_dir'], self.task_conf['task'], self.starting_time,
                                   'actions')
        actions = os.listdir(actions_dir)
        datasets_dir = os.path.join(self.global_conf['datasets_dir'], str(self.global_conf['task']), self.starting_time)
        for sense in self.task_conf['senses']:
            states_dir = os.path.join(self.global_conf['raw_datasets_dir'], self.task_conf['task'], self.starting_time,
                                      sense)
            states_ts = [state for state in os.listdir(states_dir)]
            if self.task_conf['senses'][sense]['perception'] == 'None':
                for action in actions:
                    action_ts = action
                    states_ts_aux = states_ts
                    states_ts_aux.append(action_ts)
                    states_ts_aux.sort()
                    position = states_ts_aux.index(action_ts)
                    file_extension = '.' + states_ts[0].split('.')[1]
                    state_dir = os.path.join(states_dir, states_ts[position - 1])
                    shutil.copy(state_dir, datasets_dir)
                    os.rename(os.path.join(datasets_dir, states_ts[position - 1]),
                              os.path.join(datasets_dir, action_ts.split('.')[0] + file_extension))





