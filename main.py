#!/usr/bin/env python
import time

import RPIO
from mpd import MPDClient
PLAY=8
RPIO.setup(PLAY, RPIO.IN)

client = MPDClient()

time_treshold = 0.5
last_change = time.time()
client.connect('localhost', 6600)

def play_pause(gpio_id, val):
    global client
    global last_change
    new_time = time.time()
    if new_time - last_change > time_treshold:
	status = client.status()
	if not 'state' in status:
            return
        if status['state'] == 'play':
            client.pause()
        else:
	    client.play()
 	last_change = new_time 

RPIO.add_interrupt_callback(PLAY, play_pause, threaded_callback=True)
RPIO.wait_for_interrupts(threaded=True)
while True:
    try:
	time.sleep(30)
        client.ping()
    except KeyboardInterrupt as e:   
        break
        
client.disconnect()
