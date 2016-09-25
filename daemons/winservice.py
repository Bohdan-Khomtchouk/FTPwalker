"""
=====
winservice.py
=====

Daemon service for windows.
Source: http://code.activestate.com/recipes/551780/

============================

"""

from os.path import splitext, abspath
from sys import modules

import win32serviceutil
import win32service
import win32event
import win32api


class Service(win32serviceutil.ServiceFramework):
    """
    ==============

    ``Service``
    ----------

    .. py:class:: Service()

    """
    _svc_name_ = '_unNamed'
    _svc_display_name_ = '_Service Template'

    def __init__(self, *args):
        """
        .. py:attribute:: __init__()

           :rtype: None
        """
        win32serviceutil.ServiceFramework.__init__(self, *args)
        self.log('init')
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def log(self, msg):
        """
        .. py:attribute:: log()

           :param msg: log message.
           :type msg: str
           :rtype: None

        """
        import servicemanager
        servicemanager.LogInfoMsg(str(msg))

    def SvcDoRun(self):
        """
        .. py:attribute:: SvcDoRun()

        Running the service.

           :rtype: None

        """
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.log('start')
            self.executable()
            self.log('wait')
            win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
            self.log('done')
        except Exception as exc:
            self.log('Exception : {}'.format(exc))
            self.stop()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.log('stopped')
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)


def stop(self):
    win32serviceutil.StopService(Service)
    print('Service stopped...')


def start(self, executable):
    Service.executable = executable
    win32serviceutil.StartService(Service)
