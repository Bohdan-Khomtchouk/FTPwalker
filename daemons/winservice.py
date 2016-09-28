"""
=====
winservice.py
=====

Daemon service for windows.

============================

"""

import win32serviceutil
import win32service
import win32event
import win32api


class Service(win32serviceutil.ServiceFramework):
    _svc_name_ = '_unNamed'
    _svc_display_name_ = '_Service Template'

    def __init__(self, *args):
        win32serviceutil.ServiceFramework.__init__(self, *args)
        self.log('init')
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def log(self, msg):
        import servicemanager
        servicemanager.LogInfoMsg(str(msg))

    def sleep(self, sec):
        win32api.Sleep(sec * 1000, True)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.log('start')
            self.start()
            self.log('wait')
            win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
            self.log('done')
        except Exception as x:
            self.log('Exception : %s' % x)
            self.SvcStop()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.log('stopped')
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def start(self):
        self.executable()

    def stop(self):
        self.SvcStop()


class Daemon:
    def __init__(self, stay_alive=True, **kwargs):
        self.name = kwargs['name']
        self.display_name = kwargs['display_name']
        self.stay_alive = stay_alive

    def start(self, executable):

        try:
            setattr(Service, 'executable', executable)
            setattr(Service, '_svc_name_', self.name)
            setattr(Service, '_svc_display_name_', self.display_name or self.name)
            setattr(Service, '_svc_reg_class_', "Service")
        except:
            raise

        if self.stay_alive:
            win32api.SetConsoleCtrlHandler(lambda x: True, True)
        try:
            win32serviceutil.InstallService(
                Service._svc_reg_class_,
                Service._svc_name_,
                Service._svc_display_name_,
                startType=win32service.SERVICE_AUTO_START
            )
            print('Install ok')
            win32serviceutil.StartService(
                Service._svc_name_
            )
            print('Start ok')
        except Exception as x:
            print(str(x))

    def stop(self):
        win32serviceutil.StopService(self.name)
        # win32serviceutil.ServiceCtrlHandler(win32service.SERVICE_CONTROL_STOP)
