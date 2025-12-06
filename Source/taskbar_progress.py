import sys
from ctypes import c_ulonglong
from ctypes.wintypes import HWND
from comtypes import GUID, IUnknown, COMMETHOD, HRESULT

if sys.platform != "win32":
    TaskbarProgress = None
else:
    class ITaskbarList3(IUnknown):
        _iid_ = GUID("{EA1AFB91-9E28-4B86-90E9-9E9F8A5EEFAF}")
        _methods_ = [
            COMMETHOD([], HRESULT, "HrInit"),
            COMMETHOD([], HRESULT, "AddTab", (['in'], HWND, "hwnd")),  # ← ADDED: This registers the window!
            COMMETHOD([], HRESULT, "DeleteTab", (['in'], HWND, "hwnd")),
            COMMETHOD([], HRESULT, "SetProgressValue",
                      (['in'], HWND, "hwnd"),
                      (['in'], c_ulonglong, "ullCompleted"),
                      (['in'], c_ulonglong, "ullTotal")),
            COMMETHOD([], HRESULT, "SetProgressState",
                      (['in'], HWND, "hwnd"),
                      (['in'], c_ulonglong, "tbpFlags")),
            # ... (other methods like ActivateTab if needed, but not required here)
        ]

    TBPF_NOPROGRESS    = 0
    TBPF_INDETERMINATE = 0x1
    TBPF_NORMAL        = 0x2
    TBPF_ERROR         = 0x4
    TBPF_PAUSED        = 0x8

    import comtypes.client as cc
    taskbar = cc.CreateObject("{56FDF344-FD6D-11d0-958A-006097C9A090}", interface=ITaskbarList3)
    taskbar.HrInit()  # Global init

    class TaskbarProgress:
        @staticmethod
        def set(window, value, total=100):
            hwnd = int(window.winId())
            value = int(value)
            total = int(total)
            taskbar.AddTab(hwnd)  # ← MAGIC: Registers the window (call every time, safe)

            if value <= 0:
                taskbar.SetProgressState(hwnd, c_ulonglong(TBPF_NOPROGRESS))
            elif value >= total:
                taskbar.SetProgressState(hwnd, c_ulonglong(TBPF_NORMAL))
                taskbar.SetProgressValue(hwnd, c_ulonglong(total), c_ulonglong(total))
            else:
                taskbar.SetProgressState(hwnd, c_ulonglong(TBPF_NORMAL))
                taskbar.SetProgressValue(hwnd, c_ulonglong(value), c_ulonglong(total))

        @staticmethod
        def clear(window):
            hwnd = int(window.winId())
            taskbar.AddTab(hwnd)  # Still register!
            taskbar.SetProgressState(hwnd, c_ulonglong(TBPF_NOPROGRESS))

        @staticmethod
        def error(window):
            hwnd = int(window.winId())
            taskbar.AddTab(hwnd)
            taskbar.SetProgressState(hwnd, c_ulonglong(TBPF_ERROR))

        @staticmethod
        def paused(window):
            hwnd = int(window.winId())
            taskbar.AddTab(hwnd)
            taskbar.SetProgressState(hwnd, c_ulonglong(TBPF_PAUSED))

        @staticmethod
        def indeterminate(window):
            hwnd = int(window.winId())
            taskbar.AddTab(hwnd)
            taskbar.SetProgressState(hwnd, c_ulonglong(TBPF_INDETERMINATE))