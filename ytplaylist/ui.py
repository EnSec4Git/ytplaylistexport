#-------------------------------------------------------------------------------
# Name:        ui
# Purpose:
#
# Author:      Yavor
#
# Created:
# Copyright:   (c) Yavor
# Licence:     GLPv3
#-------------------------------------------------------------------------------

from Tkinter import Button, Tk, Toplevel, Label
from tkMessageBox import *
import threading
import Tkinter


class UI:
    """
    Abstract Base Class for the user interface of the playlist exporter.
    """
    YTPLAYLIST_WINDOW_TITLE = "Youtube playlist exporter"
    YTPLAYLIST_LOGIN_BUTTON_TEXT = "Login to Youtube"
    YTPLAYLIST_NOLOGIN_BUTTON_TEXT = "Skip login"

    def start(self):
        raise NotImplementedError()

    def login(self):
        raise NotImplementedError()

    def skip_login(self):
        raise NotImplementedError()


class YTPlaylistGUI(UI):
    YTPL_UB_PY = 20
    YTPL_LB_PY = 60
    LOGIN_COMPLETE_EVENT = "<<LoginComplete>>"

    class LoggingInDialog:

        def __init__(self, parent):
            self.parent = parent
            self.top = Toplevel(parent.root)
            Label(self.top, text="Logging in...").pack()
            #b = Button(self.top, text="Cancel", command=self.cancel)
            #b.pack(pady=5)

        def cancel(self):
            self.top.destroy()
            #self.parent.cancel_login()

        def __del__(self):
            self.top.destroy()

    def __init__(self, playlist_manager):
        self.playlist_manager = playlist_manager
        self.workerThread = None

    def _create_login_window(self):
        self.root = Tk()
        self.root.title(self.YTPLAYLIST_WINDOW_TITLE)
        self.root.bind(self.LOGIN_COMPLETE_EVENT, self._login_complete)
        Button(self.root, text=self.YTPLAYLIST_LOGIN_BUTTON_TEXT,
               command=self.login).pack(side=Tkinter.TOP,
                                        pady=self.YTPL_UB_PY)
        Button(self.root, text=self.YTPLAYLIST_NOLOGIN_BUTTON_TEXT,
               command=self.skip_login).pack(side=Tkinter.TOP,
                                             pady=self.YTPL_LB_PY)

    def start(self):
        self._create_login_window()
        self.root.mainloop()

    def _login_async(self):
        self.playlist_manager.login()
        self.root.event_generate(self.LOGIN_COMPLETE_EVENT, when="tail")

    def _login_complete(self, event):
        del self._login_dialog

    def cancel_login(self):
        #self.workerThread.stop()
        raise NotImplementedError()

    def login(self):
        self.workerThread = threading.Thread(target=self._login_async)
        self.workerThread.start()
        self._login_dialog = self.LoggingInDialog(self)

    def skip_login(self):
        pass

class YTPlaylistConsoleUI(UI):
    def __init__(self, playlist_manager):
        self.playlist_manager = playlist_manager
