import logging

import os
import numpy as np
from paddleocr import PaddleOCR
import PIL
from os import listdir
import sys

fmt = '[%(asctime)-15s] [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, stream=sys.stdout)


class Perceptions():
    """
    Class that contains the different possibilities of perceptions in the form of methods.

    Parameters
    ----------
    tasks_configuration:  :class:`dict`
        Previously loaded .yaml file for tasks configuration.
    """

    def __init__(self, global_configuration, tasks_configuration):
        self.global_conf = global_configuration
        self.task_conf = tasks_configuration
        self.logger = logging.getLogger(f'{self.__class__.__name__}')
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

    def watch(self, sense):
        """
        Search the latest state and returns it without modifications.

        Parameters
        ----------
        sense:  :class:`str`
            name of the sense

        Returns
        -------
        image:  :class:`PIL.Iamage`
            The image of the latest state.
        """
        return self.search_state(sense)

    def read(self, sense):
        """
        Search the latest state and returns the text after aplying OCR.

        Parameters
        ----------
        sense:  :class:`str`
            name of the sense

        Returns
        -------
        text:  :class:`PIL.Iamage`
            The text contained in the latest state image.
        """
        state = self.search_state(sense)
        print('state', state)
        print(self.ocr.ocr(np.array(state), cls=False))
        text = self.ocr.ocr(np.array(state), cls=False)[0][0][1][0]
        print(f"text read: :{text}")  # todo: fix logger
        self.logger.info(f"text read: :{text}")
        return text

    def search_state(self, sense):
        """
        Search the latest state in the buffer and opens it as an image.
        This could be improved through a more formal buffer using indexes.

        Parameters
        ----------
        sense:  :class:`str`
            name of the sense
        """
        directory = self.global_conf['buffer_dir']
        files = listdir(directory)
        files.sort(reverse=True)
        files = [file for file in files if sense in file]
        filename = files[1]
        return PIL.Image.open(os.path.join(directory, filename))
