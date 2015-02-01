#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        main
# Purpose:
#
# Author:      Yavor
#
# Created:
# Copyright:   (c) Yavor
# Licence:     GLPv3
#-------------------------------------------------------------------------------
from __future__ import print_function
import playlist_manager
import ui
import traceback
import argparse
from ytutils import check_is_file_valid

REQUIRED_STR_LIST = 'Requires either --username or --stored'
REQUIRED_STR_EXPORT = REQUIRED_STR_LIST + ' and either --title or --index'
argparser =\
    argparse.ArgumentParser(description=
                            "Small tool to help exporting Youtube " +
                            "playlists to local .pls files. No arguments " +
                            "launches the GUI"
                            )
group1 = argparser.add_mutually_exclusive_group()
group1.add_argument('-c', '--console',
                    help='Use console version instead',
                    required=False, default=False,
                    action='store_true')
group1.add_argument('-e', '--export',
                    help='Perform an automated export. ' + REQUIRED_STR_EXPORT,
                    required=False, metavar="FILENAME")
group1.add_argument('-l', '--list',
                    help='Print all playlists belonging to user. ' +
                         REQUIRED_STR_LIST,
                    required=False, default=False, action='store_true')

group2 = argparser.add_mutually_exclusive_group()
group2.add_argument('-u', '--username',
                    help="Username to use", required=False)
group2.add_argument('-s', '--stored',
                    help="Use stored credentials (or run OAuth flow)",
                    required=False, default=False, action='store_true')

group3 = argparser.add_mutually_exclusive_group()
group3.add_argument('-t', '--title',
                    help="Title of the playlist",
                    required=False)
group3.add_argument('-i', '--index', help="Index of the playlist",
                    required=False, type=int)
arguments = vars(argparser.parse_args())


def main(args):
    has_query = args["export"] or args["list"] or args["stored"] or\
                args["username"] or args["index"] or\
                args["title"]
    console = args["console"] or has_query
    local_playlist_manager = playlist_manager.PlaylistManager(console)
    if has_query:
        perform_query(local_playlist_manager, args)
        return
    if console:
        local_ui = ui.YTPlaylistConsoleUI(local_playlist_manager)
    else:
        local_ui = ui.YTPlaylistGUI(local_playlist_manager)
    local_playlist_manager.ui = local_ui
    try:
        local_ui.start()
    except Exception:
        local_ui.display_error("Error", traceback.format_exc())
    except KeyboardInterrupt:
        print("\n\nBye!\n\n")


def perform_query(manager, args):
    if not (args["list"] or args["export"]):
        print("Incorrect usage. " +
              "Specify either --list or --export as action")
        argparser.print_help()
        return
    if args["stored"]:
        manager.login()
    elif args["username"]:
        manager.skip_login()
    else:
        print("Incorrect usage. " +
              "Specify either --username or --stored")
        argparser.print_help()
        return
    username = args["username"]
    data = manager.list_playlists(username)
    if args["list"]:
        for (i, item) in enumerate(data):
            print(u"{0}: {1}".format(i + 1, item["snippet"]["title"]).encode("utf-8"))
        return
    if not (args["index"] or args["title"]):
        print("Incorrect usage. " +
              "Specify either --index or --title")
        argparser.print_help()
        return
    fname = args["export"]
    if not check_is_file_valid(fname):
        print("Invalid file name")
        return
    if args["index"]:
        ind = args["index"]
        playlist_id = data[ind - 1]["id"]
        manager.export_playlist(playlist_id, fname)
    else:
        title = args["title"]
        for item in data:
            if item["snippet"]["title"] == title:
                playlist_id = item["id"]
                manager.export_playlist(playlist_id, fname)
                return
        else:
            print("Could not find the title in playlists")

if __name__ == '__main__':
    main(arguments)
