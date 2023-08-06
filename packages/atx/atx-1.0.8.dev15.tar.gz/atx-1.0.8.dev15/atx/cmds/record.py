#-*- encoding: utf-8 -*-

## why no memory return back..
import gc
gc.set_debug(gc.DEBUG_STATS)

import os
import sys
import time
import bisect
import tempfile
import threading
import Tkinter as tk
import win32api
import win32con
import win32gui
import win32process
import pyHook
from pyHook import HookConstants
from collections import namedtuple

from atx.device.windows import WindowsDevice
from atx.device.android import AndroidDevice

__dir__ = os.path.dirname(os.path.abspath(__file__))

class BaseRecorder(object):

    def __init__(self, device=None):
        self.steps = []
        self.device = None
        if device is not None:
            self.attach(device)

        self.running = False
        self.capture_interval = 0.2
        self.capture_maxnum = 20 # watch out your memory!
        self.lock = threading.RLock()
        self.capture_cache = []
        self.capture_tmpdir = os.path.join(__dir__, 'screenshots', time.strftime("%Y%m%d"))
        if not os.path.exists(self.capture_tmpdir):
            os.makedirs(self.capture_tmpdir)

        t = threading.Thread(target=self.async_capture)
        t.setDaemon(True)
        t.start()

    def attach(self, device):
        """Attach to device, if current device is not None, should
        detach from it first. """
        raise NotImplementedError()

    def detach(self):
        """Detach from current device."""
        raise NotImplementedError()

    def run(self):
        """Start watching inputs & device screen."""
        raise NotImplementedError()

    def stop(self):
        """Stop record."""
        raise NotImplementedError()

    def on_touch(self, position):
        """Handle touch input event."""
        t = threading.Thread(target=self.__async_handle_touch, args=(position, ))
        t.setDaemon(True)
        t.start()

    def __async_handle_touch(self, position):
        print "click at", position
        t = time.time()
        self.lock.acquire()
        try:
            # trace back a few moments, find a untouched image
            # we're sure all item[0] won't be same
            idx = bisect.bisect(self.capture_cache, (t, None))
            if idx == 0:
                return
            # just use last one for now. 
            item = self.capture_cache[idx-1]
        finally:
            self.lock.release()

        t0, img = item
        filepath = os.path.join(self.capture_tmpdir, "%d.png" % int(t0*1000))
        img.save(filepath)
        img.close()

    def on_drag(self, start, end):
        """Handle drag input event."""

    def on_text(self, text):
        """Handle text input event."""

    def dump(self, filepath=None):
        """Generate python scripts."""
        pass

    def async_capture(self):
        """Keep capturing device screen. Should run in background
        as a thread."""
        while True:
            self.lock.acquire()
            try:
                t = time.time()
                interval = self.capture_interval
                if self.capture_cache:
                    t0 = self.capture_cache[-1][0]
                    interval = min(interval, t-t0)
                time.sleep(interval)
                if not self.running or self.device is None:
                    continue
                print "capturing...", t
                img = self.device.screenshot()
                self.capture_cache.append((t, img))

                # TODO: change capture_cache to a loop list
                while len(self.capture_cache) > self.capture_maxnum:
                    _, img = self.capture_cache.pop(0)
                    img.close()

            finally:
                self.lock.release()

class WindowsRecorder(BaseRecorder):

    KBFLAG_CTRL = 0x01
    KBFLAG_ALT = 0x02
    KBFLAG_SHIFT = 0x04
    KBFLAG_CAPS = 0x08

    def __init__(self, device=None):
        self.watched_hwnds = set()
        super(WindowsRecorder, self).__init__(device)
        self.kbflag = 0
        self.hm = pyHook.HookManager()
        self.hm.MouseAllButtons = self._hook_on_mouse
        self.hm.KeyAll = self._hook_on_keyboard

        self.thread = None

    def attach(self, device):
        if self.device is not None:
            print "Warning: already attached to a device."
            if device is not self.device:
                self.detach()

        handle = device.hwnd
        def callback(hwnd, extra):
            extra.add(hwnd)
            return True
        self.watched_hwnds.add(handle)
        win32gui.EnumChildWindows(handle, callback, self.watched_hwnds)

        self.device = device
        print "attach to device", device

    def detach(self):
        print "detach from device", self.device
        self.device = None
        self.watched_hwnds = set()

    def run(self):
        self.hm.HookMouse()
        self.hm.HookKeyboard()
        with self.lock:
            self.running = True

    def stop(self):
        with self.lock:
            self.running = False
        self.hm.UnhookMouse()
        self.hm.UnhookKeyboard()

        print "collected", gc.collect()
        print "garbage", len(gc.garbage)

    def _hook_on_mouse(self, event):
        if self.device is None:
            return True
        if event.Window not in self.watched_hwnds:
            return True
        if event.Message == HookConstants.WM_LBUTTONUP:
            x, y = self.device.norm_position(event.Position)
            # ignore the touches outside the rect if the window has a frame.
            if x < 0 or y < 0:
                return True
            self.on_touch((x, y))
        return True

    def _hook_on_keyboard(self, event):
        if self.device is None:
            return True
        if event.Window not in self.watched_hwnds:
            return True
        print "on_keyboard", event.MessageName, event.Key, repr(event.Ascii), event.KeyID, event.ScanCode, 
        print event.flags, event.Extended, event.Injected, event.Alt, event.Transition
        return True

class AndroidRecorder(BaseRecorder):
    def attach(self):
        pass

    def detach(self):
        pass

class SystemTray(object):
    def __init__(self, parent, name, commands=None, icon_path=None):
        self.parent = parent
        self.name = name
        self.WM_NOTIFY = win32con.WM_USER+20

        wndproc = {
            win32con.WM_DESTROY: self.on_destroy,
            win32con.WM_COMMAND: self.on_command,
            self.WM_NOTIFY: self.on_tray_notify,
        }

        wc = win32gui.WNDCLASS()
        wc.hInstance = hinst = win32api.GetModuleHandle(None)
        wc.lpszClassName = name.title()
        wc.lpfnWndProc = wndproc
        class_atom = win32gui.RegisterClass(wc)
        self.hwnd = win32gui.CreateWindow(wc.lpszClassName, "", win32con.WS_POPUP, 0,0,1,1, parent, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)

        if icon_path is not None and os.path.isfile(icon_path):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, icon_flags)
        else:
            shell_dll = os.path.join(win32api.GetSystemDirectory(), "shell32.dll")
            large, small = win32gui.ExtractIconEx(shell_dll, 19, 1) #19 or 76
            hicon = small[0]
            win32gui.DestroyIcon(large[0])
        self.hicon = hicon

        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP | win32gui.NIF_INFO
        nid = (self.hwnd, 0, flags, self.WM_NOTIFY, self.hicon, self.name)
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)

        self.next_command_id = 1000
        self.commands = {}
        self.register_command('Exit', lambda:win32gui.DestroyWindow(self.hwnd))
        if commands is not None:
            for n, f in commands[::-1]:
                self.register_command(n, f)

    def balloon(self, msg, title=""):
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP | win32gui.NIF_INFO
        nid = (self.hwnd, 0, flags, self.WM_NOTIFY, self.hicon, self.name, msg, 300, title)
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)

    def register_command(self, name, func):
        cid = self.next_command_id
        self.next_command_id += 1
        self.commands[cid] = (name, func)
        return cid

    def on_destroy(self, hwnd, msg, wp, lp):
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, (self.hwnd, 0))
        win32gui.PostMessage(self.parent, win32con.WM_CLOSE, 0, 0)
        return True

    def on_command(self, hwnd, msg, wp, lp):
        cid = win32api.LOWORD(wp)
        if not self.commands.get(cid):
            print "Unknown command -", cid
            return
        _, func = self.commands[cid]
        try:
            func()
        except Exception as e:
            print str(e)
        return True

    def on_tray_notify(self, hwnd, msg, wp, lp):
        if lp == win32con.WM_LBUTTONUP:
            # print "left click"
            # win32gui.SetForegroundWindow(self.hwnd)
            pass
        elif lp == win32con.WM_RBUTTONUP:
            # print "right click"
            menu = win32gui.CreatePopupMenu()
            for cid in sorted(self.commands.keys(), reverse=True):
                name, _ = self.commands[cid]
                win32gui.AppendMenu(menu, win32con.MF_STRING, cid, name)

            pos = win32gui.GetCursorPos()
            win32gui.SetForegroundWindow(self.hwnd)
            win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
            win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        return True

class RecorderGUI(object):
    def __init__(self, device=None):
        self._device = device
        self._recorder = None
        self._root = root = tk.Tk()

        root.protocol("WM_DELETE_WINDOW", self.destroy)

        def calllater():
            icon_path = os.path.join(__dir__, 'static', 'recorder.ico')
            commands  = [
                ("Start Record", self.start_record),
                ("Stop Record", self.stop_record),
            ]
            tray = SystemTray(root.winfo_id(), "recorder", commands, icon_path)
            tray.balloon('hello')

        root.after(2000, calllater)

        # no window for now.
        root.withdraw()

        # need to handle device event

    def destroy(self):
        print "root destroy"
        if self._recorder is not None:
            self._recorder.stop()
        self._root.destroy()
        win32api.PostQuitMessage(0)

    def mainloop(self):
        self._root.mainloop()

    def start_record(self):
        if not self.check_recorder():
            return
        self._recorder.run()

    def stop_record(self):
        if not self.check_recorder():
            return
        self._recorder.stop()

    def check_recorder(self):
        if self._device is None:
            print "No device choosen."
            self._recorder = None
            return False

        if self._recorder is None:
            print "init recorder", type(self._device)
            if isinstance(self._device, WindowsDevice):
                record_class = WindowsRecorder
            elif isinstance(self._device, AndroidDevice):
                record_class = AndroidRecorder
            else:
                print "Unknown device type", type(self._device)
                return False
            self._recorder = record_class(self._device)
        return True

if __name__ == '__main__':
    w = RecorderGUI()
    w.mainloop()
