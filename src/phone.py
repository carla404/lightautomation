import bluetooth as bluetooth
from enum import Enum
import threading
import time


class State(Enum):
    HOME = 0
    AWAY = 1

class Phone(object):
    '''

    '''

    def __init__(self, name ,ip=None, bluetooth_address=None):
        self.name = name
        self.ip = ip
        self.BT_Address = bluetooth_address
        self.run = True
        self.state = State.AWAY


    def addCBStateChanged(self, function):
        self.cbStateChanged = function

    def startTracing(self):
        if self.cbStateChanged == None:
            Exception("No callback given")
        print("Trace")
        self.tracerThread = threading.Thread(target=self.doStartTracing)
        self.tracerThread.start()

    def stopTracing(self):
        if not self.run:
            Exception("No trace to stop")

        print("Stopping trace")
        self.run = False
        self.tracerThread.join()

    def setState(self, state):
        if self.state != state:
            self.state = state
            if state == State.HOME:
                self.cbStateChanged()
                return
            self.cbStateChanged()

    def doStartTracing(self):
        print("StartDoTracing")
        while self.run:
            if self.__isHome__():
                self.setState(State.HOME)
            else:
                self.setState(State.AWAY)
            time.sleep(5)

    def __isHome__(self):
        services = bluetooth.find_service(address=self.BT_Address)
        return True if services else False


