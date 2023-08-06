# encoding: utf-8

import random
import zmq
import time

context = zmq.Context()
worker = context.socket(zmq.DEALER)
#worker.setsockopt(zmq.IDENTITY, str(random.randint(0, 8000)))
worker.bind("tcp://127.0.0.1:5556")
start = False
while True:
    print 'SEND DATA'
    worker.send("recording data: %s" % random.randint(0,100))
    time.sleep(0.5)
        
    try:
        request = worker.recv(zmq.NOBLOCK)
        print 'RECEIVED', request
    except zmq.error.Again:
        pass
    
#     if request == "START":
#         start = True
#     if request == "STOP":
#         start = False
#     if request == "END":
#         print "A is finishing"
#         break