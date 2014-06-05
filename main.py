#!/usr/bin/env python
import time

import RPIO
from mpd import MPDClient
PLAY=8
RPIO.setup(PLAY, RPIO.IN)

client = MPDClient()

client.connect('localhost', 6600)

def play_pause(gpio_id, val):
    global client
    status = client.status()
    if not 'state' in status:
        return
    if status['state'] == 'play':
        client.pause()
    else:
        client.play()

RPIO.add_interrupt_callback(PLAY, play_pause, debounce_timeout_ms=500)
RPIO.wait_for_interrupts()
while True:
    try:
	time.sleep(30)
        client.ping()
    except KeyboardInterrupt as e:   
        break
        
client.disconnect()
