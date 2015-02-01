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

import playlist_manager
import ui


def main(console=False):
    local_playlist_manager = playlist_manager.PlaylistManager()
    if console:
        local_ui = ui.YTPlaylistConsoleUI(local_playlist_manager)
    else:
        local_ui = ui.YTPlaylistGUI(local_playlist_manager)
    try:
        local_ui.start()
    except Exception as e:
        local_ui.display_error("Error", str(e))

if __name__ == '__main__':
    main()
