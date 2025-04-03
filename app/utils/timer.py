# -*- coding: UTF-8 -*-
"""
计时器

Author: worship-dog
Email: worship76@foxmail.com>
"""

import time


class Timer:
    def __init__(self):
        self.__start_time = None
        self.__end_time = None
        self.elapsed = None
    def start_timer(self):
        self.__start_time = time.time()

    def end_timer(self, response: str) -> bool:
        if "</think>" in response and self.__start_time is not None:
            self.__end_time = time.time()
            self.elapsed = int(self.__end_time - self.__start_time)
            return True

        return False


timer_dict = {}
