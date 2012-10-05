import Tkinter
from Tkinter import Label, Entry, Button, Tk

YTPL_UL_PX = 10
YTPL_UL_PY = 10
YTPL_UF_PX = 10
YTPL_LB_PY = 20

YTPLAYLIST_WINDOW_TITLE = "Youtube playlist exporter"
YTPLAYLIST_USERNAME_LABEL_TEXT = "Enter Youtube username:"
YTPLAYLIST_USERNAME_FIELD_SIZE = 30
YTPLAYLIST_PASSWORD_LABEL_TEXT = "Enter Youtube password:"
YTPLAYLIST_PASSWORD_FIELD_SIZE = 30
YTPLAYLIST_LOGIN_BUTTON_TEXT = "Login to Youtube"

class YTPlaylist:
    def __init__(self):
        pass

class YTPlaylistUI:
    def __init__(self, playlist_manager):
        self.playlist_manager = playlist_manager
        root = Tk()
        root.title(YTPLAYLIST_WINDOW_TITLE)
        Label(root, text=YTPLAYLIST_USERNAME_LABEL_TEXT).pack(side=TOP,
                                                              padx=YTPL_UL_PX,
                                                              pady=YTPL_UL_PY)
        Entry(root, width=YTPLAYLIST_USERNAME_FIELD_SIZE).pack(side=TOP,
                                                               padx=YTPL_UF_PX)
        Label(root, text=YTPLAYLIST_PASSWORD_LABEL_TEXT).pack(side=TOP,
                                                              padx=YTPL_UL_PX,
                                                              pady=YTPL_UL_PY)
        Entry(root, width=YTPLAYLIST_PASSWORD_FIELD_SIZE).pack(side=TOP,
                                                               padx=YTPL_UF_PX)
        Button(root, text=YTPLAYLIST_LOGIN_BUTTON_TEXT,
               command=self.login).pack(side=BOTTOM, pady=YTPL_LB_PY)
        root.mainloop()
    def login

if __name__ == "__main__":
    user_interface = YTPlaylistUI()

