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
                adc.put(mote.observe(path))
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
            #adc.put(-1)
            sys.exit(1)

t=time.time()
motes="";
port = serial.Serial("/dev/serial0", baudrate=115200, timeout=0.17)


while len(motes)==0:
    print "looking for motes"
    os.system("service 6lbr start")
    time.sleep(2)
    os.system("route -A inet6 add aaaa::/64 gw bbbb::100")
    time.sleep(1)
    motes=os.popen("curl -s [bbbb::100]/sensors.html").read()
    motes=re.sub(r'><','>\n<', motes)
    motes=re.findall(r'.*?ip.*', motes)
    if(time.time()-t>30):
	os.system("service 6lbr restart")
        #os.system('sudo reboot')

for i in xrange(len(motes)):
    motes[i]=re.sub(r'.*aaaa','aaaa', motes[i])
    motes[i]=re.sub(r'\).*','',motes[i])
    motes[i]=mote(motes[i])
    print "mote",i," ip is ",motes[i].ip
    motes[i].man()
reader = threading.Thread(target=stdinread)
reader.start()
while True:
    for i in xrange(len(motes)):
        for j in xrange(motes[i].manl):
            print motes[i].observe(j)[1]+' '+motes[i].get(j)[0]


for i in xrange(len(motes)):
    motes[i].stop()
    print "stoped motes are ",motes[i].ip
