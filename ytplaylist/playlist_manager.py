#!/usr/bin/python

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

#import gdata.youtube
#import gdata.youtube.service

import httplib2
import os
import sys
import pdb

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

class PlaylistManager():
    YTPLAYLIST_SECRETS_FILE = "client_secrets.json"
    YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"


    def __init__(self):
        self.flow = None
        self.storage = None
        self.credentials = None
        self.yt_service = None
        self.__is_logged_in = False

    def login(self):
        self.flow = flow_from_clientsecrets(self.YTPLAYLIST_SECRETS_FILE,
                                       scope=self.YOUTUBE_READ_WRITE_SCOPE)
        self.storage = Storage("oauth2.json")
        self.credentials = self.storage.get()
        if self.credentials is None or self.credentials.invalid:
            flags = argparser.parse_args()
            self.credentials = run_flow(self.flow, self.storage, flags)
        self.yt_service = build(self.YOUTUBE_API_SERVICE_NAME,
                                self.YOUTUBE_API_VERSION,
                                http=self.credentials.authorize(
                                    httplib2.Http()))
        self.__is_logged_in = True
        #pdb.set_trace()

    def skip_login(self):
        self.__is_logged_in = False
        #TODO Fix this
        return

    @property
    def is_logged_in(self):
        return self.__is_logged_in

    def list_playlists(self, username=None):
        if username:
            request = self.yt_service.playlists().list(part="snippet")
        else:
            request = self.yt_service.playlists().list(part="snippet", mine=True)
        result = request.execute()
        return result["items"]


    def export_playlist(self, playlist_name, local_filename):
        pass
