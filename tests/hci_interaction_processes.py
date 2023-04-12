import os
import time

import pyautogui
import Xlib.threaded

def click_proccess(coordinates,executions, delay):
    print('click proccess', executions,delay)
    for _ in range(executions):
        import logging
        time.sleep(delay)
        print(coordinates)
        try:
            os.system(f'xdotool mousemove {coordinates[0]} {coordinates[1]}')
            os.system('xdotool click 1')
        except:
            pass


def keypress_proccess(key,executions, delay):

    for _ in range(executions):
        print('keypress', key, executions, delay)
        time.sleep(delay)
        try:
            os.system(f"xdotool key {key}")
        except Exception as e:
            raise e

