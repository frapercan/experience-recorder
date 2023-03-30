import logging
import os
import sys
from datetime import datetime

from pynput import mouse
from pynput.keyboard import Listener as KeyboardListener
from pynput.keyboard import Key
import torch
from experience_recorder.senses.senses import Senses
from experience_recorder.perceptions.perceptions import Perceptions

fmt = '[%(asctime)-15s] [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, stream=sys.stdout)

xx, yy, previous_reward = 0, 0, 0
action = ""
r_screen = True


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
        self.starting_time = datetime.now().timestamp()
        self.logger.info(f"Global Conf:\n {self.global_conf}")
        self.logger.info(f"Task Conf: \n{self.task_conf}")

    def start_senses(self):
        """
        A method that starts sensing processes in parallel.
        """
        self.senses = Senses(self.task_conf['senses'])
        for sense in self.task_conf['senses']:
            sense_proccess = torch.multiprocessing.Process(
                target=getattr(self.senses, self.task_conf['senses'][sense]['kind']), args=[sense])
            sense_proccess.start()

    def start(self):
        """
        Method that launches mouse and keyboard listeners, if configured, that calls to the store_experience method.
        """

        def on_press(key):
            global action
            print("Key pressed: {0}".format(key))
            self.store_experience(key)
            if key == Key.backspace:
                self.logger.info("Exiting recorder")
                return False

        def on_click(x, y, button, pressed):
            if button == mouse.Button.left and pressed:
                self.store_experience({'button': button, 'x': x, 'y': y})
                print('{} at {}'.format('Pressed Left Click' if pressed else 'Released Left Click', (x, y)))

        if self.task_conf['mouse']:
            listener = mouse.Listener(on_click=on_click)
            listener.start()
        if self.task_conf['keyboard']:
            keyboard_listener = KeyboardListener(on_press=on_press)
            keyboard_listener.start()
            keyboard_listener.join()

    def store_experience(self, key_info):
        """
        Used on listeners, it stores the experience after using the skills on the state immediately prior to having
        pressed the key, or the mouse.

        Files can be written in two formats, '.txt' for OCR processes and '.png' for images depending upon the skills.

        Parameters
        ----------
        key_info:  :class:`list`
            Key pressed, or mouse location depending on the sense that triggered the method.

        """
        task_dataset_dir = os.path.join(self.global_conf['datasets_dir'],
                                        str(self.global_conf['task']))
        if not os.path.exists(task_dataset_dir):
            os.makedirs('task_dataset_dir')

        experience_dir = os.path.join(task_dataset_dir, str(self.starting_time))
        if not os.path.exists(experience_dir):
            os.makedirs(experience_dir)

        dt = datetime.now().timestamp()

        action_dir = os.path.join(experience_dir, str(dt) + "-action.txt")

        with open(action_dir, 'w') as f:
            f.write(str(key_info))
            f.close()

        self.perceptions = Perceptions(self.global_conf, self.task_conf['senses'])
        for sense in self.task_conf['senses']:
            capture = getattr(self.perceptions, self.task_conf['senses'][sense]['skill'])(sense)

            format = ""

            match str(type(capture)):
                case "<class 'PIL.PngImagePlugin.PngImageFile'>":
                    format = ".png"
                case "<class 'str'>":
                    format = ".txt"

            capture_dir = os.path.join(experience_dir, f"{str(dt)}-{sense}{format}")
            if format == ".txt":
                with open(capture_dir, 'w') as f:
                    f.write(capture)
                    f.close()
            else:
                capture.save(capture_dir)

    def empty_buffer(self):
        buffer_dir = self.global_conf['buffer_dir']
        for f in os.listdir(buffer_dir):
            os.remove(os.path.join(buffer_dir, f))
