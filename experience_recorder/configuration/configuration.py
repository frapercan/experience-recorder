import logging

import os
import sys

import yaml
from pynput import mouse

fmt = '[%(asctime)-15s] [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, stream=sys.stdout)

xx, yy = 0, 0


class Configuration:
    """
    Utility class to manage the configuration of the Experience Recorder, allowing the creation and loading of
    configuration files. In this class the following is configured:
        #. Number of senses to use
        #. Name of the senses
        #. Type of senses
        #. Ability of the senses

    Parameters
    ----------
    global_configuration:  :class:`dict` or :class:`None`
        Previously created and loaded .yaml file or empty to start a new configuration.
    """

    def __init__(self, global_configuration):
        self.global_conf = global_configuration
        self.logger = logging.getLogger(f'{self.__class__.__name__}')
        self.logger.info("hola")
        self.tasks_configuration_dir = os.path.join(self.global_conf['tasks_configuration_dir'],
                                                    str(global_configuration['task']) + '.yaml')

        self.conf = self.load_configuration(self.tasks_configuration_dir) if os.path.isfile(
            self.tasks_configuration_dir) else self.create()

    def create(self):
        """
        Method to initiate the creation of a new configuration.

        Returns
        -------
        conf:  :class:`dict`
            task configuration
        """
        conf = {"task": str(self.global_conf["task"]), 'senses': {}}

        keyboard_usage = self.ask_for_keyboard_usage()
        conf['keyboard'] = keyboard_usage
        mouse_usage = self.ask_for_mouse_usage()
        conf['mouse'] = mouse_usage

        amount = self.ask_for_sense_amount()
        for i in range(0, amount):
            name, kind, skill, location = self.ask_for_sense(i)
            sense = self.new_sense(kind, skill, location)
            conf['senses'][name] = sense
        return conf

    def ask_for_sense_amount(self):
        """
        ask for amount of senses for task configuration

        Returns
        -------
        amount:  :class:`int`
            Amount of senses inserted via prompt by the user.
        """
        amount = input('Enter the amount of senses for your model: \n')
        try:
            amount = int(amount)
        except Exception:
            self.logger.error('Bad input for amount of senses')
            sys.exit(1)
        return int(amount)

    def ask_for_sense(self, index):
        """
        ask for name, kind, skill and screen coordinates for the current sense.

        Parameters
        ----------
        index:  :class:`int`
            sense index

        Returns
        -------
        name:  :class:`str`
            name identifier of the sense.
        kind:  :class:`int`
            type of sense.
        skill:  :class:`int`
            skill/processment configuration after perceiving the state.
        location:  :obj:`List(int,int,int,int)`
            Screen coordinates if sense's kind is see.
        """

        name = input(f"Name sense #{index}: \n")
        kind = input(f'Sense kind #{index} 1 - see, 2 - ear: \n')
        match kind:
            case '1':
                kind = "see"
                location = self.ask_for_coordinates()
            case '2':
                kind = "ear"
                location = None  # Audio interface maybe
            case _:
                self.logger.error('Incorrect sense kind')
                sys.exit(1)

        skill = input(f'Sense skill #{index} 1 - watch, 2 - read: \n')
        match skill:
            case '1':
                skill = "watch"
            case '2':
                skill = "read"
            case _:
                self.logger.error('Incorrect sense skill')
                sys.exit(1)

        return name, kind, skill, location

    def new_sense(self, kind, skill, location):
        """
        structure sense information into dict format.

        Parameters
        -------
        kind:  :class:`int`
            type of sense.
        skill:  :class:`int`
            skill/processment configuration after perceiving the state.
        location:  :obj:`List(int,int,int,int)`
            Screen coordinates if sense's kind is see.
        Returns
        -------
        sense:  :class:`dict`
            a dict containing all sense's properties.
        """
        if kind == "see":
            return {'kind': kind, 'skill': skill,
                    'location':
                        {'left': location[0],
                         'top': location[1],
                         'width': location[2] - location[0],
                         'height': location[3] - location[1]}
                    }

    def save_configuration(self):
        """
        Save task configuration inside tasks folder using current name.
        """
        with open(self.tasks_configuration_dir, 'w') as configuration_file:
            yaml.dump(self.conf, configuration_file, default_flow_style=False)
        self.logger.info(f"conf saved in: {dir}\n")

    def ask_for_coordinates(self):
        """
        Ask for coordinates using input prompts to user.

        Returns
        -------
        location:  :obj:`List(int,int,int,int)`
            Screen coordinates.
        """

        def on_click(x, y, button, pressed):
            global xx, yy
            xx, yy = x, y
            if not pressed:
                return False

        with mouse.Listener(on_click=on_click) as listener:
            self.logger.info("Click on left-top corner")
            listener.join()
            x1 = xx
            y1 = yy

        with mouse.Listener(on_click=on_click) as listener:
            self.logger.info("Click on right-bottom corner")
            listener.join()
            x2 = xx
            y2 = yy

        self.logger.info(f"Sceene coordinates on screen are: {x1, y1}, {x2, y2} ")

        return x1, y1, x2, y2

    def load_configuration(self, dir):
        """
        Search for a task configuration file at directory and opens it.

        Parameters
        -------
        dir:  :class:`str`
            task configuration directory.

        Returns
        -------
        conf:  :obj:`dict`
            Task configuration.
        """
        with open(dir, 'r', encoding='utf-8') as conf:
            conf = yaml.safe_load(conf)
            self.logger.info(f"Configuration loaded: {conf}")
            return conf

    def ask_for_keyboard_usage(self):
        """
        This configuration allows keyboard to be tracked.

        Returns
        -------
        keyboard_usage:  :obj:`Boolean`
        """
        self.logger.info("kb")
        keyboard_usage = input("Record keyboard? 0 - No, 1 - Yes: \n")
        try:
            return True if int(keyboard_usage) else False
        except Exception:
            self.logger.error('Bad input for keyboard usage')
            sys.exit(1)

    def ask_for_mouse_usage(self):
        """
        This configuration allows mouse to be tracked.

        Returns
        -------
        mouse_usage:  :obj:`Boolean`
        """
        self.logger.info("mouse")
        mouse_usage = input("Record mouse? 0 - No, 1 - Yes: \n")
        try:
            return True if int(mouse_usage) else False
        except Exception:
            self.logger.error('Bad input for mouse usage')
            sys.exit(1)
