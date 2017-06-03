import serial
import time
import sys

try:
    board=sys.argv[1]
except:
    board=115200
port = serial.Serial("/dev/serial0", baudrate=board, timeout=0.17)
#port = serial.Serial("/dev/tty.wchusbserial1420", baudrate=115200, timeout=0.17)
print 'input AT command'
while 1:
    while (port.inWaiting()>0):
        time.sleep(0.1)
        print port.readline().strip()
    line= sys.stdin.readline()
    line=line.strip()
#    port.write('AT+'+line)
    port.write(line)
    time.sleep(0.1)

