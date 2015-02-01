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

from Tkinter import Button, Tk, Toplevel, Label, Listbox, Scrollbar
from tkMessageBox import *
import threading
import Tkinter
import tkFileDialog, tkSimpleDialog


class UI:
    """
    Abstract Base Class for the user interface of the playlist exporter.
    """
    YTPLAYLIST_LOGIN_WINDOW_TITLE = "Youtube playlist exporter"
    YTPLAYLIST_LOGIN_BUTTON_TEXT = "Login to Youtube"
    YTPLAYLIST_NOLOGIN_BUTTON_TEXT = "Skip login"
    YTPLAYLIST_EXPORT_BUTTON_TEXT = "Export playlist to .pls file"
    YTPLAYLIST_PLAYLISTS_WINDOW_TITLE = "Your playlists"
    YTPLAYLIST_SAVE_AS_TITLE = "Save playlist as"
    YTPLAYLIST_DESTROY_CREDENTIALS_BUTTON_TEXT = "Destroy the stored credentials (a.k.a. 'Logout')"

    def start(self):
        raise NotImplementedError()

    def login(self):
        raise NotImplementedError()

    def skip_login(self):
        raise NotImplementedError()

    def display_error(self, title, message):
        raise NotImplementedError()


class _WorkingDialog:

        def __init__(self, parent, title, action=None):
            self.action = action
            self.top = Toplevel(parent)
            Label(self.top, text=title).pack()
            if action:
                b = Button(self.top, text="Cancel", command=self.cancel)
                b.pack(pady=5)

        def cancel(self):
            self.top.destroy()
            if self.action:
                self.action()

        def __del__(self):
            self.top.destroy()


class YTPlaylistGUI(UI):
    LOGIN_COMPLETE_EVENT = "<<LoginComplete>>"
    PLAYLIST_LIST_FETCH_COMPLETE_EVENT = "<<PlalistListFetched>>"
    PLAYLIST_SAVED_EVENT = "<<PlaylistSaved>>"

    def __init__(self, playlist_manager):
        self.playlist_manager = playlist_manager
        self.workerThread = None
        self.last_exception = None

    def _create_login_window(self):
        self.root = Tk()
        self.root.geometry("280x150")
        self.root.title(self.YTPLAYLIST_LOGIN_WINDOW_TITLE)
        self.root.bind(self.LOGIN_COMPLETE_EVENT, self._login_complete)
        Button(self.root, text=self.YTPLAYLIST_LOGIN_BUTTON_TEXT,
               command=self.login).pack(side=Tkinter.TOP,
                                        pady=20, padx=20, expand=True, fill=Tkinter.BOTH)
        Button(self.root, text=self.YTPLAYLIST_NOLOGIN_BUTTON_TEXT,
               command=self.skip_login).pack(side=Tkinter.TOP,
                                             pady=20, padx=20, expand=True, fill=Tkinter.BOTH)

    def _create_playlists_window(self):
        if self.root:
            self.root.destroy()
        self.root = Tk()
        self.root.geometry("300x{0}".format(280 if self.playlist_manager.is_logged_in else 250))
        self.root.title(self.YTPLAYLIST_PLAYLISTS_WINDOW_TITLE)
        if self.playlist_manager.is_logged_in:
            Button(self.root, text=self.YTPLAYLIST_DESTROY_CREDENTIALS_BUTTON_TEXT,
                   command=self.logout).pack(side=Tkinter.TOP, padx=20, pady=(10,5), fill=Tkinter.X)
        scrollbar = Scrollbar(self.root, orient=Tkinter.VERTICAL)
        self.playlist_list = Listbox(self.root, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.playlist_list.yview)
        Button(self.root, text=self.YTPLAYLIST_EXPORT_BUTTON_TEXT,
               command=self._export_playlist_item).pack(side=Tkinter.BOTTOM,
                                                        padx=20, pady=(5,10), fill=Tkinter.X)
        self.playlist_list.pack(side=Tkinter.LEFT, padx=(5,0), pady=5, expand=True, fill=Tkinter.BOTH)
        scrollbar.pack(side=Tkinter.LEFT, padx=(0,5), pady=5, fill=Tkinter.Y)
        self.root.bind(self.PLAYLIST_LIST_FETCH_COMPLETE_EVENT,
                       self._playlist_list_fetched)
        self.root.bind(self.PLAYLIST_SAVED_EVENT, self._playlist_saved)

    def start(self):
        self._create_login_window()
        self.root.mainloop()

    def _login_async(self):
        try:
            self.playlist_manager.login()
        except Exception as e:
            self.last_exception = e
        self.root.event_generate(self.LOGIN_COMPLETE_EVENT, when="tail")

    def login(self):
        self.workerThread = threading.Thread(target=self._login_async)
        self.workerThread.start()
        self._login_dialog = _WorkingDialog(self.root, "Logging in...")

    def logout(self):
        self.playlist_manager.destroy_credentials()
        self.root.destroy()

    def skip_login(self):
        self.username = tkSimpleDialog.askstring("Username", "Specify the playlist owner's username", parent=self.root)
        self.playlist_manager.skip_login()
        self._create_playlists_window()
        self.display_playlists()

    def _login_complete(self, event):
        del self._login_dialog
        self.__handle_exceptions()
        self._create_playlists_window()
        self.display_playlists()

    def display_playlists(self):
        self._loading_playlists_dialog =\
            _WorkingDialog(self.root, "Loading playlists")
        self.workerThread =\
            threading.Thread(target=self._fetch_playlists_async)
        self.workerThread.start()

    def _fetch_playlists_async(self):
        try:
            if self.playlist_manager.is_logged_in:
                result = self.playlist_manager.list_playlists()
            else:
                result = self.playlist_manager.list_playlists(self.username)
            self.playlist_data = result
        except Exception as e:
            self.last_exception = e
        self.root.event_generate(self.PLAYLIST_LIST_FETCH_COMPLETE_EVENT, when="tail")

    def _playlist_list_fetched(self, event):
        del self._loading_playlists_dialog
        self.__handle_exceptions()
        for item in self.playlist_data:
            self.playlist_list.insert(Tkinter.END, item["snippet"]["title"])
        self.root.mainloop()

    def _export_playlist_item(self):
        selection = map(int, self.playlist_list.curselection())
        playlist_id = self.playlist_data[selection[0]]["id"]
        fname = tkFileDialog.asksaveasfilename(defaultextension=".pls",
                                               filetypes=[("Playlists", "*.pls"), ("All files", "*.*")],
                                               parent=self.root,
                                               title=self.YTPLAYLIST_SAVE_AS_TITLE)
        if fname is None or fname == "": return
        self._saving_playlist_dialog = \
            _WorkingDialog(self.root, "Saving playlist")
        self.workerThread =\
            threading.Thread(target=self._export_playlist_worker, args=(playlist_id, fname))
        self.workerThread.start()

    def _export_playlist_worker(self, playlist_id, fname):
        try:
            self.playlist_manager.export_playlist(playlist_id, fname)
        except Exception as e:
            self.last_exception = e
        self.root.event_generate(self.PLAYLIST_SAVED_EVENT, when="tail")

    def _playlist_saved(self, event):
        del self._saving_playlist_dialog
        self.__handle_exceptions()
        showinfo("Playlist saved", "Saving playlist complete")

    def display_error(self, title, message):
        showerror(title, message)

    def __handle_exceptions(self):
        if self.last_exception is not None:
            self.display_error("Error", str(self.last_exception))
            exit(0)

class YTPlaylistConsoleUI(UI):
    def __init__(self, playlist_manager):
        self.playlist_manager = playlist_manager
