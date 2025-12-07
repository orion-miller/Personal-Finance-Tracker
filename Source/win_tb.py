'''Windows taskbar interface

References:
https://github.com/N3RDIUM/PyTaskbar/tree/main
https://stackoverflow.com/questions/1736394/using-windows-7-taskbar-features-in-pyqt/1744503#1744503
'''

import sys
from ctypes import c_ulonglong
from ctypes.wintypes import HWND
from comtypes import GUID, IUnknown, COMMETHOD, HRESULT
import ctypes
import comtypes.client as cc
import comtypes.gen.TaskbarLib as tbl
from comtypes.gen import _683BF642_E9CA_4124_BE43_67065B2FA653_0_1_0

if not sys.platform.startswith("win"):
    TaskbarProgress = None
else:
    try:
        cc.GetModule("./TaskbarLib.tlb")
    except:
        raise Exception("Could not find TaskbarLib.tlb")

    taskbar = cc.CreateObject(
        "{56FDF344-FD6D-11d0-958A-006097C9A090}",
        interface=tbl.ITaskbarList3) 

    # TBPF_NOPROGRESS    = 0 # normal state with no progress bar
    TBPF_INDETERMINATE = -15
    TBPF_NORMAL        = 0 # determinate progress bar
    TBPF_ERROR         = 15
    TBPF_WARNING       = 10    
    # TBPF_PAUSED        = 8    
    
    class WinTB:
        def __init__(self, hwnd: int):
            super().__init__()

            self.hwnd = hwnd

            taskbar.ActivateTab(hwnd)
            taskbar.HrInit()

        def set_state(self, state: str):
            if type(state) != str:
                raise TypeError(f"Expected `state` to be type str, not {type(state)}")
            else:          
                match state:
                    case "error":
                        taskbar.SetProgressState(self.hwnd, TBPF_ERROR)
                    case "warning":
                        taskbar.SetProgressState(self.hwnd, TBPF_WARNING)                        
                    # case "paused":
                    #     taskbar.SetProgressState(self.hwnd, TBPF_PAUSED)
                    case "indeterminate":
                        taskbar.SetProgressState(self.hwnd, TBPF_INDETERMINATE)
                    case "normal":
                        taskbar.SetProgressState(self.hwnd, TBPF_NORMAL)
                    # case "clear":
                    #     taskbar.SetProgressState(self.hwnd, TBPF_NOPROGRESS)
                    case "flash":
                        self.set_state("normal")
                        ctypes.windll.user32.FlashWindow(self.hwnd, True)                    

        def set_val(self, value: int, total=100):
            if type(value) != int:
                raise TypeError(f"Expected `value` to be type int, not {type(value)}")
            if value < 0 or value > total:
                raise Exception(f"Progress value outside of range")
            else:
                taskbar.SetProgressValue(self.hwnd, value, total)