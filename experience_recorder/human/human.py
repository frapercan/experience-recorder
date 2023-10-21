import json
import logging
import os
import sys
from datetime import datetime
import audiomath as am
from pynput import mouse
from pynput.keyboard import Listener as KeyboardListener
from pynput.keyboard import Key
from multiprocessing import active_children

fmt = '[%(asctime)-15s] [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, stream=sys.stdout)

xx, yy, previous_reward = 0, 0, 0
action = ""


class Human():
    """
    Class that contains the different possibilities of senses in the form of methods.
    At the moment only sight is contemplated.

    Parameters
    ----------
    tasks_configuration:  :class:`dict`
        Previously loaded .yaml file for tasks configuration.
    """

    def __init__(self, global_configuration, tasks_configuration,recorder_starting_time):
        self.global_conf = global_configuration
        self.task_conf = tasks_configuration
        self.recorder_starting_time = recorder_starting_time
        self.logger = logging.getLogger(f'{self.__class__.__name__}')

    def start(self):
        """
        Method that launches mouse and keyboard listeners, if configured, that calls to the store_experience method.
        """

        def on_press(key):
            global action
            self.logger.info(f"Key pressed: {key}")
            if key == Key.backspace:
                active = active_children()
                for child in active:
                    child.kill()
                self.logger.info("Exiting recorder")
                return False
            self.store_action(key)


        def on_click(x, y, button, pressed):
            if button == mouse.Button.left and pressed:
                self.store_action({'button': button, 'x': x, 'y': y})
                self.logger.info('{} at {}'.format('Pressed Left Click' if pressed else 'Released Left Click', (x, y)))

        if self.task_conf['mouse']:
            listener = mouse.Listener(on_click=on_click)
            listener.start()
        if self.task_conf['keyboard']:
            keyboard_listener = KeyboardListener(on_press=on_press)
            keyboard_listener.start()
            keyboard_listener.join()

    def store_action(self, key_info):
        """
        Used on listeners, it stores the experience after using the skills on the state immediately prior to having
        pressed the key, or the mouse.

        Parameters
        ----------
        key_info:  :class:`list`
            Key pressed, or mouse location depending on the sense that triggered the method.

        """
        actions_dir = os.path.join(self.global_conf['raw_datasets_dir'],
                                   str(self.global_conf['task']), str(self.recorder_starting_time),'actions')

        if not os.path.exists(actions_dir):
            os.makedirs(actions_dir)

        dt = str(datetime.now().timestamp()).replace(".", "").ljust(18,'0')


        info = {'action': str(key_info), 'ts':dt}

        with open(os.path.join(actions_dir, f'{dt}.json'), 'w') as outfile:
            json.dump(info, outfile)
