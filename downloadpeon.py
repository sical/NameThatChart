from threading import Thread
import time
import wget
import threading
import sys

import signal


class TimeoutException(Exception):
    pass


class Peon(Thread):

    def __init__(self, source, output):
        Thread.__init__(self)
        self.source = source
        self.output = output

    def run(self):

        try:
            print("Fetching ...  .. . " + self.source + "\n")
            wget.download(self.source, self.output)
            print('\x1b[6;30;42m' + "Done ! " + '\x1b[0m' + "\n")

        except Exception as e:
            print('\x1b[6;30;41m' + str(e) + '\x1b[0m')

        return 'DONE'