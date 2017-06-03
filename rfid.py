#!/usr/bin/env python

import signal
import time
import sys

from pirc522 import RFID

run = True
rdr = RFID()
util = rdr.util()
util.debug = False

def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()

signal.signal(signal.SIGINT, end_read)

print("Starting")
counter=1
while run:
    rdr.wait_for_tag()

    (error, data) = rdr.request()
    if not error:
        print("\nDetected: " + format(data, "02x"))

    (error, uid) = rdr.anticoll()
    if not error:
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

        print("Setting tag")
        util.set_tag(uid)
        print("\nAuthorizing")
        #util.auth(rdr.auth_a, [0x12, 0x34, 0x56, 0x78, 0x96, 0x92])
        #util.auth(rdr.auth_b, [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF])
        print("\nReading")
        if counter ==1:
            util.auth(rdr.auth_a, [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF])
            util.read_out(0)
            util.read_out(1)
            util.read_out(2)
            util.read_out(3)
            util.deauth()
            counter=counter+1
        else:
            util.auth(rdr.auth_b, [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF])
            #util.rewrite(4, [None, 0x69, 0x69, 0x24, 0x40])
            time.sleep(1)
            #util.do_auth(util.block_addr(1, 1))
            #rdr.write(4, [0x01, 0x23, 0x45, 0x67, 0x89, 0x98, 0x76, 0x54, 0x32, 0x10, 0x69, 0x27, 0x46, 0x66, 0x66, 0x64])
            util.read_out(4)
            util.read_out(5)
            util.read_out(6)
            util.read_out(7)
            util.deauth()
            counter=counter-1
        print("\nDeauthorizing")

        time.sleep(1)
