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
            self.start()
            self.log('wait')
            win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
            self.log('done')
        except Exception as exc:
            self.log('Exception : {}'.format(exc))
            self.stop()

    def stop(self):
        """
        .. py:attribute:: SvcStop()

        Stop the service.

           :rtype: None

        """
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.log('stopping')
        self.stop()
        self.log('stopped')
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def start(self, executable):
        """
        .. py:attribute:: start()

        Run the executable.

           :param executable: The executable object.
           :type executable: Callable
           :rtype: None

        """
        self.log("Start service!")
        executable()


def instart(cls, name, display_name=None, stay_alive=True):
    """
    ==============

    ``instart``
    ----------

    .. py:function:: instart(['cls', 'name', 'display_name', 'stay_alive'])

    Install and  Start (auto) a Service

       :param cls: the class (derived from Service) that implement the Service
       :type cls: Class object
       :param name: Service name
       :type name: str
       :param display_name: the name displayed in the service manager
       :type display_name: str
       :param stay_alive: Service will stop on logout if False
       :type stay_alive: boolean
       :rtype: None

    """
    cls._svc_name_ = name
    cls._svc_display_name_ = display_name or name
    try:
        module_path = modules[cls.__module__].__file__
    except AttributeError:
        # maybe py2exe went by
        from sys import executable
        module_path = executable
    module_file = splitext(abspath(module_path))[0]
    cls._svc_reg_class_ = '{}.{}'.format(module_file, cls.__name__)
    if stay_alive:
        win32api.SetConsoleCtrlHandler(lambda x: True, True)
    try:
        win32serviceutil.InstallService(
            cls._svc_reg_class_,
            cls._svc_name_,
            cls._svc_display_name_,
            startType=win32service.SERVICE_AUTO_START
        )
        print('Install ok')
        win32serviceutil.StartService(
            cls._svc_name_
        )
        print('Start ok')
    except Exception, x:
        print str(x)
