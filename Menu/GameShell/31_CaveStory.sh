#!/bin/bash

if [ -f "/home/cpi/.config/retroarch/cores/nxengine_libretro.so" ]; then
    retroarch -L /home/cpi/.config/retroarch/cores/nxengine_libretro.so /home/cpi/games/nxengine/cavestory/data
else
    retroarch -L /home/cpi/apps/emulators/nxengine_libretro.so /home/cpi/games/nxengine/cavestory/data
fi
