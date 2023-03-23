import logging

import os
import sys

import yaml
from pynput import mouse

fmt = '[%(asctime)-15s] [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, stream=sys.stdout)

xx, yy = 0, 0


class Configuration:
    def __init__(self, global_configuration):
        self.logger = logging.getLogger(f'{self.__class__.__name__}')
        self.tasks_configuration_dir = f"./conf/tasks/{global_configuration['task']}.yaml"
        self.conf = self.load_configuration(self.tasks_configuration_dir) if os.path.isfile(
            self.tasks_configuration_dir) else self.create(global_configuration)
        print(self.conf)

    def create(self, global_configuration):
        conf = {"task": str(global_configuration["task"]), 'senses': {}}

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
        amount = input('Enter the amount of senses for your model: \n')
        try:
            amount = int(amount)
        except Exception as e:
            self.logger.error('Bad input for amount of senses')
            sys.exit(1)
        return int(amount)

    def ask_for_sense(self, index):
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
        if kind == "see":
            return {'kind': kind, 'skill': skill,
                    'location': {'left': location[0], 'top': location[1], 'width': location[2]-location[0], 'height': location[3]-location[1]}}

    def save_configuration(self):
        dir = f"conf/tasks/{self.conf['task']}.yaml"
        with open(dir, 'w') as configuration_file:
            yaml.dump(self.conf, configuration_file, default_flow_style=False)
        self.logger.info(f"conf saved in: {dir}\n")

    def ask_for_coordinates(self):
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
        with open(dir, 'r', encoding='utf-8') as conf:
            conf = yaml.safe_load(conf)
            self.logger.info(f"Configuration loaded: {conf}")
            return conf

    def ask_for_keyboard_usage(self):
        keyboard_usage = input(f'Record keyboard? 0 - No, 1 - Yes: \n')
        return True if keyboard_usage else False

    def ask_for_mouse_usage(self):
        mouse_usage = input(f'Record mouse? 0 - No, 1 - Yes: \n')
        return True if mouse_usage else False