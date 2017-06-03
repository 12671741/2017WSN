import re
import os
import sys
from mote import mote
import Queue
import threading
import time
def observer(path,mote,q):
    while True:
        if q.empty():
            q.put(mote.get(path))
            time.sleep(0.5)
        else:
            s=q.get()
            if s==-1:
                break
            else:
                q.put(mote.get(path))
            time.sleep(0.5)

q=Queue.Queue()

motes=os.popen("curl -s [bbbb::100]/sensors.html").read()
motes=re.sub(r'><','>\n<', motes)
motes=re.findall(r'.*?ip.*', motes)
for i in xrange(len(motes)):
    motes[i]=re.sub(r'.*aaaa','aaaa', motes[i])
    motes[i]=re.sub(r'\).*','',motes[i])

print "motes ip are ",motes
mote=mote(motes[0])


path='/sen/adc/dio23'
t = threading.Thread(target=observer, args = (path,mote,q))
t.start()
k=0
while True:
    if not q.empty():
        k=k+1
        s = str(q.get())
        try:
            s = re.sub(r'\n','', s)
            s = re.sub(r'.*yload:\ ','', s)
        except:
            print "didnt sub"
        print s
        time.sleep(0.25)
    if k>20:
        q.put(-1)
        break
time.sleep(1)
mote.stop()
