#!/bin/bash

kernel=$(uname -r)
if [[ $kernel == *"5.7"* ]]; then
  systemctl suspend
fi

exit 0
