# GameShell launcher
This is the DEOT UI launcher for GameShell based on 320x240 resolution and D-Pad layout.
![Screenshot](https://raw.githubusercontent.com/hi80482/launcher_deot/master/.screenshot.png)

Screenshot Source: https://alioss.gcores.com/site/deot/index.html

# Create the necessary user and group
* User name: cpi
* Password: cpi
* Group ID: 31415 with group name: cpifav

```
sudo adduser cpi  
sudo groupadd cpifav -g 31415  
sudo adduser cpi cpifav  
```

# Cloning the Git repository
* login as: cpi

```
cd
git clone https://github.com/your_launcher.git ~/launcher
```

# Directory structure
```
/home/cpi/
├── apps
│   └── emulators
├── launcher <-Here we are
│   ├── Menu
│   ├── sys.py
│   ├── skin
│   └── ...
├── games
│   ├── FreeDM
│   ├── MAME
│   ├── nxengine
│   └── ...
└── music
```
## Create the necessary directories
```
mkdir -p /home/cpi/apps/emulators  
mkdir -p /home/cpi/games  
mkdir -p /home/cpi/music  
```

# Dependent packages
* validators, numpy, requests, python-mpd2, beeprint, python-pycurl, python-alsaaudio, python-pygame, python-gobject, python-xlib, python-wicd
* wicd (For Wi-Fi)
* mpd (For music player)

## Install dependent packages
```
sudo apt-get -y install mpd ncmpcpp git libuser
sudo apt-get -y install python-wicd  wicd wicd-curses python-pycurl python-alsaaudio python-pygame python-gobject python-xlib   

sudo apt-get -y install python-pip   
sudo pip install validators numpy requests python-mpd2
```

### With pip install and virtualenv

```
mkvirtualenv launcher
pip install -r requirements.txt
```

# Create “.mpd.conf” config

vim ~/.mpd.conf

```
music_directory		"/home/cpi/music"
playlist_directory	"/home/cpi/.mpd/playlists"
db_file			"/home/cpi/.mpd/tag_cache"
log_file		"/home/cpi/.mpd/mpd.log"
pid_file		"/home/cpi/.mpd/pid"
state_file		"/home/cpi/.mpd/state"
sticker_file		"/home/cpi/.mpd/sticker.sql"
user			"cpi"
bind_to_address		"/tmp/mpd.socket"

auto_update		"yes"
auto_update_depth	"2"

input {
        plugin "curl"
}

audio_output {
	type	"alsa"
	name	"ALSA Device"
}

audio_output {
	type	"fifo"
	name	"my_fifo"
	path	"/tmp/mpd.fifo"
	format	"44100:16:2"
}

filesystem_charset	"UTF-8"
# id3v1_encoding		"UTF-8"

# QOBUZ input plugin
input {
        enabled    "no"
        plugin     "qobuz"
#        app_id     "ID"
#        app_secret "SECRET"
#        username   "USERNAME"
#        password   "PASSWORD"
#        format_id  "N"
}

# TIDAL input plugin
input {
        enabled      "no"
        plugin       "tidal"
#        token        "TOKEN"
#        username     "USERNAME"
#        password     "PASSWORD"
#        audioquality "Q"
}

# Decoder #####################################################################
#

decoder {
        plugin                  "hybrid_dsd"
        enabled                 "no"
#       gapless                 "no"
}
```

# Create “.mpd.conf” config

vim ~/.gameshell_skin

```
/home/cpi/launcher/skin/DEOT
```
