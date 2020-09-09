#!/bin/bash

BASENAME=`dirname "$0"`

cd $BASENAME/sys.py

# boot sound
mplayer -volume 75 /home/cpi/music/startup.mp3

# set system volume
amixer sset 'Master' 50%

python run.py
