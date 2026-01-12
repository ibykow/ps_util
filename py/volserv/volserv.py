"""
IAudioEndpointVolumeCallback.OnNotify() example.
The OnNotify() callback method gets called on volume change.
"""

import time
from comtypes import COMObject
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolumeCallback

import servicemanager
import win32event
import win32service
import win32serviceutil

TIMEOUT = 1000
MAX_VOLUME = 0.55
CUT_VOLUME = 0.45
cut = False
output = None
vol = None

class AudioEndpointVolumeCallback(COMObject):
    _com_interfaces_ = [IAudioEndpointVolumeCallback]

    def OnNotify(self, pNotify):
        global vol
        global cut

        volf = vol.GetMasterVolumeLevelScalar()
        if (volf > MAX_VOLUME):
            vol.SetMasterVolumeLevelScalar(MAX_VOLUME, None)

        if (volf > CUT_VOLUME):
            cut = True
            
def updateDevices():
    global output
    global vol

    devices = AudioUtilities.GetAllDevices()
    s = AudioUtilities.GetSpeakers()
    activeE = type(devices[0].state).Active
    active = []

    for device in devices:
        if (device.state == activeE):
            active.append(device)
            print(device.FriendlyName)
            if (s.GetId() == device.id):
                output = device

    vol = output.EndpointVolume

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = 'pyvolserv'
    _svc_display_name_ = 'Python Volume Service'
    _svc_description_ = 'Caps the Master Volume'
    
    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        
    def GetAcceptedControls(self):
        result = win32serviceutil.ServiceFramework.GetAcceptedControls(self)
        result |= win32service.SERVICE_ACCEPT_PRESHUTDOWN
        return result
    
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    def main(self):
        global output
        global vol
        global cut

        updateDevices()

        callback = AudioEndpointVolumeCallback()
        vol.RegisterControlChangeNotify(callback)

        while True:
            result = win32event.WaitForSingleObject(self.hWaitStop, TIMEOUT)
            if result == win32event.WAIT_OBJECT_0:
                volf = vol.GetMasterVolumeLevelScalar()
                if (volf > MAX_VOLUME):
                    vol.SetMasterVolumeLevelScalar(MAX_VOLUME, None)
                break
            
            if (cut):
                volf = vol.GetMasterVolumeLevelScalar()
                if (volf > CUT_VOLUME):
                    vols = volf - 0.0001
                    vol.SetMasterVolumeLevelScalar(vols, None)
                else:
                    cut = False
    
if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(AppServerSvc)
