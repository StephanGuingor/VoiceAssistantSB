"""
Computer Class
"""
import snowboydecoder
import sys
import signal
import speech_recognition as sr
import os
from inspect import isfunction
from typing import Iterable, Callable, Union

from program import Program


SNOWBOY_ROOT_PATH = '/Users/stephan/Desktop/Coding/Python/SpeechRecog/snowboy/examples/Python3'
KEYWORDS_PATH = '/Users/stephan/Desktop/Coding/Python/SpeechRecog/snowboy/examples/Python3/resources/models/'

interrupted = False


class Computer:

    _PROGRAMS = []

    @classmethod
    def _interrupt_callback(cls):
        """
        Returns the status of the app
        """
        global interrupted
        return interrupted

    @classmethod
    def _signal_handler(cls, signal, frame):
        """
        If Ctrl+C is pressed, function will run
        """
        global interrupted
        interrupted = True

    def __init__(self):
        # capture SIGINT signal, e.g., Ctrl+C
        signal.signal(signal.SIGINT, self._signal_handler)

    def set_interrupt_callback(self, callback):
        """
        Sets 'self._interrupted_callback'
        """
        try:
            assert(isfunction(callback))

            # Setting callback
            self._interrupt_callback = callback

        except AssertionError as e:
            print(e)
            print("ERROR : Callback must be type function")

    def add_program(self, program: "Program"):
        """
        Adds a Program to the list
        """
        try:
            assert(isinstance(program, Program))
            self._PROGRAMS.append(program)
        except AssertionError as e:
            print(e)

    def start_programs(self):
        """
        Executes the main event listener from Snowboy
        """

        models = [os.path.join(KEYWORDS_PATH, program.keyword)
                  for program in self._PROGRAMS]
        callbacks = [program.callback for program in self._PROGRAMS]
        sensitivity = [program.sensitivity for program in self._PROGRAMS]

        detector = snowboydecoder.HotwordDetector(
            models, sensitivity=sensitivity)

        print(self._PROGRAMS[0].audio_callback)
        audio_callback = self._PROGRAMS[0].audio_callback
        # main loop
        detector.start(detected_callback=callbacks,
                       interrupt_check=self._interrupt_callback,
                       sleep_time=0.01, audio_recorder_callback=audio_callback)

        detector.terminate()

    def timeout_start(self, timeout, audio_callback=None):
        """
        After a timeout it stop else activates function (-2 status silence)
        """
        models = [os.path.join(KEYWORDS_PATH, program.keyword)
                  for program in self._PROGRAMS]
        callbacks = [program.callback for program in self._PROGRAMS]
        sensitivity = [program.sensitivity for program in self._PROGRAMS]

        detector = snowboydecoder.HotwordDetector(
            models, sensitivity=sensitivity)

        print(self._PROGRAMS[0].audio_callback)
        audio_callback = self._PROGRAMS[0].audio_callback
        # main loop
        detector.start(detected_callback=callbacks,
                       interrupt_check=self._interrupt_callback,
                       sleep_time=0.01, stop_timeout=timeout, audio_recorder_callback=audio_callback)

        detector.terminate()


def stop(x):
    """
    Stops the iteration of the Computer class
    """
    print(x)
    x._running = False


if __name__ == "__main__":
    from programs import ComputerController
    computer = Computer()

    computer.add_program(ComputerController(keyword='computer.umdl'))
    computer.add_program(Program(keyword='subex.umdl',
                                 callback=lambda x: print("SUCKERS")))
    computer.start_programs()
