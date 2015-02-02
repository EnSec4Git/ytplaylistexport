ytplaylist
========

A small library that allows exporting Youtube playlists to .pls files.

Scope
--------
This library contains a GUI based on Tkinter, a Console UI and
a CLI interface allowing the user export a particular playlist.


License
--------
The library is licensed under the GPLv3. For more information about 
the license, check the file `LICENSE`.

Usage
--------
Example usage:

* List "username"'s playlists

	./main.py -u username -l

* Export particular playlist
	
	./main.py -u username -e playlist.pls TestPlaylist
	
* Run the GUI
	
	./main.py
	
* Run the console UI
	
	./main.py -c

Dependencies
--------
The main dependency is the Google Youtube Data API v3.
Note that it allows only OAuth login and no username/password 
authentication.

Installation
--------
The library can be installed as customary in Go:   
`go get github.com/yavorpap/gonumeth`.