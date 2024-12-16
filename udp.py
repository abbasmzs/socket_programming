import socket, cv2, pickle,struct
from numpy import  array, empty, zeros, ones, transpose
from datetime import datetime
from random import randint
import time

def current_milli_time():
    return datetime.now().microsecond
 
localIP = "0.0.0.0"

localPort = 9810

bufferSize = 1030


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

f = 10
# Listen for incoming datagrams
im = zeros((f*16, f*32))

eddc = 0
lastCounterStored = False
while (True):
    data, addr = UDPServerSocket.recvfrom(bufferSize)
    data = array(list(data))
    ddc = data[1]
    counter = data[4]<<8 | data[5]

    imageData = data[6:1030:2] | data[6+1:1030:2]<<8

    for i in range(16):
        for j in range(f):
            for k in range(f):
                im[j+i*f][k+ddc*32::f] = imageData[32*i:32*(i+1)]
    
    if (ddc == 0):
        cv2.imshow("RECEIVING VIDEO", transpose(im/65536))

        if cv2.waitKey(1) == '13':
            break    