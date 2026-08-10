'''Windows taskbar interface

References:
https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nn-shobjidl_core-itaskbarlist3
https://github.com/N3RDIUM/PyTaskbar/tree/main
https://stackoverflow.com/questions/1736394/using-windows-7-taskbar-features-in-pyqt/1744503#1744503

heavily borrows from PyTaskbar because although it seems to contradict some of the MS docs (TBPF values), its the only implementation I've found to work
'''

import sys
import ctypes
import comtypes.client as cc


if not sys.platform.startswith("win"):
    WinTB = None
else:
    try:
        cc.GetModule("../../resources/TaskbarLib.tlb")
        import comtypes.gen.TaskbarLib as tbl
    except:
        raise Exception("Could not find TaskbarLib.tlb")

    taskbar = cc.CreateObject(
        "{56FDF344-FD6D-11d0-958A-006097C9A090}",
        interface=tbl.ITaskbarList3) 

    TBPF_INDETERMINATE = -15
    TBPF_NORMAL        = 0 
    TBPF_ERROR         = 15
    TBPF_WARNING       = 10     
    
    class WinTB:
        def __init__(self, hwnd: int):
            super().__init__()

            self.hwnd = hwnd

            taskbar.ActivateTab(hwnd)
            taskbar.HrInit()

        def set_state(self, state: str):
            #sets taskbar icon state
            
            if type(state) != str:
                raise TypeError(f"Expected `state` to be type str, not {type(state)}")
            else:          
                match state:
                    case "normal":
                        taskbar.SetProgressState(self.hwnd, TBPF_NORMAL)                    
                    case "indeterminate":
                        taskbar.SetProgressState(self.hwnd, TBPF_INDETERMINATE)
                    case "flash":
                        self.set_state("normal")
                        ctypes.windll.user32.FlashWindow(self.hwnd, True)                           
                    case "warning":
                        taskbar.SetProgressState(self.hwnd, TBPF_WARNING)
                        self.set_val(50) #need to reset a value to show color change because it goes to 0 otherwise  
                    case "error":
                        taskbar.SetProgressState(self.hwnd, TBPF_ERROR)  
                        self.set_val(50) #need to reset a value to show color change because it goes to 0 otherwise                                                                                    

        def set_val(self, value: int, total=100):
            #sets taskbar icon value with determinate progress bar

            if type(value) != int:
                raise TypeError(f"Expected `value` to be type int, not {type(value)}")
            if value < 0 or value > total:
                raise Exception(f"Progress value outside of range")
            else:
                taskbar.SetProgressValue(self.hwnd, value, total)