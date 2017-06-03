import re
import os
import sys
from mote import mote
import Queue
import threading
import time
import serial
def observer(path,mote):
    while True:
        if adc.empty():
            adc.put(mote.observe(path))
        else:
            time.sleep(0.5)
            s=adc.get()
            if s==-1:
                break
            else:
                adc.put(mote.get(path))
        time.sleep(0.5)
def getter(path,mote):
    while True:
        if adc.empty():
            adc.put(mote.get(path))
        else:
            time.sleep(0.5)
            s=adc.get()
            if s==-1:
                break
            else:
                adc.put(mote.get(path))
        time.sleep(0.5)
def stdinread():
    while True:
        line= sys.stdin.readline()
        if line=='q\n':
            for i in xrange(len(motes)):
                motes[i].stop()
                print "stoped motes are ",motes[i].ip
            adc.put(-1)
            sys.exit(1)



port = serial.Serial("/dev/serial0", baudrate=115200, timeout=0.17)
motes=os.popen("curl -s [bbbb::100]/sensors.html").read()
motes=re.sub(r'><','>\n<', motes)
motes=re.findall(r'.*?ip.*', motes)
for i in xrange(len(motes)):
    motes[i]=re.sub(r'.*aaaa','aaaa', motes[i])
    motes[i]=re.sub(r'\).*','',motes[i])
    motes[i]=mote(motes[i])
    print "mote",i," ip is ",motes[i].ip
    num=motes[i].man()

adc=Queue.Queue()
temp=Queue.Queue()
adct = threading.Thread(target=observer, args = (2,motes[1]))
adct.start()
reader = threading.Thread(target=stdinread)
reader.start()

while True:
    line=adc.get()[0]+'\n\n'+line
    port.write(line)
    #print line


for i in xrange(len(motes)):
    motes[i].stop()
    print "stoped motes are ",motes[i].ip
