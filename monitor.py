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


motes="";
port = serial.Serial("/dev/serial0", baudrate=115200, timeout=0.17)
os.system("sudo service 6lbr start")
time.sleep(1)
t=time.time()
while len(motes)==0:
    print "looking for motes"
    time.sleep(1)
    os.system("sudo ip -6 addr add bbbb::101/64 dev tap0")
    time.sleep(1)
    os.system("sudo ip -6 addr add bbbb::101/64 dev wlan0")
    time.sleep(1)
    os.system("sudo route -A inet6 add aaaa::/64 gw bbbb::100")
    time.sleep(2)
    motes=os.popen("curl -s [bbbb::100]/sensors.html").read()
    motes=re.sub(r'><','>\n<', motes)
    motes=re.findall(r'.*?ip.*', motes)
    if(time.time()-t>10 and len(motes)==0):
        os.system("sudo service 6lbr start")
        print("restarting 6lbr server------------------")
        time.sleep(1)
        t=time.time()
        #os.system('sudo reboot')
for i in xrange(len(motes)):
    motes[i]=re.sub(r'.*aaaa','aaaa', motes[i])
    motes[i]=re.sub(r'\).*','',motes[i])
    motes[i]=mote(motes[i])
    print "mote",i," ip is ",motes[i].ip
    num=motes[i].man()

reader = threading.Thread(target=stdinread)
reader.start()
#line2=''
x=0
pushup=0
gledstate=0
rledstate=0
while True:
    line1=''
    line2=''
    for i in xrange(len(motes)):
        if motes[i].ip=='aaaa::212:4b00:7a8:4b07':
            hrate=int(motes[i].observe(2)[0])/30+50
            line1=line1+' '+str(hrate)+'\n'
            line1=line1+' '+motes[i].get(13)[0]+'\n'
            line1=line1+' '+motes[i].get(16)[0]+'\n'
            line1=line1+' '+motes[i].get(12)[0]+'\n'
            if(abs(float(motes[i].get(18)[0])-x)>0.7): pushup+=1
            x=float(motes[i].get(18)[0])
            if hrate<=60:
                if gledstate==0:
                    motes[i].post(9,'1')
                    gledstate=1
                if rledstate==1:
                    motes[i].post(10,'1')
                    rledstate=0
            if 60<hrate<130:
                if gledstate==1:
                    motes[i].post(9,'1')
                    gledstate=0
                if rledstate==1:
                    motes[i].post(10,'1')
                    rledstate=0
            if hrate>130:
                if gledstate==1:
                    motes[i].post(9,'1')
                    gledstate=0
                if rledstate==0:
                    motes[i].post(10,'1')
                    rledstate=1
        if motes[i].ip=='aaaa::212:4b00:c66:f982':
            #line2=line2+' mote2: '+motes[i].observe(0)[0]
            line2=' '+motes[i].observe(0)[0]+'\n'
    strp=line1+' '+str(pushup)+'\n'+line2
    port.write(strp)
    #print strp
    time.sleep(0.5)

for i in xrange(len(motes)):
    motes[i].stop()
    print "stoped motes are ",motes[i].ip
