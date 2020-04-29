import time
from evdev import InputDevice
from select import select
import alsaaudio

m = alsaaudio.Mixer()
sound_volume=m.getvolume()[0]
# print("cur aound volume:%d",sound_volume)

dev = InputDevice('/dev/input/event1')

while True:
    select([dev], [], [])
    for event in dev.read():
        # print "code:%s value:%s" % (event.code, event.value)
        if(event.code==74 and event.value==1):
            sound_volume=sound_volume - 4
            if(sound_volume<0):
                sound_volume=0
            try:
                m = alsaaudio.Mixer()
                m.setvolume(sound_volume)
            except Exception,e:
                print(str(e))
        elif(event.code==78 and event.value==1):
            sound_volume=sound_volume + 4
            if(sound_volume>100):
                sound_volume=98
            try:
                m = alsaaudio.Mixer()
                m.setvolume(sound_volume)
            except Exception,e:
                print(str(e))

