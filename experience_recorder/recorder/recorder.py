import json
import logging
import os
import sys
from datetime import datetime
import shutil

from multiprocessing import Process

import experience_recorder.computer as computer
from experience_recorder.human.human import Human
from experience_recorder.perceptions.perceptions import Perceptions

fmt = '[%(asctime)-15s] [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, stream=sys.stdout)


class Recorder:
    """
    This class is responsible for initiating and handling the recording process of both computer and human experiences.
    It processes and maps the experiences to create a final dataset.
    """

    def __init__(self, global_configuration, task_configuration):
        """
        Initialize the Recorder object.

        Parameters:
        - global_configuration: Contains configurations applicable throughout the system.
        - task_configuration: Contains configurations specific to the current task.
        """
        self.global_conf = global_configuration
        self.task_conf = task_configuration

        # Setup a logger specific to this class, for recording operational messages.
        self.logger = logging.getLogger(f'{self.__class__.__name__}')
        self.logger.info('Starting recorder...')

        # Generate a unique timestamp for this recording session. Useful for keeping records distinct.
        self.starting_time = str(datetime.now().timestamp()).replace(".", "").ljust(18, '0')
        self.logger.info(f"Global Configuration:\n {self.global_conf}")
        self.logger.info(f"Task Configuration: \n{self.task_conf}")

        self.computer_processes = []

    def start_computer_recording(self):
        """
        Initiates the recording processes for each configured computer sense in parallel.

        For each sense (like vision, sound), a new process is spawned that will start its recording function.
        """
        for sense in self.task_conf['senses']:
            print('sense',sense)
            print('sense',sense)
            print('sense',sense)
            print('sense',sense)
            print('sense',sense)
            # Dynamically get the appropriate class/object from the `computer` module based on the 'kind' of sense
            # then instantiate it with necessary parameters.
            sense_object = getattr(computer, self.task_conf['senses'][sense]['kind'])(self.global_conf,
                                                                                      self.task_conf['senses'], sense,
                                                                                      self.starting_time)
            # Start the recording process for the given sense in a separate process.
            print(sense_object)

            sense_proccess = Process(target=getattr(sense_object, 'start'))
            self.computer_processes.append(sense_proccess)
            sense_proccess.start()


    def start_human_recording(self):
        """
        Initiates the recording of human experiences.

        Uses the Human class to start capturing human-related events/data.
        """
        Human(self.global_conf, self.task_conf, self.starting_time).start()

    def start(self):
        """
        Central method to start all the recording processes.

        It activates both computer and human recording functions.
        """
        self.start_computer_recording()
        self.start_human_recording()

    def empty_buffer(self):
        """
        Clears the raw_datasets directory.

        This is a clean-up utility function. Before starting a new recording session, it can be useful to ensure
        that no residual files from a previous session are left behind.
        """
        raw_datasets_dir = self.global_conf['raw_datasets_dir']
        if os.path.exists(raw_datasets_dir):
            for raw_datasets in os.listdir(raw_datasets_dir):
                shutil.rmtree(os.path.join(raw_datasets_dir,raw_datasets))

    def percept_on_actions(self):
        """
        Maps sensory perceptions onto actions to generate enriched action data.

        For each action, its related sensory data (like vision or sound at the time of the action) is fetched and
        combined, then saved as an enriched record in the dataset.
        """
        self.perceptions = Perceptions(self.global_conf, self.task_conf['senses'], self.starting_time)
        datasets_dir = os.path.join(self.global_conf['datasets_dir'], str(self.global_conf['task']), self.starting_time)

        os.makedirs(datasets_dir, exist_ok=True)

        # Loop through each sense, extract relevant data and map it to each action.
        for sense in self.task_conf['senses']:
            states_dir = os.path.join(self.global_conf['raw_datasets_dir'], self.task_conf['task'], self.starting_time,
                                      sense)
            actions_dir = os.path.join(self.global_conf['raw_datasets_dir'], self.task_conf['task'], self.starting_time,
                                       'actions')

            for action in os.listdir(actions_dir):
                action_file = open(os.path.join(actions_dir, action), "r")
                action_dict = json.load(action_file)
                data_info_file = open(os.path.join(datasets_dir, f"{action_dict['ts']}.json"), "w")

                # If a perception method is defined for the sense, fetch the perception and add it to the action data.
                if self.task_conf['senses'][sense]['perception'] != 'None':
                    perception = getattr(self.perceptions, self.task_conf['senses'][sense]['perception'])(sense,
                                                                                                          action_dict[
                                                                                                              'ts'])
                    action_dict = action_dict | {sense: perception}
                    json.dump(action_dict, data_info_file)

    def post_process(self):
        """
        Applies a sequence of post-processing steps to the raw data.

        This method prepares the final dataset by merging actions with their perceptions, and mapping states to actions.
        """
        self.percept_on_actions()
        self.map_states_to_actions()

    def map_states_to_actions(self):
        """
        Establishes a correlation between system states and user actions.

        For each action, the state of the system is determined and associated. This can help in understanding
        the context of the action.
        """
        actions_dir = os.path.join(self.global_conf['raw_datasets_dir'], self.task_conf['task'], self.starting_time,
                                   'actions')
        actions = os.listdir(actions_dir)
        datasets_dir = os.path.join(self.global_conf['datasets_dir'], str(self.global_conf['task']), self.starting_time)

        for sense in self.task_conf['senses']:
            states_dir = os.path.join(self.global_conf['raw_datasets_dir'], self.task_conf['task'], self.starting_time,
                                      sense)
            states_ts = [state for state in os.listdir(states_dir)]

            # If no perception method is defined, directly map the state to the action.
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
