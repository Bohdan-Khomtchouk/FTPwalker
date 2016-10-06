from new_winservice import Service, instart
import win32serviceutil


class Test(Service):
    def __setattr__(self, name, value):
        setattr(name, value)

    def start(self):
        pass

    def stop(self):
        self.log("I'm done")


def initialize(executable):
    Test.start = lambda self: executable()


def start(executable):
    initialize(executable)
    instart(Test, 'FTPwalker', 'FTPwalker', stay_alive=False)

def stop():
    win32serviceutil.StopService('FTPwalker')
