import logging
import os
import numpy as np
from paddleocr import PaddleOCR
import PIL
from os import listdir
import sys

fmt = '[%(asctime)-15s] [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, stream=sys.stdout)


class Skills():
    def __init__(self, tasks_configuration):
        self.task_conf = tasks_configuration
        self.logger = logging.getLogger(f'{self.__class__.__name__}')
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

    def watch(self, sense):
        return self.search_state(sense)

    def read(self, sense):
        state = self.search_state(sense)
        text = self.ocr.ocr(np.array(state), cls=False)[0][0][1][0]
        print(f"text read: :{text}")  # todo: fix logger
        self.logger.info(f"text read: :{text}")
        return text

    def search_state(self, sense):
        directory = "./__buffer__/"
        files = listdir(directory)
        files.sort(reverse=True)
        files = [file for file in files if sense in file]
        filename = files[1]
        return PIL.Image.open(os.path.join(directory, filename))
